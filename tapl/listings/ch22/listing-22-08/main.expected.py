# Python
from urllib.parse import urlparse, parse_qs

u = urlparse("https://example.com/rust?name=hello&age=20")
print(f"Query string: {u.query}")

params = parse_qs(u.query)
print(f"Parameter count: {len(params)}")
