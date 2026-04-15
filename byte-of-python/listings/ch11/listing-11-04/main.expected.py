class Robot:
    def __init__(self, name):
        self.name = name
        print(f'(Initializing {self.name})')

    def say_hi(self):
        print(f'Greetings, my masters call me {self.name}.')

    def die(self):
        print(f'{self.name} is being destroyed!')


def main():
    droid1 = Robot('R2-D2')
    droid1.say_hi()

    droid2 = Robot('C-3PO')
    droid2.say_hi()

    print('\nRobots can do some work here.\n')

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()


if __name__ == "__main__":
    main()
