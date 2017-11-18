class BadInputException(Exception):
    """
    Exception raised when parameters ar set to wrong values
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
