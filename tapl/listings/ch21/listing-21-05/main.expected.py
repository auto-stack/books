# Python
from datetime import datetime, timedelta

def main():
    now = datetime.now()
    print(now)

    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted)

    parsed = datetime.strptime("2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
    print(parsed)

    duration = timedelta(hours=2, minutes=30)
    print(duration)

    later = now + duration
    print(later)

    diff = later - now
    print(int(diff.total_seconds() / 60))

if __name__ == "__main__":
    main()
