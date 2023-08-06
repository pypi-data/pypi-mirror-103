import re
import json
import logging
import requests
import time

from botocore.compat import ensure_bytes, ensure_unicode, urlparse, urljoin
from botocore.monitoring import APICallAttemptEvent, APICallEvent
from botocore.retryhandler import EXCEPTION_MAP as RETRYABLE_EXCEPTIONS

logger = logging.getLogger(__name__)


class PrintPublisher(object):
    def __init__(self, serializer):
        """Prints monitor events to console

        :type socket: socket.socket
        :param socket: The socket object to use to publish events

        :type host: string
        :param host: The host to send events to

        :type port: integer
        :param port: The port on the host to send events to

        :param serializer: The serializer to use to serialize the event
            to a form that can be published to the socket. This must
            have a `serialize()` method that accepts a monitor event
            and return bytes
        """
        self._serializer = serializer

    def publish(self, event):
        """Publishes a specified monitor event

        :type event: BaseMonitorEvent
        :param event: The monitor event to be sent
        """
        serialized_event = self._serializer.serialize(event)
        print(serialized_event)


class IAMZPublisher(object):
    def __init__(self, host, serializer):
        """Publishes monitor events to an iam-zero collector via a HTTP request

        :param host: The URL of the iam-zero collector (eg http://localhost:9090)

        :param serializer: The serializer to use to serialize the event
            to a form that can be published to the socket. This must
            have a `serialize()` method that accepts a monitor event
            and return bytes
        """
        self._serializer = serializer
        if host is None:
            self._collector_url = None
        else:
            self._collector_url = urljoin(host, "/api/v1/events")

    def publish(self, event):
        """Publishes a specified monitor event

        :type event: BaseMonitorEvent
        :param event: The monitor event to be sent
        """
        if event.http_status_code < 400 or event.http_status_code >= 500:
            # we only dispatch events for failed API calls
            # so skip the event if it's not a 4xx code
            return

        if self._collector_url is None:
            logger.error(
                "IAMZERO_HOST is not set! Please set the IAMZERO_HOST to dispatch IAM errors"
            )
        else:
            serialized_event = self._serializer.serialize(event)

            headers = {"Content-Type": "application/json"}

            requests.post(
                url=self._collector_url, data=serialized_event, headers=headers
            )


