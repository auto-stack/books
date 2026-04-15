# Inheritance

The language feature most often associated with object-oriented programming is **inheritance**. Inheritance is the ability to define a new class that is a modified version of an existing class.

In this chapter I demonstrate inheritance using classes that represent playing cards, decks of cards, and poker hands. If you don't play poker, don't worry -- I'll tell you what you need to know.

## Representing cards

There are 52 playing cards in a standard deck -- each of them belongs to one of four suits and one of thirteen ranks. The suits are Spades, Hearts, Diamonds, and Clubs. The ranks are Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, and King.

If we want to define a new object to represent a playing card, it is obvious what the attributes should be: `rank` and `suit`. One possibility is to use strings like `'Spade'` for suits and `'Queen'` for ranks. But a problem with this implementation is that it would not be easy to compare cards to see which had a higher rank or suit.

An alternative is to use integers to **encode** the ranks and suits. In this context, "encode" means that we are going to define a mapping between numbers and suits, or between numbers and ranks.

| Suit | Code |
| --- | --- |
|  Spades     |   3  |
|  Hearts     |   2  |
|  Diamonds   |   1  |
|  Clubs      |   0  |

To encode the ranks, we'll use the integer `2` to represent the rank `2`, `3` to represent `3`, and so on up to `10`.

| Rank | Code |
| --- | --- |
|  Jack     |   11  |
|  Queen   |   12  |
|  King      |   13  |

And we can use either `1` or `14` to represent an Ace, depending on whether we want it to be considered lower or higher than the other ranks.

To represent these encodings, we will use two lists of strings as module-level variables, one with the names of the suits and the other with the names of the ranks.

```auto
type Card {
    suit: int,
    rank: int,
}

let suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
let rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "Jack", "Queen", "King", "Ace"]
```

The first element of `rank_names` is `None` because there is no card with rank zero. By including `None` as a place-keeper, we get a list with the nice property that the index `2` maps to the string `'2'`, and so on.

## Card attributes

Here's an `init` method for the `Card` class -- it takes `suit` and `rank` as parameters and assigns them to attributes with the same names.

```auto
fn init(&self, suit: int, rank: int) {
    self.suit = suit
    self.rank = rank
}
```

Now we can create a `Card` object like this.

```auto
let queen = Card(1, 12)
```

We can use the new instance to access the attributes.

```auto
print(queen.suit)  // 1
print(queen.rank)  // 12
```

## Printing cards

Here's a `to_string` method for `Card` objects.

```auto
fn to_string(&self) -> str {
    let rank_name = rank_names[self.rank]
    let suit_name = suit_names[self.suit]
    return f"{rank_name} of {suit_name}"
}
```

When we print a `Card`, Auto calls the `to_string` method to get a human-readable representation of the card.

```auto
print(queen)  // Queen of Diamonds
```

## Comparing cards

Suppose we create a second `Card` object with the same suit and rank.

```auto
let queen2 = Card(1, 12)
print(queen2)  // Queen of Diamonds
```

If we use the `==` operator to compare them without defining `__eq__`, the default behavior checks whether `queen` and `queen2` refer to the same object. They don't, so it returns `false`.

We can change this behavior by defining the special method `__eq__`.

```auto
fn __eq__(&self, other: Card) -> bool {
    return self.suit == other.suit and self.rank == other.rank
}
```

`__eq__` takes two `Card` objects as parameters and returns `true` if they have the same suit and rank, even if they are not the same object. When we use the `==` operator with `Card` objects, Auto calls the `__eq__` method.

```auto
print(queen == queen2)  // true
```

Now suppose we want to compare two cards to see which is bigger. To change the behavior of the `<` operator, we can define a special method called `__lt__`, which is short for "less than".

For the sake of this example, let's assume that suit is more important than rank -- so all Spades outrank all Hearts, which outrank all Diamonds, and so on. If two cards have the same suit, the one with the higher rank wins.

```auto
fn __lt__(&self, other: Card) -> bool {
    return (self.suit, self.rank) < (other.suit, other.rank)
}
```

Tuple comparison compares the first elements from each tuple, which represent the suits. If they are the same, it compares the second elements, which represent the ranks.

```auto
let six = Card(1, 6)
print(six < queen)  // true
```

