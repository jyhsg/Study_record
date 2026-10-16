"""DocPilot Agent 的自定义异常。

业务代码只抛出这些有明确含义的异常，程序入口负责把它们转换为
日志、退出码或后续的 HTTP 响应。
"""


class DocPilotError(Exception):
    """应用内可预期异常的基类。"""


class ConfigurationError(DocPilotError):
    """配置缺失、格式错误或取值不合法。"""


class ResourceError(DocPilotError):
    """资源申请、使用或释放失败。"""
