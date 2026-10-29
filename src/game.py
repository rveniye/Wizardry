from src.modules.w_parser import parse


class Game:
    def __init__(self, p1_name: str, p2_name: str, p1_deck: list, p2_deck: list):
        """
        Initialises a game instance to hold objects in memory, which is way faster than standard databases.

        :param p1_deck: The first player's deck (this is the player that goes first)
        :param p2_deck: The second player's deck 
        """
        self.p1_name = p1_name
        self.p2_name = p2_name
        self._index = 1
        self.decks = {p1_name: {}, p2_name: {}}

        for _ in p1_deck:
            self.decks[p1_name][str(self._index)] = _
            self._index += 1

        for _ in p2_deck:
            self.decks[p2_name][str(self._index)] = _
            self._index += 1

        self.graveyard = {p1_name: {}, p2_name: {}}
        self.hand = {p1_name: {}, p2_name: {}}
        self.lands = {p1_name: {}, p2_name: {}}
        self.active_creatures = {p1_name: {}, p2_name: {}}

        self.card_abilities = {p1_name: {}, p2_name: {}}
        
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

        # Iterate through each ID and Game Object
        for k, v in self.decks[p1_name].items():
            self.card_abilities[p1_name][k] = parse(v.effect, self, p1_name)

        for k, v in self.decks[p1_name].items():
            self.card_abilities[p2_name][k] = parse(v.effect, self, p2_name)


    def get_card_abilities(self, card_id: str) -> dict:
        """
        Gets the abilities of the card.


        """
        p1_field, p2_field = self.card_abilities.get(self.p1_name), self.card_abilities.get(self.p2_name)

        for k1, k2 in zip(p1_field, p2_field):
            if k1 == card_id and p1_field[k1] is not None: return p1_field[k1]
            if k2 == card_id and p1_field[k2] is not None: return p2_field[k2]
            else: raise KeyError("Card does not exist.")

    def is_in_hand(self, player: str, card_id: str) -> bool:
        """
        Validates whether the card is in the player's hand, and whether the player is actually able to play the card.

        Args:
            player (str): The name of the current player.
            card_id (str): The id of the card being played.

        Returns:
            bool: Whether the move is legal.
        """
        target_card = self.hand[player].get(card_id)
        if target_card is None:
            print("Not in hand (is_in_hand)")
            return False
 
        # Lands are free to play.
        if target_card.type == "Land":
            return True
 
        # Check if the player has enough mana to play
        total_mana = sum(self.mana_pools[player].values())
        return total_mana >= target_card.generic_mana + 1
            
    def play_creature(self, player: str, card_id: str, payment: dict) -> bool:
        """
        Plays a creature from the hand into the active_creatures pile.

        Args:
            player (str): The name of the current player.
            card_id (str): The id of the card being played.
            payment (dict): The colours of mana being spent, in the format {'red': x, 'blue': y, 'green': z} - obviously the required colour mana has to be spent.

        Return:
            bool: Whether the move is legal.
        """
        if not self.is_in_hand(player, card_id):
            print("Not in hand (play_creature)")
            return False
 
        self.active_creatures[player][card_id] = self.hand[player].pop(card_id)
        
        self.mana_pools
        return True
    
    def play_land(self, player: str, card_id: str) -> bool:
        """
        Plays a land from the hand into the lands pile.

        Args:
            player (str): The name of the current player.
            card_id (str): The id of the card being played.

        Return:
            bool: Whether the move is legal.
        """
        if not self.is_in_hand(player, card_id):
            return False
 
        self.lands[player][card_id] = self.hand[player].pop(card_id)
        return True

    def tap_land(self, player: str, card_id: str) -> bool:
        """
        Taps a card to execute its abilities.

        Args:
            player (str): The name of the current player.
            card_id (str): The id of the card being played.

        Return:
            bool: Whether the move is legal.
            
        """
        land = self.lands[player].get(card_id)
        if land is None or land.tapped:
            return False
 
        land.tapped = 1    # Makes the card tapped.
        return True

    def attack_with(self):
        pass

    def defend_with(self):
        pass
        
