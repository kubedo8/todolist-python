import DbObj
import Category
import datetime
from Exception import BadInputException


class Todo(DbObj):
    def __init__(self, title, description, dueDate, category, priority, completed):
        """Constructor of Todo.

        Args:
            title (str): Title of Category.

        """
        if description is None or not isinstance(description, str):
            raise BadInputException("Description is in bad format!")
        elif category is None or not isinstance(category, Category.Category):
            raise BadInputException("Category is in bad format!")
        elif dueDate is None or not isinstance(dueDate, datetime.date):
            raise BadInputException("DueDate is not a date!")
        elif priority is None or not isinstance(dueDate, int) or priority < 0 or priority > 5:
            raise BadInputException("Category is in bad format!")
        elif completed is None or not isinstance(completed, bool):
            raise BadInputException("Completed is in bad format!")
        else:
            super().__init__(title, Todo)
            self.description = description
            self.dueDate = dueDate
            self.category = category
            self.priority = priority
            self.completed = completed

    def __str__(self):
        """String representation of todo object
        """
        return self.title + " - " + self.description

    def __cmp__(self, other):
        """Comparison for todo
        """
        return isinstance(other, Todo) and self.id == other.id
