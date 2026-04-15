# 继承

与面向对象编程最常相关的语言特性是**继承**（inheritance）。继承是定义一个新类作为现有类的修改版本的能力。

在本章中，我使用表示扑克牌、牌组和牌手的类来演示继承。如果你不玩扑克，别担心 -- 我会告诉你需要知道的内容。

## 表示牌

一副标准扑克牌有 52 张牌 -- 每张牌属于四种花色之一和十三个点数之一。花色是黑桃、红心、方块和梅花。点数是 A、2、3、4、5、6、7、8、9、10、J、Q 和 K。

如果我们想定义一个新对象来表示扑克牌，属性应该是显而易见的：`rank` 和 `suit`。一种可能是使用字符串如 `'Spade'` 表示花色，`'Queen'` 表示点数。但这种实现的问题是很难比较牌的大小。

另一种方法是使用整数来**编码**（encode）点数和花色。在这种情况下，"编码"意味着我们在数字和花色之间，或数字和点数之间定义映射。

| 花色 | 编码 |
| --- | --- |
|  黑桃     |   3  |
|  红心     |   2  |
|  方块   |   1  |
|  梅花      |   0  |

为了编码点数，我们使用整数 `2` 表示点数 `2`，`3` 表示 `3`，依此类推直到 `10`。

| 点数 | 编码 |
| --- | --- |
|  J     |   11  |
|  Q   |   12  |
|  K      |   13  |

我们可以使用 `1` 或 `14` 来表示 A，取决于我们希望它比其他点数低还是高。

为了表示这些编码，我们将使用两个字符串列表作为模块级变量，一个是花色名称，另一个是点数名称。

```auto
type Card {
    suit: int,
    rank: int,
}

let suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
let rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "Jack", "Queen", "King", "Ace"]
```

`rank_names` 的第一个元素是 `None`，因为没有点数为零的牌。通过包含 `None` 作为占位符，我们得到了一个具有良好属性的列表：索引 `2` 映射到字符串 `'2'`，依此类推。

## 牌的属性

下面是 `Card` 类的 `init` 方法 -- 它接受 `suit` 和 `rank` 作为参数并将它们赋给同名属性。

```auto
fn init(&self, suit: int, rank: int) {
    self.suit = suit
    self.rank = rank
}
```

现在我们可以这样创建一个 `Card` 对象：

```auto
let queen = Card(1, 12)
```

我们可以使用新实例来访问属性：

```auto
print(queen.suit)  // 1
print(queen.rank)  // 12
```

## 打印牌

下面是 `Card` 对象的 `to_string` 方法：

```auto
fn to_string(&self) -> str {
    let rank_name = rank_names[self.rank]
    let suit_name = suit_names[self.suit]
    return f"{rank_name} of {suit_name}"
}
```

当我们打印一个 `Card` 时，Auto 调用 `to_string` 方法来获取牌的人类可读表示。

```auto
print(queen)  // Queen of Diamonds
```

## 比较牌

假设我们创建第二个具有相同花色和点数的 `Card` 对象：

```auto
let queen2 = Card(1, 12)
print(queen2)  // Queen of Diamonds
```

如果我们在没有定义 `__eq__` 的情况下使用 `==` 运算符比较它们，默认行为检查 `queen` 和 `queen2` 是否引用同一个对象。它们不是，所以返回 `false`。

我们可以通过定义特殊方法 `__eq__` 来改变这种行为：

```auto
fn __eq__(&self, other: Card) -> bool {
    return self.suit == other.suit and self.rank == other.rank
}
```

`__eq__` 接受两个 `Card` 对象作为参数，如果它们具有相同的花色和点数则返回 `true`，即使它们不是同一个对象。当我们对 `Card` 对象使用 `==` 运算符时，Auto 调用 `__eq__` 方法。

```auto
print(queen == queen2)  // true
```

现在假设我们想比较两张牌看哪张大。要改变 `<` 运算符的行为，我们可以定义一个名为 `__lt__` 的特殊方法，是 "less than" 的缩写。

为了这个示例，我们假设花色比点数更重要 -- 所以所有黑桃大于所有红心，红心大于所有方块，依此类推。如果两张牌花色相同，点数较高的获胜。

