# Foreword

Auto was born from a simple question: what would a programming language look
like if it were designed from the ground up to be written *with* AI, not just
*by* humans?

The answer is a language that strips away ceremony, eliminates entire classes
of bugs at compile time, and makes concurrency as natural as writing sequential
code. Auto borrows hard-won lessons from Rust—ownership, move semantics,
zero-cost abstractions—while removing the annotation burden that makes those
concepts explicit in Rust. In Auto, the compiler handles lifetimes, borrowing,
and resource cleanup automatically through the AutoFree system.

But Auto is more than "Rust with less syntax." Its `is`/`has`/`spec` type
system offers a fresh take on inheritance, composition, and polymorphism.
Its Actor-based concurrency model, built around `task` and `mailbox`, makes
data races physically impossible by design. And its `#[]` comptime system
brings metaprogramming into the language itself, without the complexity of
procedural macros.

This book is structured after *The Rust Programming Language*, one of the
finest programming language books ever written. We follow the same chapter
progression so that readers familiar with Rust can map their knowledge
directly. Code examples are presented in both Auto and Rust, highlighting
the correspondence between the two languages.

Welcome to Auto.

- The Auto Language Team
