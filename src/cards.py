from typing import Any, Dict


class Card:
    def __init__(self, name: str, generic_mana: int, sp_mana: str, card_type: str, description: str, effect: str) -> None:
        """
        Parent class for type Card.

        :param name: Name of the card.
        :type name: str
        :param generic_mana: Any coloured mana cost.
        :type generic_mana: int
        :param sp_mana: Coloured mana type.
        :type sp_mana: str
        :param card_type: The card type - can be a Land/Creature/Spell/Enchant.
        :type card_type: str
        :param description: The description of the card.
        :type description: str
        :param effect: The card's effects scripted in custom syntax.
        :type effect: str
        """
        self.name = name
        self.generic_mana = generic_mana
        self.sp_mana = sp_mana
        self.type = card_type
        self.description = description
        self.effect = effect
        self.tapped = 0     # 0 for untapped, 1 for tapped
        self.statuses = []
        self.id = 0 

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the card.

        :rtype: dict
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "generic_mana": self.generic_mana,
            "sp_mana": self.sp_mana,
            "description": self.description,
            "tapped": self.tapped,
            "statuses": self.statuses,
            "effect": self.effect,
        }


class LandCard(Card):
    def __init__(self, name: str, generic_mana: int, sp_mana: str, description: str, effect: Any) -> None:
        """
        Initialises a Land Card.
        
        :param name: Name of the card.
        :type name: str
        :param generic_mana: Any coloured mana cost.
        :type generic_mana: int
        :param sp_mana: Coloured mana type.
        :type sp_mana: int
        :param description: The description of the card.
        :type description: str
        :param effect: The card's effects scripted in custom syntax.
        :type effect: str
        """
        super().__init__(name, generic_mana, sp_mana, "Land", description, effect)

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the card.
        
        :rtype: Dict[str, Any]
        """
        data = super().to_dict()
        return data
     

class CreatureCard(Card):
    def __init__(self, name: str, generic_mana: int, sp_mana: str, description: str, att: int, end: int, effect: str) -> None:
        """
        Initialises a Creature Card.
        
        :param name: Name of the card.
        :type name: str
        :param generic_mana: Any coloured mana cost.
        :type generic_mana: int
        :param sp_mana: Coloured mana type.
        :type sp_mana: int
        :param description: The description of the card.
        :type description: str
        :param att: The creature's attack value.
        :type att: int
        :param end: The creature's defence value.
        :type end: int
        :param effect: The card's effects scripted in custom syntax.
        :type effect: str
        """
        super().__init__(name, generic_mana, sp_mana, "Creature", description, effect)
        self.attack = att
        self.defence = end
     
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the card.
        
        :rtype: dict
        """
        data = super().to_dict()
        data.update(
            {
                "attack": self.attack,
                "defence": self.defence,
            }
        )
        return data
     

class SpellCard(Card):
    def __init__(self, name: str, generic_mana: int, sp_mana: str, description: str, effect: str):
        """
        Initialises a Spell Card.
        
        :param name: Name of the card.
        :type name: str
        :param generic_mana: Any coloured mana cost.
        :type generic_mana: int
        :param sp_mana: Coloured mana type.
        :type sp_mana: int
        :param description: The description of the card.
        :type description: str
        :param effect: The card's effects scripted in custom syntax.
        :type effect: str
        """
        super().__init__(name, generic_mana, sp_mana, "Spell", description, effect)
     
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the card.
        
        :rtype: dict
        """
        data = super().to_dict()
        return data


# class EnchantCard(Card):
#     def __init__(self, name: str, generic_mana: int, sp_mana: int, description: str, effect: str) -> None:
#         """
#         Initialises an Enchantment Card.
#
#         :param name: Name of the card.
#         :type name: str
#         :param generic_mana: Any coloured mana cost.
#         :type generic_mana: int
#         :param sp_mana: Coloured mana type.
#         :type sp_mana: int
#         :param description: The description of the card.
#         :type description: str
#         :param effect: The card's effects scripted in custom syntax.
#         :type effect: str
#         """
#         super().__init__(name, generic_mana, sp_mana, "Enchantment", description, effect)
#
#     def to_dict(self) -> dict:
#         """
#         Returns a dictionary representation of the card.
#
#         :rtype: dict
#         """
#         data = super().to_dict()
#         return data
