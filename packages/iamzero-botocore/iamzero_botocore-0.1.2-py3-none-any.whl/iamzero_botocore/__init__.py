import logging

__version__ = "0.1.0"


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# Configure default logger to do nothing
log = logging.getLogger("iamzero_botocore")
log.addHandler(NullHandler())