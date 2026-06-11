# Python
import csv
from io import StringIO

data = "name,age\nAlice,30\nBob,25\nCharlie,35"
reader = csv.DictReader(StringIO(data))

print("People over 28:")
for row in reader:
    name = row["name"]
    age = int(row["age"])
    if age > 28:
        print(f"  {name} ({age})")
