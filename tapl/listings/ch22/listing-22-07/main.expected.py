# Python
from urllib.parse import urlparse

u = urlparse("https://example.com/path?query=1")
print(f"Scheme: {u.scheme}")
print(f"Host:   {u.hostname}")
print(f"Path:   {u.path}")