```auto
fn __lt__(&self, other: Card) -> bool {
    return (self.suit, self.rank) < (other.suit, other.rank)
}
```

元组比较首先比较每个元组的第一个元素（代表花色）。如果相同，再比较第二个元素（代表点数）。

```auto
let six = Card(1, 6)
print(six < queen)  // true
```

<Listing number="17-1" file-name="card_class.auto" caption="带有比较功能的 Card 类定义">

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
    // 创建牌
    let queen = Card(1, 12)
    print(queen)  // Queen of Diamonds

    let ace = Card(3, 14)
    print(ace)    // Ace of Spades

    // 模块级变量（直接访问）
    print(suit_names[0])   // Clubs
    print(rank_names[11])  // Jack

    // 牌的等价性
    let queen2 = Card(1, 12)
    print(queen == queen2)  // true
    print(queen != queen2)  // false

    // 牌的比较（先花色，后点数）
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
    # 创建牌
    queen = Card(1, 12)
    print(queen)  # Queen of Diamonds

    ace = Card(3, 14)
    print(ace)    # Ace of Spades

    # 类变量（通过类访问）
    print(Card.suit_names[0])   # Clubs
    print(Card.rank_names[11])  # Jack

    # 牌的等价性
    queen2 = Card(1, 12)
    print(queen == queen2)  # True
    print(queen != queen2)  # False

    # 牌的比较（先花色，后点数）
    six = Card(1, 6)
    print(six < queen)      # True
    print(queen <= queen2)  # True
    print(queen >= six)     # True
    print(queen == six)     # False


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`Card` 类型使用整数编码表示 `suit` 和 `rank`。模块级列表 `suit_names` 和 `rank_names` 为这些编码提供人类可读的名称。`__eq__` 方法基于花色和点数编码检查等价性。`__lt__` 和 `__le__` 方法使用元组比较，先比较花色（花色编码高的获胜），再比较点数（点数高的获胜）。这使得 `Card` 对象是**全序的**（totally ordered），即可以排序。

> **Python 程序员注意：**
>
> 在 Auto 中，模块级变量如 `suit_names` 和 `rank_names` 的作用与 Python 的类变量相同。在 Auto 中通过名称直接访问，而在 Python 中你会使用 `Card.suit_names`。

## 牌组

既然我们有了表示牌的对象，让我们定义表示牌组的对象。以下是 `Deck` 的类定义，带有一个 `init` 方法，它接受一个 `Card` 对象列表作为参数并将其赋给名为 `cards` 的属性。

```auto
type Deck {
    cards: list,
}

fn init(&self, cards: list) {
    self.cards = cards
}
```

要创建包含一副标准 52 张牌的列表，我们将使用以下静态方法：

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

在 `make_cards` 中，外层循环遍历花色从 `0` 到 `3`。内层循环遍历点数从 `2` 到 `14` -- 其中 `14` 表示大于 K 的 A。每次迭代创建一个具有当前花色和点数的新 `Card`，并将其追加到 `cards` 中。

以下是我们创建牌列表和包含它的 `Deck` 对象的方式：

```auto
let cards = Deck.make_cards()
let deck = Deck(cards)
print(f"Deck has {len(deck.cards)} cards")  // Deck has 52 cards
```

## 打印牌组

以下是 `Deck` 的 `to_string` 方法：

```auto
fn to_string(&self) -> str {
    let res = []
    for card in self.cards {
        res.append(card.to_string())
    }
    return "\n".join(res)
}
```

这个方法演示了一种积累大字符串的高效方法 -- 构建一个字符串列表，然后使用字符串方法 `join`。

## 添加、移除、洗牌和排序

要发牌，我们需要一个从牌组中移除一张牌并返回它的方法。列表方法 `pop` 提供了一种方便的方式。

```auto
fn take_card(&self) -> Card {
    return self.cards.pop()
}
```

要添加一张牌，我们可以使用列表方法 `append`：

```auto
fn put_card(&self, card: Card) {
    self.cards.append(card)
}
```

要洗牌，我们可以使用 `random` 模块的 `shuffle` 函数：

```auto
fn shuffle(&self) {
    random.shuffle(self.cards)
}
```

