# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import queue


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.dimensions = rowDimension
        # how many mines in total
        self.mines = totalMines
        # a (rowDimension * colDimension) game board
        self.map = [["*" for i in range(rowDimension)] for j in range(colDimension)]
        # how many uncovered block currently need to be flag
        self.flag = []
        # how many mines we already flagged
        self.flagged = 0
        # list of covered block that is yet unchecked but garateed to be safe
        self.safe_covered = []
        # a pair that stores the current block location
        self.current = (startX, startY)
        self.double_check = []
        # bool value indicates we got all mines and need to finish up
        self.finished = False

    def find_covered_neighbor(self, row, col) -> list:
        neighbors = []
        # valid left neighbor
        if (row - 1 >= 0):
            if (self.map[row - 1][col] == "*"):
                neighbors.append((row - 1, col))
        # valid top left neighbor
        if ((row - 1 >= 0 and col + 1 <= self.dimensions - 1)):
            if (self.map[row - 1][col + 1] == "*"):
                neighbors.append((row - 1, col + 1))
        # valid top neighbor
        if (col + 1 <= self.dimensions - 1):
            if (self.map[row][col + 1] == "*"):
                neighbors.append((row, col + 1))
        # valid right neighbor
        if (row + 1 <= self.dimensions - 1):
            if (self.map[row + 1][col] == "*"):
                neighbors.append((row + 1, col))
        # valid top right neighbor
        if (row + 1 <= self.dimensions - 1 and col + 1 <= self.dimensions - 1):
            if (self.map[row + 1][col + 1] == "*"):
                neighbors.append((row + 1, col + 1))
        # valid bottom neighbor
        if (col - 1 >= 0):
            if (self.map[row][col - 1] == "*"):
                neighbors.append((row, col - 1))
        # valid bottom right neighbor
        if (col - 1 >= 0 and row + 1 <= self.dimensions - 1):
            if (self.map[row + 1][col - 1] == "*"):
                neighbors.append((row + 1, col - 1))
        # valid bottom left neighbor
        if (col - 1 >= 0 and row - 1 >= 0):
            if (self.map[row - 1][col - 1] == "*"):
                neighbors.append((row - 1, col - 1))

        return neighbors

    def find_next_covered(self) -> (int, int):
        found = -1
        for i in range(len(self.safe_covered)):
            x, y = self.safe_covered[i]
            if (self.map[x][y] == "*"):
                found = i
                break

        if (found == -1):
            # if we fail to find one unchecked
            self.safe_covered = []
            return (-1, -1)
        else:
            row, col = self.safe_covered[found]
            self.safe_covered = self.safe_covered[(found + 1):]
            return (row, col)

    def find_next_double_check(self) -> (int, int, int):
        found = -1
        for i in range(len(self.double_check)):
            x, y, n = self.double_check[i]
            nb = self.find_covered_neighbor(x, y)
            if (len(nb) > 0):
                found = i
                self.double_check = self.double_check[(found + 1):]
                return (x, y, n)

        return (-1, -1, -1)

    def getAction(self, number: int) -> "Action Object":
        # update our map each turn
        row, col = self.current
        self.map[row][col] = number

        if (self.mines == self.flagged):
            self.safe_covered = []
            self.finished = True
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    if (self.map[i][j] == "*"):
                        self.safe_covered.append((i, j))

        if (self.finished):
            if (self.safe_covered):
                x, y = self.safe_covered[0]
                self.safe_covered = self.safe_covered[1:]
                self.current = (x, y)
                return Action(AI.Action.UNCOVER, x, y)
            else:
                return Action(AI.Action.LEAVE)

        # Rule of thumb algorithms
        else:
            neignbour = self.find_covered_neighbor(row, col)
            if (neignbour):
                if (number == 0):
                    self.safe_covered = neignbour + self.safe_covered
                elif (number == len(neignbour)):
                    self.flag = self.flag + neignbour
                elif (number > 0):
                    x, y = self.current
                    num = number
                    self.double_check.append((x, y, num))

            if (self.flag):
                x, y = self.flag[0]
                self.current = (x, y)
                self.flag = self.flag[1:]
                self.flagged += 1
                return Action(AI.Action.FLAG, x, y)

            elif (self.safe_covered):
                x, y = self.find_next_covered()
                if (x != -1):
                    self.current = (x, y)
                    return Action(AI.Action.UNCOVER, x, y)

            if (self.double_check):
                x, y, num = self.find_next_double_check()
                if (x != -1):
                    self.current = (x, y)
                    return self.getAction(num)

            print("there is something wrong! (This should never been printed)")
            return Action(AI.Action.LEAVE)



