# Getting Started

Let's start your Auto journey! There's a lot to learn, but every journey starts
somewhere. In this chapter, we'll discuss:

- Installing Auto on Linux, macOS, and Windows
- Writing a program that prints `Hello, world!`
- Using `automan`, Auto's package manager and build system

## Installation

The first step is to install Auto. You'll need an internet connection for the
download.

> ### Command Line Notation
>
> In this chapter and throughout the book, we'll show some commands used in the
> terminal. Lines that you should enter in a terminal all start with `$`. You
> don't need to type the `$` character; it's the command line prompt shown to
> indicate the start of each command. Lines that don't start with `$` typically
> show the output of the previous command. Additionally, PowerShell-specific
> examples will use `>` rather than `$`.

### Installing on Linux or macOS

If you're using Linux or macOS, open a terminal and enter the following command:

```console
$ curl --proto '=https' https://sh.auto.dev | sh
```

The command downloads a script and starts the installation of the Auto
toolchain, which includes the `autoc` compiler and the `automan` package
manager. You might be prompted for your password. If the install is successful,
the following line will appear:

```text
Auto is installed now. Great!
```

You will also need a _linker_, which is a program that the compiler uses to
join its compiled outputs into one file. It is likely you already have one. If
you get linker errors, you should install a C compiler, which will typically
include a linker.

On macOS, you can get a C compiler by running:

```console
$ xcode-select --install
```

Linux users should generally install GCC or Clang, according to their
distribution's documentation. For example, if you use Ubuntu, you can install
the `build-essential` package.

### Installing on Windows

On Windows, go to the Auto website and follow the instructions for installing
Auto. At some point in the installation, you'll be prompted to install Visual
Studio. This provides a linker and the native libraries needed to compile
programs.

The rest of this book uses commands that work in both _cmd.exe_ and PowerShell.
If there are specific differences, we'll explain which to use.

### Troubleshooting

To check whether you have Auto installed correctly, open a shell and enter this
line:

```console
$ autoc --version
```

You should see the version number in the following format:

```text
autoc x.y.z (yyyy-mm-dd)
```

If you see this information, you have installed Auto successfully! If you don't
see this information, check that Auto is in your `%PATH%` system variable as
follows.

In Windows CMD, use:

```console
> echo %PATH%
```

In PowerShell, use:

```powershell
> echo $env:Path
```

In Linux and macOS, use:

```console
$ echo $PATH
```

If that's all correct and Auto still isn't working, there are a number of
places you can get help. Check the Auto community page for ways to get in touch
with other Auto developers.

### Updating and Uninstalling

Once Auto is installed, updating to a newly released version is easy. From your
shell, run the following command:

```console
$ autoc update
```

To uninstall Auto, run the following command from your shell:

```console
$ autoc self uninstall
```

### Local Documentation

The installation of Auto also includes a local copy of the documentation so
that you can read it offline. Run `autoc doc` to open the local documentation
in your browser.

Any time a type or function is provided by the standard library and you're not
sure what it does or how to use it, use the API documentation to find out!

### Using Text Editors and IDEs

This book makes no assumptions about what tools you use to author Auto code.
Just about any text editor will get the job done! Many text editors and IDEs
have built-in support for Auto through language server plugins.

## Hello, World!

Now that you've installed Auto, it's time to write your first program. It's
traditional when learning a new language to write a little program that prints
the text `Hello, world!` to the screen, so we'll do the same here!

> Note: This book assumes basic familiarity with the command line. Auto makes
> no specific demands about your editing or tooling or where your code lives, so
> if you prefer to use an IDE instead of the command line, feel free to use your
> favorite IDE.

### Project Directory Setup

You'll start by making a directory to store your Auto code. It doesn't matter
to Auto where your code lives, but for the exercises and projects in this book,
we suggest making a _projects_ directory in your home directory and keeping all
your projects there.

Open a terminal and enter the following commands to make a _projects_ directory
and a directory for the "Hello, world!" project within the _projects_ directory.

For Linux, macOS, and PowerShell on Windows, enter this:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

For Windows CMD, enter this:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

### Auto Program Basics

