from flash.assistant import FlashAssistant
from flash.providers import OllamaProvider
from flash.memory import MemoryStore

def main():
    provider = OllamaProvider()
    memory = MemoryStore()
    flash = FlashAssistant(provider, memory=memory,)

    print("Flash online! 'sair' para encerrar.")

    try:
        while True:
            message = input("\nVocê: ").strip()

            if message.lower() == 'sair':
                print("Flash: Até mais!")
                break

            if not message:
                continue

            try:
                response = flash.chat(message)
                print(f"\nFlash: {response}")
            except Exception as error:
                print(f"\nErro ao conversar com o Ollama: {error}")

    finally:
        memory.close()

if __name__ == "__main__":
    main()