from tools import parse_spec, extract_endpoints, indentify_auth, genetate_client

spec = parse_spec("specs/petstore.yaml")

endppoints = extract_endpoints(spec)
for e in endppoints:
    print(e)

auth = indentify_auth(spec)
print("Auth:", auth)

base_url = spec.get("servers", [{}])[0].get("url", "https://api.example.com")
client_code = genetate_client(endppoints, auth, base_url)

with open("output/client.py", "w") as f:
    f.write(client_code)

print("Generated client.py")