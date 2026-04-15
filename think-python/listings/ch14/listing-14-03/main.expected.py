class Time:
    pass


def print_time(time):
    s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def time_to_int(time):
    minutes = time.hour * 60 + time.minute
    seconds = minutes * 60 + time.second
    return seconds


def int_to_time(seconds):
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    return make_time(hour, minute, second)


# Modifier: changes the object in place
def increment_time(time, hours, minutes, seconds):
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    carry, time.second = divmod(time.second, 60)
    carry, time.minute = divmod(time.minute + carry, 60)
    _, time.hour = divmod(time.hour + carry, 24)


# Pure function: does not modify the original
def add_time(time, hours, minutes, seconds):
    duration = make_time(hours, minutes, seconds)
    total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)


def main():
    # --- Modifier approach ---
    start = make_time(9, 40, 0)
    print("Start (modifier): ", end="")
    print_time(start)  # 09:40:00

    increment_time(start, 1, 32, 0)
    print("After increment:  ", end="")
    print_time(start)  # 11:12:00
    # Note: start has been changed!

    # --- Pure function approach ---
    fresh = make_time(9, 40, 0)
    end = add_time(fresh, 1, 32, 0)
    print("Start (pure):     ", end="")
    print_time(fresh)  # 09:40:00  -- unchanged!
    print("End (pure):       ", end="")
    print_time(end)  # 11:12:00

    # Pure function with large values
    end2 = add_time(fresh, 0, 90, 120)
    print("End (+90m +120s): ", end="")
    print_time(end2)  # 11:12:00

    # Convert to/from int
    t = make_time(1, 1, 1)
    secs = time_to_int(t)
    print(f"01:01:01 = {secs} seconds")  # 3661 seconds
    back = int_to_time(secs)
    print_time(back)  # 01:01:01


if __name__ == "__main__":
    main()
