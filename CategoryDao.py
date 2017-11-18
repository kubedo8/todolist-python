from Category import Category
import pickle
from Exception import ParseException, StoringException, DuplicateObjectException


class CategoryDao:
    def __init__(self):
        self.__categories = self.readcategories()

    def getcategories(self):
        return self.__categories

    def addcategory(self, category):
        if self.findcategory(category.title) == -1:
            self.__categories.append(category)
            self.savecategories()
        else:
            raise DuplicateObjectException('Category with name {} already exists'.format(category.title))

    def updatecategory(self, category, newname):
        if category.title == newname:
            return
        index = self.findcategory(category)
        if index == -1:
            self.__categories[index].title = newname
            self.savecategories()
        else:
            raise DuplicateObjectException('Category with name {} already exists'.format(newname))

    def removecategory(self, category):
        index = self.findcategory(category.title)
        if index >= 0:
            del self.__categories[index]
            self.savecategories()

    def findcategory(self, name):
        for index, category in enumerate(self.__categories):
            if category.title == name:
                return index
        else:
            return -1

    def readcategories(self):
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

    def savecategories(self):
        try:
            with open('categories.bin', 'wb') as f:
                pickle.dump(self.__categories, f)
        except Exception:
            raise StoringException('Failed to store categories')
