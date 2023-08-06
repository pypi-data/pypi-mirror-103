class Page(object):
    def __init__(self, current, size):
        self.__current = current
        self.__size = size
        self.__total = 0
        self.data = []

    @property
    def current(self):
        return self.__current

    @property
    def size(self):
        return self.__size

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value

    @size.setter
    def size(self, value):
        if not isinstance(value, int):
            raise ValueError('current must be a integer')
        self.__size = value

    @current.setter
    def current(self, value):
        if not isinstance(value, int):
            raise ValueError('current must be a integer')
        self.__current = value
