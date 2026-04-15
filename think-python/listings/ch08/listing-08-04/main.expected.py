import re

def main():
    text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."

    # Basic search
    pattern = "Dracula"
    result = re.search(pattern, text)
    print(f"Found: {result.group()}")
    print(f"Span: {result.span()}")

    # Search that fails
    result2 = re.search("Count", text)
    print(f"Not found: {result2}")

    # Alternation: match either name
    pattern2 = "Mina|Murray"
    result3 = re.search(pattern2, "Mina Murray was there")
    print(f"Alternation: {result3.group()}")

    # Anchors: start and end of string
    result4 = re.search("^Dracula", "Dracula is here")
    print(f"Starts with Dracula: {result4.group()}")

    result5 = re.search("Harker$", "Mr. Harker")
    print(f"Ends with Harker: {result5.group()}")

    # Optional character with ?
    pattern3 = "colou?r"
    result6 = re.sub(pattern3, "color", "The colour of the sky")
    print(f"Sub colour: {result6}")
    result7 = re.sub(pattern3, "color", "The color of the sky")
    print(f"Sub color: {result7}")

    # Grouping with parentheses
    pattern4 = "cent(er|re)"
    result8 = re.sub(pattern4, "center", "the centre of town")
    print(f"Sub centre: {result8}")
    result9 = re.sub(pattern4, "center", "the center of town")
    print(f"Sub center: {result9}")

    # findall: find all matches
    words = "cat bat rat cat hat"
    result10 = re.findall("cat", words)
    print(f"findall cat: {result10}")


if __name__ == "__main__":
    main()
