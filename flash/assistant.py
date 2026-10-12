
from flash.providers import AIProvider, Message


class FlashAssistant:
    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.history: list[Message] = [
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

    def chat(self, message: str) -> str:
        message = message.strip()

        if not message:
            raise ValueError("A mensagem não pode estar vazia.")

        self.history.append({
            "role": "user",
            "content": message,
        })

        try:
            response = self.provider.reply(self.history)

        except Exception:
            self.history.pop()
            raise

        self.history.append({
            "role": "assistant",
            "content": response,
        })
        return response