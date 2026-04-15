# Installation

When we refer to "Python 3" in this book, we will be referring to any version of Python equal to or greater than version [Python 3.10](https://www.python.org/downloads/).

## Installing Auto

The Auto toolchain includes the `autoc` compiler and the `automan` package manager. You will also need the `a2p` transpiler since this book focuses on transpiling Auto code to Python.

### Linux or macOS

Open a terminal and run:

```console
$ curl --proto '=https' https://sh.auto.dev | sh
```

This command downloads a script and installs the Auto toolchain. You might be prompted for your password.

Next, install the `a2p` transpiler using automan:

```console
$ automan install a2p
```

### Windows

Go to the Auto website at <https://auto.dev> and download the Windows installer. Run the installer and follow the on-screen instructions.

> **Caution:** Make sure you check the option to add Auto to your system `PATH` during installation.

After installing the toolchain, install the `a2p` transpiler:

```console
> automan install a2p
```

## Installing Python

Since this book transpiles Auto code to Python using `a2p`, you will need Python 3.10 or later installed on your system.

### Linux

Use your distribution's package manager. For example, on Debian and Ubuntu:

```console
$ sudo apt-get update && sudo apt-get install python3
```

### macOS

Use [Homebrew](https://brew.sh):

```console
$ brew install python3
```

### Windows

Download Python from <https://www.python.org/downloads/> and run the installer.

> **Caution:** Make sure you check the option `Add Python to PATH` during installation.

## Verifying Your Installation

Open a terminal (or Command Prompt on Windows) and run the following commands to verify that everything is installed correctly:

```console
$ autoc --version
```

You should see the version number, for example:

```text
autoc 1.0.0 (2025-01-01)
```

```console
$ a2p --version
```

```console
$ python3 --version
```

You should see something like:

```text
Python 3.12.0
```

> **Note:** `$` is the prompt of the shell. It will be different for you depending on the settings of your operating system, hence I will indicate the prompt by just the `$` symbol. On Windows, you may see a `>` prompt instead.

> **Caution:** The output may be different on your computer depending on the versions of the software installed.

## Building the Listings

Throughout this book, you will find code listings that you can compile and run. Each listing is an Auto source file that can be transpiled to Python using the `a2p` transpiler.

To build a listing, navigate to the listing's directory and run:

```console
$ auto b
```

This command transpiles the Auto code to Python and runs the resulting Python file. If you encounter any errors, make sure both `autoc` and `python3` are properly installed and accessible from your terminal.

## Summary

From now on, we will assume that you have both the Auto toolchain and Python 3.10+ installed on your system.

Next, we will write our first Auto program.
