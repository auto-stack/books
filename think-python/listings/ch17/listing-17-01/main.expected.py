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
