class Obstacle :

    def __init__(self, size : float, positition : tuple[float]):
        self.__size = size
        self.__position = positition

        self.map = None

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position
