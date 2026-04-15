class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f'{self.name} makes a sound')


class Dog(Animal):
    def speak(self):
        print(f'{self.name} says Woof!')


class Cat(Animal):
    def speak(self):
        print(f'{self.name} says Meow!')


def main():
    animals = [Dog('Rex'), Cat('Whiskers'), Animal('Creature')]
    for animal in animals:
        animal.speak()


if __name__ == "__main__":
    main()
