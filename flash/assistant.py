
from flash.providers import AIProvider


class FlashAssistant:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def chat(self, message: str) -> str:
        message = message.strip()

        if not message:
            raise ValueError("A mensagem não pode estar vazia.")

        return self.provider.reply(message)