# Python
import re

text = "abc 123 def 456"
replaced = re.sub(r"\d+", "NUM", text)
print(f"Original: {text}")
print(f"Replaced: {replaced}")