<Listing number="17-1" file-name="card_class.auto" caption="Card class definition with comparison">

```auto
type Card {
    suit: int,
    rank: int,
}

let suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
let rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "Jack", "Queen", "King", "Ace"]

fn init(&self, suit: int, rank: int) {
    self.suit = suit
    self.rank = rank
}

fn to_string(&self) -> str {
    let rank_name = rank_names[self.rank]
    let suit_name = suit_names[self.suit]
    return f"${rank_name} of ${suit_name}"
}

fn __eq__(&self, other: Card) -> bool {
    return self.suit == other.suit and self.rank == other.rank
}

fn to_tuple(&self) -> tuple {
    return (self.suit, self.rank)
}

fn __lt__(&self, other: Card) -> bool {
    return self.to_tuple() < other.to_tuple()
}

fn __le__(&self, other: Card) -> bool {
    return self.to_tuple() <= other.to_tuple()
}

fn main() {
    // Creating cards
    let queen = Card(1, 12)
    print(queen)  // Queen of Diamonds

    let ace = Card(3, 14)
    print(ace)    // Ace of Spades

    // Module-level variables (accessed directly)
    print(suit_names[0])   // Clubs
    print(rank_names[11])  // Jack

    // Card equivalence
    let queen2 = Card(1, 12)
    print(queen == queen2)  // true
    print(queen != queen2)  // false

    // Card comparison (suit first, then rank)
    let six = Card(1, 6)
    print(six < queen)   // true
    print(queen <= queen2)  // true
    print(queen >= six)  // true
    print(queen == six)  // false
}
```

```python
class Card:
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank_name = Card.rank_names[self.rank]
        suit_name = Card.suit_names[self.suit]
        return f"{rank_name} of {suit_name}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def to_tuple(self):
        return (self.suit, self.rank)

    def __lt__(self, other):
        return self.to_tuple() < other.to_tuple()

    def __le__(self, other):
        return self.to_tuple() <= other.to_tuple()


def main():
    # Creating cards
    queen = Card(1, 12)
    print(queen)  # Queen of Diamonds

    ace = Card(3, 14)
    print(ace)    # Ace of Spades

    # Class variables (accessed via the class)
    print(Card.suit_names[0])   # Clubs
    print(Card.rank_names[11])  # Jack

    # Card equivalence
    queen2 = Card(1, 12)
    print(queen == queen2)  # True
    print(queen != queen2)  # False

    # Card comparison (suit first, then rank)
    six = Card(1, 6)
    print(six < queen)      # True
    print(queen <= queen2)  # True
    print(queen >= six)     # True
    print(queen == six)     # False


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `Card` type uses integer codes for `suit` and `rank`. Module-level lists `suit_names` and `rank_names` provide human-readable names for these codes. The `__eq__` method checks equivalence based on suit and rank codes. The `__lt__` and `__le__` methods use tuple comparison, which first compares suits (higher suit code wins) and then ranks (higher rank wins). This makes `Card` objects **totally ordered**, meaning they can be sorted.

> **Note for Python Programmers:**
>
> In Auto, module-level variables like `suit_names` and `rank_names` serve the same purpose as Python's class variables. They are accessed directly by name in Auto, whereas in Python you would use `Card.suit_names`.

## Decks

Now that we have objects that represent cards, let's define objects that represent decks. The following is a class definition for `Deck` with an `init` method that takes a list of `Card` objects as a parameter and assigns it to an attribute called `cards`.

```auto
type Deck {
    cards: list,
}