Next, make a new source file and call it _main.auto_. Auto files always end with
the _.auto_ extension. If you're using more than one word in your filename, the
convention is to use an underscore to separate them. For example, use
_hello_world.auto_ rather than _helloworld.auto_.

Now open the _main.auto_ file you just created and enter the code in Listing 1-1.

<Listing number="1-1" file-name="main.auto" caption="A program that prints `Hello, world!`">

```auto
fn main() ! {
    print("Hello, world!")
}
```

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Save the file and go back to your terminal window. On Linux or macOS, enter the
following commands to compile and run the file:

```console
$ autoc main.auto
$ ./main
Hello, world!
```

On Windows, enter the command `.\main` instead of `./main`:

```powershell
> autoc main.auto
> .\main
Hello, world!
```

Regardless of your operating system, the string `Hello, world!` should print to
the terminal.

If `Hello, world!` did print, congratulations! You've officially written an Auto
program. That makes you an Auto programmer—welcome!

### The Anatomy of an Auto Program

Let's review this "Hello, world!" program in detail. Here's the first piece of
the puzzle:

```auto
fn main() ! {

}
```

These lines define a function named `main`. The `main` function is special: It
is always the first code that runs in every executable Auto program. Here, the
first line declares a function named `main` that has no parameters and returns
nothing. If there were parameters, they would go inside the parentheses `()`.

The `!` after the parentheses indicates that this function uses Auto's error
propagation mechanism. We'll discuss this in detail in Chapter 9.

The function body is wrapped in `{}`. Auto requires curly brackets around all
function bodies. It's good style to place the opening curly bracket on the same
line as the function declaration, adding one space in between.

The body of the `main` function holds the following code:

```auto
print("Hello, world!")
```

This line does all the work in this little program: It prints text to the
screen. Note a few differences from Rust:

- Auto uses `print()` as a regular function, not a macro—no `!` needed.
- Auto does not require semicolons at the end of statements. The compiler uses
  line breaks and context to determine where statements end.
- If you want a newline, use `println()`. `print()` outputs without a trailing
  newline.

### Compilation and Execution

Before running an Auto program, you must compile it using the Auto compiler by
entering the `autoc` command and passing it the name of your source file, like
this:

```console
$ autoc main.auto
```

After compiling successfully, Auto outputs a binary executable. From here, you
run the executable:

```console
$ ./main  # or .\main on Windows
```

If your _main.auto_ is your "Hello, world!" program, this line prints `Hello,
world!` to your terminal.

Auto is an _ahead-of-time compiled_ language, meaning you can compile a program
and give the executable to someone else, and they can run it even without having
Auto installed.

Auto also offers a VM mode through `autovm`, which allows you to run programs
directly without a separate compile step—useful for development and rapid
iteration:

```console
$ autovm main.auto
Hello, world!
```

Just compiling with `autoc` is fine for simple programs, but as your project
grows, you'll want to manage all the options and make it easy to share your
code. Next, we'll introduce you to the `automan` tool, which will help you
write real-world Auto programs.

## Hello, automan!

automan is Auto's build system and package manager. Most Auto developers use
this tool to manage their projects because automan handles a lot of tasks for
you, such as building your code, downloading the libraries your code depends on,
and building those libraries. (We call the libraries that your code needs
_dependencies_.)

The simplest Auto programs, like the one we've written so far, don't have any
dependencies. As you write more complex Auto programs, you'll add dependencies,
and if you start a project using automan, adding dependencies will be much
easier.

