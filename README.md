# knowledge-graph-workshop

A playground for learning how knowledge graphs and ontologies work, and for exploring an ontology with a graph visualizer and an LLM-powered assistant.

## Project contents

- [`ontology/ontology.owl.ttl`](ontology/ontology.owl.ttl) is the hand-written OWL/RDF ontology for a supermarket and retail domain.
- [`graph-view/visualize.html`](graph-view/visualize.html) is a standalone browser-based Turtle graph visualizer. It uses [`graph-view/vis-network.min.js`](graph-view/vis-network.min.js) and includes a small Turtle parser. Open the HTML file in a browser and load a `.ttl` file with its file picker.
- [`src/ontology_agent.py`](src/ontology_agent.py) reads the ontology and sends it with questions to an LLM through OpenRouter. It supports one-shot questions and an interactive terminal session.
- [`src/server.py`](src/server.py) serves a small Flask web interface for asking questions about the ontology. Its page is [`src/ui/index.html`](src/ui/index.html).

## Setup

Requires Python 3.13 or later and [uv](https://docs.astral.sh/uv/).

Install the project dependencies:

```bash
uv sync
```

The assistant requires an OpenRouter API key. Create a `.env` file in the repository root (it is gitignored) with:

```env
OPENROUTER_API_KEY=your_key_here
```

Do not commit or share your API key.

## Run the assistant

Ask one question from the terminal:

```bash
uv run python -m src.ontology_agent "What classes exist for pricing?"
```

Start an interactive terminal session:

```bash
uv run python -m src.ontology_agent
```

Start the web interface, then open <http://localhost:5000>:

```bash
uv run python -m src.server
```

## Visualize the ontology

Open `graph-view/visualize.html` directly in a browser and load `ontology/ontology.owl.ttl` using the page's file picker.

## Project layout

```text
.
├── graph-view/
│   ├── vis-network.min.js
│   └── visualize.html
├── ontology/
│   └── ontology.owl.ttl
├── src/
│   ├── __init__.py
│   ├── ontology_agent.py
│   ├── server.py
│   └── ui/
│       └── index.html
├── .env                 # local API key; not committed
├── pyproject.toml
└── README.md
```
