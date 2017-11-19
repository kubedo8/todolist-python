from Category import Category
from Todo import Todo
from Exception import ParseException, StoringException, BadInputException, ObjectNotFoundException
import pickle
import operator
from datetime import datetime
import xml.etree.ElementTree as et


class TodoDao:
    def __init__(self):
        self.__todos = self._read_todos()
        self.sort_by_keys = ['title', 'description', 'priority', 'duedate']
        self.__sortby = self.sort_by_keys[0]
        self.find_by_keys = ['title', 'description', 'priority']
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
            self._save_todos()
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
            new_todo = Todo(new_title, new_description, new_duedate, todo.category, new_priority)
            new_todo.id = todo.id
            index = self.find_todo(todo.id)
            if index >= 0:
                self.__todos[index] = new_todo
                self.sort()
                self._save_todos()
            else:
                raise ObjectNotFoundException('Todo with id {} not found'.format(todo.id))
        except BadInputException as e:
            raise e

    def remove_todo(self, id):
        """Deletes selected todo

        Args:
            id(int): Id to delete

        """
        index = self.find_todo(id)
        if index >= 0:
            del self.__todos[index]
            self._save_todos()

    def set_sort(self, new_sort):
        """Sets new sort

        Args:
            new_sort(str): New sort attribute

        """
        index = self._sort_index(new_sort)
        if index == -1:
            raise BadInputException('Sorting method {} does not exists'.format(new_sort))
        else:
            self.__sortby = self.sort_by_keys[index]
            self.sort()

    def sort(self):
        """Sort todos
        """
        self.__todos.sort(key=operator.attrgetter(self.__sortby))

    def get_todos(self, category):
        """

        Args:
            category(Category): Category for which to find todos

        Returns:
            List of actual todos

        """
        return [x for x in self.__todos if x.category.title == category.title]

    def get_all(self):
        return self.__todos

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

    def find_todos(self, category, attr, value):
        """Finds todos with specific attribute and value

        Args:
            category(Category): Todo category
            attr(str): Todo attribute
            value(str): Value of attribute

        Returns:
            List of accepted todos

        """
        if not self._is_valid_find_key(attr):
            raise BadInputException('Find by {} does not exists'.format(attr))
        if attr == 'priority':
            if value.isdigit():
                return [x for x in self.get_todos(category) if x.priority == int(value)]
            else:
                return list()
        else:
            call = operator.attrgetter(attr)
            return [x for x in self.get_todos(category) if value.lower() in call(x).lower()]

    def import_todos(self, category, file_name):
        """Import todos for category from xml file

        Args:
            category(Category): Todo category
            file_name(str): Name of the file without .xml extension

        Returns:
            number of successfuly imported todos
        """
        num_imported = 0
        try:
            tree = et.parse(file_name + '.xml')
            root = tree.getroot()
            if root.tag != 'Todos':
                return
            for togo_tag in root:
                if togo_tag.tag != 'Todo':
                    continue
                try:
                    title = None
                    description = None
                    duedate = None
                    priority = None
                    for child in togo_tag:
                        if child.tag == 'Title':
                            title = child.text
                        elif child.tag == 'Description':
                            description = child.text
                        elif child.tag == 'Duedate':
                            duedate = datetime.strptime(child.text, '%d.%m.%Y').date()
                        elif child.tag == 'Priority':
                            priority = int(child.text)
                    self.__todos.append(Todo(title, description, duedate, category, priority))
                    num_imported += 1
                except Exception:
                    pass  # we just skip bad data
        except FileNotFoundError:
            pass
        finally:
            self._save_todos()
            return num_imported

    def export_todos(self, category, file_name):
        """Export todos from category as xml file

        Args:
            category(Category): Todo category
            file_name(str): Name of the file without .xml extension
        """
        top = et.Element('Todos')
        for todo in self.get_todos(category):
            todo_sub = et.SubElement(top, 'Todo')
            title = et.SubElement(todo_sub, 'Title')
            title.text = todo.title
            description = et.SubElement(todo_sub, 'Description')
            description.text = todo.description
            duedate = et.SubElement(todo_sub, 'Duedate')
            duedate.text = "%s.%s.%s" % (todo.duedate.day, todo.duedate.month, todo.duedate.year)
            priority = et.SubElement(todo_sub, 'Priority')
            priority.text = str(todo.priority)

        et.ElementTree(top).write(file_name + '.xml')

    def _read_todos(self):
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

    def _save_todos(self):
        """Saves todos to disk
        """
        try:
            with open('todos.bin', 'wb') as f:
                pickle.dump(self.__todos, f)
        except Exception:
            raise StoringException('Failed to store todos')

    def _sort_index(self, key):
        """Finds sort index
        """
        for index, item in enumerate(self.sort_by_keys):
            if key == item:
                return index
        return -1

    def _is_valid_find_key(self, key):
        """Check if given key for finding is valid
        """
        for item in self.find_by_keys:
            if key == item:
                return True
        return False
