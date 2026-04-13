# More About automan

So far we've used only the most basic features of `automan` to build, run, and
test our code, but it can do a lot more. In this chapter, we'll discuss some of
its other, more advanced features to show you how to do the following:

- Customize your build through release profiles
- Publish libraries on a package registry
- Organize large projects with workspaces
- Install binaries from a package registry
- Extend `automan` using custom commands

`automan` shares many concepts with Cargo, Rust's build system. If you've used
Cargo before, much of this will feel familiar, though Auto's tooling is still
evolving.

## Customizing Builds with Release Profiles

In Auto, _release profiles_ are predefined, customizable profiles with different
configurations that allow a programmer to have more control over various options
for compiling code. Each profile is configured independently of the others.

`automan` has two main profiles: the `dev` profile used when you run
`automan build`, and the `release` profile used when you run
`automan build --release`. The `dev` profile is defined with good defaults for
development, and the `release` profile has good defaults for release builds.

These profile names might be familiar from the output of your builds:

```console
$ automan build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ automan build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

The `dev` and `release` are these different profiles used by the compiler.

`automan` has default settings for each of the profiles that apply when you
haven't explicitly added any `[profile.*]` sections in the project's _auto.toml_
file. By adding `[profile.*]` sections for any profile you want to customize, you
override any subset of the default settings. For example, here are the default
values for the `opt-level` setting for the `dev` and `release` profiles:

Filename: auto.toml

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

The `opt-level` setting controls the number of optimizations the compiler will
apply to your code, with a range of 0 to 3. Applying more optimizations extends
compiling time, so if you're in development and compiling your code often, you'll
want fewer optimizations to compile faster even if the resultant code runs slower.
The default `opt-level` for `dev` is therefore `0`. When you're ready to release
your code, it's best to spend more time compiling. You'll only compile in release
mode once, but you'll run the compiled program many times, so release mode trades
longer compile time for code that runs faster. That is why the default
`opt-level` for the `release` profile is `3`.

You can override a default setting by adding a different value for it in
_auto.toml_. For example, if we want to use optimization level 1 in the
development profile, we can add these two lines to our project's _auto.toml_
file:

Filename: auto.toml

```toml
[profile.dev]
opt-level = 1
```

This code overrides the default setting of `0`. Now when we run `automan build`,
`automan` will use the defaults for the `dev` profile plus our customization to
`opt-level`. Because we set `opt-level` to `1`, `automan` will apply more
optimizations than the default, but not as many as in a release build.

This works the same way as Cargo's release profiles. For the full list of
configuration options and defaults for each profile, see `automan`'s
documentation.

## Publishing a Package to a Registry

We've used packages from a registry as dependencies of our project, but you can
also share your code with other people by publishing your own packages. A package
registry distributes the source code of your packages, so it primarily hosts code
that is open source.

> **Note:** Auto's package registry is still under development. The concepts in
> this section describe how publishing _will_ work once the registry is available.
> In the meantime, you can share Auto packages by publishing them as Rust crates
> via the Auto-to-Rust transpilation workflow, or by hosting Git repositories
> directly.

Auto and `automan` have features that make your published package easier for
people to find and use. We'll talk about some of these features next and then
explain how to publish a package.

### Making Useful Documentation Comments

Accurately documenting your packages will help other users know how and when to
use them, so it's worth investing the time to write documentation. In Chapter 3,
we discussed how to comment Auto code using two slashes, `//`. Auto also has a
particular kind of comment for documentation, known conveniently as a
_documentation comment_, that will generate HTML documentation. The HTML displays
the contents of documentation comments for public API items intended for
programmers interested in knowing how to _use_ your package as opposed to how
your package is _implemented_.

Documentation comments use three slashes, `///`, instead of two and support
Markdown notation for formatting the text. Place documentation comments just
before the item they're documenting. Listing 14-1 shows documentation comments
for an `add_one` function in a package named `my_package`.

