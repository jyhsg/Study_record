# 20天学习

## uv 虚拟环境
虚拟环境初始化：首先运行`uv init`来初始化项目， uv 通常会生成.python-version、pyproject.toml、README.md、main.py

创建虚拟环境：在有 `pyproject.toml` 的项目中执行`uv sync`来同步项目环境，如果是一个全新的项目可以自己手动创建虚拟环境 `uv venv --python 3.11 .venv`。

激活虚拟环境：PowerShell `.venv\Scripts\Activate.ps1`  Bash `source .venv/Scripts/activate`  CMD  .venv\Scripts\activate.bat

退出虚拟环境: deactivate

安装项目依赖: `uv add 包名` 比如`uv add fastapi` 也可以一次性安装多个版本 比如 `uv add fastapi "uvicorn[standard]" pydantic-settings python-dotenv` uv add 会同时完成：修改 pyproject.toml、更新 uv.lock、将包安装到 .venv。 
精确指定版本安装依赖： `uv add "fastapi==0.115.0"`
指定最低版本: `uv add "fastapi>=0.115.0"`
指定版本范围: `指定版本范围`
安装开发依赖：`uv add --dev pytest pytest-asyncio httpx ruff mypy` 

github项目同步环境操作：
git clone https://github.com/jyhsg/Study_record.git
cd Study_record
uv sync

导出 requirements.txt: `uv export --format requirements-txt --output-file requirements.txt`
运行测试：`uv run pytest`
运行代码检查：`uv run ruff check .`
启动 FastAP: `uv run uvicorn app.main:app --reload`

安装正式项目依赖：uv add
复现项目环境：uv sync
在项目环境中运行：uv run
临时兼容 pip 操作：uv pip

## 第一天动手任务

项目已实现：

- `app/config.py`：统一配置类、环境变量读取和配置校验。
- `app/logging_config.py`：日志初始化和常见敏感字段脱敏。
- `app/exceptions.py`：应用、配置和资源异常体系。
- `app/main.py`：命令行入口和 FastAPI 健康检查入口。
- `app/utils/timer.py`：支持同步、异步函数的耗时装饰器。
- `app/utils/test_resource.py`：保证资源释放的上下文管理器。

运行命令行演示：

```powershell
uv run python -m app.main
# 或使用 pyproject.toml 中注册的命令
uv run docpilot-agent
```

运行测试：

```powershell
uv run python -m unittest discover -s tests -v
```

启动 FastAPI 并访问 `http://127.0.0.1:8000/health`：

```powershell
uv run uvicorn app.main:app --reload
```
