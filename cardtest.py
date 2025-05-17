import random


class Card:
    def __init__(self):
        self.ranks = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]
        self.suits = ["Spade", "Club", "Diamond", "Heart"]
        self.rank = random.choice(self.ranks)
        self.suit = random.choice(self.suits)
        
    
    

    def tellCard(self):
        return f"{self.rank} of {self.suit}s,"

        


new_hand = [Card() for i in range(8)]
hand_tell = " ".join([i.tellCard() for i in new_hand])
hand_tell = hand_tell[:-1]
print(hand_tell)