要排序，我们可以使用列表方法 `sort`，它"就地"排序元素 -- 即修改列表而不是创建新列表。

```auto
fn sort(&self) {
    self.cards.sort()
}
```

当我们调用 `sort` 时，它使用 `__lt__` 方法来比较牌。这种将责任传递下去的方式称为**委托**（delegation）。

<Listing number="17-2" file-name="deck_class.auto" caption="带有牌操作的 Deck 类">

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
    // 创建一副完整的牌
    let cards = Deck.make_cards()
    let deck = Deck(cards)
    print(f"Deck has ${len(deck.cards)} cards")  // Deck has 52 cards

    // 打印前几张牌
    for card in deck.cards[:3] {
        print(card)
    }
    // 2 of Clubs
    // 3 of Clubs
    // 4 of Clubs

    // 抽一张牌
    let card = deck.take_card()
    print(f"Took: ${card}")  // Took: Ace of Clubs
    print(f"Deck now has ${len(deck.cards)} cards")  // Deck now has 51 cards

    // 放回去
    deck.put_card(card)
    print(f"Deck has ${len(deck.cards)} cards again")  // Deck has 52 cards again

    // 洗牌
    deck.shuffle()
    print("After shuffle, first 4 cards:")
    for card in deck.cards[:4] {
        print(f"  ${card}")
    }

    // 排序
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
    # 创建一副完整的牌
    cards = Deck.make_cards()
    deck = Deck(cards)
    print(f"Deck has {len(deck.cards)} cards")  # Deck has 52 cards

    # 打印前几张牌
    for card in deck.cards[:3]:
        print(card)
    # 2 of Clubs
    # 3 of Clubs
    # 4 of Clubs

    # 抽一张牌
    card = deck.take_card()
    print(f"Took: {card}")  # Took: Ace of Clubs
    print(f"Deck now has {len(deck.cards)} cards")  # Deck now has 51 cards

    # 放回去
    deck.put_card(card)
    print(f"Deck has {len(deck.cards)} cards again")  # Deck has 52 cards again

    # 洗牌
    deck.shuffle()
    print("After shuffle, first 4 cards:")
    for card in deck.cards[:4]:
        print(f"  {card}")

    # 排序
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

**工作原理**

`Deck` 类型包装了一个 `Card` 对象列表。静态方法 `make_cards` 通过遍历花色（0-3）和点数（2-14）创建所有 52 张牌。`take_card` 方法从列表中移除并返回最后一张牌（使用 `pop`），`put_card` 将牌添加回去。`shuffle` 方法使用 `random.shuffle` 随机化顺序，`sort` 使用列表的内置排序和 `Card.__lt__` 进行比较。`move_cards` 方法将指定数量的牌从一个牌组发到另一个。

## 父类和子类

继承是定义一个新类作为现有类的修改版本的能力。例如，假设我们想要一个类来表示"手牌"，即一个玩家手中的牌。

- 手牌类似于牌组 -- 两者都是由一组牌组成的，都需要添加和移除牌的操作。

- 手牌也与牌组不同 -- 有些对手牌有意义的操作对牌组没有意义。

这种类之间的关系 -- 其中一个是另一个的特化版本 -- 适合使用继承。

要基于现有类定义新类，我们在冒号后放置现有类的名称。

```auto
type Hand: Deck {
    label: str,
}

fn init(&self, label: str = "") {
    self.label = label
    self.cards = []
}
```

这个定义表示 `Hand` 继承自 `Deck`，这意味着 `Hand` 对象可以访问 `Deck` 中定义的方法，如 `take_card` 和 `put_card`。

`Hand` 也从 `Deck` 继承了 `init`，但如果我们在 `Hand` 类中定义 `init`，它会覆盖 `Deck` 类中的那个。这个版本接受一个可选字符串作为参数，并总是以空牌列表开始。

当我们创建一个 `Hand` 时，Auto 调用这个方法，而不是 `Deck` 中的那个。

```auto
let hand = Hand("player 1")
print(f"Hand label: {hand.label}")  // Hand label: player 1
```

要发牌，我们可以使用 `take_card` 从 `Deck` 中移除一张牌，使用 `put_card` 将牌添加到 `Hand` 中。`Deck` 中的 `move_cards` 方法自动完成这个过程。

