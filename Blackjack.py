#importing module
import random

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
#value of Jack, Queen and King is 10
#value of Ace is 11(another special rule ahead)
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

playing = True
#the card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'
#the deck creation
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return f'The deck has: {deck_comp}'
    #shuffle the cards
    def shuffle(self):
        random.shuffle(self.deck)
    #pop one card from deck
    def deal_one(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0 
    #adding one card to the hand
    def add_cards(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1
    #the ace special rule
    def adjust_for_ace(self):
        while self.value > 21 and self.aces: #accounting for boolean value of zero
            self.value -= 10
            self.aces -= 1
#betting chips
class Chips:
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0
    #winning reward
    def win_bet(self):
        self.total += self.bet
    #losing consequences
    def lose_bet(self):
        self.total -= self.bet
#taking bet
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, you do not have enough chips! You have {chips.total}")
            else:
                break
#picking one card from the deck
def hit(deck, hand):
    single_card = deck.deal_one()
    hand.add_cards(single_card)
    hand.adjust_for_ace()
#deciding whether to hit or stand
def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("Hit or Stand? Enter h or s: ")
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print("Sorry I did not understand that, Please enter h or s only!")
            continue
        break
#showing value of cards, hiding one dealer card
def show_some(player, dealer):
    print('\n')
    print('DEALERS HAND:')
    print('one card hidden!')
    print(dealer.cards[1])
    print('PLAYERS HAND:')
    for card in player.cards:
        print(card)
    print('\n')
#showing value of all cards
def show_all(player, dealer):
    print('\n')
    print('DEALERS HAND:')
    for card in dealer.cards:
        print(card)
    print('PLAYERS CARDS:')
    for card in player.cards:
        print(card)
    print('\n')
#if player busts, exceeds 21
def player_bust(player, dealer, chips):
    print('BUST PLAYER')
    chips.lose_bet()
#if player wins
def player_wins(player, dealer, chips):
    print('PLAYER WINS')
    chips.win_bet()
#if dealer busts, goes beyond 21
def dealer_busts(player, dealer, chips):
    print('PLAYER WINS! DEALER BUSTED!')
    chips.win_bet()
#if dealer wins
def dealer_wins(player, dealer, chips):
    print('DEALER WINS!')
    chips.lose_bet()
#if player and dealer tie   
def push(player, dealer):
    print('Dealer and player tie! PUSH')
#main play
while True:
    print("WELCOME TO BLACKJACK")
    #creating the deck
    deck = Deck()
    deck.shuffle()
    #giving player two cards from deck
    player_hand = Hand()
    player_hand.add_cards(deck.deal_one())
    player_hand.add_cards(deck.deal_one())
    #giving dealer two cards from deck
    dealer_hand = Hand()
    dealer_hand.add_cards(deck.deal_one())
    dealer_hand.add_cards(deck.deal_one())
    #initialising betting chips
    player_chips = Chips()
    take_bet(player_chips)
    #showing cards, one dealer card hidden
    show_some(player_hand, dealer_hand)
    #game logic
    while playing:
        #player can choose btn hitting and standing
        hit_or_stand(deck, player_hand)
        
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            #dealer has to hit
            hit(deck, dealer_hand)
        #showing all cards  
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    #showing chip balance after play
    print(f'\nPlayer total chips are at: {player_chips.total}')
    #prompting player for another game
    new_game = input('Would you like to play another hand? y/n: ')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing')
        break
