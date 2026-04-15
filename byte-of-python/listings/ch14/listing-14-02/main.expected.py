import os
import platform
import logging


def main():
    platform_name = platform.platform()
    user_home = os.path.expanduser("~")

    log_file: str
    if platform_name.contains("Windows"):
        home_drive = os.environ.get("HOMEDRIVE", "C:")
        home_path = os.environ.get("HOMEPATH", "\\")
        log_file = os.path.join(home_drive + home_path, "test.log")
    else:
        log_file = os.path.join(user_home, "test.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s : %(levelname)s : %(message)s",
        filename=log_file,
    )

    logging.debug("Start of the program")
    logging.info("Doing something")
    logging.warning("Dying now")

    print(f"Logging to: {log_file}")
    print("Check the log file for details.")


if __name__ == "__main__":
    main()