这个方法是多态的 -- 即它适用于多种类型：`self` 和 `other` 可以是 `Hand` 或 `Deck`。

当新类继承现有类时，现有类称为**父类**（parent），新类称为**子类**（child）。一般来说：

- 子类的实例应该具有父类的所有属性，但可以有额外的属性。

- 子类应该具有父类的所有方法，但可以有额外的方法。

- 如果子类覆盖了父类的方法，新方法应该接受相同的参数并返回兼容的结果。

这组规则称为"Liskov 替换原则"。如果你遵循这些规则，任何设计用于处理父类实例的函数或方法也能处理子类的实例。

<Listing number="17-3" file-name="hand_inheritance.auto" caption="继承：Hand 继承 Deck">

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

// Hand 继承自 Deck
type Hand: Deck {
    label: str,
}

fn init(&self, label: str = "") {
    self.label = label
    self.cards = []
}

fn main() {
    // 创建牌组和手牌
    let cards = Deck.make_cards()
    let deck = Deck(cards)
    let hand = Hand("player 1")
    print(f"Hand label: ${hand.label}")  // Hand label: player 1

    // Hand 从 Deck 继承 put_card
    deck.shuffle()
    deck.move_cards(hand, 5)
    print(f"Hand has ${len(hand.cards)} cards:")
    print(hand)

    // Hand 从 Deck 继承 sort
    hand.sort()
    print("After sorting:")
    print(hand)

    // 多态：move_cards 适用于 Deck 和 Hand
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
    # 创建牌组和手牌
    cards = Deck.make_cards()
    deck = Deck(cards)
    hand = Hand("player 1")
    print(f"Hand label: {hand.label}")  # Hand label: player 1

    # Hand 从 Deck 继承 put_card
    deck.shuffle()
    deck.move_cards(hand, 5)
    print(f"Hand has {len(hand.cards)} cards:")
    print(hand)

    # Hand 从 Deck 继承 sort
    hand.sort()
    print("After sorting:")
    print(hand)

    # 多态：move_cards 适用于 Deck 和 Hand
    hand2 = Hand("player 2")
    deck.move_cards(hand2, 5)
    print(f"Hand2 has {len(hand2.cards)} cards")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在 Auto 中，`type Hand: Deck { ... }` 将 `Hand` 定义为 `Deck` 的子类。这等价于 Python 的 `class Hand(Deck)`。`Hand` 类型从 `Deck` 继承所有方法（`take_card`、`put_card`、`sort`、`shuffle`、`move_cards`），但覆盖了 `init` 以添加 `label` 字段并从空牌列表开始。`move_cards` 方法是多态的 -- 它适用于任何 `Deck` 子类，因此你可以在 `Deck` 和 `Hand` 对象之间互换地发牌。

> **Python 程序员注意：**
>
> Auto 使用 `type Hand: Deck { ... }` 代替 Python 的 `class Hand(Deck)`。冒号语法表示继承。`a2p` 转译器会将此转换为 Python 的类继承语法。

## 特化

让我们创建一个名为 `BridgeHand` 的类来表示桥牌中的手牌 -- 桥牌是一种广泛流行的纸牌游戏。我们将从 `Hand` 继承并添加一个名为 `high_card_point_count` 的新方法，使用"大牌点"方法来评估手牌。

下面是一个包含将牌名映射到其分值字典的类定义：

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

给定一张牌的点数（如 `12`），我们可以使用 `rank_names` 获取点数的字符串表示，然后使用 `hcp_dict` 获取其分数。

以下方法遍历 `BridgeHand` 中的牌并累加它们的分数：

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

`BridgeHand` 继承了 `Hand` 的变量和方法，并添加了一个字典和一个特定于桥牌的方法。这种使用继承的方式称为**特化**（specialization），因为它定义了一个为特定用途（如打桥牌）特化的新类。

<Listing number="17-4" file-name="card_deck_hand.auto" caption="完整的 Card/Deck/Hand/BridgeHand 示例">

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

// Hand 继承自 Deck
type Hand: Deck {
    label: str,
}

fn init(&self, label: str = "") {
    self.label = label
    self.cards = []
}

// BridgeHand 特化 Hand，添加了计分方法
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
    // 创建并洗牌
    let cards = Deck.make_cards()
    let deck = Deck(cards)
    deck.shuffle()

    // 发桥牌手牌（通常13张，演示用5张）
    let hand = BridgeHand("player 2")
    deck.move_cards(hand, 5)
    print(f"${hand.label}'s hand:")
    print(hand)

    // 计算大牌点
    let points = hand.high_card_point_count()
    print(f"High card points: ${points}")

    // 继承链：BridgeHand -> Hand -> Deck
    // BridgeHand 从 Hand/Deck 继承 put_card, sort, take_card
    hand.sort()
    print("Sorted hand:")
    print(hand)

    // 多态：move_cards 适用于任何 Deck 子类型
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
    # 创建并洗牌
    cards = Deck.make_cards()
    deck = Deck(cards)
    deck.shuffle()

    # 发桥牌手牌（通常13张，演示用5张）
    hand = BridgeHand("player 2")
    deck.move_cards(hand, 5)
    print(f"{hand.label}'s hand:")
    print(hand)

    # 计算大牌点
    points = hand.high_card_point_count()
    print(f"High card points: {points}")

    # 继承链：BridgeHand -> Hand -> Deck
    # BridgeHand 从 Hand/Deck 继承 put_card, sort, take_card
    hand.sort()
    print("Sorted hand:")
    print(hand)

    # 多态：move_cards 适用于任何 Deck 子类型
    another_hand = Hand("player 3")
    deck.move_cards(another_hand, 5)
    print(f"\n{another_hand.label}'s hand has {len(another_hand.cards)} cards")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

此 listing 演示了完整的继承链：`BridgeHand` 继承自 `Hand`，`Hand` 继承自 `Deck`。`BridgeHand` 添加了 `hcp_dict` 和 `high_card_point_count` 方法，根据大牌（A=4，K=3，Q=2，J=1）为手牌计分。尽管有特化，`BridgeHand` 仍然可以访问其祖先的所有方法 -- 它可以通过 `move_cards` 被发牌，通过 `sort` 排序，通过 `to_string` 打印。这就是继承的本质：通过扩展实现复用。

## 调试

继承是一个有用的特性。没有继承会显得重复的程序可以通过继承更简洁地编写。此外，继承可以促进代码复用，因为你可以自定义父类的行为而不必修改它。

另一方面，继承会使程序难以阅读。当一个方法被调用时，有时不清楚在哪里找到它的定义 -- 相关代码可能分布在多个模块中。

每当你在程序中不确定执行流程时，最简单的解决方案是在相关方法的开头添加 print 语句。如果一个方法打印类似"Running Deck.shuffle"的消息，那么随着程序运行，它会跟踪执行流程。

## 术语表

**继承：**
定义一个新类作为先前定义的类的修改版本的能力。

**编码：**
通过在两组值之间构建映射来用一组值表示另一组值。

**类变量：**
在类定义内部定义但不在任何方法内部的变量。在 Auto 中，这些是与类型关联的模块级变量。

**全序：**
如果可以比较任何两个元素且结果一致，则一组对象是全序的。

**委托：**
当一个方法将大部分或全部工作传递给另一个方法时。

**父类：**
被继承的类。

**子类：**
从另一个类继承的类。

**特化：**
使用继承创建一个作为现有类的特化版本的新类的方式。

## 练习

### 练习

在合约桥牌中，"一墩"是每个玩家各出一张牌的一轮比赛。编写一个 `Trick` 方法 `find_winner`，遍历 `Trick`（继承自 `Deck`）中的牌并返回获胜牌的索引。赢家是"领出花色"（第一张打出的牌的花色）中最大的牌。

### 练习

编写一个 `PokerHand` 方法 `has_flush`，检查手牌是否有"同花" -- 即是否包含至少五张相同花色的牌。

### 练习

编写一个 `PokerHand` 方法 `has_straight`，检查手牌是否包含"顺子"，即五张点数连续的牌。记住 A 可以是高（14）或低（1），但顺子不能"环绕"（K、A、2、3、4 不是顺子）。

### 练习

编写一个 `PokerHand` 方法 `has_pair`，检查手牌是否包含两张或更多相同点数的牌。
