class Time:
    """Represents the time of day."""

    def print_time(self):
        s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        print(s)

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    def add_time(self, hours, minutes, seconds):
        duration = make_time(hours, minutes, seconds)
        total = Time.time_to_int(self) + Time.time_to_int(duration)
        return Time.int_to_time(total)

    @staticmethod
    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return make_time(hour, minute, second)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def main():
    start = make_time(9, 45, 0)

    # Calling a method on an instance
    start.print_time()  # 09:45:00

    # Another method
    secs = start.time_to_int()
    print(f"Seconds since midnight: {secs}")  # 35100

    # Calling a method that returns a new object
    end = start.add_time(1, 32, 0)
    end.print_time()  # 11:17:00

    # Calling the static method via the class
    t = Time.int_to_time(3661)
    t.print_time()  # 01:01:01


if __name__ == "__main__":
    main()
