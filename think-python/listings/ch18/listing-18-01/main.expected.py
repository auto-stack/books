from __future__ import annotations

def main():
    # Creating a set from a list
    languages = {"Python", "Auto", "Java", "C++", "Python"}
    print(languages)

    # Adding elements
    languages.add("Rust")
    print(languages)

    # Checking membership
    print("Auto" in languages)
    print("Go" in languages)

    # Removing elements
    languages.remove("C++")
    print(languages)

    # Set size
    print(len(languages))

    # Set operations
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    # Union
    print(a | b)

    # Intersection
    print(a & b)

    # Difference
    print(a - b)

    # Symmetric difference
    print(a ^ b)


if __name__ == "__main__":
    main()
