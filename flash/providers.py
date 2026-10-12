
from typing import Protocol


class AIProvider(Protocol):
    def reply(self, message: str) -> str:
        ...


class MockProvider:
    def reply(self, message: str) -> str:
        return f"Recebi tua mensagem: {message}"