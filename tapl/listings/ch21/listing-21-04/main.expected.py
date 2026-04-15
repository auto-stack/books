# Python

def main():
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_nums = sorted(nums)
    for n in sorted_nums:
        print(n)

    rev = list(reversed([1, 2, 3, 4, 5]))
    print(rev)

    uniq = list(dict.fromkeys([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))
    print(uniq)

    flat = [x for sub in [[1, 2], [3, 4], [5, 6]] for x in sub]
    print(flat)

    names = ["Alice", "Bob", "Carol"]
    scores = [95, 87, 92]
    pairs = list(zip(names, scores))
    for pair in pairs:
        print(pair)

    data = [1, 2, 3, 4, 5, 6, 7]
    chunked = [data[i:i+3] for i in range(0, len(data), 3)]
    for c in chunked:
        print(c)

if __name__ == "__main__":
    main()
