# Python
import json

def main():
    alice = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    json_str = json.dumps(alice)
    print(json_str)

    parsed = json.loads(json_str)
    print(parsed["name"])
    print(parsed["age"])

    pretty = json.dumps(alice, indent=2)
    print(pretty)

    bob = {"name": "Bob", "age": 25, "email": "bob@example.com"}
    users = [alice, bob]
    users_json = json.dumps(users)
    print(users_json)

if __name__ == "__main__":
    main()