class IAMZSerializer(object):
    """
    The methods herein are modified from the AWS CLI CSMSerializer class.

    Specifically, we make the following modifications:
    - remove credentials such as session tokens from being serialized
    - remove latency being serialized
    """

    _MAX_CLIENT_ID_LENGTH = 255
    _MAX_EXCEPTION_CLASS_LENGTH = 128
    _MAX_ERROR_CODE_LENGTH = 128
    _MAX_USER_AGENT_LENGTH = 256
    _MAX_MESSAGE_LENGTH = 512
    _RESPONSE_HEADERS_TO_EVENT_ENTRIES = {
        "x-amzn-requestid": "XAmznRequestId",
        "x-amz-request-id": "XAmzRequestId",
        "x-amz-id-2": "XAmzId2",
    }
    _AUTH_REGEXS = {
        "v4": re.compile(
            r"AWS4-HMAC-SHA256 "
            r"Credential=(?P<access_key>\w+)/\d+/"
            r"(?P<signing_region>[a-z0-9-]+)/"
        ),
        "s3": re.compile(r"AWS (?P<access_key>\w+):"),
    }
    _SERIALIZEABLE_EVENT_PROPERTIES = [
        "service",
        "operation",
        "timestamp",
        "attempts",
        "retries_exceeded",
        "url",
        "params",
        "data",
        "request_headers",
        "http_status_code",
        "response_headers",
        "parsed_error",
        "wire_exception",
    ]

    def __init__(self, arn, user_id, account):
        """Serializes monitor events to iamzero format"""
        self.arn = arn
        self.user_id = user_id
        self.account = account

    def serialize(self, event):
        """Serializes a monitor event to the CSM format

        :type event: BaseMonitorEvent
        :param event: The event to serialize to bytes

        :rtype: bytes
        :returns: The CSM serialized form of the event
        """
        event_dict = self._get_base_event_dict(event)
        event_type = self._get_event_type(event)
        event_dict["Type"] = event_type
        for attr in self._SERIALIZEABLE_EVENT_PROPERTIES:
            value = getattr(event, attr, None)
            if value is not None:
                getattr(self, "_serialize_" + attr)(
                    value, event_dict, event_type=event_type
                )
        return ensure_bytes(json.dumps(event_dict, separators=(",", ":")))

    def _get_base_event_dict(self, event):
        return {
            "Version": 1,
            "IAMZArn": self.arn,
            "IAMZUserId": self.user_id,
            "IAMZAccount": self.account,
        }

    def _serialize_service(self, service, event_dict, **kwargs):
        event_dict["Service"] = service

    def _serialize_data(self, data, event_dict, **kwargs):
        if data != b'':
            # if `data` was a dict already, we wouldn't 
            # need to deserialize it
            event_dict["Data"] = json.loads(data)

    def _serialize_params(self, params, event_dict, **kwargs):
        event_dict["Params"] = params

    def _serialize_operation(self, operation, event_dict, **kwargs):
        event_dict["Api"] = operation

    def _serialize_timestamp(self, timestamp, event_dict, **kwargs):
        event_dict["Timestamp"] = timestamp

    def _serialize_attempts(self, attempts, event_dict, **kwargs):
        event_dict["AttemptCount"] = len(attempts)
        if attempts:
            self._add_fields_from_last_attempt(event_dict, attempts[-1])

    def _add_fields_from_last_attempt(self, event_dict, last_attempt):
        if last_attempt.request_headers:
            # It does not matter which attempt to use to grab the region
            # for the ApiCall event, but SDKs typically do the last one.
            region = self._get_region(last_attempt.request_headers)
            if region is not None:
                event_dict["Region"] = region
            event_dict["UserAgent"] = self._get_user_agent(last_attempt.request_headers)
        if last_attempt.http_status_code is not None:
            event_dict["FinalHttpStatusCode"] = last_attempt.http_status_code
        if last_attempt.parsed_error is not None:
            self._serialize_parsed_error(
                last_attempt.parsed_error, event_dict, "ApiCall"
            )
        if last_attempt.wire_exception is not None:
            self._serialize_wire_exception(
                last_attempt.wire_exception, event_dict, "ApiCall"
            )

    def _serialize_retries_exceeded(self, retries_exceeded, event_dict, **kwargs):
        event_dict["MaxRetriesExceeded"] = 1 if retries_exceeded else 0

    def _serialize_url(self, url, event_dict, **kwargs):
        event_dict["Url"] = url

    def _serialize_request_headers(self, request_headers, event_dict, **kwargs):
        event_dict["UserAgent"] = self._get_user_agent(request_headers)
        region = self._get_region(request_headers)
        if region is not None:
            event_dict["Region"] = region

    def _serialize_http_status_code(self, http_status_code, event_dict, **kwargs):
        event_dict["HttpStatusCode"] = http_status_code

    def _serialize_response_headers(self, response_headers, event_dict, **kwargs):
        for header, entry in self._RESPONSE_HEADERS_TO_EVENT_ENTRIES.items():
            if header in response_headers:
                event_dict[entry] = response_headers[header]

    def _serialize_parsed_error(self, parsed_error, event_dict, event_type, **kwargs):
        field_prefix = "Final" if event_type == "ApiCall" else ""
        event_dict[field_prefix + "AwsException"] = self._truncate(
            parsed_error["Code"], self._MAX_ERROR_CODE_LENGTH
        )
        event_dict[field_prefix + "AwsExceptionMessage"] = self._truncate(
            parsed_error["Message"], self._MAX_MESSAGE_LENGTH
        )

    def _serialize_wire_exception(
        self, wire_exception, event_dict, event_type, **kwargs
    ):
        field_prefix = "Final" if event_type == "ApiCall" else ""
        event_dict[field_prefix + "SdkException"] = self._truncate(
            wire_exception.__class__.__name__, self._MAX_EXCEPTION_CLASS_LENGTH
        )
        event_dict[field_prefix + "SdkExceptionMessage"] = self._truncate(
            str(wire_exception), self._MAX_MESSAGE_LENGTH
        )

    def _get_event_type(self, event):
        if isinstance(event, APICallEvent):
            return "ApiCall"
        elif isinstance(event, APICallAttemptEvent):
            return "ApiCallAttempt"

    def _get_region(self, request_headers):
        if not self._is_signed(request_headers):
            return None
        auth_val = self._get_auth_value(request_headers)
        signature_version, auth_match = self._get_auth_match(auth_val)
        if signature_version != "v4":
            return None
        return auth_match.group("signing_region")

    def _get_user_agent(self, request_headers):
        return self._truncate(
            ensure_unicode(request_headers.get("User-Agent", "")),
            self._MAX_USER_AGENT_LENGTH,
        )

    def _is_signed(self, request_headers):
        return "Authorization" in request_headers

    def _get_auth_value(self, request_headers):
        return ensure_unicode(request_headers["Authorization"])

    def _get_auth_match(self, auth_val):
        for signature_version, regex in self._AUTH_REGEXS.items():
            match = regex.match(auth_val)
            if match:
                return signature_version, match
        return None, None

    def _truncate(self, text, max_length):
        if len(text) > max_length:
            logger.debug(
                "Truncating following value to maximum length of " "%s: %s",
                text,
                max_length,
            )
            return text[:max_length]
        return text


