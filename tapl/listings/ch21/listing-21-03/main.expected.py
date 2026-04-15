# Python
import os

def main():
    path = os.path.join("data", "output.txt")
    print(path)

    with open(path, "w") as f:
        f.write("Hello from Auto!")
    with open(path, "r") as f:
        content = f.read()
    print(content)

    print(os.path.exists(path))
    print(os.path.exists("nonexistent.txt"))

    os.makedirs("data/backup", exist_ok=True)
    for entry in os.listdir("data"):
        print(entry)

if __name__ == "__main__":
    main()
