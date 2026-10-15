from cards import Card
        
    
class Game:
    def __init__(self, p1_name: str, p2_name: str, p1_deck: list, p2_deck: list):
        """
        Initialises a game instance to hold objects in memory, which is way faster than standard databases.

        :param p1_deck: The first player's deck (this is the player that goes first)
        :param p2_deck: The second player's deck 
        """
        self.p1_name = p1_name
        self.p2_name = p2_name
        self._creature_index = 1
        self.decks = {p1_name: {}, p2_name: {}}

        for _ in p1_deck:
            self.decks[p1_name][str(self._creature_index)] = _
                        
        self.graveyard = {p1_name: {}, p2_name: {}}
        self.hand = {p1_name: {}, p2_name: {}}
        self.lands = {p1_name: {}, p2_name: {}}
        self.active_creatures = {p1_name: {}, p2_name: {}}
        
        self.attacking = {}
        self.blocking = {}
        self.mana_pools = {
            p1_name: {
                "red": 0,
                "blue": 0,
                "green": 0
            },

            p2_name: {
                "red": 0,
                "blue": 0,
                "green": 0,
            }
        }

        self.current_player = p1_name

    def is_in_hand(self, player: str, card_id: str) -> bool:
        """
        Validates whether the card is in the player's hand, and whether the player is actually able to play the card.

        Args:
            player (str): The name of the current player.
            card_id (str): The id of the card being played.

        Returns:
            bool: Whether the move is legal.
        """
        target_card: Card = self.decks[player][card_id]
        if not target_card:
            return False
        
        # Check if the player has enough mana to play
        x = 0
        for _, v in self.mana_pools[player].items():
            x += v

        if x < target_card.generic_mana + 1:
            return False

        return True
            
    def play_creature(self, player: str, card_id: str) -> bool:
        """
        
        """
        if self.is_in_hand(player, card_id):
            for key, value in self.hand[player]:
                if key == card_id:
                    self.active_creatures[player].update({key: value})
                    self.hand[player].pop(card_id, None)
                else:
                    return False

        return True
    
    def play_land(self, player: str, card_id: str) -> bool:
        if self.is_in_hand(player, card_id):
            for key, value in self.hand[player]:
                if key == card_id:
                    self.lands[player].update({key: value})
                    self.hand[player].pop(card_id, None)
                else:
                    return False

        return True

    def tap_land(self, player: str, card_id: str):
        # Check if the card is in the player's land.
        for k, v in self.lands[player]:
            if k == card_id:
                v.tapped = 1    # Makes the card tapped.
                return True

        return False

    def attack_with(self):
        pass

    def defend_with(self):
        pass
        
