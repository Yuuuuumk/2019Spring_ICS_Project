
from Card import *
from random import shuffle


class Deck(list):
    """Represents a deck of playing cards."""

    def __init__(self, cls=Card):
        """Initialize a deck of 52 cards."""
        list.__init__(self, [cls(i) for i in range(52)])


    def shuffle(self):
        """Shuffle the deck."""
        shuffle(self)


    def deal(self, *args):
        """Removes the ﬁrst n Card objects from the deck and returns them in a list."""

        if len(args) == 1 and isinstance(args[0], int):
            num_cards = args[0]
            return [self.pop(0) for i in range(num_cards)]
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            num_cards = args[0]
            num_hands = args[1]
            hands = [ ]

            # Initiate however many hands specified in the argument
            for hand in range(num_hands):
                hands.append([ ])

            # Deal one card at a time to each hand
            for card in range(num_cards):
                for hand in range(num_hands):
                    hands[hand].append(self.pop(0))

            return hands
        else:
            raise ValueError("deal() only handles a maximum of two arguments in the form of integers")


    def restore(self, a):
        """Add a list of Card objects to the end of the deck.

        Args:
            a: An array (or list) of Card objects.

        Returns:
            Nothing.
        """

        # Verify that every element in a is a Card object.
        for element in a:
            if not isinstance(element, Card):
                raise ValueError("We can only restore a list of Card objects onto the original deck.")
        self += a

    def append(self, card):
        """Append a Card object.

        Args:
            card: A Card object.

        Returns:
            Nothing.
        """
        if not isinstance(card, Card):
            raise ValueError("We can only append Card objects onto the deck.")
        self.append(card)


class PinochleDeck(Deck):

    def __init__(self):
        """Initialize a deck of 52 pinochle cards."""

        p_deck = []

        for i in range(52):
            # We only want 9's and above i.e. 9, 10, J, Q, K, A
            if i % 13 >= 7:
                # We want two copies of each card, so append twice
                p_deck.append(Card(i))
                p_deck.append(Card(i))

        list.__init__(self, p_deck)
