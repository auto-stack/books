# Python
import os

os.environ["AUTO_GREETING"] = "Hello from Auto"

val = os.environ.get("AUTO_GREETING", "default")
print(f"Greeting: {val}")

missing = os.environ.get("NONEXISTENT_VAR", "not set")
print(f"Missing: {missing}")
