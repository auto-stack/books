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
