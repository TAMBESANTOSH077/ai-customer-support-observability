import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }

        if hasattr(record, "request_id"):

            log_data["request_id"] = (
                record.request_id
            )

        return json.dumps(log_data)


def setup_logger():

    logger = logging.getLogger(
        "ai_support"
    )

    logger.setLevel(
        logging.INFO
    )

    if not logger.handlers:

        handler = logging.StreamHandler()

        handler.setFormatter(
            JsonFormatter()
        )

        logger.addHandler(
            handler
        )

    return logger