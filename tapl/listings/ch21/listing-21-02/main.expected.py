# Python
import math

def clamp(value, lo, hi):
    return max(lo, min(value, hi))

def main():
    print(min(3, 7))
    print(max(3, 7))
    print(abs(-42))
    print(round(3.7))
    print(math.floor(3.9))
    print(math.ceil(3.1))
    print(clamp(15, 0, 10))
    print(pow(2.0, 10.0))
    print(math.sqrt(144.0))

if __name__ == "__main__":
    main()
