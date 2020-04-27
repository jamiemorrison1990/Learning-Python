'''
Running this should enable you to play Blackjack 
with the computer as the dealer

You will be able to give your name and change your stake
and decide whether to stick or twist with each card.

You will not be able to split or double down.

We'll start be defining what we need, and then run them
in a manner that plays the game.
'''
# Importing random so we can shuffle
import random

# Importing clear_output so we can get rid of the output at appropriate times
from IPython.display import clear_output

# Creating an Account class that we'll use to track the player's balance as they
# progress, and also to take from/deposit to when they make/win their bets
class Account:
    
    # creating an instance of an account with an owner and a balance. Default balance is 0
    def __init__(self, owner, balance = 0):
        '''
        Inits an Account with an owner (which we expect to be a string) and a balance (integer, default value 0).
        '''
        self.owner = owner
        self.balance = balance
    
    # Create a method to add money to the account. This method adds money to the existing balance
    # We'll call this when the player draws with the dealer (to return their stake), and when they
    # win to give them their winnings.
    def deposit(self, deposit_amount):
        '''
        Method to increase the balance of an Account by the deposit_amount.
        '''
        self.balance = self.balance + deposit_amount
        
    # Create a method to bet money. Two cases: where there is and is not enough money to cover bet
    # If there is enough money, then balance is updated to new amount and tell them it was successful
    # If there is not enough money, then tell them there wasn't enough money
    def bet(self, bet_amount):
        '''
        Method to bet bet_amount from the account, if the current balance is sufficient. Otherwise explains why.
        '''
        if bet_amount <= self.balance:
            self.balance = self.balance - bet_amount
            print('£' + str(bet_amount) + ' bet accepted')
        else:
            print('Balance not high enough to allow £' + str(bet_amount) + ' bet')

# Simple function to ask for a player's name.
def ask_player_name():
    '''
    Requests a name from the player and returns it as a string.
    '''
    return input("Enter your name")

# Simple function to get a player's first deposit. Need to make sure it's an integer amount.
def ask_initial_deposit():
    '''
    Requests an initial deposit amount from the player and returns it as an integer.
    '''
    while True:
        try:
            val = int(input("How much would you like to deposit?"))
        except:
            print("We only accept integer amounts!")
            continue
        else:
            print("Deposit accepted")
            break
    return val

# A function to allow the player to set their stake for the next hand of blackjack. Needs to be an integer
def set_stake():
    '''
    Asks the user how much they would like to bet, verifies they can bet that amount, and returns it as an integer.
    '''
    while True:
        try:
            val = int(input("How much would you like to bet?"))
        except:
            print("You must enter an integer value to bet")
            continue
        else:
            if val <= player_account.balance:
                player_account.bet(val)
                break
            else:
                print("Your balance is £" + str(player_account.balance) + ", try again with a smaller amount.")
    return val


'''
Now we want to make a dictionary to assign cards (and their values in blackjack) to integers. I've done this 
in two stages. Firstly a mapping from the integers 0-3 (inclusive) to the suits, and secondly a mapping from
the integers 0-11 (inclusive) to 2-A. Using the floor and mod functions, we can then map the integers 0-51
to cards in a deck
'''

SuitDictionary = {0:'clubs', 1:'diamonds', 2:'hearts', 3:'spades'}

