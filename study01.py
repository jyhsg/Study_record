from collections.abc import Callable,Iterator

# def execute_tool(tool: Callable[[str],str],args: str) -> str:
#     return tool(args)

# def search(query: str) -> str:
#     return f"Searching for {query}"

# result = execute_tool(search, "Python programming")
# print(result)  # Output: Searching for Python programming



from dataclasses import dataclass,field

@dataclass
class Message:
    role: str
    content: str
    
message = Message(role="user", content="Hello, how are you?")
print(message)  # Output: Message(role='user', content='Hello, how are you?')


@dataclass
class AgentConfig: 
    model: str = "default-model" # 默认值
    temperature: float = 0.2
    max_steps: int = 10

config = AgentConfig(model="advanced-model", temperature=0.5)
print(config)  # Output: AgentConfig(model='advanced-model', temperature=0.5


# @dataclass
# class Conversation:
#     messages: list[Message] = field(default_factory=list)

# @dataclass(frozen=True)
# class ToolResult:
#     success: bool
#     content: str

# tool_result = ToolResult(success=True, content="Tool executed successfully.")
# print(tool_result)  # Output: ToolResult(success=True, content='Tool executed successfully.')
# tool_result.success = False  # This will raise an error because ToolResult is frozen



# class NumberRange:
#     def __init__(self, start: int, end: int):
#         self.current = start
#         self.end = end

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.current > self.end:
#             raise StopIteration
#         value = self.current
#         self.current += 1
#         return value

# for number in NumberRange(1, 5):
#     print(number,end=", ")  # Output: 1, 2, 3, 4, 5
# def number_range(start: int, end: int) -> Iterator[int]:
#     current = start
#     while current <= end:
#         yield current
#         current += 1
# print(*number_range(1, 5), sep=", ")  # Output: 1, 2, 3, 4, 5


# def stream_answer() -> Iterator[str]:
#     words = ["Agent", "正在", "生成", "回答"]

#     for word in words:
#         yield word

# for chunk in stream_answer():
#     print(chunk, end="")  # Output: Agent 正在 生成 回答

# generator = stream_answer()
# print(list(generator))  # Output: ['Agent', '正在', '生成', '回答']
# print(list(generator))  # Output: [] because the generator has been exhausted


from collections.abc import Callable
from functools import wraps
from typing import Any

from functools import wraps
from typing import Any

# # *args: Any, **kwargs: Any ???? 
# def log_call(func: Callable[..., Any]) -> Callable[..., Any]:
#     @wraps(func)
#     def wrapper(*args: Any, **kwargs: Any) -> Any:
#         print(f"开始调用：{func.__name__}")

#         result = func(*args, **kwargs)

#         print(f"调用结束：{func.__name__}")
#         return result

#     return wrapper

# @log_call
# def add(a: int, b: int) -> int:
#     return a + b

# add(3, 5)  # Output: 开始调用：add



# from collections.abc import Callable
# from functools import wraps
# from typing import Any


# def retry(max_attempts: int) -> Callable[..., Any]:
#     def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
#         @wraps(func)
#         def wrapper(*args: Any, **kwargs: Any) -> Any:
#             last_error: Exception | None = None

#             for attempt in range(1, max_attempts + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except ConnectionError as exc:
#                     last_error = exc
#                     print(f"第 {attempt} 次调用失败")

#             if last_error is not None:
#                 raise last_error

#             raise RuntimeError("未执行任何重试")

#         return wrapper

#     return decorator

# @retry(max_attempts=3)
# def call_model() -> str:
#     raise ConnectionError("模型服务暂时不可用")

# print(call_model())  # Output: 第 1 次调用失败, 第 2 次调用失败, 第 3 次调用失败, ConnectionError: 模型服务暂时不可用