fn init(&self, cards: list) {
    self.cards = cards
}
```

To create a list that contains the 52 cards in a standard deck, we'll use the following static method.

```auto
fn make_cards() -> list {
    let cards = []
    for suit in range(4) {
        for rank in range(2, 15) {
            cards.append(Card(suit, rank))
        }
    }
    return cards
}
```

In `make_cards`, the outer loop enumerates the suits from `0` to `3`. The inner loop enumerates the ranks from `2` to `14` -- where `14` represents an Ace that outranks a King. Each iteration creates a new `Card` with the current suit and rank, and appends it to `cards`.

Here's how we make a list of cards and a `Deck` object that contains it.

```auto
let cards = Deck.make_cards()
let deck = Deck(cards)
print(f"Deck has {len(deck.cards)} cards")  // Deck has 52 cards
```

## Printing the deck

Here is a `to_string` method for `Deck`.

```auto
fn to_string(&self) -> str {
    let res = []
    for card in self.cards {
        res.append(card.to_string())
    }
    return "\n".join(res)
}
```

This method demonstrates an efficient way to accumulate a large string -- building a list of strings and then using the string method `join`.

## Add, remove, shuffle and sort

To deal cards, we would like a method that removes a card from the deck and returns it. The list method `pop` provides a convenient way to do that.

```auto
fn take_card(&self) -> Card {
    return self.cards.pop()
}
```

To add a card, we can use the list method `append`.

```auto
fn put_card(&self, card: Card) {
    self.cards.append(card)
}
```

To shuffle the deck, we can use the `shuffle` function from the `random` module.

```auto
fn shuffle(&self) {
    random.shuffle(self.cards)
}
```

To sort the cards, we can use the list method `sort`, which sorts the elements "in place" -- that is, it modifies the list rather than creating a new list.

```auto
fn sort(&self) {
    self.cards.sort()
}
```

When we invoke `sort`, it uses the `__lt__` method to compare cards. Passing along responsibility like this is called **delegation**.

<Listing number="17-2" file-name="deck_class.auto" caption="Deck class with card operations">

```auto
type Card {
    suit: int,
    rank: int,
}

let suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
let rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "Jack", "Queen", "King", "Ace"]

fn init(&self, suit: int, rank: int) {
    self.suit = suit
    self.rank = rank
}

fn to_string(&self) -> str {
    let rank_name = rank_names[self.rank]
    let suit_name = suit_names[self.suit]
    return f"${rank_name} of ${suit_name}"
}

fn __lt__(&self, other: Card) -> bool {
    return (self.suit, self.rank) < (other.suit, other.rank)
}

type Deck {
    cards: list,
}

fn init(&self, cards: list) {
    self.cards = cards
}

fn to_string(&self) -> str {
    let res = []
    for card in self.cards {
        res.append(card.to_string())
    }
    return "\n".join(res)
}

fn make_cards() -> list {
    let cards = []
    for suit in range(4) {
        for rank in range(2, 15) {
            let card = Card(suit, rank)
            cards.append(card)
        }
    }
    return cards
}

fn take_card(&self) -> Card {
    return self.cards.pop()
}

fn put_card(&self, card: Card) {
    self.cards.append(card)
}

fn shuffle(&self) {
    random.shuffle(self.cards)
}

