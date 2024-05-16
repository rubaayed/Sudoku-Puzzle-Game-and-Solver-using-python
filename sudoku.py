from abc import ABC, abstractmethod
import random


# This is an abstract class with all methods needed in the child class (Course )

class Player(ABC):

    @abstractmethod
    def fillCellOnePlayer(self, singlePoints):
        pass

    @abstractmethod
    def giveHint(self, singlePoints):
        pass


class Sudoku():

    def __init__(self):
        self._table = [[0] * 9 for i in range(9)]
        self._solvedTable = [[0] * 9 for i in range(9)]

    def getTable(self):
        return self._table

    def getSolvedTable(self):
        return self._solvedTable

    def initiateSolvedTable(self):
        for i in range(9):
            for j in range(9):
                self._solvedTable[i][j] = self._table[i][j]

    def loadRandompuzzel(self):
        level = input("Enter the level of difficulty")
        while True:
            if level.upper() == 'E':
                fillNumber = 33
                break
            elif level.upper() == 'M':
                fillNumber = 21
                break
            elif level.upper() == 'D':
                fillNumber = 9
                break
            else:
                print("You entered an invalid level. Try again")
                level = input("Enter the level of difficulty")

        for i in range(fillNumber):
            row = random.randint(0, 8)
            column = random.randint(0, 8)
            num = random.randint(1, 9)
            while self._table[row][column] != 0 or not self.CheckValid(self._table, row, column, num):
                row = random.randint(0, 8)
                column = random.randint(0, 8)
                num = random.randint(1, 9)
            self._table[row][column] = num
        self.viewTable(self._table)

    def loadPuzzleFromFile(self):
        filename = input("Enter file name:")
        f = open(filename)
        fileList = f.readlines()
        lineNumber = 0
        while lineNumber < len(fileList) - 1:
            fileList[lineNumber] = fileList[lineNumber][0:len(fileList[lineNumber]) - 1]
            lineSplit = fileList[lineNumber].split(",")
            for splitted in range(9):
                self._table[lineNumber][splitted] = lineSplit[splitted]
            lineNumber = lineNumber + 1
        lineSplit = fileList[lineNumber].split(",")
        for splitted2 in range(9):
            self._table[8][splitted2] = lineSplit[splitted2]

    def viewTable(self, tableToShow):
        TableTB = "|--------------------------------|"
        TableMD = "|----------+----------+----------|"
        print(TableTB)
        for x in range(9):
            for y in range(9):
                if (x == 3 or x == 6) and y == 0:
                    print(TableMD)
                if y == 0 or y == 3 or y == 6:
                    print("|", end=" ")
                print(" " + str(tableToShow[x][y]), end=" ")
                if y == 8:
                    print("|")
        print(TableTB)

    def CheckValid(self, table, row, col, num):
        valid = True
        for x in range(9):
            if table[x][col] == num:
                valid = False
        for y in range(9):
            if table[row][y] == num:
                valid = False
        rowSection = row // 3
        colSection = col // 3
        for x in range(3):
            for y in range(3):
                if table[rowSection * 3 + x][colSection * 3 + y] == num:
                    valid = False
        return valid

    def findNextCellToFill(self, table, i, j):
        for x in range(i, 9):
            for y in range(j, 9):
                if table[x][y] == 0:
                    return x, y
        for x in range(0, 9):
            for y in range(0, 9):
                if table[x][y] == 0:
                    return x, y
        return -1, -1

    def isValid(self, table, i, j, e):
        rowOk = all([e != table[i][x] for x in range(9)])
        if rowOk:
            columnOk = all([e != table[x][j] for x in range(9)])
            if columnOk:
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if table[x][y] == e:
                            return False
                return True
        return False

    def solveSudoku(self, i=0, j=0):
        i, j = self.findNextCellToFill(self._solvedTable, i, j)
        if i == -1 and j == -1:
            return True
        for e in range(1, 10):
            if self.isValid(self._solvedTable, i, j, e):
                self._solvedTable[i][j] = e
                if self.solveSudoku(i, j):
                    return True
                self._solvedTable[i][j] = 0
        return False

    def isSolved(self):
        for i in range(9):
            for j in range(9):
                if self._table[i][j] == 0:
                    return False

        return True

    def canFillCell(self, i, j, num):
        if num == self._solvedTable[i][j]:
            self._table[i][j] = num
            return True
        else:
            return False


