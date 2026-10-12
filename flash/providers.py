from ollama import chat
from typing import Protocol


class AIProvider(Protocol):
    def reply(self, message: str) -> str:
        ...


class MockProvider:
    def reply(self, message: str) -> str:
        return f"Recebi tua mensagem: {message}"

class OllamaProvider:
    def __init__(self, model: str = "qwen3:1.7b"):
        self.model = model

    def reply(self, message:str) -> str:
        response = chat(
            model= self.model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return response.message.content or ""