Because the vast majority of Auto projects use automan, the rest of this book
assumes that you're using automan too. automan comes installed with Auto if you
used the official installers discussed in the
["Installation"](#installation) section.

### Creating a Project with automan

Let's create a new project using automan. Navigate back to your _projects_
directory (or wherever you decided to store your code). Then, on any operating
system, run the following:

```console
$ automan new hello_auto
$ cd hello_auto
```

The first command creates a new directory and project called _hello_auto_.

Go into the _hello_auto_ directory and list the files. You'll see that automan
has generated two files and one directory for us: a _auto.toml_ configuration
file and a _src_ directory with a _main.auto_ file inside.

It has also initialized a new Git repository along with a _.gitignore_ file.

Open _auto.toml_ in your text editor. It should look similar to the code in
Listing 1-2.

<Listing number="1-2" file-name="auto.toml" caption="Contents of *auto.toml* generated by `automan new`">

```toml
[package]
name = "hello_auto"
version = "0.1.0"

[dependencies]
```

</Listing>

This file is in the _TOML_ format, which is automan's configuration format.

The first line, `[package]`, is a section heading that indicates that the
following statements are configuring a package.

The next two lines set the configuration information automan needs to compile
your program: the name and the version.

The last line, `[dependencies]`, is the start of a section for you to list any
of your project's dependencies. In Auto, packages of code are referred to as
_modules_. We won't need any other modules for this project, but we will in the
first project in Chapter 2.

Now open _src/main.auto_ and take a look:

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    print("Hello, world!")
}
```

```rust
fn main() {
    println!("Hello, world!");
}
```

automan has generated a "Hello, world!" program for you, just like the one we
wrote in Listing 1-1! The differences between our project and the project
automan generated are that automan placed the code in the _src_ directory, and
we have a _auto.toml_ configuration file in the top directory.

automan expects your source files to live inside the _src_ directory. The
top-level project directory is just for README files, license information,
configuration files, and anything else not related to your code. Using automan
helps you organize your projects. There's a place for everything, and
everything is in its place.

### Building and Running an automan Project

Now let's look at what's different when we build and run the "Hello, world!"
program with automan! From your _hello_auto_ directory, build your project by
entering the following command:

```console
$ automan build
   Compiling hello_auto v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 2.85s
```

This command creates an executable file in _target/debug/hello_auto_ (or
_target\debug\hello_auto.exe_ on Windows). You can run the executable:

```console
$ ./target/debug/hello_auto  # or .\target\debug\hello_auto.exe on Windows
Hello, world!
```

Running `automan build` for the first time also causes automan to create a new
file at the top level: _auto.lock_. This file keeps track of the exact versions
of dependencies in your project. You won't ever need to change this file
manually; automan manages its contents for you.

We can also use `automan run` to compile the code and then run the resultant
executable all in one command:

```console
$ automan run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/hello_auto`
Hello, world!
```

Using `automan run` is more convenient than having to remember to run `automan
build` and then use the whole path to the binary, so most developers use
`automan run`.

automan also provides a command called `automan check`. This command quickly
checks your code to make sure it compiles but doesn't produce an executable:

```console
$ automan check
    Checking hello_auto v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.32s
```

`automan check` is much faster than `automan build` because it skips the step
of producing an executable. If you're continually checking your work while
writing the code, using `automan check` will speed up your development cycle.

Let's recap what we've learned so far about automan:

- We can create a project using `automan new`.
- We can build a project using `automan build`.
- We can build and run a project in one step using `automan run`.
- We can build a project without producing a binary to check for errors using
  `automan check`.
- Instead of saving the result of the build in the same directory as our code,
  automan stores it in the _target/debug_ directory.

### Building for Release

When your project is finally ready for release, you can use `automan build
--release` to compile it with optimizations. This command will create an
executable in _target/release_ instead of _target/debug_. The optimizations
make your Auto code run faster, but turning them on lengthens the time it takes
for your program to compile. This is why there are two different profiles: one
for development, when you want to rebuild quickly and often, and another for
building the final program you'll give to a user.

### Leveraging automan's Conventions

With simple projects, automan doesn't provide a lot of value over just using
`autoc`, but it will prove its worth as your programs become more intricate.
Once programs grow to multiple files or need a dependency, it's much easier to
let automan coordinate the build.

## Summary

You're already off to a great start on your Auto journey! In this chapter, you
learned how to:

- Install Auto using the official installer.
- Update to a newer Auto version.
- Open locally installed documentation.
- Write and run a "Hello, world!" program using `autoc` directly.
- Create and run a new project using the conventions of automan.

This is a great time to build a more substantial program to get used to reading
and writing Auto code. So, in Chapter 2, we'll build a guessing game program.
If you would rather start by learning how common programming concepts work in
Auto, see Chapter 3 and then return to Chapter 2.
