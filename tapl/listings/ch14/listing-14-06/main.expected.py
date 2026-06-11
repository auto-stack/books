# Python
import os

with open("lines.txt", "w") as f:
    f.write("Rust\nFun\nAuto")

with open("lines.txt", "r") as f:
    data = f.read()

print(f"Content: {data}")
print(f"Length: {len(data)}")

for line in data.split("\n"):
    print(f"  Line: {line}")

os.remove("lines.txt")
