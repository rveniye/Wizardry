class ParseError(Exception):
    """An exception that occurs when handling parsing."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class CardNotFound(Exception):
    """When a card is requested that does not exist."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        