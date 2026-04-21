import os

from ai.client_factory import get_ai_client


def test_ai_integration():

    # -------------------------------------------------------------
    # Arrange
    # -------------------------------------------------------------

    provider = os.getenv(
        "AI_PROVIDER",
        "ollama",
    )

    client = get_ai_client(provider)

    # model variable removed (was unused)

    prompt = "Respond with the word OK only."

    # -------------------------------------------------------------
    # Act
    # -------------------------------------------------------------

    response_text = client.generate(
        prompt=prompt,
        temperature=0,
        max_tokens=20,
    )

    # -------------------------------------------------------------
    # Assert
    # -------------------------------------------------------------

    assert response_text is not None
    assert "ok" in response_text.lower()
