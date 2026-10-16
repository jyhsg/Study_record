import asyncio
import logging
import unittest

from app.config import load_settings
from app.exceptions import ConfigurationError, ResourceError
from app.logging_config import redact_sensitive_data
from app.utils.test_resource import TestResource, managed_test_resource
from app.utils.timer import log_execution_time


class SettingsTests(unittest.TestCase):
    def test_load_settings_uses_defaults(self) -> None:
        settings = load_settings({})

        self.assertEqual(settings.app_env, "development")
        self.assertEqual(settings.log_level, "INFO")
        self.assertEqual(settings.model_name, "demo-model")

    def test_environment_values_override_defaults(self) -> None:
        settings = load_settings(
            {
                "APP_ENV": "test",
                "LOG_LEVEL": "debug",
                "LLM_MODEL_NAME": "test-model",
                "LLM_API_KEY": "secret-value",
            }
        )

        self.assertEqual(settings.app_env, "test")
        self.assertEqual(settings.log_level, "DEBUG")
        self.assertEqual(settings.require_api_key(), "secret-value")
        self.assertNotIn("secret-value", repr(settings))

    def test_invalid_log_level_raises_configuration_error(self) -> None:
        with self.assertRaises(ConfigurationError):
            load_settings({"LOG_LEVEL": "verbose"})

    def test_require_api_key_fails_when_key_is_missing(self) -> None:
        settings = load_settings({})

        with self.assertRaises(ConfigurationError):
            settings.require_api_key()


class LoggingTests(unittest.TestCase):
    def test_sensitive_values_are_redacted(self) -> None:
        message = "api_key=abc123 password:hello token=my-token"

        redacted = redact_sensitive_data(message)

        self.assertEqual(redacted, "api_key=*** password:*** token=***")


class TimerTests(unittest.TestCase):
    def test_sync_decorator_preserves_name_and_records_time(self) -> None:
        @log_execution_time
        def add(left: int, right: int) -> int:
            return left + right

        with self.assertLogs(level=logging.INFO) as captured:
            result = add(2, 3)

        self.assertEqual(result, 5)
        self.assertEqual(add.__name__, "add")
        self.assertIn("elapsed_ms=", " ".join(captured.output))

    def test_async_decorator_supports_coroutines(self) -> None:
        @log_execution_time
        async def double(value: int) -> int:
            return value * 2

        with self.assertLogs(level=logging.INFO):
            result = asyncio.run(double(4))

        self.assertEqual(result, 8)


class ResourceTests(unittest.TestCase):
    def test_context_manager_opens_and_closes_resource(self) -> None:
        resource: TestResource

        with managed_test_resource("normal-resource") as resource:
            self.assertTrue(resource.is_open)
            resource.write("record")

        self.assertFalse(resource.is_open)
        self.assertEqual(resource.records, ["record"])

    def test_context_manager_closes_resource_after_exception(self) -> None:
        resource: TestResource | None = None

        with self.assertRaisesRegex(RuntimeError, "模拟业务异常"):
            with managed_test_resource("failing-resource") as resource:
                raise RuntimeError("模拟业务异常")

        self.assertIsNotNone(resource)
        assert resource is not None
        self.assertFalse(resource.is_open)

    def test_closed_resource_rejects_write(self) -> None:
        resource = TestResource("closed-resource")

        with self.assertRaises(ResourceError):
            resource.write("invalid")


if __name__ == "__main__":
    unittest.main()
