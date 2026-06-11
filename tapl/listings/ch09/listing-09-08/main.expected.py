# Python
def main():
    msg = "hello"
    try:
        result = msg
        val = result
        print(f"Got: {val}")

        raise Exception("something went wrong")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