CardValueDictionary = {}
'''
This maps the integers 0-51 to tuples of the form (card as string, suit as integer, card value as integer)
'''
for i in range(0,52):
    if (i//4) + 2 == 11:
        CardValueDictionary[i] = ('J', i%4, 10)
    elif (i//4) + 2 == 12:
        CardValueDictionary[i] = ('Q', i%4, 10)
    elif (i//4) + 2 == 13:
        CardValueDictionary[i] = ('K', i%4, 10)
    elif (i//4) + 2 == 14:
        CardValueDictionary[i] = ('A', i%4, 11)
    else:
        CardValueDictionary[i] = (str((i//4)+2), i%4, (i//4)+2)
        
CardDictionary = {}
'''
This just combines the two dictionaries, so now we have a Dictionary mapping the integers 0-51 to tuples of the form
(card as string, suit as string, card value as integer). Now we can easily look up an integer and get the playing 
card it maps to (card and suit) and its value in blackjack from a single Dictionary.
'''
for x in CardValueDictionary:
    CardDictionary[x] = (CardValueDictionary[x][0], SuitDictionary[CardValueDictionary[x][1]], CardValueDictionary[x][2])  

'''
Simple function to provice us with a shuffled 'deck' of integers. We can then look up these integers in CardDictionary
to actually use them to play blackjack with
'''
def deck_shuffle():
    '''
    Outputs a shuffled 'deck' in the form of a randomised list of the integers 0-51 (inclusive).
    '''
    global deck
    deck = []
    for i in range(0,52):
        deck.append(i)
    random.shuffle(deck)

'''
Function to make the initial deal to the player and the dealer. Here I'm 'popping off' the first card in the shuffled
deck to the player and then to the dealer (it technically doesn't matter, as they're randomised, but I preferred to
keep the image of the cards being dealt)
'''
def initial_deal():
    '''
    Output is two lists (player_hand and dealer_hand) that have the first 'cards' (in the form of integers) that the player and dealer are dealt. 
	Need to use CardDictionary to map them back to playing cards.
	'''
    global player_hand
    global dealer_hand
    player_hand = [deck.pop(0)]
    dealer_hand = [deck.pop(0)]
    player_hand.append(deck.pop(0))
    dealer_hand.append(deck.pop(0))

'''
Function to output the player's hand in the form e.g. 'A of spades'
'''
def display_player_hand():
    '''
    Prints out the player's hand.
    '''
    print("Your hand is:")
    for card in player_hand:
        print(CardDictionary[card][0] + ' of ' + CardDictionary[card][1])

'''
Function to calculate the player's maximum current score (taking into account that A can count as 1 or 11, but is the only card that can be 11)
'''
def calculate_player_score():
    '''
    Output is the best score the player can get from the cards they have, returned as an integer player_score.
    '''
    player_card_values = []
    for x in player_hand:
        player_card_values.append(CardDictionary[x][2])
    number_of_aces = player_card_values.count(11)
    score_without_ace_adjustment = sum(player_card_values)
    global player_score
    if score_without_ace_adjustment <= 21:
        player_score = score_without_ace_adjustment
    elif number_of_aces == 0:
        # if the player's score is over 21 and they have no aces, they must be bust. For all subsequent conditions, the player has at least one A, so they have a chance to adjust their score
        player_score = 'BUST'
    elif number_of_aces >= 1 and score_without_ace_adjustment <= 31:
        # if the player's score is between 22 and 31 and they have at least one A, they can make one of them count as 1 instead of 11 (reducing the total by 10)
        player_score = score_without_ace_adjustment - 10
    elif number_of_aces >= 2 and score_without_ace_adjustment <= 41:
        # if the player's score is between 32 and 41 and they have at least two As, they can make two of them count as 1 instead of 11 (reducing their total by 20)
        player_score = score_without_ace_adjustment - 20
    elif number_of_aces >= 3 and score_without_ace_adjustment <= 51:
        # if the player's score is between 42 and 51 and they have at least three As, they can make three of them count as 1 instead of 11 (reducing their total by 30)
        player_score = score_without_ace_adjustment - 30
    elif number_of_aces == 4 and score_without_ace_adjustment <= 61:
        # if they player's score is between 52 and 61 and they have four As, they can make them all count as 1 instead of 11 (reducing their total by 40)
        player_score = score_without_ace_adjustment - 40
    else:
        # if the player does have at least one A but none of these conditions are met, they would still be bust even if they counted all their As as 1. Therefore they are bust
        player_score = 'BUST'
    return player_score


# Function to deal another card to the player (to be used if they ask for it)
def hit_player():
    '''
    Output is an additional integer moved from the 'deck' to 'player_hand'.
    '''
    global player_hand
    player_hand.append(deck.pop(0))

# Function to use the dictionay to output the player's hand in the form e.g. 'A of spades'
def display_dealer_hand():
    '''
    Prints out the dealer's hand.
    '''
    print("Dealer's hand is the")
    for card in dealer_hand:
        print(CardDictionary[card][0] + ' of ' + CardDictionary[card][1])

# Like calculate_player_score() but for the dealer instead
def calculate_dealer_score():
    '''
    Output is the best score the dealer can get from the cards they have, returned as an integer dealer_score.
    '''
    dealer_card_values = []
    for x in dealer_hand:
        dealer_card_values.append(CardDictionary[x][2])
    number_of_aces = dealer_card_values.count(11)
    score_without_ace_adjustment = sum(dealer_card_values)
    global dealer_score
    if score_without_ace_adjustment <= 21:
        dealer_score = score_without_ace_adjustment
    elif number_of_aces == 0:
        dealer_score = 'BUST'
    elif number_of_aces >= 1 and score_without_ace_adjustment <= 31:
        dealer_score = score_without_ace_adjustment - 10
    elif number_of_aces >= 2 and score_without_ace_adjustment <= 41:
        dealer_score = score_without_ace_adjustment - 20
    elif number_of_aces >= 3 and score_without_ace_adjustment <= 51:
        dealer_score = score_without_ace_adjustment - 30
    elif number_of_aces == 4 and score_without_ace_adjustment <= 61:
        dealer_score = score_without_ace_adjustment - 40
    else:
        dealer_score = 'BUST'
    return dealer_score

# Function to deal an additional card to the dealer if they need it
def hit_dealer():
    '''
    Output is an additional integer moved from the 'deck' to 'dealer_hand'.
    '''
    global dealer_hand
    dealer_hand.append(deck.pop(0))

# Function to use the dictionary to print out just the dealer's first card, which is visible immediately
def display_dealer_shown_card():
    '''
    Output is a string telling us what the dealer's first card is.
    '''
    print("Dealer's shown card is " + CardDictionary[dealer_hand[0]][0] + ' of ' + CardDictionary[dealer_hand[0]][1])

# Function to call when it is the player's turn to make decisions. Tell them their score, ask if they want to stick or hit. If hit, give them another card, and recalculate their score (e.g. A could change to a 1). Then ask again until the player is bust or they stick on <= 21.
def player_turn():
    '''
    Function to call when it is the player's turn. When function reaches end, player's turn is over.

    Two possible outcomes: either the player is bust, in which case the hand is over, or the player has 'stuck' on <= 21, in which case it is the dealer's turn to try to equal or better their score.
    '''
    stick_or_hit = '' #included this so that I can reason about it in the while condition
    while player_score != 'BUST' and stick_or_hit.upper() != 'S':
        stick_or_hit = input("Your score is " + str(player_score) + ", would you like to Hit (H) or Stick (S)? ")
        if stick_or_hit.upper() == 'H':
            print("Player hits")
            hit_player()
            print("Player receives the " + CardDictionary[player_hand[-1]][0] + " of " + CardDictionary[player_hand[-1]][1])
            calculate_player_score()
        elif stick_or_hit.upper() == 'S':
            print("Player sticks on " + str(player_score) + ". Dealer's turn.")
        else:
            stick_or_hit = input("Try agan; Hit (H) or Stick (S)?")

''' 
Function to call when it is the dealer's turn. If it is the dealer's turn, it means the player must have stuck on a score <= 21 (because otherwise they would be bust and the player woul have lost).
Logicaly, we first show the dealer's full hand (up until now we've only shown their first card), and calculate their score. Then as long as the dealer has a score lower than the player, they will 
draw another card to try to beat/draw with the player. This ends when the dealer is bust (player wins, receives their stake back and the same again in winnings), the dealer and the player have the 
same score (draw; player receives their stake back), or when the dealer has a score closer to 21 than the player (dealer wins; player does not receive any money back).
''' 
def dealer_turn():
    '''
    Function to call when it is the dealer's turn. When function reaches end, the hand is over, we have got a winner (or draw), and we have paid the player if necessary.
    '''
    display_dealer_hand()
    calculate_dealer_score()
    print("Dealer's score is " + str(dealer_score))
    try:
        while dealer_score < player_score <= 21:
            print("Dealer draws extra card")
            hit_dealer()
            calculate_dealer_score()
            print("Dealer receives the " + CardDictionary[dealer_hand[-1]][0] + " of " + CardDictionary[dealer_hand[-1]][1] + ". Dealer score is now " + str(dealer_score))
        if dealer_score == player_score <= 21:
            print("Hand is a tie. Bets returned")
            player_account.deposit(stake)
        elif player_score < dealer_score <= 21:
            print("Dealer has won. Bet is lost")
    except:
        if dealer_score == 'BUST':
            print("Dealer is bust. Player has won")
            player_account.deposit(stake*2)

'''
A function to call to see if the player wants to play another hand
'''
def replay():
    '''
    Asks the user if they want to play again, and returns True if they do, and False if they don't.
    '''
    play_again = input("Would you like to play again? (Y/N)")
    while not (play_again.upper() == 'Y' or play_again.upper() == 'N'):
        play_again = input("Enter 'Y' to play again, or 'N' to end the game")
    if play_again.upper() == 'Y':
        return True
    else:
        return False

'''
Now just need to call these functions in the right order and we have a game of blackjack!
'''

print("Welome to blackjack")
player_account = Account(ask_player_name(), ask_initial_deposit())
while True:
    clear_output()
    print("Your balance is £" + str(player_account.balance))
    stake = set_stake()
    deck_shuffle()
    initial_deal()
    display_player_hand()
    calculate_player_score()
    display_dealer_shown_card()
    player_turn()
    if player_score == 'BUST':
        print("Player is bust. Bet lost.")
    else:
        dealer_turn()
    if player_account.balance == 0:
        print("Game over. You have run out of money.")
        break
    elif not replay():
        print("Player leaves with £" + str(player_account.balance) + " remaining.")
        break
