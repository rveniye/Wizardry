from src.cards import Card

def increment_att(card: Card, by: int) -> Card:
    card.att += by
    return card
