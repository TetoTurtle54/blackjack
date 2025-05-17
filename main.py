import pygame, random

"""
PROJECT: Make Blackjack in Pygame

FUNDAMENTALS OF BLACKJACK:
Player and Dealer play with a standard deck of 52 playing cards.
The goal for the player is to reach or get as close to the total of the cards in their hand adding up to 21 without going over.
(Suit doesn't really matter so it will be easier on me to code them without suits, but I might have to later.)

CARDS:
Numbered cards 2 - 10 are worth their face value.
There are 4 of every numbered card in the deck, so there are 36 numbered cards.
Aces are worth 1 or 11 and are interchangable based what benefits the player, there are 4 Aces in the deck.
Face cards are worth 10 points, there are 12 face cards in the deck.
36 numbered + 4 Aces + 12 face = 52 cards
(Unlike TwentyOne, I NEED to code a proper deck this time.)


GAMEPLAY:
At the start of the game, the player places their bet, and the player and the dealer both recieve 2 cards.
The first card the dealer draws is hidden from the player. This is known as the hole card, and is revealed at the end of the round.
(If the dealer's 2nd card is an Ace, they must immediately check the hole card for a Blackjack. If a Blackjack is present, push.)

Player Actions:

HIT - Draw another card.
STAND - Keep your current hand.
DOUBLE DOWN - Double your bet and HIT for the last time before STANDing.
SPLIT - [not implementing right now]
FORFEIT - Fold and collect half of your bet. (If played bet is 1, collect no bet.)

Dealer Actions:

Once the player STANDs, the dealer will HIT until the total of their cards reaches at least 17.


GAME OUTCOMES:

2:1 Payout (Pays 2:1, so if I bet 200, I get back 400. My bet times 2.)
3:2 Payout (Pays 3:1, so if I bet 200, I get back 500. My bet plus my bet times (3/2).)

Player Wins:
If the player's hand is closer to 21 than the Dealer, the player wins a payout of 2:1.
If the player's hand is 21, they Blackjack, and win a payout of 3:2.
If the dealer busts, the player wins a payout of 2:1.

Player Loses:
If the player's hand is farther from 21 than the Dealer, they lose their bet.
If the player busts, they lose their bet.
If the player FORFEITs, they recieve half of their bet.

Player Pushes:
If the player and Dealer tie, they push and the player recieves their bet back.
If the Dealer immediately Blackjacks, they push and the player recieves their bet back.

"""

"""
TODO:

code end screen

code bet system

code starting a new round


"""

# test for git
# push to master
# push from origin
# git push -u master origin

# init pygame
pygame.init()

# create a display surface
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Blackjack!")

# set FPS and make a clock
FPS = 60
clock = pygame.time.Clock()

# variables
# CONSTANTS
GREEN = ((38, 182, 128))


# variables

# wow this is empty



# load fonts



# load game text



# load music and sounds

# *tumbleweed rolls by*

# load images




# CARD STUFF AHEAD
# create the deck to choose from






class CardNG(pygame.sprite.Sprite):
    """This class is for cards initializing"""
    def __init__(self, suit, rank):
        super().__init__()
        self.suit = suit
        self.rank = rank
    
    def tellRank(self):
        return f"{self.rank} of {self.suit}"


