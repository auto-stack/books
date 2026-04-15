class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main():
    # Creating with all arguments
    t1 = Time(9, 40, 0)
    print(t1.__str__())  # 09:40:00

    # Creating with default values (no arguments)
    t2 = Time()
    print(t2.__str__())  # 00:00:00

    # Partial arguments
    t3 = Time(9)
    print(t3.__str__())  # 09:00:00

    t4 = Time(9, 45)
    print(t4.__str__())  # 09:45:00

    # Named arguments
    t5 = Time(minute=30, second=15)
    print(t5.__str__())  # 00:30:15


if __name__ == "__main__":
    main()
