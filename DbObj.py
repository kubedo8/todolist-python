from Exception import BadInputException
from random import randint

import datetime


class DbObj:
    def __init__(self, title):
        """Constructor of DbObj.

        Args:
            title (str): Title of object.

        """
        if title is None or not title.isdigit():
            raise BadInputException("Title is in bad format!")
        else:
            self.id = self.generateid()
            self.title = title
            self.createdAt = datetime.datetime.now()

    def __str__(self):
        """String representation of database object
        """
        return self.title + " at %s" % self.createdAt

    def __cmp__(self, other):
        """Comparison for database object
        """
        return isinstance(other, DbObj) and self.id == other.id

    def generateid(self):
        """Generates unique id for database object

        Returns:
            Unique integer

        """
        return randint(1, 1000000000)