<Listing number="14-1" file-name="src/lib.at" caption="A documentation comment for a function">

```auto
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5
/// let answer = my_package::add_one(arg)
///
/// assert_eq(6, answer)
/// ```
pub fn add_one(x int) int {
    x + 1
}
```

```rust
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

Here, we give a description of what the `add_one` function does, start a section
with the heading `Examples`, and then provide code that demonstrates how to use
the `add_one` function. We can generate the HTML documentation from this
documentation comment by running `automan doc`. This command uses the `autodoc`
tool (equivalent to Rust's `rustdoc`) and puts the generated HTML documentation
in the _target/doc_ directory.

For convenience, running `automan doc --open` will build the HTML for your
current package's documentation (as well as the documentation for all of your
package's dependencies) and open the result in a web browser.

#### Commonly Used Sections

We used the `# Examples` Markdown heading in Listing 14-1 to create a section in
the HTML with the title "Examples." Here are some other sections that package
authors commonly use in their documentation:

- **Panics**: The scenarios in which the function being documented could panic.
  Callers of the function who don't want their programs to panic should make sure
  they don't call the function in these situations.
- **Errors**: If the function returns `!T` (Auto's error type), describing the
  kinds of errors that might occur and what conditions might cause those errors
  to be returned can help callers write code to handle the different kinds of
  errors in different ways.
- **Safety**: If the function uses the `sys` keyword (we discuss `sys` in
  Chapter 20), there should be a section explaining why the function is unsafe
  and covering the invariants that the function expects callers to uphold.

Most documentation comments don't need all of these sections, but this is a good
checklist to remind you of the aspects of your code users will be interested in
knowing about.

#### Documentation Comments as Tests

Adding example code blocks in your documentation comments can help demonstrate how
to use your library and has an additional bonus: running `automan test` will run
the code examples in your documentation as tests. Nothing is better than
documentation with examples. But nothing is worse than examples that don't work
because the code has changed since the documentation was written. If we run
`automan test` with the documentation for the `add_one` function from Listing
14-1, we will see a section in the test results that looks like this:

```text
   Doc-tests my_package

running 1 test
test src/lib.at - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out
```

Now, if we change either the function or the example so that the `assert_eq` in
the example panics, and run `automan test` again, we'll see that the doc tests
catch that the example and the code are out of sync with each other.

#### Contained Item Comments

The style of doc comment `//!` adds documentation to the item that _contains_ the
comments rather than to the items _following_ the comments. We typically use these
doc comments inside the package root file (_src/lib.at_ by convention) or inside a
module to document the package or the module as a whole.

For example, to add documentation that describes the purpose of the `my_package`
that contains the `add_one` function, we add documentation comments that start
with `//!` to the beginning of the _src/lib.at_ file, as shown in Listing 14-2.

<Listing number="14-2" file-name="src/lib.at" caption="The documentation for the `my_package` package as a whole">

```auto
//! # My Package
//!
//! `my_package` is a collection of utilities to make performing certain
//! calculations more convenient.

/// Adds one to the number given.
// --snip--
///
/// # Examples
///
/// ```
/// let arg = 5
/// let answer = my_package::add_one(arg)
///
/// assert_eq(6, answer)
/// ```
pub fn add_one(x int) int {
    x + 1
}
```

```rust
//! # My Crate
//!
//! `my_crate` is a collection of utilities to make performing certain
//! calculations more convenient.

/// Adds one to the number given.
// --snip--
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

Notice there isn't any code after the last line that begins with `//!`. Because we
started the comments with `//!` instead of `///`, we're documenting the item that
contains this comment rather than an item that follows this comment. In this case,
that item is the _src/lib.at_ file, which is the package root. These comments
describe the entire package.

When we run `automan doc --open`, these comments will display on the front page of
the documentation for `my_package` above the list of public items in the package.

Documentation comments within items are useful for describing packages and modules
especially. Use them to explain the overall purpose of the container to help your
users understand the package's organization.

### Exporting a Convenient Public API

The structure of your public API is a major consideration when publishing a
package. People who use your package are less familiar with the structure than you
are and might have difficulty finding the pieces they want to use if your package
has a large module hierarchy.

In Chapter 7, we covered how to organize code with types and extensions, and how
to bring items into a scope with the `use` keyword. However, the structure that
makes sense to you while you're developing a package might not be very convenient
for your users. You might want to organize your types in a hierarchy containing
multiple levels, but then people who want to use a type you've defined deep in the
hierarchy might have trouble finding out that type exists. They might also be
annoyed at having to enter `use my_package::some_module::another_module::UsefulType`
rather than `use my_package::UsefulType`.

The good news is that if the structure _isn't_ convenient for others to use from
another library, you don't have to rearrange your internal organization: instead,
you can re-export items to make a public structure that's different from your
private structure by using `pub use`. _Re-exporting_ takes a public item in one
location and makes it public in another location, as if it were defined in the
other location instead.

For example, say we made a library named `art` for modeling artistic concepts.
Within this library are two modules: a `kinds` module containing two enums named
`PrimaryColor` and `SecondaryColor`, and a `utils` module containing a function
named `mix`, as shown in Listing 14-3.

<Listing number="14-3" file-name="src/lib.at" caption="An `art` library with items organized into `kinds` and `utils` modules">

```auto
//! # Art
//!
//! A library for modeling artistic concepts.

pub mod kinds {
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red
        Yellow
        Blue
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange
        Green
        Purple
    }
}

pub mod utils {
    use kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1 PrimaryColor, c2 PrimaryColor) SecondaryColor {
        // --snip--
        // TODO: implementation
    }
}
```

```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub mod kinds {
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red,
        Yellow,
        Blue,
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange,
        Green,
        Purple,
    }
}

pub mod utils {
    use crate::kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1: PrimaryColor, c2: PrimaryColor) -> SecondaryColor {
        // --snip--
        unimplemented!();
    }
}
```

</Listing>

Note that the `PrimaryColor` and `SecondaryColor` types aren't listed on the
front page of the generated documentation, nor is the `mix` function. We have to
click `kinds` and `utils` to see them.

Another package that depends on this library would need `use` statements that
bring the items from `art` into scope, specifying the module structure that's
currently defined. Listing 14-4 shows an example of a package that uses the
`PrimaryColor` and `mix` items from the `art` package.

<Listing number="14-4" file-name="src/main.at" caption="A package using the `art` package's items with its internal structure exported">

```auto
use art::kinds::PrimaryColor
use art::utils::mix

fn main() {
    let red = PrimaryColor.Red
    let yellow = PrimaryColor.Yellow
    mix(red, yellow)
}
```

```rust
use art::kinds::PrimaryColor;
use art::utils::mix;

fn main() {
    let red = PrimaryColor::Red;
    let yellow = PrimaryColor::Yellow;
    mix(red, yellow);
}
```

</Listing>

The author of the code in Listing 14-4 had to figure out that `PrimaryColor` is
in the `kinds` module and `mix` is in the `utils` module. The module structure of
the `art` package is more relevant to developers working on it than to those using
it. The internal structure doesn't contain any useful information for someone
trying to understand how to _use_ the `art` package, but rather causes confusion
because developers who use it have to figure out where to look, and must specify
the module names in the `use` statements.

To remove the internal organization from the public API, we can modify the `art`
package code in Listing 14-3 to add `pub use` statements to re-export the items at
the top level, as shown in Listing 14-5.

<Listing number="14-5" file-name="src/lib.at" caption="Adding `pub use` statements to re-export items">

```auto
//! # Art
//!
//! A library for modeling artistic concepts.

pub use self::kinds::PrimaryColor
pub use self::kinds::SecondaryColor
pub use self::utils::mix

pub mod kinds {
    // --snip--
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red
        Yellow
        Blue
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange
        Green
        Purple
    }
}

pub mod utils {
    // --snip--
    use kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1 PrimaryColor, c2 PrimaryColor) SecondaryColor {
        SecondaryColor.Orange
    }
}
```

```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub use self::kinds::PrimaryColor;
pub use self::kinds::SecondaryColor;
pub use self::utils::mix;

pub mod kinds {
    // --snip--
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red,
        Yellow,
        Blue,
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange,
        Green,
        Purple,
    }
}

pub mod utils {
    // --snip--
    use crate::kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1: PrimaryColor, c2: PrimaryColor) -> SecondaryColor {
        SecondaryColor::Orange
    }
}
```

</Listing>

The API documentation that `automan doc` generates for this package will now list
and link re-exports on the front page, making the `PrimaryColor` and
`SecondaryColor` types and the `mix` function easier to find.

The `art` package users can still see and use the internal structure from Listing
14-3 as demonstrated in Listing 14-4, or they can use the more convenient
structure in Listing 14-5, as shown in Listing 14-6.

<Listing number="14-6" file-name="src/main.at" caption="A program using the re-exported items from the `art` package">

```auto
use art::PrimaryColor
use art::mix

fn main() {
    // --snip--
    let red = PrimaryColor.Red
    let yellow = PrimaryColor.Yellow
    mix(red, yellow)
}
```

```rust
use art::PrimaryColor;
use art::mix;

fn main() {
    // --snip--
    let red = PrimaryColor::Red;
    let yellow = PrimaryColor::Yellow;
    mix(red, yellow);
}
```

</Listing>

In cases where there are many nested modules, re-exporting the types at the top
level with `pub use` can make a significant difference in the experience of people
who use the package. Another common use of `pub use` is to re-export definitions
of a dependency in the current package to make that package's definitions part of
your package's public API.

Creating a useful public API structure is more an art than a science, and you can
iterate to find the API that works best for your users. Choosing `pub use` gives
you flexibility in how you structure your package internally and decouples that
internal structure from what you present to your users.

### Setting Up an Account

> **Note:** Auto's package registry is under development. The account setup
> process will be similar to other language registries (such as crates.io for
> Rust). The following describes the expected workflow.

Before you can publish any packages, you'll need to create an account on the Auto
package registry and get an API token. Then, run the `automan login` command and
paste your API key when prompted:

```console
$ automan login
abcdefghijklmnopqrstuvwxyz012345
```

This command will inform `automan` of your API token and store it locally in
_~/.automan/credentials.toml_. Note that this token is a secret: do not share it
with anyone else. If you do share it for any reason, you should revoke it and
generate a new token.

### Adding Metadata to a New Package

Before publishing, you'll need to add some metadata in the `[package]` section of
the package's _auto.toml_ file. Your package will need a unique name. Package
names on the registry are allocated on a first-come, first-served basis. Before
attempting to publish, search for the name you want to use. If the name has been
used, you'll need to find another name and edit the `name` field in _auto.toml_:

Filename: auto.toml

```toml
[package]
name = "guessing_game"
```

When you run `automan publish`, you'll get a warning and an error if required
metadata is missing:

```text
warning: manifest has no description, license, documentation, homepage or repository.
error: failed to publish to registry
missing or empty metadata fields: description, license.
```

Add a description and a license to _auto.toml_. For the `license` field, use a
SPDX license identifier. For example, to specify the MIT License:

Filename: auto.toml

```toml
[package]
name = "guessing_game"
license = "MIT"
```

You can also specify multiple licenses separated by `OR`:

```toml
[package]
name = "guessing_game"
version = "0.1.0"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"
```

With a unique name, the version, your description, and a license added, the
_auto.toml_ file for a project that is ready to publish might look like this:

Filename: auto.toml

```toml
[package]
name = "guessing_game"
version = "0.1.0"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

### Publishing to the Registry

Now that you've created an account, saved your API token, chosen a name for your
package, and specified the required metadata, you're ready to publish! Publishing
a package uploads a specific version to the registry for others to use.

Be careful, because a publish is _permanent_. The version can never be
overwritten, and the code cannot be deleted except in certain circumstances. One
major goal of a package registry is to act as a permanent archive of code so that
builds of all projects that depend on packages from the registry will continue to
work. Allowing version deletions would make fulfilling that goal impossible.
However, there is no limit to the number of package versions you can publish.

Run the `automan publish` command to publish your package:

```console
$ automan publish
   Packaging guessing_game v0.1.0
    Packaged 6 files, 1.2KiB
   Verifying guessing_game v0.1.0
   Compiling guessing_game v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0
    Published guessing_game v0.1.0
```

Congratulations! You've now shared your code with the Auto community, and anyone
can easily add your package as a dependency of their project.

### Publishing a New Version of an Existing Package

When you've made changes to your package and are ready to release a new version,
change the `version` value specified in your _auto.toml_ file and republish. Use
the Semantic Versioning rules to decide what an appropriate next version number
is, based on the kinds of changes you've made. Then run `automan publish` to
upload the new version.

### Deprecating Versions from the Registry

Although you can't remove previous versions of a package, you can prevent any
future projects from adding them as a new dependency. This is useful when a
package version is broken for one reason or another. In such situations,
`automan` supports yanking a package version.

_Yanking_ a version prevents new projects from depending on that version while
allowing all existing projects that depend on it to continue. Essentially, a yank
means that all projects with an _auto.lock_ file will not break, and any future
_auto.lock_ files generated will not use the yanked version.

To yank a version of a package, run `automan yank` and specify which version you
want to yank:

```console
$ automan yank --vers 1.0.1
    Yanking guessing_game@1.0.1
```

By adding `--undo` to the command, you can also undo a yank and allow projects to
start depending on a version again:

```console
$ automan yank --vers 1.0.1 --undo
    Unyanking guessing_game@1.0.1
```

A yank _does not_ delete any code. It cannot, for example, delete accidentally
uploaded secrets. If that happens, you must reset those secrets immediately.

## automan Workspaces

In Chapter 12, we built a package that included a binary and a library. As your
project develops, you might find that the library continues to get bigger and you
want to split your package further into multiple library packages. `automan`
offers a feature called _workspaces_ that can help manage multiple related
packages that are developed in tandem.

### Creating a Workspace

A _workspace_ is a set of packages that share the same _auto.lock_ and output
directory. Let's make a project using a workspace — we'll use trivial code so
that we can concentrate on the structure of the workspace. There are multiple
ways to structure a workspace, so we'll just show one common way. We'll have a
workspace containing a binary and two libraries. The binary, which will provide
the main functionality, will depend on the two libraries. One library will
provide an `add_one` function and the other library an `add_two` function.

First, create a new directory for the workspace:

```console
$ mkdir add
$ cd add
```

Next, in the _add_ directory, create the _auto.toml_ file that will configure the
entire workspace. This file won't have a `[package]` section. Instead, it will
start with a `[workspace]` section:

Filename: auto.toml

```toml
[workspace]
members = []
```

Next, create the `adder` binary package by running `automan new` within the _add_
directory:

```console
$ automan new adder
     Created binary (application) `adder` package
```

Running `automan new` inside a workspace also adds the newly created package to
the `members` key in the `[workspace]` definition:

```toml
[workspace]
members = ["adder"]
```

At this point, we can build the workspace by running `automan build`. The files
in your _add_ directory should look like this:

```text
├── auto.lock
├── auto.toml
├── adder
│   ├── auto.toml
│   └── src
│       └── main.at
└── target
```

The workspace has one _target_ directory at the top level that the compiled
artifacts will be placed into; the `adder` package doesn't have its own _target_
directory. Even if we were to run `automan build` from inside the _adder_
directory, the compiled artifacts would still end up in _add/target_ rather than
_add/adder/target_. `automan` structures the _target_ directory in a workspace
like this because the packages in a workspace are meant to depend on each other.
If each package had its own _target_ directory, each package would have to
recompile each of the other packages in the workspace to place the artifacts in
its own _target_ directory. By sharing one _target_ directory, the packages can
avoid unnecessary rebuilding.

### Creating the Second Package in the Workspace

Next, let's create another member package in the workspace and call it `add_one`.
Generate a new library package named `add_one`:

```console
$ automan new add_one --lib
     Created library `add_one` package
```

The top-level _auto.toml_ will now include `add_one` in the `members` list:

Filename: auto.toml

```toml
[workspace]
members = ["adder", "add_one"]
```

Your _add_ directory should now have these directories and files:

```text
├── auto.lock
├── auto.toml
├── add_one
│   ├── auto.toml
│   └── src
│       └── lib.at
├── adder
│   ├── auto.toml
│   └── src
│       └── main.at
└── target
```

In the _add_one/src/lib.at_ file, let's add an `add_one` function:

<Listing number="14-7" file-name="add_one/src/lib.at" caption="An `add_one` function in a library package">

```auto
pub fn add_one(x int) int {
    x + 1
}
```

```rust
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

Now we can have the `adder` package with our binary depend on the `add_one`
package that has our library. First, we need to add a path dependency on `add_one`
to _adder/auto.toml_:

Filename: adder/auto.toml

```toml
[dependencies]
add_one = { path = "../add_one" }
```

`automan` doesn't assume that packages in a workspace will depend on each other,
so we need to be explicit about the dependency relationships.

Next, let's use the `add_one` function in the `adder` package. Open
_adder/src/main.at_ and change the `main` function to call `add_one`, as in
Listing 14-8.

<Listing number="14-8" file-name="adder/src/main.at" caption="Using the `add_one` library package from the `adder` package">

```auto
fn main() {
    let num = 10
    print(f"Hello, world! ${num} plus one is ${add_one::add_one(num)}!")
}
```

```rust
fn main() {
    let num = 10;
    println!("Hello, world! {} plus one is {}!", num, add_one::add_one(num));
}
```

</Listing>

Let's build the workspace by running `automan build` in the top-level _add_
directory:

```console
$ automan build
   Compiling add_one v0.1.0
   Compiling adder v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

To run the binary package from the _add_ directory, specify which package in the
workspace we want to run by using the `-p` argument and the package name:

```console
$ automan run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running target/debug/adder
Hello, world! 10 plus one is 11!
```

### Depending on an External Package

Notice that the workspace has only one _auto.lock_ file at the top level, rather
than having an _auto.lock_ in each package's directory. This ensures that all
packages are using the same version of all dependencies. If we add the same
external package to both _adder/auto.toml_ and _add_one/auto.toml_, `automan`
will resolve both of those to one version and record that in the one _auto.lock_.
Making all packages in the workspace use the same dependencies means the packages
will always be compatible with each other.

Let's add an external dependency to the _add_one/auto.toml_ file:

Filename: add_one/auto.toml

```toml
[dependencies]
rand = "0.8.5"
```

Building the whole workspace by running `automan build` in the _add_ directory
will bring in and compile the `rand` dependency.

The top-level _auto.lock_ now contains information about the dependency of
`add_one` on `rand`. However, even though `rand` is used somewhere in the
workspace, we can't use it in other packages in the workspace unless we add `rand`
to their _auto.toml_ files as well. This ensures each package declares its own
dependencies explicitly.

### Adding a Test to a Workspace

For another enhancement, let's add a test of the `add_one::add_one` function
within the `add_one` package:

<Listing number="14-9" file-name="add_one/src/lib.at" caption="Adding a test to the `add_one` library package">

```auto
pub fn add_one(x int) int {
    x + 1
}

#[test]
fn it_works() {
    assert_eq(3, add_one(2))
}
```

```rust
pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(3, add_one(2));
    }
}
```

</Listing>

Now run `automan test` in the top-level _add_ directory. Running `automan test`
in a workspace structured like this one will run the tests for all the packages in
the workspace:

```console
$ automan test
   Compiling add_one v0.1.0
   Compiling adder v0.1.0
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.at (add_one)

