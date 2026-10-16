"""用于练习资源生命周期管理的测试资源。"""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
import logging

from app.exceptions import ResourceError


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class TestResource:
    """模拟数据库连接、文件句柄等需要显式释放的资源。"""

    name: str
    is_open: bool = False
    records: list[str] = field(default_factory=list)

    def open(self) -> None:
        if self.is_open:
            raise ResourceError(f"资源 {self.name!r} 已经打开")
        self.is_open = True
        logger.info("测试资源已打开 resource=%s", self.name)

    def write(self, value: str) -> None:
        if not self.is_open:
            raise ResourceError(f"资源 {self.name!r} 尚未打开")
        self.records.append(value)
        logger.debug("测试资源写入完成 resource=%s", self.name)

    def close(self) -> None:
        if self.is_open:
            self.is_open = False
            logger.info("测试资源已关闭 resource=%s", self.name)


@contextmanager
def managed_test_resource(name: str) -> Iterator[TestResource]:
    """申请测试资源，并保证正常或异常退出时都释放资源。"""

    resource = TestResource(name=name)
    resource.open()
    try:
        yield resource
    finally:
        resource.close()
