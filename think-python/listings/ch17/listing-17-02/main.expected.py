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
