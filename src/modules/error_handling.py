class ParseError(Exception):
    """An exception that occurs when handling parsing."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