class IAMZMonitorEventAdapter(object):
    def __init__(self, time=time.time):
        """Adapts event emitter events to produce monitor events

        :type time: callable
        :param time: A callable that produces the current time
        """
        self._time = time

    def feed(self, emitter_event_name, emitter_payload):
        """Feed an event emitter event to generate a monitor event

        :type emitter_event_name: str
        :param emitter_event_name: The name of the event emitted

        :type emitter_payload: dict
        :param emitter_payload: The payload to associated to the event
            emitted

        :rtype: BaseMonitorEvent
        :returns: A monitor event based on the event emitter events
            fired
        """
        return self._get_handler(emitter_event_name)(**emitter_payload)

    def _get_handler(self, event_name):
        return getattr(self, "_handle_" + event_name.split(".")[0].replace("-", "_"))

    def _handle_before_parameter_build(self, model, context, **kwargs):
        context["current_api_call_event"] = APICallEvent(
            service=model.service_model.service_id,
            operation=model.wire_name,
            timestamp=self._get_current_time(),
        )

    def _handle_request_created(self, request, **kwargs):
        # request is an botocore.awsrequest.AWSRequest object
        # we can capture relevant fields from it here and map them to the monitoring event to be used by iamzer
        context = request.context
        new_attempt_event = context["current_api_call_event"].new_api_call_attempt(
            timestamp=self._get_current_time()
        )
        new_attempt_event.request_headers = request.headers
        new_attempt_event.url = request.url

        # added for iamzero
        new_attempt_event.data = request.data
        new_attempt_event.params = request.params

        context["current_api_call_attempt_event"] = new_attempt_event

    def _handle_response_received(self, parsed_response, context, exception, **kwargs):
        attempt_event = context.pop("current_api_call_attempt_event")
        attempt_event.latency = self._get_latency(attempt_event)
        if parsed_response is not None:
            attempt_event.http_status_code = parsed_response["ResponseMetadata"][
                "HTTPStatusCode"
            ]
            attempt_event.response_headers = parsed_response["ResponseMetadata"][
                "HTTPHeaders"
            ]
            attempt_event.parsed_error = parsed_response.get("Error")
        else:
            attempt_event.wire_exception = exception
        return attempt_event

    def _handle_after_call(self, context, parsed, **kwargs):
        context["current_api_call_event"].retries_exceeded = parsed[
            "ResponseMetadata"
        ].get("MaxAttemptsReached", False)
        return self._complete_api_call(context)

    def _handle_after_call_error(self, context, exception, **kwargs):
        # If the after-call-error was emitted and the error being raised
        # was a retryable connection error, then the retries must have exceeded
        # for that exception as this event gets emitted **after** retries
        # happen.
        context[
            "current_api_call_event"
        ].retries_exceeded = self._is_retryable_exception(exception)
        return self._complete_api_call(context)

    def _is_retryable_exception(self, exception):
        return isinstance(
            exception, tuple(RETRYABLE_EXCEPTIONS["GENERAL_CONNECTION_ERROR"])
        )

    def _complete_api_call(self, context):
        call_event = context.pop("current_api_call_event")
        call_event.latency = self._get_latency(call_event)
        return call_event

    def _get_latency(self, event):
        return self._get_current_time() - event.timestamp

    def _get_current_time(self):
        return int(self._time() * 1000)