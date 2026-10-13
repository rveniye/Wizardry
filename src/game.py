from cards import Card


class Game:
    def __init__(self, p1_name: str, p2_name: str, p1_deck, p2_deck):
        """
        Initialises a game instance to hold objects in memory, which is way faster than standard databases.

        :param p1_deck: The first player's deck (this is the player that goes first)
        :param p2_deck: The second player's deck 
        """
        self.p1_deck = p1_deck
        self.p2_deck = p2_deck
        self.p1_graveyard = {}
        self.p2_graveyard = {}

        self.p1_hand = {}
        self.p2_hand = {}
        self.p1_lands = {}
        self.p2_lands = {}

        self.p1_active_creatures = {}
        self.p2_active_creatures = {}
        
        self.attacking = {}
        self.blocking = {}
                
        self.cooldowns = {}
        self.graveyard = []
        
        self.p1_mana = {
            "red": 0,
            "blue": 0,
            "green": 0
        }
        
        self.p1_mana = {
                    "red": 0,
                    "blue": 0,
                    "green": 0
        }

    def play_card(self):
        pass
    
    def play_land(self):
        pass

    def tap_land(self):
        pass

    def attack_with(self):
        pass

    def defend_with(self):
        pass
        
