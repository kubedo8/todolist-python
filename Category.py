from DbObj import DbObj


class Category(DbObj):
    def __init__(self, title):
        """Constructor of Category.

        Args:
            title (str): Title of Category.

        """
        super().__init__(title, Category)

    def __cmp__(self, other):
        """Comparison for category
        """
        return isinstance(other, Category) and self.title == other.title
