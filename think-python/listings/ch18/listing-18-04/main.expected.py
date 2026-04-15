def main():
    # Conditional expressions (ternary operator)
    age = 20
    category = "child" if age < 13 else ("teenager" if age < 18 else "adult")
    print(f"Age {age}: {category}")

    score = 85
    grade = ("A" if score >= 90 else ("B" if score >= 80 else ("C" if score >= 70 else ("D" if score >= 60 else "F"))))
    print(f"Score {score}: Grade {grade}")

    # any: at least one element is truthy
    numbers = [0, 0, 0, 1, 0]
    print(any(numbers))

    empty = []
    print(any(empty))

    all_zeros = [0, 0, 0]
    print(any(all_zeros))

    # all: all elements are truthy
    positives = [1, 2, 3, 4]
    print(all(positives))

    mixed = [1, 2, 0, 4]
    print(all(mixed))

    # Practical example: checking if all strings are non-empty
    words = ["hello", "world", "auto"]
    all_nonempty = True
    for word in words:
        if len(word) == 0:
            all_nonempty = False
            break
    print(all_nonempty)

    # Practical example: checking if any string contains a digit
    inputs = ["hello", "test123", "world"]
    has_digit = False
    for s in inputs:
        for c in s:
            if c.isdigit():
                has_digit = True
                break
        if has_digit:
            break
    print(has_digit)

    # Combining conditional expressions with any/all
    scores = [65, 72, 88, 91, 45]

    filtered = []
    for s in scores:
        if s >= 60:
            filtered.append(s)
    print(filtered)
    print(all(filtered))

    # Using any with a generator-like pattern
    any_failing = False
    for s in scores:
        if s < 60:
            any_failing = True
            break
    print(any_failing)


if __name__ == "__main__":
    main()