class OM(Player):
    def fillCellOnePlayer(self, tableObject, singlePoints):
        answer = input("Please enter row column and number separated by spaces")
        a = tuple(int(x) for x in answer.split(" "))
        row = a[0]
        col = a[1]
        num = a[2]

        if (0 < int(row) <= 9) and (0 < int(col) <= 9) and (0 < int(num) <= 9):
            pass
        else:
            print("The value you entered for row, column, or value is out of range!")
            return singlePoints

        upDown = tableObject.canFillCell(row, col, num)
        if upDown:
            singlePoints += 1
        else:
            singlePoints -= 1

        return singlePoints

    def giveHint(self, tableObject, singlePoints):
        row = random.randint(0, 8)
        column = random.randint(0, 8)
        while tableObject.getTable()[row][column] != 0:
            row = random.randint(0, 8)
            column = random.randint(0, 8)
        singlePoints -= 2
        tableObject.getTable()[row][column] = tableObject.getSolvedTable()[row][column]
        print("The value at row ", row, " and column ", column, " is ", tableObject.getSolvedTable()[row][column])
        return singlePoints


class TM(Player):
    def fillCellOnePlayer(self, tableObject, singlePoints):
        answer = input("Please enter row column and number seperated by spaces")
        a = tuple(int(x) for x in answer.split(" "))
        row = a[0]
        col = a[1]
        num = a[2]

        if (0 <= int(row) <= 9) and (0 <= int(col) <= 9) and (0 <= int(num) <= 9):
            pass
        else:
            print("The value you entered for row, column, or value is out of range!")
            return singlePoints

        upDown = tableObject.canFillCell(row, col, num)
        if upDown:
            singlePoints += 1
        else:
            singlePoints -= 1

        return singlePoints

    def giveHint(self, tableObject, singlePoints):
        row = random.randint(0, 8)
        column = random.randint(0, 8)
        while tableObject.getTable()[row][column] != 0:
            row = random.randint(0, 8)
            column = random.randint(0, 8)
        singlePoints -= 2
        tableObject.getTable()[row][column] = tableObject.getSolvedTable()[row][column]
        print("The value at row ", row, " and column ", column, " is ", tableObject.getSolvedTable()[row][column])
        return singlePoints


def manuFor1():
    print("1- Fill")
    print("2- Hint")
    print("3- Solve")


def manuFor2():
    print("1- Fill")
    print("2- Pass")
    print("3- Solve")


tableObject = Sudoku()

fromFileRandom = input("Please enter 1 if you want to load the sudoku or 2 to generate a random game")
while fromFileRandom != "1" and fromFileRandom != "2":
    fromFileRandom = input("Wrong entry, please try again")

if fromFileRandom == "1":
    tableObject.loadPuzzleFromFile()
    tableObject.initiateSolvedTable()
    tableObject.solveSudoku()
else:
    tableObject.loadRandompuzzel()
    tableObject.initiateSolvedTable()
    tableObject.solveSudoku()

oneOrTwo = input("Enter 1 for one player mode or 2 for 2 players mode")
while oneOrTwo != "1" and oneOrTwo != "2":
    oneOrTwo = input("Wrong entry, please try again")

if oneOrTwo == "1":
    onePlayer = OM()
    points = 0
    while not tableObject.isSolved():
        manuFor1()
        option = input("Enter your option")
        while option != "1" and option != "2" and option != "3":
            option = input("Wrong entry, please try again")
        if option == "1":
            points = onePlayer.fillCellOnePlayer(tableObject, points)
            tableObject.viewTable(tableObject.getTable())
        elif option == "2":
            points = onePlayer.giveHint(tableObject, points)
            tableObject.viewTable(tableObject.getTable())
        else:
            tableObject.viewTable(tableObject.getSolvedTable())
            break

else:
    twoPlayer = TM()
    points = [0, 0]
    turn = 0
    passes = 0
    while not tableObject.isSolved():
        print("It's Player ", turn + 1, " Turn")

        manuFor2()
        option = input("Enter your option")
        while option != "1" and option != "2" and option != "3":
            option = input("Wrong entry, please try again")
        if option == "1":  # fill
            points[turn] = twoPlayer.fillCellOnePlayer(tableObject, points[turn])
            if turn == 0:
                turn += 1
            else:
                turn -= 1
            tableObject.viewTable(tableObject.getTable())
        elif option == "2":  # pass
            passes += 1
            if passes == 4:
                passes = 0
                points[turn] = twoPlayer.giveHint(tableObject, points[turn])
                if turn == 0:
                    # print(points[1])
                    points[1] = points[1] - 2
                else:
                    points[0] = points[0] - 2
                if turn == 0:
                    turn += 1
                else:
                    turn -= 1
            tableObject.viewTable(tableObject.getTable())
        else:  # solve
            tableObject.viewTable(tableObject.getSolvedTable())
            break
