class Obstacle :

    def __init__(self, positition : tuple[float],size : float):
        self.__size = size
        self.__position = positition

        self.map = None

    #this is used to get the size of the obstacle
    @property
    def size(self):
        return self.__size

    #this is used to get the position of the obstacle
    @property
    def position(self):
        return self.__position
