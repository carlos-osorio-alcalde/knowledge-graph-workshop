"""Web UI for the ontology agent.

Usage:
    uv run python -m src.server

Then open http://localhost:5000 in a browser. Requires OPENROUTER_API_KEY in
the environment or a .env file (see ontology_agent.build_client).
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

from .ontology_agent import (
    DEFAULT_MODEL,
    ask,
    build_client,
    build_system_prompt,
)

UI_DIR = Path(__file__).parent / "ui"

app = Flask(__name__, static_folder=str(UI_DIR), static_url_path="")
_system_prompt = build_system_prompt()
_client: OpenAI | None = None


@app.get("/")
def index():
    return send_from_directory(UI_DIR, "index.html")


@app.post("/api/ask")
def api_ask():
    global _client

    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400

    if _client is None:
        try:
            _client = build_client()
        except RuntimeError as error:
            return jsonify({"error": str(error)}), 503

    answer = ask(question, _system_prompt, _client, model=DEFAULT_MODEL)
    return jsonify({"answer": answer})


def main() -> None:
    app.run(port=5000, debug=False)


if __name__ == "__main__":
    main()