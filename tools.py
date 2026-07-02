# Jada Jones - tools.py 
import json
import yaml

def parse_spec(path: str) -> dict:
    with open(path) as f: 
        if path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.safe_load(f)
        return json.load(f)

def extract_endpoints(spec: dict) -> list:
    endpoints = []
    for path, methods in spec["paths"].items():
        for method, details in methods.items():
            if method in ("get", "post", "put", "patch", "delete"):
                endpoints.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "parameters": details.get("parameters", []),
                    "request_body": details.get("requestBody", {}),
                    "responses": details.get("responses", {}),
                    "operation_id": details.get("operationId", ""),
                })
    return endpoints

def indentify_auth(spec: dict) -> dict:
    schemes = spec.get("components", {}).get("securitySchemes", {})
    global_security = spec.get("security", [])

    if not schemes:
        return {"type": "none"}
    
    for name, details in schemes.items():
        scheme_type = details.get("type", "")

        if scheme_type == "apiKey":
            return {
                "type": "apiKey",
                "name": details.get("name", ""),
                "in": details.get("in", "header"),
            }
        
        if scheme_type == "http":
            return {
                "type": "http",
                "scheme": details.get("scheme", "bearer"),
            }
        
        if scheme_type == "oauth2":
            return {
                "type": "oauth2",
            }
    return {"type": "unknown"}

def genetate_client(endpoints: list, auth: dict, base_url: str) -> str:
    lines = []

    lines.append("import requests")
    lines.append("")
    lines.append("")
    lines.append("class APIClient:")
    lines.append(f'          BASE_URL = "{base_url}"')
    lines.append("")

    if auth["type"] == "apiKey":
        lines.append("      def __init__(self, api_key: str):")
        if auth["in"] == "header":
            lines.append(f'         self.headers = {{"{auth["name"]}": api_key}}')
        else:
            lines.append(f'         self.api_key = api_key')
    elif auth["type"] == "http":
        lines.append("      def __init__(self, token: str):")
        lines.append('               self.headers = {"Authorization": f"Bearer {token}"}')
    else:
        lines.append("      def __init__(self):")
        lines.append("               self.headers = {}")

    lines.append("")

    for e in endpoints:
        method = e["method"].lower()
        operation_id = e["operation_id"] or (method + "_" + e["path"].replace("/", "_").strip("_"))
        params = [p["name"] for p in e["parameters"] if p.get("required")]

        args = ", ".join(params)
        if args: 
            args = ", " + args

        lines.append(f"      def {operation_id}(self{args}):")
        lines.append(f'               url = self.BASE_URL + f"{e["path"]}"')
        lines.append(f'               response = requests.{method}(url, headers=self.headers)')
        lines.append("              response.raise_for_status()")
        lines.append("              return response.json()")
        lines.append("")
    return "\n".join(lines)