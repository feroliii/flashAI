
from flash.assistant import FlashAssistant
from flash.providers import MockProvider


def test_chat_returns_provider_response():
    flash = FlashAssistant(MockProvider())

    result = flash.chat("Olá")

    assert result == "Recebi tua mensagem: Olá"


def test_empty_message_is_rejected():
    flash = FlashAssistant(MockProvider())

    try:
        flash.chat("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")