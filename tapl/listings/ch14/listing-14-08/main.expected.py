# Python
import csv
from io import StringIO

csv_str = "name,age\nAlice,30\nBob,25"
reader = csv.DictReader(StringIO(csv_str))

for row in reader:
    print(f"Name: {row['name']}, Age: {row['age']}")
