from flash.memory import MemoryStore
from flash.providers import AIProvider, Message


class FlashAssistant:
    def __init__(
            self, 
            provider: AIProvider,
            memory: MemoryStore | None = None
        ):
        self.provider = provider
        self.memory = memory or MemoryStore()

        self.system_message: Message = [
            {
                "role": "system",
                "content": (
                    "Seu nome é Flash. Você é uma assistente de IA útil, clara e amigável. "
                    "Responda em português quando o usuário falar português. "
                    "Preste muita atenção em quem realizou cada ação nas mensagens. "
                    "Use o histórico da conversa para responder perguntas sobre o que o usuário disse. "
                    "Se não souber a resposta, admita que não sabe em vez de inventar. Não tem problema admitir erros!"
                )
            }
        ]

        self.history: list[Message] = [
            self.system_message,
            *self.memory.get_recent_messages(limit = 20),
        ]

    def update_memory_context(self) -> None:
        facts = self.memory.get_facts()

        facts_text = "\n".join(
            f"- {content}" for _, content in facts
        )

        self.history[0]["content"] = (
            "Seu nome é Flash. Você é uma assistente de IA útil, clara e amigável. "
            "Responda em português quando o usuário falar português. "
            "Preste muita atenção em quem realizou cada ação nas mensagens. "
            "Use o histórico da conversa para responder perguntas sobre o que o usuário disse. "
            "Se não souber a resposta, admita que não sabe em vez de inventar. Não tem problema admitir erros!"
            "\nFatos armazenados sobre o usuário:\n"
            + (facts_text if facts_text else "Nenhum fato armazenado.")
        )

    def chat(self, message: str) -> str:
        message = message.strip()

        if not message:
            raise ValueError("A mensagem não pode estar vazia.")

        self.history.append({
            "role": "user",
            "content": message,
        })

        try:
            self.update_memory_context()
            response = self.provider.reply(self.history)

        except Exception:
            self.history.pop()
            raise

        self.history.append({
            "role": "assistant",
            "content": response,
        })

        self.memory.add_message("user", message)
        self.memory.add_message("assistant", response)

        return response