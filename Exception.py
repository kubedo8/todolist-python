class BadInputException(Exception):
    """
    Exception raised when parameters ar set to wrong values
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ParseException(Exception):
    """
    Exception raised when parsing input file
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class StoringException(Exception):
    """
    Exception raised when storing file
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class DuplicateObjectException(Exception):
    """
    Exception raised when storing file
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
