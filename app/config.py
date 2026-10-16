"""集中管理应用配置。"""

from collections.abc import Mapping
from dataclasses import dataclass, field
import os

from app.exceptions import ConfigurationError


VALID_ENVIRONMENTS = {"development", "test", "production"}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(frozen=True, slots=True)
class Settings:
    """应用的统一配置对象。

    frozen=True 避免运行过程中被意外修改；repr=False 避免打印配置对象时
    泄露 API Key。
    """

    app_name: str
    app_env: str
    log_level: str
    model_name: str
    test_resource_name: str
    api_key: str | None = field(default=None, repr=False)

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    def require_api_key(self) -> str:
        """在真正调用模型时再要求 API Key，允许本地 demo 无密钥启动。"""

        if not self.api_key:
            raise ConfigurationError("缺少环境变量 LLM_API_KEY")
        return self.api_key


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """从环境变量加载并校验配置。

    environ 参数使测试可以传入独立字典，避免修改真实系统环境。
    """

    values = os.environ if environ is None else environ
    app_env = values.get("APP_ENV", "development").strip().lower()
    log_level = values.get("LOG_LEVEL", "INFO").strip().upper()

    if app_env not in VALID_ENVIRONMENTS:
        allowed = ", ".join(sorted(VALID_ENVIRONMENTS))
        raise ConfigurationError(
            f"APP_ENV={app_env!r} 无效，可选值：{allowed}"
        )

    if log_level not in VALID_LOG_LEVELS:
        allowed = ", ".join(sorted(VALID_LOG_LEVELS))
        raise ConfigurationError(
            f"LOG_LEVEL={log_level!r} 无效，可选值：{allowed}"
        )

    return Settings(
        app_name=values.get("APP_NAME", "DocPilot Agent").strip(),
        app_env=app_env,
        log_level=log_level,
        model_name=values.get("LLM_MODEL_NAME", "demo-model").strip(),
        test_resource_name=values.get(
            "TEST_RESOURCE_NAME", "demo-resource"
        ).strip(),
        api_key=values.get("LLM_API_KEY") or None,
    )


# 保留旧名称，已有学习代码如果导入 Config 仍可继续使用。
Config = Settings
