"""Chat agent that answers questions about the practice ontology via OpenRouter.

The ontology file is small enough to paste directly into the system prompt, so
the model reads it as plain text rather than calling tools to query it.

Usage:
    uv run python -m ai_knowledge_graphs.agent.ontology_agent "What classes exist for pricing?"
    uv run python -m ai_knowledge_graphs.agent.ontology_agent  # interactive REPL

Requires OPENROUTER_API_KEY in the environment or a .env file.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_ONTOLOGY_PATH = Path(__file__).parent.parent / "ontology" / "ontology.owl.ttl"
DEFAULT_MODEL = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-5.5-sonnet")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT_TEMPLATE = """\
You are an assistant ontology exploration assistant. Below is the full contents of an 
OWL/RDF ontology, written in Turtle syntax. Answer questions about it by 
reading the classes, properties, and comments directly. Your an assistant so answer question 
naturally

```turtle
{ontology}
```
"""

def build_system_prompt(path: Path = DEFAULT_ONTOLOGY_PATH) -> str:
    ontology_text = path.read_text()
    return SYSTEM_PROMPT_TEMPLATE.format(ontology=ontology_text)


def build_client() -> OpenAI:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your .env file or export it in the shell."
        )
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def ask(question: str, system_prompt: str, client: OpenAI, model: str = DEFAULT_MODEL) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> None:
    import sys

    system_prompt = build_system_prompt()
    client = build_client()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(ask(question, system_prompt, client))
        return

    print("Ontology agent ready. Ctrl-D to exit.")
    while True:
        try:
            question = input("> ").strip()
        except EOFError:
            print()
            break
        if not question:
            continue
        print(ask(question, system_prompt, client))


if __name__ == "__main__":
    main()