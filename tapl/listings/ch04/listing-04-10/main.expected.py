# Python
people = [
    {"name": "Zoe", "age": 25},
    {"name": "Al", "age": 60},
    {"name": "John", "age": 1},
]

print("Sorted by age:")
people.sort(key=lambda p: p["age"])
for p in people:
    print(f"  {p['name']} ({p['age']})")
