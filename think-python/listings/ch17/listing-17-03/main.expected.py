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
