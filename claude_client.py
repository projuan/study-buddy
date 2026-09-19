import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-opus-5"


def ask_claude(prompt: str, system: str = "") -> str:
    message = _client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


if __name__ == "__main__":
    reply = ask_claude(
        prompt="Say hello and tell me one interesting fact about spaced repetition.",
        system="You are a friendly study assistant.",
    )
    print(reply)
