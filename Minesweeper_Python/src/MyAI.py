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
        self.covered = rowDimension * colDimension
        self.uncovered = 0
        self.flagged = 0
        # list of covered block that is yet unchecked but garateed to be safe
        self.safe_covered = []
        # a pair that stores the current block location
        self.current = (startX, startY)
        self.double_check = []

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

    def double_check_algorithm(self) -> "Action Object":
        for v in self.double_check:
            x, y, num = v
            nb = self.find_covered_neighbor(x, y)
            if (not nb):
                continue
            elif (len(nb) == num):
                double_check = []
                x, y = nb[0]
                self.flag = self.flag + nb[1:]
                return Action(AI.Action.FLAG, x, y)

    def getAction(self, number: int) -> "Action Object":
        # update our map each turn
        print(number)
        row, col = self.current
        self.map[row][col] = number
        if (self.covered == self.flagged + self.uncovered):
            return Action(AI.Action.LEAVE)


        # Rule of thumb algorithms
        else:
            neignbour = self.find_covered_neighbor(row, col)
            if (neignbour):
                if (number == 0):
                    self.safe_covered = self.safe_covered + neignbour
                elif (number == len(neignbour)):
                    self.flag = self.flag + neignbour
                elif (number > 0):
                    x, y = self.current
                    num = number
                    self.double_check.append((x, y, num))
                elif (number == -1):
                    self.safe_covered = self.safe_covered + neignbour

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
                    self.uncovered += 1
                    return Action(AI.Action.UNCOVER, x, y)

            elif (self.double_check):
                self.double_check_algorithm()
            else:
                return Action(AI.Action.LEAVE)