fn sort(&self) {
    self.cards.sort()

fn move_cards(&self, other: Deck, num: int) {
    for i in range(num) {
        let card = self.take_card()
        other.put_card(card)
    }

fn main() {
    // Create a full deck
    let cards = Deck.make_cards()
    let deck = Deck(cards)
    print(f"Deck has ${len(deck.cards)} cards")  // Deck has 52 cards

    // Print first few cards
    for card in deck.cards[:3] {
        print(card)
    }
    // 2 of Clubs
    // 3 of Clubs
    // 4 of Clubs

    // Take a card
    let card = deck.take_card()
    print(f"Took: ${card}")  // Took: Ace of Clubs
    print(f"Deck now has ${len(deck.cards)} cards")  // Deck now has 51 cards

    // Put it back
    deck.put_card(card)
    print(f"Deck has ${len(deck.cards)} cards again")  // Deck has 52 cards again

    // Shuffle
    deck.shuffle()
    print("After shuffle, first 4 cards:")
    for card in deck.cards[:4] {
        print(f"  ${card}")
    }

    // Sort
    deck.sort()
    print("After sort, first 4 cards:")
    for card in deck.cards[:4] {
        print(f"  ${card}")
    }
    // 2 of Clubs
    // 3 of Clubs
    // 4 of Clubs
    // 5 of Clubs
}
```

```python
import random


class Card:
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank_name = Card.rank_names[self.rank]
        suit_name = Card.suit_names[self.suit]
        return f"{rank_name} of {suit_name}"

    def __lt__(self, other):
        return (self.suit, self.rank) < (other.suit, other.rank)


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return "\n".join(res)

    @staticmethod
    def make_cards():
        cards = []
        for suit in range(4):
            for rank in range(2, 15):
                card = Card(suit, rank)
                cards.append(card)
        return cards

    def take_card(self):
        return self.cards.pop()

    def put_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def move_cards(self, other, num):
        for i in range(num):
            card = self.take_card()
            other.put_card(card)


def main():
    # Create a full deck
    cards = Deck.make_cards()
    deck = Deck(cards)
    print(f"Deck has {len(deck.cards)} cards")  # Deck has 52 cards

    # Print first few cards
    for card in deck.cards[:3]:
        print(card)
    # 2 of Clubs
    # 3 of Clubs
    # 4 of Clubs

    # Take a card
    card = deck.take_card()
    print(f"Took: {card}")  # Took: Ace of Clubs
    print(f"Deck now has {len(deck.cards)} cards")  # Deck now has 51 cards

    # Put it back
    deck.put_card(card)
    print(f"Deck has {len(deck.cards)} cards again")  # Deck has 52 cards again

    # Shuffle
    deck.shuffle()
    print("After shuffle, first 4 cards:")
    for card in deck.cards[:4]:
        print(f"  {card}")

    # Sort
    deck.sort()
    print("After sort, first 4 cards:")
    for card in deck.cards[:4]:
        print(f"  {card}")
    # 2 of Clubs
    # 3 of Clubs
    # 4 of Clubs
    # 5 of Clubs


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `Deck` type wraps a list of `Card` objects. The static method `make_cards` creates all 52 cards by iterating over suits (0-3) and ranks (2-14). The `take_card` method removes and returns the last card from the list (using `pop`), while `put_card` adds a card back. The `shuffle` method uses `random.shuffle` to randomize the order, and `sort` uses the list's built-in sort with `Card.__lt__` for comparison. The `move_cards` method deals a specified number of cards from one deck to another.

## Parents and children

Inheritance is the ability to define a new class that is a modified version of an existing class. As an example, let's say we want a class to represent a "hand", that is, the cards held by one player.

- A hand is similar to a deck -- both are made up of a collection of cards, and both require operations like adding and removing cards.

- A hand is also different from a deck -- there are operations we want for hands that don't make sense for a deck.

This relationship between classes -- where one is a specialized version of another -- lends itself to inheritance.

To define a new class that is based on an existing class, we put the name of the existing class after a colon.

```auto
type Hand: Deck {
    label: str,
}

fn init(&self, label: str = "") {
    self.label = label
    self.cards = []
}
```

This definition indicates that `Hand` inherits from `Deck`, which means that `Hand` objects can access methods defined in `Deck`, like `take_card` and `put_card`.

`Hand` also inherits `init` from `Deck`, but if we define `init` in the `Hand` class, it overrides the one in the `Deck` class. This version takes an optional string as a parameter and always starts with an empty list of cards.

When we create a `Hand`, Auto invokes this method, not the one in `Deck`.

```auto
let hand = Hand("player 1")
print(f"Hand label: {hand.label}")  // Hand label: player 1
```

To deal cards, we can use `take_card` to remove a card from a `Deck`, and `put_card` to add the card to a `Hand`. The `move_cards` method from `Deck` does this automatically.

This method is polymorphic -- that is, it works with more than one type: `self` and `other` can be either a `Hand` or a `Deck`.

When a new class inherits from an existing one, the existing one is called the **parent** and the new class is called the **child**. In general:

- Instances of the child class should have all of the attributes of the parent class, but they can have additional attributes.

- The child class should have all of the methods of the parent class, but it can have additional methods.

- If a child class overrides a method from the parent class, the new method should take the same parameters and return a compatible result.

This set of rules is called the "Liskov substitution principle". If you follow these rules, any function or method designed to work with an instance of a parent class will also work with instances of a child class.

<Listing number="17-3" file-name="hand_inheritance.auto" caption="Inheritance: Hand extends Deck">

```auto
type Card {
    suit: int,
    rank: int,
}

let suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
let rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "Jack", "Queen", "King", "Ace"]

fn init(&self, suit: int, rank: int) {
    self.suit = suit
    self.rank = rank
}

fn to_string(&self) -> str {
    let rank_name = rank_names[self.rank]
    let suit_name = suit_names[self.suit]
    return f"${rank_name} of ${suit_name}"
}

fn __lt__(&self, other: Card) -> bool {
    return (self.suit, self.rank) < (other.suit, other.rank)
}

type Deck {
    cards: list,
}

fn init(&self, cards: list) {
    self.cards = cards
}

fn to_string(&self) -> str {
    let res = []
    for card in self.cards {
        res.append(card.to_string())
    }
    return "\n".join(res)
}

fn make_cards() -> list {
    let cards = []
    for suit in range(4) {
        for rank in range(2, 15) {
            cards.append(Card(suit, rank))
        }
    }
    return cards
}

fn take_card(&self) -> Card {
    return self.cards.pop()
}

fn put_card(&self, card: Card) {
    self.cards.append(card)
}

fn shuffle(&self) {
    random.shuffle(self.cards)
}

fn sort(&self) {
    self.cards.sort()

fn move_cards(&self, other: Deck, num: int) {
    for i in range(num) {
        other.put_card(self.take_card())
    }

// Hand inherits from Deck
type Hand: Deck {
    label: str,
}

fn init(&self, label: str = "") {
    self.label = label
    self.cards = []
}

fn main() {
    // Create a deck and a hand
    let cards = Deck.make_cards()
    let deck = Deck(cards)
    let hand = Hand("player 1")
    print(f"Hand label: ${hand.label}")  // Hand label: player 1

    // Hand inherits put_card from Deck
    deck.shuffle()
    deck.move_cards(hand, 5)
    print(f"Hand has ${len(hand.cards)} cards:")
    print(hand)

    // Hand inherits sort from Deck
    hand.sort()
    print("After sorting:")
    print(hand)

    // Polymorphism: move_cards works with Deck and Hand
    let hand2 = Hand("player 2")
    deck.move_cards(hand2, 5)
    print(f"Hand2 has ${len(hand2.cards)} cards")
}
```

```python
import random


class Card:
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank_name = Card.rank_names[self.rank]
        suit_name = Card.suit_names[self.suit]
        return f"{rank_name} of {suit_name}"

    def __lt__(self, other):
        return (self.suit, self.rank) < (other.suit, other.rank)


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return "\n".join(res)

    @staticmethod
    def make_cards():
        cards = []
        for suit in range(4):
            for rank in range(2, 15):
                cards.append(Card(suit, rank))
        return cards

    def take_card(self):
        return self.cards.pop()

    def put_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def move_cards(self, other, num):
        for i in range(num):
            other.put_card(self.take_card())


class Hand(Deck):
    def __init__(self, label=""):
        self.label = label
        self.cards = []


def main():
    # Create a deck and a hand
    cards = Deck.make_cards()
    deck = Deck(cards)
    hand = Hand("player 1")
    print(f"Hand label: {hand.label}")  # Hand label: player 1

    # Hand inherits put_card from Deck
    deck.shuffle()
    deck.move_cards(hand, 5)
    print(f"Hand has {len(hand.cards)} cards:")
    print(hand)

    # Hand inherits sort from Deck
    hand.sort()
    print("After sorting:")
    print(hand)

    # Polymorphism: move_cards works with Deck and Hand
    hand2 = Hand("player 2")
    deck.move_cards(hand2, 5)
    print(f"Hand2 has {len(hand2.cards)} cards")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In Auto, `type Hand: Deck { ... }` defines `Hand` as a child of `Deck`. This is equivalent to Python's `class Hand(Deck)`. The `Hand` type inherits all methods from `Deck` (`take_card`, `put_card`, `sort`, `shuffle`, `move_cards`) but overrides `init` to add a `label` field and start with an empty card list. The `move_cards` method is polymorphic -- it works with any `Deck` subclass, so you can deal cards between `Deck` and `Hand` objects interchangeably.

> **Note for Python Programmers:**
>
> Auto uses `type Hand: Deck { ... }` instead of Python's `class Hand(Deck)`. The colon syntax indicates inheritance. The `a2p` transpiler converts this to Python's class inheritance syntax.

## Specialization

Let's make a class called `BridgeHand` that represents a hand in bridge -- a widely played card game. We'll inherit from `Hand` and add a new method called `high_card_point_count` that evaluates a hand using a "high card point" method.

Here's a class definition that contains a dictionary that maps from card names to their point values.

```auto
type BridgeHand: Hand {
    hcp_dict: dict,
}

let hcp_dict = {
    "Ace": 4,
    "King": 3,
    "Queen": 2,
    "Jack": 1,
}
```

Given the rank of a card, like `12`, we can use `rank_names` to get the string representation of the rank, and then use `hcp_dict` to get its score.

The following method loops through the cards in a `BridgeHand` and adds up their scores.

```auto
fn high_card_point_count(&self) -> int {
    let count = 0
    for card in self.cards {
        let rank_name = rank_names[card.rank]
        count += hcp_dict.get(rank_name, 0)
    }
    return count
}
```

`BridgeHand` inherits the variables and methods of `Hand` and adds a dictionary and a method that are specific to bridge. This way of using inheritance is called **specialization** because it defines a new class that is specialized for a particular use, like playing bridge.

<Listing number="17-4" file-name="card_deck_hand.auto" caption="Full Card/Deck/Hand/BridgeHand example">

```auto
type Card {
    suit: int,
    rank: int,
}

let suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
let rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "Jack", "Queen", "King", "Ace"]

fn init(&self, suit: int, rank: int) {
    self.suit = suit
    self.rank = rank
}

fn to_string(&self) -> str {
    let rank_name = rank_names[self.rank]
    let suit_name = suit_names[self.suit]
    return f"${rank_name} of ${suit_name}"
}

fn __eq__(&self, other: Card) -> bool {
    return self.suit == other.suit and self.rank == other.rank
}

fn __lt__(&self, other: Card) -> bool {
    return (self.suit, self.rank) < (other.suit, other.rank)
}

type Deck {
    cards: list,
}

fn init(&self, cards: list) {
    self.cards = cards
}

fn to_string(&self) -> str {
    let res = []
    for card in self.cards {
        res.append(card.to_string())
    }
    return "\n".join(res)
}

fn make_cards() -> list {
    let cards = []
    for suit in range(4) {
        for rank in range(2, 15) {
            cards.append(Card(suit, rank))
        }
    }
    return cards
}

fn take_card(&self) -> Card {
    return self.cards.pop()
}

fn put_card(&self, card: Card) {
    self.cards.append(card)
}

fn shuffle(&self) {
    random.shuffle(self.cards)
}

fn sort(&self) {
    self.cards.sort()

fn move_cards(&self, other: Deck, num: int) {
    for i in range(num) {
        other.put_card(self.take_card())
    }

// Hand inherits from Deck
type Hand: Deck {
    label: str,
}

fn init(&self, label: str = "") {
    self.label = label
    self.cards = []
}

// BridgeHand specializes Hand with a scoring method
type BridgeHand: Hand {
    hcp_dict: dict,
}

let hcp_dict = {
    "Ace": 4,
    "King": 3,
    "Queen": 2,
    "Jack": 1,
}

fn high_card_point_count(&self) -> int {
    let count = 0
    for card in self.cards {
        let rank_name = rank_names[card.rank]
        count += hcp_dict.get(rank_name, 0)
    }
    return count
}

fn main() {
    // Create and shuffle a deck
    let cards = Deck.make_cards()
    let deck = Deck(cards)
    deck.shuffle()

    // Deal a bridge hand (normally 13, using 5 for demo)
    let hand = BridgeHand("player 2")
    deck.move_cards(hand, 5)
    print(f"${hand.label}'s hand:")
    print(hand)

    // Count high card points
    let points = hand.high_card_point_count()
    print(f"High card points: ${points}")

    // Inheritance chain: BridgeHand -> Hand -> Deck
    // BridgeHand inherits put_card, sort, take_card from Hand/Deck
    hand.sort()
    print("Sorted hand:")
    print(hand)

    // Polymorphism: move_cards works with any Deck subtype
    let another_hand = Hand("player 3")
    deck.move_cards(another_hand, 5)
    print(f"\n${another_hand.label}'s hand has ${len(another_hand.cards)} cards")
}
```

```python
import random


class Card:
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank_name = Card.rank_names[self.rank]
        suit_name = Card.suit_names[self.suit]
        return f"{rank_name} of {suit_name}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        return (self.suit, self.rank) < (other.suit, other.rank)


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return "\n".join(res)

    @staticmethod
    def make_cards():
        cards = []
        for suit in range(4):
            for rank in range(2, 15):
                cards.append(Card(suit, rank))
        return cards

    def take_card(self):
        return self.cards.pop()

    def put_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def move_cards(self, other, num):
        for i in range(num):
            other.put_card(self.take_card())


class Hand(Deck):
    def __init__(self, label=""):
        self.label = label
        self.cards = []


class BridgeHand(Hand):
    hcp_dict = {
        "Ace": 4,
        "King": 3,
        "Queen": 2,
        "Jack": 1,
    }

    def high_card_point_count(self):
        count = 0
        for card in self.cards:
            rank_name = Card.rank_names[card.rank]
            count += BridgeHand.hcp_dict.get(rank_name, 0)
        return count


def main():
    # Create and shuffle a deck
    cards = Deck.make_cards()
    deck = Deck(cards)
    deck.shuffle()

    # Deal a bridge hand (normally 13, using 5 for demo)
    hand = BridgeHand("player 2")
    deck.move_cards(hand, 5)
    print(f"{hand.label}'s hand:")
    print(hand)

    # Count high card points
    points = hand.high_card_point_count()
    print(f"High card points: {points}")

    # Inheritance chain: BridgeHand -> Hand -> Deck
    # BridgeHand inherits put_card, sort, take_card from Hand/Deck
    hand.sort()
    print("Sorted hand:")
    print(hand)

    # Polymorphism: move_cards works with any Deck subtype
    another_hand = Hand("player 3")
    deck.move_cards(another_hand, 5)
    print(f"\n{another_hand.label}'s hand has {len(another_hand.cards)} cards")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

This listing demonstrates the full inheritance chain: `BridgeHand` inherits from `Hand`, which inherits from `Deck`. `BridgeHand` adds a `hcp_dict` and a `high_card_point_count` method that scores a hand based on face cards (Ace=4, King=3, Queen=2, Jack=1). Despite the specialization, `BridgeHand` still has access to all methods from its ancestors -- it can be dealt cards via `move_cards`, sorted via `sort`, and printed via `to_string`. This is the essence of inheritance: reuse through extension.

## Debugging

Inheritance is a useful feature. Some programs that would be repetitive without inheritance can be written more concisely with it. Also, inheritance can facilitate code reuse, since you can customize the behavior of a parent class without having to modify it.

On the other hand, inheritance can make programs difficult to read. When a method is invoked, it is sometimes not clear where to find its definition -- the relevant code may be spread across several modules.

Any time you are unsure about the flow of execution through your program, the simplest solution is to add print statements at the beginning of the relevant methods. If a method prints a message like "Running Deck.shuffle", then as the program runs it traces the flow of execution.

## Glossary

**inheritance:**
The ability to define a new class that is a modified version of a previously defined class.

**encode:**
To represent one set of values using another set of values by constructing a mapping between them.

**class variable:**
A variable defined inside a class definition, but not inside any method. In Auto, these are module-level variables associated with the type.

**totally ordered:**
A set of objects is totally ordered if we can compare any two elements and the results are consistent.

**delegation:**
When one method passes responsibility to another method to do most or all of the work.

**parent class:**
A class that is inherited from.

**child class:**
A class that inherits from another class.

**specialization:**
A way of using inheritance to create a new class that is a specialized version of an existing class.

## Exercises

### Exercise

In contract bridge, a "trick" is a round of play in which each of four players plays one card. Write a `Trick` method called `find_winner` that loops through the cards in a `Trick` (which inherits from `Deck`) and returns the index of the card that wins. The winner is the highest card in the "led suit" (the suit of the first card played).

### Exercise

Write a `PokerHand` method called `has_flush` that checks whether a hand has a "flush" -- that is, whether it contains at least five cards of the same suit.

### Exercise

Write a `PokerHand` method called `has_straight` that checks whether a hand contains a straight, which is a set of five cards with consecutive ranks. Remember that an Ace can be high (14) or low (1), but a straight cannot "wrap around" (King, Ace, 2, 3, 4 is not a straight).

### Exercise

Write a `PokerHand` method called `has_pair` that checks whether a hand contains two or more cards with the same rank.
