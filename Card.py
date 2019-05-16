
from random import sample

class Card:
    """Represents a playing card"""

    ranks = { 0:2, 1:3, 2:4, 3:5, 4:6, 5:7, 6:8, 7:9, 8:10, 9:'J', 10:'Q', 11:'K', 12:'A'}

    rank_value = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, '10':8, 'J':9, 'Q':10, 'K':11, 'A':12}

    suits = {
        0:'\u2663',  # Clubs
        1:'\u2666',  # Diamonds
        2:'\u2665',  # Hearts
        3:'\u2660'   # Spades
        }

    suit_value = {
        '\u2663':0,  # Clubs
        '\u2666':1,  # Diamonds
        '\u2665':2,  # Hearts
        '\u2660':3   # Spades
        }


    def __init__(self, *args):
        """Construct a Card object by passing either an id number or rank and suit"""
        if len(args) == 1:
            if args[0] not in range(54):
                raise ValueError("Card id must be between 0 and 51")
            self.id = args[0]
        elif len(args) == 2:
            if args[0] not in Card.rank_value or args[1] not in Card.suit_value:
                raise ValueError("Invalid card")
            # r denotes remainder, while q denotes quotient
            r = Card.rank_value[args[0]]
            q = Card.suit_value[args[1]]

            self.id = (13 * q) + r
        else:
            raise Exception("Usage: Card(id) or Card(rank, suit)")


    def rank(self):
        """Return rank."""
        return self.id % 13


    def suit(self):
        """Return suit."""
        return self.id // 13


    def points(self):
        """Return points."""
        if 9 <= self.rank() <= 12:
            return self.rank() - 8
        else:
            return 0


    def __repr__(self):
        """Return formal representation of a Card object."""
        return "{}{}".format(Card.ranks[self.rank()], Card.suits[self.suit()])


    def __lt__(self, other):
        """Compare cards.

        Args:
            other: Other card.

        Returns:
            True iff this card's id (self) comes before the other card's id.
        """
        return self.id < other.id


class BlackjackCard(Card):
    """Subclass of Card.  Represents properties of a Blackjack game."""

    def points(self):
        """Return points."""
        if self.rank() == 12:
            return 11
        if 9 <= self.rank() <= 11:
            return 10
        else:
            return Card.ranks[self.rank()]


    def __lt__(self, other):
        """Compare cards.

        Args:
            other: Other card.

        Returns:
            True iff this card's rank (self) is lower than the other card's rank.
        """
        return self.rank() < other.rank()


def points(li):
    """Takes a list of cards and return the sum of the point values of the cards.

    Args:
        li: A list of Card objects.

    Returns:
        The sum of the point values of the cards.
    """
    return sum([i.points() for i in li])


def new_deck(type=Card):
    """Creates a list of card objects of a speciﬁed class.

    Args:
        type: Name of the class that speciﬁes which type of card to make.
        The default type is the class Card.

    Returns:
        A list of card objects of a specified class.
    """
    return [type(i) for i in range(52)]
