
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def ask_ai(prompt: str) -> str:
    """
    Send a prompt to the locally running Ollama model.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result.get(
            "response",
            "Sorry, I couldn't generate a response."
        )

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Please start Ollama and try again."

    except requests.exceptions.Timeout:
        return "The AI model took too long to respond. Please try again."

    except requests.exceptions.RequestException as error:
        print("Ollama API Error:", error)
        return "Something went wrong while communicating with the AI model."
