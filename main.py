from flash.assistant import FlashAssistant
from flash.providers import OllamaProvider

def main():
    provider = OllamaProvider()
    flash = FlashAssistant(provider)

    print("Flash online! 'sair' para encerrar.")

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

if __name__ == "__main__":
    main()