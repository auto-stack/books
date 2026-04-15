# Object Oriented Programming

In all the programs we wrote till now, we have designed our program around functions i.e. blocks of statements which manipulate data. This is called the _procedure-oriented_ way of programming. There is another way of organizing your program which is to combine data and functionality and wrap it inside something called an object. This is called the _object oriented_ programming paradigm. Most of the time you can use procedural programming, but when writing large programs or have a problem that is better suited to this method, you can use object oriented programming techniques.

Classes and objects are the two main aspects of object oriented programming. A **class** creates a new _type_ where **objects** are **instances** of the class. An analogy is that you can have variables of type `int` which translates to saying that variables that store integers are variables which are instances (objects) of the `int` class.

> **Note for Static Language Programmers**
>
> Note that even integers are treated as objects (of the `int` class). This is unlike C++ and Java (before version 1.5) where integers are primitive native types.
>
> See `help(int)` for more details on the class.
>
> C# and Java 1.5 programmers will find this similar to the _boxing and unboxing_ concept.

Objects can store data using ordinary variables that _belong_ to the object. Variables that belong to an object or class are referred to as **fields**. Objects can also have functionality by using functions that _belong_ to a class. Such functions are called **methods** of the class. This terminology is important because it helps us to differentiate between functions and variables which are independent and those which belong to a class or object. Collectively, the fields and methods can be referred to as the **attributes** of that class.

Fields are of two types - they can belong to each instance/object of the class or they can belong to the class itself. They are called **instance variables** and **class variables** respectively.

A class is created using the `type` keyword in Auto. The fields and methods of the class are listed in a block enclosed by `{}`.

## The `&self`

Class methods have only one specific difference from ordinary functions - they must have an extra first parameter that has to be added to the beginning of the parameter list, but you **do not** give a value for this parameter when you call the method, the `a2p` transpiler (via Python) will provide it. In Auto, this particular parameter is written as `&self` and it refers to the object _itself_.

Although you could imagine giving any name for this parameter, Auto uses the Rust-inspired `&self` convention which makes it immediately clear that this is a reference to the current instance. This is a deliberate design choice that differentiates Auto from Python's `self` convention while keeping the same underlying semantics.

