from ollama import chat
from typing import Protocol


Message = dict[str, str]

class AIProvider(Protocol):
    def reply(self, message: str) -> str:
        ...


class MockProvider:
    def reply(self, messages: list[Message]) -> str:
        last_message = messages[-1]["content"]
        return f"Recebi tua mensagem: {last_message}"

class OllamaProvider:
    def __init__(self, model: str = "qwen3:1.7b"):
        self.model = model

    def reply(self, messages:list[Message]) -> str:
        response = chat(
            model= self.model,
            messages= messages,
        )

        return response.message.content or ""