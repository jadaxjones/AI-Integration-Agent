# Jada Jones - agent.py
import anthropic
from tools import parse_spec, extract_endpoints, indentify_auth, generate_client

client = anthropic.Anthropic()

tools = [
    {
        "name": "parse_spec",
        "description": "Parse an OpenAPI spec file (JSON or YAML) and return the raw spec dict",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the OpenAPI spec file",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "extract_endpoints",
        "description": "Extract all endpoints from a parsed OpenAPI spec as a flat list",
        "input_schema": {
            "type": "object",
            "properties": {
                "spec": {
                    "type": "object",
                    "description": "The parsed OpenAPI spec dict",
                }
            },
            "required": ["spec"],
        },
    },
    {
        "name": "identify_auth",
        "description": "Identify the authentication scheme used by the API",
        "input_schema": {
            "type": "object",
            "properties": {
                "spec": {
                    "type": "object",
                    "description": "The parsed OpenAPI spec dict",
                }
            },
            "required": ["spec"],
        },
    },
    {
        "name": "generate_client",
        "description": "Generate a Python client class from endpoints, auth info, and base URL",
        "input_schema": {
            "type": "object",
            "properties": {
                "endpoints": {"type": "array"},
                "auth": {"type": "object"},
                "base_url": {"type": "string"},
            },
            "required": ["endpoints", "auth", "base_url"],
        },
    },
]

def run_agent(spec_path: str):
    print(f"Running agent on {spec_path}...")

    messages = [
        {
            "role": "user",
            "content": f"Generate a Python client for the API spec at {spec_path}. Parse the spec, extract the endpoints, identify the auth, and generate the client code."
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(block.text)
            break
    
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Calling tool: {block.name} with {block.input}")

                if block.name == "parse_spec":
                    result = parse_spec(block.input["path"])
                elif block.name == "extract_endpoints":
                    result = extract_endpoints(block.input["spec"])
                elif block.name == "identify_auth":
                    result = indentify_auth(block.input["spec"])
                elif block.name == "generate_client":
                    result = generate_client(
                        block.input["endpoints"],
                        block.input["auth"],
                        block.input["base_urls"]
                    )
                else:
                    result = {"error": f"Unknown tool: {block.name}"}

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    run_agent("specs/petstore.yaml")