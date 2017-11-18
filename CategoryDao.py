from Category import Category
from Exception import ParseException, StoringException, DuplicateObjectException, ObjectNotFoundException
import pickle


class CategoryDao:
    def __init__(self):
        self.__categories = self._read_categories()

    def get_categories(self):
        """

        Returns:
            List of actual categories

        """
        return self.__categories

    def add_category(self, title):
        """Adds category to list

        Args:
            title(str): Category to add

        """
        if self.find_category(title) == -1:
            self.__categories.append(Category(title))
            self._save_categories()
        else:
            raise DuplicateObjectException('Category with name {} already exists'.format(title))

    def update_category(self, category, new_name):
        """Updates category in list

        Args:
            category(Category): Category to update
            new_name(str): New name for category

        """
        if category.title == new_name:
            return
        index = self.find_category(new_name)
        if index == -1:
            index2 = self.find_category(category.title)
            if index2 >= 0:
                self.__categories[index2].title = new_name
                self._save_categories()
            else:
                raise ObjectNotFoundException('Category with name {} not found'.format(category.title))
        else:
            raise DuplicateObjectException('Category with name {} already exists'.format(new_name))

    def remove_category(self, category):
        """Removes category from list

        Args:
            category(Category): Category to remove

        """
        index = self.find_category(category.title)
        if index >= 0:
            del self.__categories[index]
            self._save_categories()

    def find_category(self, name):
        """Finds category index

        Args:
            name(str): Category name to find

        Returns:
            Category index, -1 otherwise

        """
        for index, category in enumerate(self.__categories):
            if category.title == name:
                return index
        else:
            return -1

    def _read_categories(self):
        """Reads categories from disk
        """
        categories = list()
        try:
            with open('categories.bin', 'rb') as f:
                categories = pickle.load(f)
        except FileNotFoundError:
            categories = list()
        except Exception:
            raise ParseException('Failed to parse categories')
        finally:
            return categories

    def _save_categories(self):
        """Saves categories to disk
        """
        try:
            with open('categories.bin', 'wb') as f:
                pickle.dump(self.__categories, f)
        except Exception:
            raise StoringException('Failed to store categories')
