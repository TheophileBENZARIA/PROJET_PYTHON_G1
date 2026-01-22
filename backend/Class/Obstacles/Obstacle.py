class Obstacle :

    def __init__(self, positition : tuple[float],size : float):
        self.__size = size
        self.__position = positition

        self.map = None

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position
