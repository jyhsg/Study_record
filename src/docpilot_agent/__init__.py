def main() -> None:
    """uv 项目脚本入口，复用 app.main 中的真实启动逻辑。"""

    from app.main import main as run_application

    raise SystemExit(run_application())
