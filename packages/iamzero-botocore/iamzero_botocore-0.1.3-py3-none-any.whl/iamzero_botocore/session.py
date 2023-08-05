from botocore import monitoring as botomonitoring
from . import monitor
from botocore.session import Session as BaseSession
import os


class Session(BaseSession):
    def _register_components(self):
        super()._register_components()
        self._register_iamzero_monitor()

    def _register_iamzero_monitor(self):
        self._internal_components.lazy_register_component(
            "iamzero_monitor", self._create_iamzero_monitor
        )

    def _create_iamzero_monitor(self):
        # TODO: call AWS STS get-caller-identity endpoint in background to determine identity
        arn = "arn:aws:sts::123456789:assumed-role/AWSReservedSSO_AWSReadOnlyAccess_90da1eee638a66fc/chris@exponentlabs.io"
        user_id = "DSAFLKJHCAYBUAE:chris@exponentlabs.io"
        account = "123456789"

        iamzero_host = os.getenv("IAMZERO_HOST", "https://app.iamzero.dev")

        handler = botomonitoring.Monitor(
            adapter=botomonitoring.MonitorEventAdapter(),
            publisher=monitor.IAMZPublisher(
                host=iamzero_host,
                serializer=monitor.IAMZSerializer(
                    arn=arn, user_id=user_id, account=account
                ),
            ),
        )
        return handler

    def create_client(
        self,
        service_name,
        region_name=None,
        api_version=None,
        use_ssl=True,
        verify=None,
        endpoint_url=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        config=None,
    ):
        client = super().create_client(
            service_name,
            region_name=region_name,
            api_version=api_version,
            use_ssl=use_ssl,
            verify=verify,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            config=config,
        )

        iamzero_monitor = self._get_internal_component("iamzero_monitor")
        if iamzero_monitor is not None:
            iamzero_monitor.register(client.meta.events)
        return client


def get_session(env_vars=None):
    """
    Return a new session object.
    """
    return Session(env_vars)