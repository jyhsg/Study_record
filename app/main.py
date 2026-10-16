"""DocPilot Agent 程序入口。"""

import logging

from fastapi import FastAPI

from app.config import Settings, load_settings
from app.exceptions import DocPilotError
from app.logging_config import configure_logging
from app.utils.test_resource import managed_test_resource
from app.utils.timer import log_execution_time


app = FastAPI(title="DocPilot Agent")
logger = logging.getLogger(__name__)


@app.get("/health")
def health_check() -> dict[str, str]:
    """供部署平台检查服务是否存活。"""

    return {"status": "ok"}


@log_execution_time
def run_demo(settings: Settings) -> None:
    """演示统一配置、日志、装饰器和上下文管理器。"""

    logger.info(
        "应用启动 app=%s environment=%s model=%s",
        settings.app_name,
        settings.app_env,
        settings.model_name,
    )

    with managed_test_resource(settings.test_resource_name) as resource:
        resource.write("DocPilot Agent 第一日练习")
        logger.info(
            "测试资源操作完成 resource=%s records=%d",
            resource.name,
            len(resource.records),
        )


def main() -> int:
    """命令行程序入口，返回 0 表示成功，返回 1 表示可预期失败。"""

    try:
        settings = load_settings()
        configure_logging(settings.log_level)
        run_demo(settings)
    except DocPilotError as exc:
        configure_logging("ERROR")
        logging.getLogger(__name__).error("程序启动失败 error=%s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
