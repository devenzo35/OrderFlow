import datetime as dt
import json
import logging
from typing import override


class MyJSONFormatter(logging.Formatter):
    def __init__(self, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields: dict[str, str | dt.datetime] = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        message: dict[str, str | dt.datetime] = {}
        for key, val in self.fmt_keys.items():
            if (msg_val := always_fields.pop(val, None)) is not None:
                message[key] = msg_val
            else:
                message[key] = getattr(record, val)

        message.update(always_fields)

        return message