# create graphical card class
class Card(pygame.sprite.Sprite):
    """This is a class for cards that are graphical."""
    def __init__(self, rank, suit, x, y, hidden):
        super().__init__()
        if hidden:
            self.image = pygame.transform.scale_by(pygame.image.load(f"cards/hidden_card.png"), 0.2)
        else:
            self.image = pygame.transform.scale_by(pygame.image.load(f"cards/{rank}_of_{suit}.png"), 0.2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# create Game class
class Game:
    """This is the main game class."""
    def __init__(self, card_group):
        self.card_group = card_group
        self.font = pygame.font.Font("game_font.ttf", 60) # GAMBA FONT!!
        self.deck = self.make_deck() # make the deck
        self.round_start(100) # start round with bet of 100
        self.frame_count = 0 # why do i have this again?
        self.DEALER_DRAW_TIMER = pygame.USEREVENT + 1 # timer for when the dealer draws cards
        self.round_over = False # round over
        

    def make_deck(self) -> list:
        """Make the deck of cards to draw from"""
        self.suits = ["spades","diamonds","hearts","clubs"] # establish suits
        self.deck = [] # create deck

        # make the deck
        for suit in self.suits:
            for i in range(1): # lol
                self.deck.append(CardNG(suit, "ace"))
                self.deck.append(CardNG(suit, "king"))
                self.deck.append(CardNG(suit, "queen"))
                self.deck.append(CardNG(suit, "jack"))
                for j in range(10,1,-1):
                    self.deck.append(CardNG(suit, j))
        
        return self.deck
    
    def count_card_total(self, hand: list, hidden_dealer: bool):
        """Count the cards for the given hand, and hide the hidden card if bool is true"""
        total = 0
        hidden_total = 0
        for i, card in enumerate(hand):
            if i == 0 and hand == self.dealer_hand: # if its the first card and the dealer hand is being counted..
                if card.rank == "king" or card.rank == "queen" or card.rank == "jack":
                    hidden_total += 10
                if card.rank == "ace":
                    hidden_total += 1
                for i in range(10,1,-1):
                    if card.rank == i:
                        hidden_total += i
            else:
                if card.rank == "king" or card.rank == "queen" or card.rank == "jack":
                    hidden_total += 10
                    total += 10
                if card.rank == "ace":
                    hidden_total += 1
                    total += 1
                for i in range(10,1,-1):
                    if card.rank == i:
                        hidden_total += i
                        total += i
        
        if hand == self.dealer_hand and hidden_dealer:
            return f"{total} + ?"
        elif not hidden_dealer and hand == self.dealer_hand:
            return hidden_total
        else:
            return total
        

    def draw_card(self, target_hand: list, deck: list):
        """draw a card to the target_hand from the given deck, then remove that card from the deck"""
        global player_stand # AHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        self.deck = deck
        if len(self.deck) == 0:
            print("No More Cards") # this still crashes, lol
            # self.deck_empty()
        card_drawn = random.choice(self.deck)
        self.deck.remove(card_drawn)
        target_hand.append(card_drawn)
        if self.round_started:
            #print(f'player: {self.count_card_total(self.hand, False)}')
            #print(f'dealer: {self.count_card_total(self.dealer_hand, True)}')
            self.player_card_total = self.count_card_total(self.hand, False)
            if not player_stand:
                self.dealer_card_total = self.count_card_total(self.dealer_hand, True)
            else:
                self.dealer_card_total = self.count_card_total(self.dealer_hand, False)
            self.draw_result = self.parse_score((self.player_card_total, self.dealer_card_total))
        return self.draw_result # why am i returning this again??
        

    def round_start(self, bet):
        """Start the round, giving 2 cards to both the player and dealer"""
        self.round_started = True
        self.hand = []
        self.dealer_hand = []
        self.draw_card(self.hand, self.deck)
        self.draw_card(self.dealer_hand, self.deck)
        self.draw_card(self.hand, self.deck)
        self.draw_card(self.dealer_hand, self.deck)
        print(self.count_card_total(self.hand, False))
        print(self.count_card_total(self.dealer_hand, True))
    
    def display_cards(self, dealer_turn):
        card_group.empty() 
        x_pos_d = 280
        x_pos_p = 280
        for num, card in enumerate(self.dealer_hand):
            x_pos_d += 300 // len(self.dealer_hand) * 2 # this looks weird, but it works!
            if not dealer_turn:
                if num == 0:
                    current_card = Card(card.rank, card.suit, x_pos_d, 200, True)
                    card_group.add(current_card)
                else:
                    current_card = Card(card.rank, card.suit, x_pos_d, 200, False)
                    card_group.add(current_card)
            if dealer_turn:
                current_card = Card(card.rank, card.suit, x_pos_d, 200, False)
                card_group.add(current_card)
            
        
        for num, card in enumerate(self.hand):
            x_pos_p += 300 // len(self.hand) * 2 # this looks weird, but it works!
            current_card = Card(card.rank, card.suit, x_pos_p, 500, False)
            card_group.add(current_card)
    
    def display_gui(self, card_totals, round_over):
        global result # Bad Practice!!
        player_total = card_totals[0]
        dealer_total = card_totals[1]

        if player_total > 21: # put one for dealer too
            score_color = (200,0,0)
        else:
            score_color = (210, 210, 210)

        pygame.draw.line(display_surface, (230,230,230), (950, 0), (950, WINDOW_HEIGHT), 3)
        pygame.draw.rect(display_surface, (0, 134, 72), (950, 0, WINDOW_WIDTH-950, WINDOW_HEIGHT))
        title_gui = self.font.render(f"BLACKJACK", True, (15,15,15)) # is it "goo-ey" or "gee-you-i"
        title_rect = title_gui.get_rect()
        title_rect.center = (1110, 80)

        player_gui_1 = self.font.render(f"PLAYER:", True, (210,210,210))
        player_gui_1_rect = player_gui_1.get_rect()
        player_gui_1_rect.center = (1100, 450)

        player_gui_2 = self.font.render(f"{player_total} / 21", True, score_color)
        player_gui_2_rect = player_gui_2.get_rect()
        player_gui_2_rect.center = (1100, 500)

        dealer_gui_1 = self.font.render(f"DEALER:", True, (210, 210, 210))
        dealer_gui_1_rect = dealer_gui_1.get_rect()
        dealer_gui_1_rect.center = (1100, 140)

        dealer_gui_2 = self.font.render(f"{dealer_total} / 21", True, score_color)
        dealer_gui_2_rect = dealer_gui_2.get_rect()
        dealer_gui_2_rect.center = (1100, 190)


        
        display_surface.blit(title_gui, title_rect)
        display_surface.blit(player_gui_1, player_gui_1_rect)
        display_surface.blit(player_gui_2, player_gui_2_rect)
        display_surface.blit(dealer_gui_1, dealer_gui_1_rect)
        display_surface.blit(dealer_gui_2, dealer_gui_2_rect)

        if round_over: # currently where I'm at, I HATE ALIGNING THINGS
            pygame.draw.rect(display_surface, (170,170,170), (200,200,WINDOW_WIDTH-400, WINDOW_HEIGHT-400))
            pygame.draw.rect(display_surface, (0,0,0), (200,200,WINDOW_WIDTH-400, WINDOW_HEIGHT-400), 3)
    
    def parse_score(self, card_totals):
        pass # need to rewrite (are you sure?)
    
    def dealer_turn(self):
        """function for the dealer's turn (THIS IS SO MESSY IM SORRY SUNSHINE)"""
        true_dealer_total = self.count_card_total(self.dealer_hand, False)
        self.dealer_card_total = true_dealer_total
        old_frame = self.frame_count # what am i even keeping this for??
        if int(true_dealer_total) < 17:
            pygame.time.set_timer(self.DEALER_DRAW_TIMER, 900)
            print(self.dealer_card_total)
        else:
            self.round_over = True # I NEED TO DO SOMETHING WITH THIS BUT WHAT I DONT KNOW



        


            
    
    def update(self):
        """update a bunch of stuff"""
        global player_stand # bad practice!!!!! 
        self.frame_count += 1 # what are you doing?????
        if not player_stand:
            self.display_cards(False)
        if player_stand:
            self.display_cards(True)
        if player_stand and self.round_over:
            self.display_gui((self.player_card_total, self.dealer_card_total), True)
        else:
            self.display_gui((self.player_card_total, self.dealer_card_total), False)
        
        




# create card class group
card_group = pygame.sprite.Group()


# Draw a hand of 8 cards using cards from the deck
"""
x_pos = 100

for card in hand:
    x_pos += 100
    print(card.tellRank()) # say all of the cards
    current_card = Card(card.rank, card.suit, x_pos, 300) # make card object with rank and suit chosen, positioning them on the screen
    card_group.add(current_card) # add card object to group
"""
player_stand = False # grrr u little
my_game = Game(card_group)
result = None

# main game loop
running = True
while running:
    for event in pygame.event.get():
        #ILOVELONGIFSTATEMENTS!!!!!!!
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not player_stand:
            result = my_game.draw_card(my_game.hand, my_game.deck)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            player_stand = True
            my_game.dealer_turn()
        if event.type == my_game.DEALER_DRAW_TIMER and not my_game.round_over:
            my_game.draw_card(my_game.dealer_hand, my_game.deck)
            my_game.dealer_turn()
    

    # draw the background
    display_surface.fill((38, 182, 128))

    # draw card group to display surface
    card_group.draw(display_surface)
    
    my_game.update()



    # update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)



# quit pygame
pygame.quit()