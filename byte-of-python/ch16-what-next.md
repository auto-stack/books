# What Next

If you have read this book thoroughly and practiced writing a lot of programs, you must have become comfortable and familiar with Auto. You have probably created some Auto programs to try out things and to exercise your new skills as well. If you have not done it already, you should. The question now is "What Next?".

## Suggested Projects

The best way to consolidate what you have learned is to build something real. Here are a few project ideas to get you started:

### Address Book

Create your own command-line *address-book* program using which you can browse, add, modify, delete, or search for your contacts such as friends, family, and colleagues along with their information such as email address and/or phone number. Details must be stored for later retrieval.

This is fairly easy if you think about it in terms of all the various things we have come across so far -- use classes to represent contact information, dictionaries to store contacts with their name as the key, and the `json` or `pickle` module to persist data to disk.

### File Replacement Tool

Implement a command-line tool that replaces one string with another across a list of files. The tool can be as simple or as sophisticated as you wish -- from straightforward string substitution to searching for patterns using regular expressions.

### A Simple Web Scraper

Use the `urllib` module (or the third-party `requests` library) to fetch a web page and extract useful information from it. You could scrape weather data, news headlines, or book prices -- whatever interests you.

### A Command-Line Calculator

Build a calculator that reads expressions from the command line and evaluates them. Start with basic arithmetic, then add support for variables, functions, and perhaps even operator precedence.

If you found these projects too easy, here are some more ideas and comprehensive project lists to explore:

- [Exercises for Programmers: 57 Challenges to Develop Your Coding Skills](https://pragprog.com/book/bhwb/exercises-for-programmers)
- [Intermediate Python Projects](https://openhatch.org/wiki/Intermediate_Python_Workshop/Projects)
- [Project list on GitHub](https://github.com/thekarangoel/Projects#numbers)

## Exploring Auto Further

Auto is more than a single-language tool. One of its unique strengths is the ability to transpile to multiple target languages. Here are some directions to explore:

### Transpiling to Rust with a2r

The `a2r` transpiler converts Auto code into idiomatic Rust. This gives you the performance and safety guarantees of Rust while writing in Auto's friendlier syntax. If you need high performance or want to ship systems-level software, a2r is the path forward.

### Transpiling to TypeScript with a2ts

The `a2ts` transpiler converts Auto code into TypeScript, opening the door to the entire JavaScript ecosystem. Use it to build web front-ends, Node.js backends, or full-stack applications -- all while writing in a single, consistent language.

### Transpiling to C with a2c

The `a2c` transpiler converts Auto code into C. This is useful when you need to target embedded systems, operating systems, or any environment where C is the standard. Auto lets you write safe, high-level code that compiles down to efficient C.

### Other Books in This Series

Auto has a growing collection of books for different backgrounds and target languages. Look for other "A Byte of Auto" titles to continue your learning journey with different transpilation targets and advanced topics.

## Exploring Python Further

Since Auto transpiles to Python, everything you learn about Python applies directly to your Auto programs. Here are some areas worth exploring:

### Web Development with Flask

[Flask](http://flask.pocoo.org) is a lightweight web framework for Python. It is a great starting point for building web applications. Some resources:

- [Flask Official Quickstart](http://flask.pocoo.org/docs/quickstart/)
- [The Flask Mega-Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### Data Science

Python is the dominant language in data science and machine learning. Key libraries to explore:

- [NumPy](https://numpy.org) -- numerical computing
- [Pandas](https://pandas.pydata.org) -- data manipulation and analysis
- [Matplotlib](https://matplotlib.org) -- data visualization

### Testing

Writing tests is a critical skill for any programmer. Python has excellent testing tools:

- **pytest** -- a powerful, flexible testing framework
- **unittest** -- Python's built-in testing module (available via `use unittest` in Auto)

### Package Management with pip

The [Python Package Index (PyPI)](https://pypi.org) hosts hundreds of thousands of third-party packages. Use [pip](https://pip.pypa.io) to install and manage these packages:

```
$ pip install requests
```

### Virtual Environments

When working on multiple projects, it is good practice to use virtual environments so that each project has its own set of dependencies. Python's built-in `venv` module makes this easy:

```
$ python -m venv myproject_env
$ source myproject_env/bin/activate  (Linux/macOS)
$ myproject_env\Scripts\activate     (Windows)
```

## Further Reading

Here are some resources to continue your programming journey:

- [Official Python Documentation](https://docs.python.org/3/) -- the definitive reference for Python
- [Python Package Index (PyPI)](https://pypi.org) -- find and install third-party libraries
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com) -- practical Python projects for beginners
- [Python Module of the Week](https://pymotw.com/3/) -- in-depth guides to standard library modules
- [The Hitchhiker's Guide to Python!](https://docs.python-guide.org/) -- best practices and Pythonic style

## Summary

We have now come to the end of this book but, as they say, this is *the beginning of the end*. You are now an Auto programmer and you are ready to solve many problems. You can automate your computer to do all kinds of previously unimaginable things, build web applications, analyze data, or transpile your code to Rust, TypeScript, or C for deployment in any environment.

The most important thing now is to keep practicing. Pick a project that excites you and start building. Every line of code you write makes you a better programmer.

So, get started!
