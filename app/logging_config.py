"""日志初始化以及敏感信息脱敏。"""

import logging
from logging.config import dictConfig
import re


SENSITIVE_VALUE_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|authorization|password|token)"
    r"(\s*[:=]\s*)([^\s,;]+)"
)


def redact_sensitive_data(message: str) -> str:
    """遮盖日志文本中常见的凭证字段。"""

    return SENSITIVE_VALUE_PATTERN.sub(r"\1\2***", message)


class SensitiveDataFilter(logging.Filter):
    """在日志写入控制台前统一进行脱敏。"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact_sensitive_data(record.getMessage())
        record.args = ()
        return True


def configure_logging(level: str = "INFO") -> None:
    """配置整个应用的日志格式和级别。

    dictConfig 每次都会替换根 logger 的 handler，重复调用不会叠加输出。
    """

    normalized_level = level.upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "sensitive_data": {"()": SensitiveDataFilter},
            },
            "formatters": {
                "standard": {
                    "format": (
                        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": normalized_level,
                    "formatter": "standard",
                    "filters": ["sensitive_data"],
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {
                "level": normalized_level,
                "handlers": ["console"],
            },
        }
    )
