from Exception import BadInputException
from random import randint
import datetime


class DbObj:
    def __init__(self, title, obj_type):
        """Constructor of DbObj.

        Args:
            title (str): Title of object.
            obj_type: Object type

        """
        if title is None or not isinstance(title, str):
            raise BadInputException("Title is in bad format!")
        else:
            self.id = self._generateid()
            self.title = title
            self.obj_type = obj_type
            self.createdAt = datetime.datetime.now()

    def __str__(self):
        """String representation of database object
        """
        return self.title

    def __cmp__(self, other):
        """Comparison for database object
        """
        return self.obj_type == other.obj_type and self.id == other.id

    def __repr__(self):
        """Representation of database object
        """
        return "{} with id: {}".format(self.obj_type, self.id)

    def _generateid(self):
        """Generates unique id for database object

        Returns:
            Unique integer

        """
        return randint(1, 1000000000)
