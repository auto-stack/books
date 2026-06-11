# Python
import hashlib

result = hashlib.sha256(b"hello world").hexdigest()
print(f"SHA-256: {result}")
