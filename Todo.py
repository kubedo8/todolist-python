from DbObj import DbObj
from Category import Category
import datetime
from Exception import BadInputException


class Todo(DbObj):
    def __init__(self, title, description, duedate, category, priority):
        """Constructor of Todo.

        Args:
            title (str): Title of todo.
            description (str): Description of todo.
            duedate (date): Date by which the task must be accomplished
            category (Category): Category of todo.
            priority (int): Priority of todo, from 1 to 5.
        """
        if description is None or not isinstance(description, str):
            raise BadInputException("Description is in bad format!")
        elif duedate is None or not isinstance(duedate, datetime.date):
            raise BadInputException("DueDate is not a date!")
        elif category is None or not isinstance(category, Category):
            raise BadInputException("Category is in bad format!")
        elif priority is None or not isinstance(priority, int) or priority < 1 or priority > 6:
            raise BadInputException("Priority must be from 1 to 5!")
        else:
            super().__init__(title, Todo)
            self.description = description
            self.duedate = duedate
            self.category = category
            self.priority = priority

    def __str__(self):
        """String representation of todo object
        """
        date = "due to: %s/%s/%s" % (self.duedate.day, self.duedate.month, self.duedate.year)
        return self.title + " | " + self.description + " | " + date + " | from category: " + self.category.title + " | with priority: " + str(
            self.priority)

    def __cmp__(self, other):
        """Comparison for todo
        """
        return isinstance(other, Todo) and self.id == other.id