running 1 test
test it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out
```

We can also run tests for one particular package in a workspace from the
top-level directory by using the `-p` flag:

```console
$ automan test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.at (add_one)

running 1 test
test it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out
```

If you publish the packages in the workspace to a registry, each package in the
workspace will need to be published separately. Like `automan test`, we can
publish a particular package by using the `-p` flag and specifying the name of
the package we want to publish.

As your project grows, consider using a workspace: it enables you to work with
smaller, easier-to-understand components than one big blob of code. Furthermore,
keeping the packages in a workspace can make coordination between packages easier
if they are often changed at the same time.

## Installing Binaries with `automan install`

The `automan install` command allows you to install and use binary packages
locally. This isn't intended to replace system packages; it's meant to be a
convenient way for Auto developers to install tools that others have shared on
the package registry. Note that you can only install packages that have binary
targets — that is, packages with a _src/main.at_ file or another file specified
as a binary, as opposed to a library target that isn't runnable on its own but is
suitable for including within other programs.

All binaries installed with `automan install` are stored in the installation
root's _bin_ folder. If you don't have any custom configurations, this directory
will be _$HOME/.automan/bin_. Ensure that this directory is in your `$PATH` to be
able to run programs you've installed with `automan install`.

For example, to install a tool published on the registry:

```console
$ automan install some-tool
   Installing some-tool v1.2.3
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.automan/bin/some-tool
   Installed package `some-tool v1.2.3`
