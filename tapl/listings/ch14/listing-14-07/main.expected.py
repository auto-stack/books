# Python
import os

content = "line1\nline2\nline3"
path = "test_temp.txt"

with open(path, "w") as f:
    f.write(content)

with open(path, "r") as f:
    text = f.read()

line_count = 0
for line in text.split("\n"):
    line_count += 1
    print(f"  [{line_count}] {line}")
print(f"Total lines: {line_count}")

os.remove(path)
