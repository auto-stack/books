class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    @staticmethod
    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return Time(hour, minute, second)

    # Operator overloading: comparison
    def is_after(self, other):
        return self.time_to_int() > other.time_to_int()

    # Operator overloading: + operator
    def __add__(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds)

    # Operator overloading: == operator
    def __eq__(self, other):
        return self.time_to_int() == other.time_to_int()


def main():
    start = Time(9, 45, 0)
    end = Time(11, 17, 0)
    duration = Time(1, 32, 0)

    # Comparing: is_after
    print(end.is_after(start))  # True
    print(start.is_after(end))  # False
    print(end.is_after(end))  # False

    # Operator overloading: +
    result = start + duration
    print(result.__str__())  # 11:17:00

    # Chaining additions
    result2 = start + duration + Time(0, 30, 0)
    print(result2.__str__())  # 11:47:00

    # Operator overloading: ==
    print(start == Time(9, 45, 0))  # True
    print(start == end)  # False

    # Combining operators
    total = duration + Time(0, 30, 0)
    finish = start + total
    print(finish.__str__())  # 11:47:00


if __name__ == "__main__":
    main()
