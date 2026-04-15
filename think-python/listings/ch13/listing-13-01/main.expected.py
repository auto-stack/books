import os


def main():
    # Current working directory
    cwd = os.getcwd()
    print(f"Current directory: {cwd}")

    # Absolute path
    abs_path = os.path.abspath("memo.txt")
    print(f"Absolute path of 'memo.txt': {abs_path}")

    # f-string style formatting in Auto
    num_years = 1.5
    num_camels = 23

    line1 = f"Years of observation: {num_years}"
    line2 = f"Camels spotted: {num_camels}"
    print(line1)
    print(line2)

    # f-string with expressions
    months = int(num_years * 12)
    line3 = f"In {months} months I have spotted {num_camels} camels"
    print(line3)

    # os.path operations
    joined = os.path.join("photos", "jan-2023", "photo1.jpg")
    print(f"Joined path: {joined}")

    # Check if path exists (demonstration)
    print(f"Does 'photos' exist? {os.path.exists('photos')}")

    # isdir and isfile checks
    print(f"Is '.' a directory? {os.path.isdir('.')}")
    print(f"Is 'memo.txt' a file? {os.path.isfile('memo.txt')}")


if __name__ == "__main__":
    main()
