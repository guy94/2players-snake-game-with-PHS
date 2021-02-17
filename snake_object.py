import pygame


class MyNode:
    """
    This class represents a single element of the snake object.
    each node has a coordinate in order to be able to draw, and move that node in space.
    """
    NUM = 0

    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._next = None
        self.id = None

    def setRow(self, row):
        self._row = row

    def setCol(self, col):
        self._col = col

    def setNext(self, node):
        self._next = node

    def inc_n_get_num(self):
        self.id = MyNode.NUM
        MyNode.NUM += 1

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col

    def getNext(self):
        return self._next

    def getID(self):
        return self.id


class SnakeQ:
    """
    A snake object built from MyNode objects.
    """

    def __init__(self, color):
        self._head = None
        self._tail = None
        self.time = 15
        self.color = color
        self._size = 0
        self.heading = "i"
        self.pos_list = [0, 0]
        self.xChange = 0
        self.yChange = 0
        self._oldCol = 50
        self._oldRow = 50
        self._player_moved = False
        self.clock = pygame.time.Clock()

    def enqueue(self, node):
        """
        After consuming a piece of food, the snake grows - MyNode object is added to the snake object
        :param node:
        :return:
        """
        if self._head is None:
            self._head = node
            self._tail = node

        else:
            node.setNext(self._tail)
            self._tail = node

        node.inc_n_get_num()
        self._size += 1

    def tail_to_head(self):
        """
        In order to move the snake in space, each clock tick the tail node is moved to be the head node.
        this way, I simulate a movement and make it as efficient as possible - O(1) time complexity.,
        :return:
        """
        if self._size == 1:
            temp = self._tail

        else:
            temp = self._tail.getNext()

        self._head.setNext(self._tail)
        self._head = self._tail
        self._tail = temp
        self._head.setNext(None)

    def getClock(self):
        return self.clock

    def getPlayerMoved(self):
        return self._player_moved

    def setPlayerMoved(self, booli):
        self._player_moved = booli

    def getOldRow(self):
        return self._oldRow

    def setOldRow(self, oldRow):
        self._oldRow = oldRow

    def getOldCol(self):
        return self._oldCol

    def setOldCol(self, oldCol):
        self._oldCol = oldCol

    def getPosList(self):
        return self.pos_list

    def setPosList(self, posList):
        self.pos_list = posList

    def getHeading(self):
        return self.heading

    def setHeading(self, heading):
        self.heading = heading

    def getHead(self):
        return self._head

    def setHead(self, node):
        self._head = node

    def getTail(self):
        return self._tail

    def setTail(self, node):
        self._tail = node

    def getSize(self):
        return self._size

    def setSize(self, num):
        self._size = num

    def getTime(self):
        return self.time

    def getColor(self):
        return self.color

    def setTime(self, time):
        self.time = time