```

As long as the installation directory is in your `$PATH`, you can then run the
installed tool directly from the command line.

## Extending automan with Custom Commands

`automan` is designed so you can extend it with new subcommands without having to
modify `automan` itself. If a binary in your `$PATH` is named
`automan-something`, you can run it as if it was an `automan` subcommand by
running `automan something`. Custom commands like this are also listed when you
run `automan --list`. Being able to use `automan install` to install extensions
and then run them just like the built-in `automan` tools is a super convenient
benefit of `automan`'s design!

## automan vs Cargo Quick Reference

| Feature | Auto (`automan`) | Rust (`cargo`) |
|---------|-------------------|----------------|
| Build | `automan build` | `cargo build` |
| Run | `automan run` | `cargo run` |
| Test | `automan test` | `cargo test` |
| Doc | `automan doc` | `cargo doc` |
| Publish | `automan publish` | `cargo publish` |
| Install | `automan install` | `cargo install` |
| New project | `automan new name` | `cargo new name` |
| Config file | `auto.toml` | `Cargo.toml` |
| Lock file | `auto.lock` | `Cargo.lock` |
| Source extension | `.at` | `.rs` |
| Registry | (TBD) | crates.io |

## Summary

Sharing code with `automan` and a package registry is part of what makes the Auto
ecosystem useful for many different tasks. Auto's standard library is small and
stable, but packages are easy to share, use, and improve on a timeline different
from that of the language. Don't be shy about sharing code that's useful to you;
it's likely that it will be useful to someone else as well!

In this chapter, we covered:

1. **Release profiles** — customizing build optimization for `dev` vs `release`
2. **Documentation comments** — `///` and `//!` for generating docs and running
   doc tests
3. **`pub use` re-exports** — making your public API convenient for users
4. **Publishing packages** — account setup, metadata, versioning, and yanking
5. **Workspaces** — managing multiple related packages that share dependencies
6. **Installing binaries** — `automan install` for local tool installation
7. **Custom commands** — extending `automan` with `automan-*` binaries

In the next chapter, we'll explore references and pointers in Auto and how they
relate to Rust's smart pointer types.
