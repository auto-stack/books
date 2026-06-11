# Python
import json

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {"name": self.name, "age": self.age}

alice = User("Alice", 30)
json_str = json.dumps(alice.to_dict())
print(json_str)

parsed = json.loads(json_str)
print(parsed["name"])
print(parsed["age"])

bob = User("Bob", 25)
users = [alice.to_dict(), bob.to_dict()]
array_json = json.dumps(users)
print(array_json)