> **Note for C++/Java/C# Programmers**
>
> The `&self` in Auto (equivalent to Python's `self`) is conceptually similar to the `this` pointer in C++ and the `this` reference in Java and C#.

You must be wondering how Python gives the value for `self` and why you don't need to give a value for it. An example will make this clear. Say you have a class called `MyClass` and an instance of this class called `myobject`. When you call a method of this object as `myobject.method(arg1, arg2)`, this is automatically converted by Python into `MyClass.method(myobject, arg1, arg2)` - this is all the special `self` is about.

This also means that if you have a method which takes no arguments, then you still have to have one argument - `&self`.

> **Note for Python Programmers:**
>
> In Python, the `self` parameter is a naming convention (though strongly recommended). In Auto, `&self` is a language keyword for method receivers. The `&` prefix indicates that the method takes a reference to the instance, mirroring Rust's borrowing semantics. The `a2p` transpiler converts `&self` to `self` in the generated Python code.

## Classes

The simplest class possible is shown in the following example (save as `oop_simplestclass.at`):

<Listing number="11-1" file-name="oop_simplestclass.auto" caption="Creating a class">

```auto
type Person {}

fn main() {
    let p = Person{}
    print(p)
}
```

```python
class Person:
    pass


def main():
    p = Person()
    print(p)


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ a2p oop_simplestclass.at && python oop_simplestclass.py
<__main__.Person object at 0x...>
```

**How It Works**

We create a new class using the `type` statement and the name of the class. This is followed by a block enclosed by `{}` which forms the body of the class. In this case, we have an empty block. The `a2p` transpiler converts this to a Python class with a `pass` statement as its body.

Next, we create an object/instance of this class using the name of the class followed by `{}`. (We will learn [more about instantiation](#the-init-method) in the next section). For our verification, we confirm the type of the variable by simply printing it. It tells us that we have an instance of the `Person` class in the `__main__` module.

Notice that the address of the computer memory where your object is stored is also printed. The address will have a different value on your computer since Python can store the object wherever it finds space.

> **Note for Python Programmers:**
>
> Auto uses `type` instead of Python's `class` keyword. An empty `type Person {}` is equivalent to `class Person: pass`. The `a2p` transpiler handles this conversion automatically. Objects are created with `Person{}` instead of `Person()`.

## Methods

We have already discussed that classes/objects can have methods just like functions except that we have an extra `&self` parameter. We will now see an example (save as `oop_method.at`):

<Listing number="11-2" file-name="oop_method.auto" caption="Using object methods">

```auto
type Person {
    fn say_hi(&self) {
        print("Hello, how are you?")
    }
}

fn main() {
    let p = Person{}
    p.say_hi()
}
```

```python
class Person:
    def say_hi(self):
        print('Hello, how are you?')


def main():
    p = Person()
    p.say_hi()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ a2p oop_method.at && python oop_method.py
Hello, how are you?
```

**How It Works**

Here we see the `&self` in action. Notice that the `say_hi` method takes no parameters but still has `&self` in the function definition. The `a2p` transpiler converts `fn say_hi(&self)` to `def say_hi(self)`, and the method is called in the same way as in Python: `p.say_hi()`.

## The `init` Method

There are many method names which have special significance in Python classes. We will see the significance of the `__init__` method now, and how Auto handles it.

In Auto, the constructor method is defined using `fn init(&self, ...)`. The `a2p` transpiler converts this to the Python `__init__` method. The `init` method is run as soon as an object of a class is instantiated (i.e. created). The method is useful to do any *initialization* (i.e. passing initial values to your object) you want to do with your object.

Example (save as `oop_init.at`):

<Listing number="11-3" file-name="oop_init.auto" caption="Using the init method">

```auto
type Person {
    name: str

    fn init(&self, name: str) {
        .name = name
    }

    fn say_hi(&self) {
        print("Hello, my name is", .name)
    }
}

fn main() {
    let p = Person{"Swaroop"}
    p.say_hi()
}
```

```python
class Person:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print('Hello, my name is', self.name)


def main():
    p = Person('Swaroop')
    p.say_hi()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ a2p oop_init.at && python oop_init.py
Hello, my name is Swaroop
```

**How It Works**

Here, we define the `init` method as taking a parameter `name` (along with the usual `&self`). We declare a field `name: str` at the top of the type block. Inside `init`, we assign the parameter to the field using `.name = name`. Notice these are two different variables even though they are both called 'name'. There is no problem because the `.name` notation means that there is something called "name" that is part of the object (i.e. `self.name`), and the other `name` is a local parameter.

When creating a new instance `p` of the `Person` type, we do so by using the type name followed by the arguments in `{}`: `p = Person{"Swaroop"}`. The `a2p` transpiler converts `Person{"Swaroop"}` to `Person('Swaroop')` in the generated Python code.

We do not explicitly call the `init` method. This is the special significance of this method.

Now, we are able to use the `.name` field in our methods (which becomes `self.name` in Python), as demonstrated in the `say_hi` method.

> **Note for Python Programmers:**
>
> Auto uses `fn init(&self, ...)` instead of Python's `def __init__(self, ...)`. Inside the method, `.field = value` is equivalent to `self.field = value`. The `a2p` transpiler converts `fn init` to `def __init__` and `.field` references to `self.field`. Field declarations like `name: str` at the top of the type block become instance variables assigned in `__init__`.

## Class and Object Variables

We have already discussed the functionality part of classes and objects (i.e. methods), now let us learn about the data part. The data part, i.e. fields, are nothing but ordinary variables that are _bound_ to the **namespaces** of the classes and objects. This means that these names are valid within the context of these classes and objects only. That's why they are called _name spaces_.

There are two types of _fields_ - class variables and object variables which are classified depending on whether the class or the object _owns_ the variables respectively.

**Class variables** are shared - they can be accessed by all instances of that class. There is only one copy of the class variable and when any one object makes a change to a class variable, that change will be seen by all the other instances.

**Object variables** are owned by each individual object/instance of the class. In this case, each object has its own copy of the field i.e. they are not shared and are not related in any way to the field by the same name in a different instance.

Let's first see a simple example of object variables (save as `oop_objvar.at`):

<Listing number="11-4" file-name="oop_objvar.auto" caption="Using object variables">

```auto
type Robot {
    name: str

    fn init(&self, name: str) {
        .name = name
        print(f"(Initializing $.name)")
    }

    fn say_hi(&self) {
        print(f"Greetings, my masters call me $.name.")
    }

    fn die(&self) {
        print(f"$.name is being destroyed!")
    }
}

fn main() {
    let droid1 = Robot{"R2-D2"}
    droid1.say_hi()

    let droid2 = Robot{"C-3PO"}
    droid2.say_hi()

    print("\nRobots can do some work here.\n")

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()
}
```

```python
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
```

</Listing>

Output:

```
$ a2p oop_objvar.at && python oop_objvar.py
(Initializing R2-D2)
Greetings, my masters call me R2-D2.
(Initializing C-3PO)
Greetings, my masters call me C-3PO.

Robots can do some work here.

Robots have finished their work. So let's destroy them.
R2-D2 is being destroyed!
C-3PO is being destroyed!
```

**How It Works**

In this example, the `name` field belongs to each individual object (it is assigned using `.name` inside the `init` method), so each `Robot` instance has its own copy of `name`. The `.name` notation inside methods is equivalent to `self.name` in Python. This is an **object variable** (also called an instance variable).

Now let's add a **class variable** to track the robot population (save as `oop_classvar.at`):

<Listing number="11-5" file-name="oop_classvar.auto" caption="Class and object variables">

```auto
type Robot {
    population: int = 0

    name: str

    fn init(&self, name: str) {
        .name = name
        print(f"(Initializing $.name)")
        Robot.population += 1
    }

    fn die(&self) {
        print(f"$.name is being destroyed!")
        Robot.population -= 1
        if Robot.population == 0 {
            print(f"$.name was the last one.")
        } else {
            print(f"There are still {Robot.population} robots working.")
        }
    }

    fn say_hi(&self) {
        print(f"Greetings, my masters call me $.name.")
    }

    fn how_many() {
        print(f"We have {Robot.population} robots.")
    }
}

fn main() {
    let droid1 = Robot{"R2-D2"}
    droid1.say_hi()
    Robot.how_many()

    let droid2 = Robot{"C-3PO"}
    droid2.say_hi()
    Robot.how_many()

    print("\nRobots can do some work here.\n")

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()

    Robot.how_many()
}
```

```python
class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        print(f'(Initializing {self.name})')
        Robot.population += 1

    def die(self):
        print(f'{self.name} is being destroyed!')
        Robot.population -= 1
        if Robot.population == 0:
            print(f'{self.name} was the last one.')
        else:
            print(f'There are still {Robot.population} robots working.')

    def say_hi(self):
        print(f'Greetings, my masters call me {self.name}.')

    @classmethod
    def how_many(cls):
        print(f'We have {cls.population} robots.')


def main():
    droid1 = Robot('R2-D2')
    droid1.say_hi()
    Robot.how_many()

    droid2 = Robot('C-3PO')
    droid2.say_hi()
    Robot.how_many()

    print('\nRobots can do some work here.\n')

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()

    Robot.how_many()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ a2p oop_classvar.at && python oop_classvar.py
(Initializing R2-D2)
Greetings, my masters call me R2-D2.
We have 1 robots.
(Initializing C-3PO)
Greetings, my masters call me C-3PO.
We have 2 robots.

Robots can do some work here.

Robots have finished their work. So let's destroy them.
R2-D2 is being destroyed!
There are still 1 robots working.
C-3PO is being destroyed!
C-3PO was the last one.
We have 0 robots.
```

**How It Works**

This is a long example but helps demonstrate the nature of class and object variables. Here, `population` is declared as a field at the top of the `Robot` type with a default value of `0`. Since it is referenced using `Robot.population` (the type name, not `.population`), it is a **class variable** shared by all instances. The `name` variable belongs to the object (it is assigned using `.name`) and hence is an **object variable**.

Thus, we refer to the `population` class variable as `Robot.population` and not as `.population`. We refer to the object variable `name` using `.name` notation in the methods of that object. Remember this simple difference between class and object variables. Also note that an object variable with the same name as a class variable will hide the class variable!

Instead of `Robot.population`, we could have also used `self.__class__.population` because every object refers to its class via the `self.__class__` attribute.

The `how_many` method does not take `&self` as a parameter, meaning it is not an instance method. In Python, this becomes a `@classmethod`. It belongs to the class and not to any individual object.

Observe that the `init` method is used to initialize the `Robot` instance with a name. In this method, we increase the `Robot.population` count by 1 since we have one more robot being added. Also observe that the values of `.name` are specific to each object which indicates the nature of object variables.

Remember, that you must refer to the variables and methods of the same object using `.field` notation only. This is called an *attribute reference*.

In the `die` method, we simply decrease the `Robot.population` count by 1.

> **Note for Python Programmers:**
>
> In Auto, class variables are declared as fields with default values at the top of the `type` block (e.g., `population: int = 0`). The `a2p` transpiler recognizes that these are not assigned via `.field = value` in `init` and places them as class-level attributes in the Python output. Methods without `&self` (like `fn how_many()`) are converted to `@classmethod` with a `cls` parameter.

## Inheritance

One of the major benefits of object oriented programming is **reuse** of code and one of the ways this is achieved is through the **inheritance** mechanism. Inheritance can be best imagined as implementing a **type and subtype** relationship between classes.

Suppose you want to write a program which has to keep track of the teachers and students in a college. They have some common characteristics such as name, age and address. They also have specific characteristics such as salary, courses and leaves for teachers and, marks and fees for students.

You can create two independent classes for each type and process them but adding a new common characteristic would mean adding to both of these independent classes. This quickly becomes unwieldy.

A better way would be to create a common class called `SchoolMember` and then have the teacher and student classes _inherit_ from this class, i.e. they will become sub-types of this type (class) and then we can add specific characteristics to these sub-types.

There are many advantages to this approach. If we add/change any functionality in `SchoolMember`, this is automatically reflected in the subtypes as well. For example, you can add a new ID card field for both teachers and students by simply adding it to the SchoolMember class. However, changes in the subtypes do not affect other subtypes. Another advantage is that you can refer to a teacher or student object as a `SchoolMember` object which could be useful in some situations such as counting of the number of school members. This is called **polymorphism** where a sub-type can be substituted in any situation where a parent type is expected, i.e. the object can be treated as an instance of the parent class.

Also observe that we reuse the code of the parent class and we do not need to repeat it in the different classes as we would have had to in case we had used independent classes.

The `SchoolMember` class in this situation is known as the **base class** or the **superclass**. The `Teacher` and `Student` classes are called the **derived classes** or **subclasses**.

In Auto, inheritance is expressed using a colon after the type name: `type Sub: Super {}`. The `a2p` transpiler converts this to `class Sub(Super):` in Python.

We will now see this example as a program (save as `oop_subclass.at`):

<Listing number="11-6" file-name="oop_subclass.auto" caption="Inheritance">

```auto
type SchoolMember {
    name: str
    age: int

    fn init(&self, name: str, age: int) {
        .name = name
        .age = age
        print(f"(Initialized SchoolMember: $.name)")
    }

    fn tell(&self) {
        print(f"Name:\"$.name\" Age:\"$.age\"", end = " ")
    }
}

type Teacher: SchoolMember {
    salary: int

    fn init(&self, name: str, age: int, salary: int) {
        SchoolMember.init(self, name, age)
        .salary = salary
        print(f"(Initialized Teacher: $.name)")
    }

    fn tell(&self) {
        SchoolMember.tell(self)
        print(f"Salary: \"$.salary\"")
    }
}

type Student: SchoolMember {
    marks: int

    fn init(&self, name: str, age: int, marks: int) {
        SchoolMember.init(self, name, age)
        .marks = marks
        print(f"(Initialized Student: $.name)")
    }

    fn tell(&self) {
        SchoolMember.tell(self)
        print(f"Marks: \"$.marks\"")
    }
}

fn main() {
    let t = Teacher{"Mrs. Shrividya", 40, 30000}
    let s = Student{"Swaroop", 25, 75}

    // prints a blank line
    print()

    let members = [t, s]
    for member in members {
        // Works for both Teachers and Students
        member.tell()
    }
}
```

```python
class SchoolMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f'(Initialized SchoolMember: {self.name})')

    def tell(self):
        print(f'Name:"{self.name}" Age:"{self.age}"', end=" ")


class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print(f'(Initialized Teacher: {self.name})')

    def tell(self):
        SchoolMember.tell(self)
        print(f'Salary: "{self.salary}"')


class Student(SchoolMember):
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print(f'(Initialized Student: {self.name})')

    def tell(self):
        SchoolMember.tell(self)
        print(f'Marks: "{self.marks}"')


def main():
    t = Teacher('Mrs. Shrividya', 40, 30000)
    s = Student('Swaroop', 25, 75)

    # prints a blank line
    print()

    members = [t, s]
    for member in members:
        # Works for both Teachers and Students
        member.tell()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ a2p oop_subclass.at && python oop_subclass.py
(Initialized SchoolMember: Mrs. Shrividya)
(Initialized Teacher: Mrs. Shrividya)
(Initialized SchoolMember: Swaroop)
(Initialized Student: Swaroop)

Name:"Mrs. Shrividya" Age:"40" Salary: "30000"
Name:"Swaroop" Age:"25" Marks: "75"
```

**How It Works**

To use inheritance, we specify the base class name after a colon following the type name in the type definition (for example, `type Teacher: SchoolMember`). The `a2p` transpiler converts this to `class Teacher(SchoolMember):`.

Next, we observe that the `init` method of the base class is explicitly called using `SchoolMember.init(self, name, age)` so that we can initialize the base class part of an instance in the subclass. This is very important to remember - since we are defining an `init` method in `Teacher` and `Student` subclasses, the transpiler (like Python) does not automatically call the constructor of the base class `SchoolMember`, you have to explicitly call it yourself.

In contrast, if we have not defined an `init` method in a subclass, the base class constructor will be called automatically.

While we could treat instances of `Teacher` or `Student` as we would an instance of `SchoolMember` and access the `tell` method of `SchoolMember`, we instead define another `tell` method in each subclass (using the `tell` method of `SchoolMember` for part of it) to tailor it for that subclass. Because we have done this, when we call `member.tell()` in the loop, the correct `tell` method for that subclass is used vs the superclass. However, if we did not have a `tell` method in the subclass, the `tell` method in the superclass would be used. Python always starts looking for methods in the actual subclass type first, and if it doesn't find anything, it starts looking at the methods in the subclass's base classes.

The `end` parameter is used in the `print` function in the superclass's `tell()` method to print a line and allow the next print to continue on the same line. This is a trick to make `print` not print a `\n` (newline) symbol at the end of the printing.

> **Note for Python Programmers:**
>
> Auto uses `type Sub: Super {}` for inheritance instead of Python's `class Sub(Super):`. The base class constructor is called explicitly as `Super.init(self, ...)` instead of `Super.__init__(self, ...)`. The `a2p` transpiler converts `Super.init(self, ...)` to `Super.__init__(self, ...)` in the generated Python code. Similarly, calling a parent method like `SchoolMember.tell(self)` is translated to `SchoolMember.tell(self)` in Python.

## Method Overriding and Polymorphism

In the previous example, we saw that both `Teacher` and `Student` define their own `tell` method, which overrides the `tell` method from `SchoolMember`. This is called **method overriding**. When we iterate over a list of `SchoolMember` objects and call `tell` on each, the appropriate version is called based on the actual type of the object - this is **polymorphism** in action.

Let's see a simpler example that focuses on this concept (save as `oop_polymorphism.at`):

<Listing number="11-7" file-name="oop_polymorphism.auto" caption="Method overriding and polymorphism">

```auto
type Animal {
    name: str

    fn init(&self, name: str) {
        .name = name
    }

    fn speak(&self) {
        print(f"$.name makes a sound")
    }
}

type Dog: Animal {
    fn speak(&self) {
        print(f"$.name says Woof!")
    }
}

type Cat: Animal {
    fn speak(&self) {
        print(f"$.name says Meow!")
    }
}

fn main() {
    let animals = [Dog{"Rex"}, Cat{"Whiskers"}, Animal("Creature")]
    for animal in animals {
        animal.speak()
    }
}
```

```python
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
```

</Listing>

Output:

```
$ a2p oop_polymorphism.at && python oop_polymorphism.py
Rex says Woof!
Whiskers says Meow!
Creature makes a sound
```

**How It Works**

We define a base type `Animal` with a `speak` method that provides a default behavior. Then we create two subtypes: `Dog` and `Cat`, both of which override the `speak` method with their own implementation.

In `main`, we create a list containing a `Dog`, a `Cat`, and a plain `Animal`. When we iterate over the list and call `animal.speak()` on each, Python's method resolution order ensures that the correct version of `speak` is called for each object:
- For the `Dog` instance, `Dog.speak` is called, printing "Woof!"
- For the `Cat` instance, `Cat.speak` is called, printing "Meow!"
- For the plain `Animal` instance, `Animal.speak` is called, printing the default sound

This is polymorphism: the same method call (`speak`) produces different behavior depending on the actual type of the object. This makes our code extensible - we can add new animal types (like `Bird`, `Fish`, etc.) without changing the loop that calls `speak`.

> **Note for Python Programmers:**
>
> Method overriding in Auto works exactly the same way as in Python. If a subtype defines a method with the same name as a method in the base type, the subtype's version overrides the base type's version. The `a2p` transpiler generates standard Python inheritance, so all of Python's method resolution order (MRO) rules apply to the generated code.

## Summary

We have now explored the various aspects of classes and objects as well as the various terminologies associated with it. We have also seen the benefits and pitfalls of object-oriented programming. Auto provides a clean, Rust-inspired syntax for OOP that transpiles directly to Python classes.

Key takeaways for this chapter:

- **`type` for classes** -- Auto uses the `type` keyword to define classes. `type Person {}` becomes `class Person: pass`.
- **`&self` parameter** -- Methods take `&self` as their first parameter, equivalent to Python's `self`. The `a2p` transpiler converts `&self` to `self`.
- **`fn init(&self, ...)`** -- The constructor method. Transpiles to `def __init__(self, ...)`.
- **`.field` for instance access** -- Inside methods, `.field` refers to `self.field`. The transpiler handles this conversion.
- **Field declarations** -- Fields declared at the top of a `type` block (e.g., `name: str`) become instance variables initialized in `__init__`.
- **Class variables** -- Fields with default values (e.g., `population: int = 0`) become class-level attributes in Python.
- **`type Sub: Super {}`** -- Inheritance syntax. Transpiles to `class Sub(Super):`.
- **Method overriding** -- Defining a method in a subtype with the same name as a base type method overrides it. Polymorphism works naturally.
- **`ClassName{args}`** -- Object construction. Transpiles to `ClassName(args)`.

Next, we will learn about input/output and how to access files.
