class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main():
    start = Time(9, 45, 30)

    # Calling __str__ explicitly
    s = start.__str__()
    print(s)  # 09:45:30

    # __str__ is called automatically by print
    print(start)  # 09:45:30

    # Using f-string interpolation
    print(f"The time is {start}")  # The time is 09:45:30

    # Comparing two times via their string representation
    end = Time(10, 30, 0)
    print(start.__str__() < end.__str__())  # True (lexicographic)

    # Demonstrating formatting control
    noon = Time(12, 0, 0)
    print(noon.__str__())  # 12:00:00


if __name__ == "__main__":
    main()
