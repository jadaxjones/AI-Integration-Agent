# AI Integration Agent

A tool-use agent that reads any OpenAPI spec and automatically generates a production-ready Python client — no manual API documentation reading required. Uses a RAG layer to retrieve relevant schema context before generating code, reducing hallucinated endpoint signatures and improving output quality.

## How it works

1. Parses a JSON or YAML OpenAPI spec file
2. Extracts all endpoints, methods, and parameters
3. Indexes endpoints into ChromaDB using sentence-transformers embeddings
4. Identifies the authentication scheme (API key, Bearer token, OAuth2)
5. Uses the Anthropic SDK tool-use loop to orchestrate the process
6. Retrieves relevant schema context via RAG before generating code
7. Generates a Python client class with a method for every endpoint

## Setup

```bash
# Install dependencies
pip install anthropic pyyaml python-dotenv sentence-transformers chromadb

# Add your Anthropic API key
cp .env.example .env
# Edit .env and paste your key

# Add a spec file to the specs/ folder, then run
python agent.py
```

## Project Structure

```
AI-Integration-Agent/
├── tools.py        # Core functions: parse_spec, extract_endpoints, identify_auth, generate_client
├── agent.py        # Anthropic SDK tool-use agent loop
├── rag.py          # RAG layer: sentence-transformers embeddings + ChromaDB retrieval
├── test.py         # Test tools independently against a spec file
├── specs/          # Drop OpenAPI spec files here (JSON or YAML)
└── output/         # Generated client code written here
```

## Example

Drop any OpenAPI spec into `specs/` and run:

```bash
python agent.py
```

The agent calls tools in sequence — parse, extract, index into ChromaDB, identify auth, retrieve relevant context, generate — and writes the finished client to `output/client.py`.

## Tech

- Python
- Anthropic SDK (tool-use / agentic workflow)
- sentence-transformers (endpoint embeddings)
- ChromaDB (vector store for schema retrieval)
- PyYAML
