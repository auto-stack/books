# Python
import base64

original = "hello world"
encoded = base64.b64encode(original.encode()).decode()
print(encoded)

decoded = base64.b64decode(encoded).decode()
print(decoded)

binary = b"\x00\x01\x02\x03"
b64 = base64.b64encode(binary).decode()
print(b64)
