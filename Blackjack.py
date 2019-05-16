

from tkinter import *
from tkinter.messagebox import showinfo
from CardLabel import *
from Deck import *

###############################################################################################################

# Note that total(hands) will calculate points based on the BlackjackCard points system
# Deck() now has and optional argument to specify class
deck = Deck(BlackjackCard)

# Dealer and player hands
dealer = [ ]
player = [ ]

# Score tally
dwin_score = 0
pwin_score = 0

###############################################################################################################

def reset():
    """Reset window for a new game."""
    global dealer, player

    deck.restore(dealer)
    dealer = [ ]
    deck.restore(player)
    player = [ ]

    for card in range(6):
        dealer_label[card].display('blank')
        player_label[card].display('blank')


def new_game():
    """Reset button states."""
    hit_button.config(state='disabled')
    pass_button.config(state='disabled')
    deal_button.config(state='normal')


def dealerwins():
    """Show a message when dealer wins.  Add 1 point to dwin_score."""
    global dwin_score
    showinfo(message = 'You lose! Better luck next time.')
    new_game()
    dwin_score += 1
    dealer_win.config(text = 'dealer wins: {}'.format(dwin_score))


def playerwins():
    """Show a message when player wins.  Add 1 point to pwin_score."""
    global pwin_score
    showinfo(message = 'You win! Winner winner chicken dinner!')
    new_game()
    pwin_score += 1
    player_win.config(text = 'player wins: {}'.format(pwin_score))


def tiegame():
    """Show a message when there is a tie."""
    showinfo(message = 'Tie game!')
    new_game()


def total(hand):
    """Compute total number of points for a hand in Blackjack."""
    num_aces = 0

    # Sum up the values of cards in the hand
    result = points(hand)

    # Also sum up the number of aces
    for card in hand:
        if card.rank() == 12:
            num_aces += 1

    # While value of hand is > 21 and there is an ace in the hand with value 11,
    # convert its value to 1
    while result > 21 and num_aces > 0:
        result -= 10
        num_aces -= 1

    return result


def debug():
    print("dealer hand =", dealer)
    print("player hand =", player)
    print("dealer score =", total(dealer))
    print("player score =", total(player))


def deal():
    """Shuffle a deck of cards, then deals 2 cards to the dealer (one face down
    and one face up) and 2 cards to the player (both face down)."""
    global dealer, player

    reset()
    deck.shuffle()

    # Add the cards to the dealer's/player's hand as they are dealt
    dealer += deck.deal(2)
    player += deck.deal(2)

    dealer_label[0].display('back', dealer[0].id)
    dealer_label[1].display('front', dealer[1].id)
    player_label[0].display('front', player[0].id)
    player_label[1].display('front', player[1].id)

    hit_button.config(state='normal')
    pass_button.config(state='normal')
    deal_button.config(state='disabled')

    if total(player) == 21:
        playerwins()

    elif total(dealer) == 21:
        dealerwins()

    # debug()


def hit():
    """Turn over the next card in the bottom row and update
    the player's score."""
    global player

    card_index = len(player)

    player += deck.deal(1)

    player_label[card_index].display('front', player[-1].id)

    if total(player) > 21:
        dealerwins()

    elif total(player) == 21:
        playerwins()

    # debug()


def card_pass():
    """Turn over the dealer's hidden card and compute the total points for
    the cards in the dealer's row."""
    global dealer, player

    dealer_label[0].display('front', dealer[0].id)

    while total(dealer) < 17:

        card_index = len(dealer)
        dealer += deck.deal(1)
        dealer_label[card_index].display('front', dealer[-1].id)

    if total(dealer) > 21:
        playerwins()

    elif total(dealer) > total(player):
        dealerwins()

    elif total(dealer) < total(player):
        playerwins()

    elif total(dealer) == total(player):
        tiegame()

    # debug()

###############################################################################################################

root = Tk()
CardLabel.load_images()  # Call after creating top level app

###############################################################################################################

# Card labels
dealer_label = [0]*6
player_label = [0]*6

for card in range(6):

    # Create labels for dealer
    dealer_label[card] = CardLabel(root)
    dealer_label[card].grid(row=0, column=card, padx=10, pady=10)
    dealer_label[card].display('blank')

    # Create labels for player
    player_label[card] = CardLabel(root)
    player_label[card].grid(row=1, column=card, padx=10, pady=10)
    player_label[card].display('blank')

###############################################################################################################

# Score update label
dealer_win = Label(root, text='Dealer\'s score:  ')
dealer_win.grid(row=0, column=6, sticky=W, padx=20, pady=10)

player_win = Label(root, text='Player\'s score:  ')
player_win.grid(row=1, column=6, sticky=W, padx=20, pady=10)

###############################################################################################################

# Control buttons
deal_button = Button(root, text='Deal', command=deal)
deal_button.grid(row=2, column=0, columnspan=2, pady=10)

hit_button = Button(root, text='Hit', state='disabled', command=hit)
hit_button.grid(row=2, column=2, columnspan=2, pady=10)

pass_button = Button(root, text='Pass', state='disabled', command=card_pass)
pass_button.grid(row=2, column=4, columnspan=2, pady=10)

###############################################################################################################

# Note the grid is part of the parent
root.rowconfigure(0, minsize=115)
root.columnconfigure(0, minsize=85)


if __name__ == '__main__':
    root.mainloop()
