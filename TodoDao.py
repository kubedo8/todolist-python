from Category import Category
from Todo import Todo
from Exception import ParseException, StoringException, BadInputException, ObjectNotFoundException
import pickle
import operator


class TodoDao:
    def __init__(self):
        self.__todos = self.read_todos()
        self.__sort_by_keys = ['title', 'description', 'priority', 'duedate']
        self.__sortby = self.__sort_by_keys[0]
        self.sort()

    def add_todo(self, title, description, duedate, category, priority):
        """Adds todo to list

        Args:
            title(str): Todo title
            description(str): Todo description
            duedate(date): Todo due date
            category(Category): Todo category
            priority(int): Todo priority

        """
        try:
            new_todo = Todo(title, description, duedate, category, priority)
            self.__todos.append(new_todo)
            self.sort()
            self._save_categories()
        except BadInputException as e:
            raise e

    def update_todo(self, todo, new_title, new_description, new_duedate, new_priority):
        """Updates todo in list

        Args:
            new_title(str): Todo title
            new_description(str): Todo description
            new_duedate(date): Todo due date
            new_priority(int): Todo priority

        """
        try:
            new_todo = Todo(new_title, new_description,new_duedate, todo.category, new_priority)
            new_todo.id = todo.id
            index = self.find_todo(todo.id)
            if index >= 0:
                self.__todos[index] = new_todo
                self.sort()
                self._save_categories()
            else:
                raise ObjectNotFoundException('Todo with id {} not found'.format(todo.id))
        except BadInputException as e:
            raise e

    def set_sort(self, new_sort):
        """Sets new sort

        Args:
            new_sort(str): New sort attribute

        """
        index = self.__sort_by_keys.index(new_sort)
        if index == -1:
            raise BadInputException('Sorting method {} does not exists'.format(new_sort))
        else:
            self.__sortby = self.__sort_by_keys[index]

    def sort(self):
        """Sort todos
        """
        self.__todos.sort(key = operator.attrgetter(self.__sortby))

    def get_todos(self, category):
        """

        Args:
            category(Category): Category for which to find todos

        Returns:
            List of actual todos

        """
        return [x for x in self.__todos if x.category.title == category.title]

    def find_todo(self, id):
        """Finds todo index

        Args:
            id(int): Todo id to find

        Returns:
            Todo index, -1 otherwise

        """
        for index, todo in enumerate(self.__todos):
            if todo.id == id:
                return index
        else:
            return -1

    def read_todos(self):
        """Reads todos from disk
        """
        todos = list()
        try:
            with open('todos.bin', 'rb') as f:
                todos = pickle.load(f)
        except FileNotFoundError:
            todos = list()
        except Exception:
            raise ParseException('Failed to parse todos')
        finally:
            return todos

    def _save_categories(self):
        """Saves todos to disk
        """
        try:
            with open('todos.bin', 'wb') as f:
                pickle.dump(self.__todos, f)
        except Exception:
            raise StoringException('Failed to store todos')
