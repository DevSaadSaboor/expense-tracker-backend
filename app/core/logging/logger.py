import logging
import structlog

from app.core.observability.context import get_user_id,get_operation,get_request_id


def add_request_context(logger,method_name, event_dict):
    event_dict['request_id'] = get_request_id()
    # event_dict['user_id'] = get_user_id()
    event_dict['operation'] = get_operation()
    return event_dict

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        add_request_context,
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO)
)
logger  = structlog.get_logger()


