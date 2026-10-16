"""函数执行时间统计装饰器。"""

from collections.abc import Callable
from functools import wraps
import inspect
import logging
from time import perf_counter
from typing import Any, TypeVar, cast


Function = TypeVar("Function", bound=Callable[..., Any])


def log_execution_time(func: Function) -> Function:
    """记录同步或异步函数的执行时间，并保留原函数元信息。"""

    logger = logging.getLogger(func.__module__)

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            succeeded = False
            try:
                result = await func(*args, **kwargs)
                succeeded = True
                return result
            finally:
                elapsed_ms = (perf_counter() - start) * 1000
                logger.info(
                    "函数执行完成 function=%s elapsed_ms=%.3f success=%s",
                    func.__qualname__,
                    elapsed_ms,
                    succeeded,
                )

        return cast(Function, async_wrapper)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter()
        succeeded = False
        try:
            result = func(*args, **kwargs)
            succeeded = True
            return result
        finally:
            elapsed_ms = (perf_counter() - start) * 1000
            logger.info(
                "函数执行完成 function=%s elapsed_ms=%.3f success=%s",
                func.__qualname__,
                elapsed_ms,
                succeeded,
            )

    return cast(Function, wrapper)
