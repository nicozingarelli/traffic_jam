import  sys, random

# set up the board
BOARDWIDTH = 6  # number of columns in the board
BOARDHEIGHT = 6 # number of rows in the board
GOAL_STATE = (3,0)

def main ():
    print("main")
    board = readPuzzle(sys.argv[1])
    guy = board.getBoardHash()
    visited = {guy}
    red_car = board.getRedCar()
    board.findAllNewStates()

# if RedCar.x == 4:
	#"We're done"

def readPuzzle(puzzle):
    cars = []
    with open(puzzle, "r") as puzzle:
        for sor in puzzle:
            c = sor.split()
            cars.append(Car(int(c[0]), int(c[1]), c[2], int(c[3]), c[4]))
    return Table(cars, GOAL_STATE)

def reset_to_0(the_array):
    for i, e in enumerate(the_array):
        if isinstance(e, list):
            reset_to_0(e)
        else:
            the_array[i] = 0

class Car(object):

    def __init__(self, x, y, lie, length, sign):
        """
        Stores the position datas of the car.

        (x,y): gives the position of upper left side of the car, in Descartes coordinate system.
               positive direct: x:right y:down
        direction: gives, whether the car lie horizontally or vertically
        """
        self.x = x
        self.y = y
        self.lie = lie			# Whether it's vertical or horizantal
        self.len = length		# length of the car
        self.sign = sign        # red car or not

        #This is the physical moving where we change the car physical location
    def Move(self, direction, steps):
        operator = {'f': 1 , 'b': -1}
        if self.lie == 'h':
            self.x += (operator[direction]*steps)
        elif self.lie == 'v':
            self.y += (operator[direction]*steps)

        #This returns where the car is in the map
    def GetCoordinates(self):
        if self.lie == 'v':
            return[(self.x,self.y + i) for i in range(self.len)]
        elif self.lie == 'h':
            return[(self.x + i,self.y) for i in range(self.len)]
        # This returns the cordinates dictionry of the car weather it's h and v at all times
    def GetCoordinatesDict(self):
        return dict(map(lambda t:(t,self),self.GetCoordinates()))
        #This decides the direction and the number of steps between tile1 and tile2 but we just need to make sure first they're in the same direction first to use this
    def getStep(self, tile1, tile2):
        movingindex = {'h':0,'v':1}
        # map of all available coordinates
        movingcoords = map(lambda t: t[movingindex[self.lie]], self.GetCoordinates())
        # if ((tile2[movingindex[self.lie]] > tile1[movingindex[self.lie]]) and (tile2[1] == tile1[1])):
        # if the hor/vert value of newTile > oldTile
        if tile2[movingindex[self.lie]] > tile1[movingindex[self.lie]]:
            direction = 'f'
            steps = tile2[movingindex[self.lie]] - max(movingcoords)
        # if the hor/vert value of newTile < oldTile
        elif tile2[movingindex[self.lie]] < tile1[movingindex[self.lie]]:
            direction = 'b'
            steps = min(movingcoords) - tile2[movingindex[self.lie]]
        else:
            direction = 'b'
            steps = 0
        return (direction, steps)

class Table(object):

    def __init__(self, cars, goal_state, size = 6):
        self.size = size
        self.cars = cars
        self.goal_state = goal_state
        self.board = [[0]*size for _ in range(size)]
        self.hash = self.getBoardHash()
        self.updateBoard()
        # self.cars_blocking = self.getCarsBlocking()
        #Returning the car that has a sign of R from the dictionary of cars
    def getRedCar(self):
        return dict([(c.sign,c) for c in self.cars])['R']
        # Returns any car requested by car name (letter ex: 'F')
    def getCar(self, car_name):
        return dict([(c.sign,c) for c in self.cars])[car_name]
        #Returns the corrddinates dictionary of all cars
    def GetCoordinates(self):
        d = {}
        for c in self.cars:
            d.update(c.GetCoordinatesDict())
        return d
        #This just returns if the car moving is a valid step or not it doesn't move it
    def isValidStep(self, c, direction, steps):
        carcoordinates = self.GetCoordinates()
        movingcoord = {'h': c.x , 'v': c.y}  #First cordinate of the car
        startpos = {'f': movingcoord[c.lie] + c.len , 'b': movingcoord[c.lie] - 1} #Starting position of the car
        endpos = {'f': movingcoord[c.lie] + c.len + steps , 'b':  movingcoord[c.lie] - steps - 1}  #ending position of the car
        rangesteps = {'f': 1 , 'b': -1} #This just so that we know if we're going to the fron or backwards
        route = range(startpos[direction] , endpos[direction] , rangesteps[direction]) #The actaul route of this move the car just did
        if c.lie == 'h':
             freecoordinates = map(lambda i:(i,c.y) not in carcoordinates, route)
        elif c.lie == 'v':
             freecoordinates = map(lambda i:(c.x,i) not in carcoordinates, route)
        freecoordinates.append(True)
        return reduce(lambda a, b: a and b , freecoordinates) and endpos[direction] <= self.size and endpos[direction] + 1 >= 0

    def getCarsBlocking(self):
        if self.goalTest(): return 0
        num_blocking = 0
        movingindex = {'h':0,'v':1}
        indices = self.getDirectPathIndices()
        for car in self.cars:
            if(car.sign == 'R'):
                continue
            elif car.lie == 'h':
                for i in range(0, car.len):
                    if([car.x + i, car.y] in indices):
                        num_blocking += 1
                        print(car.sign)
            elif car.lie == 'v':
                for i in range(0, car.len):
                    if([car.x, car.y + i] in indices):
                        [car.x, car.y + i]
                        num_blocking += 1
                        print(car.sign)
        return num_blocking

    def getDirectPathIndices(self):
        red_car = self.getRedCar()
        x = red_car.x
        y = red_car.y
        path_indices = []
        path_to_goal = red_car.getStep([x, y], self.goal_state)
        if red_car.lie == 'h':
            if(path_to_goal[0] == 'f'):
                for i in range(1, path_to_goal[1] + 1):
                    path_indices.append([x + i ,y])
            else:
                for i in range(1, path_to_goal[1] + 1):
                    path_indices.append([x - i ,y])
        else:
            if(path_to_goal[0] == 'f'):
                for i in range(1, path_to_goal[1] + 1):
                    path_indices.append([x, y + i])
            else:
                for i in range(1, path_to_goal[1] + 1):
                    path_indices.append([x, y - i])
        return path_indices

    def goalTest(self):
        return True if self.getRedCar().x == self.goal_state[1] and self.getRedCar().y == self.goal_state[0] else False

    def updateBoard(self):
        reset_to_0(self.board)
        for car in self.cars:
            isTruck = (car.len == 3)
            char = 't' if isTruck else 'c'
            if(car.lie == 'h'):
                self.board[car.y][car.x] = char.capitalize()
                self.board[car.y][car.x + 1] = char
                if(isTruck):
                    self.board[car.y][car.x + 2] = char
            else:
                self.board[car.y][car.x] = char.capitalize()
                self.board[car.y + 1][car.x] = char
                if(isTruck):
                    self.board[car.y + 2][car.x] = char
    def printBoard(self):
        self.updateBoard()
        print('\n'.join([''.join(['{:1}'.format(item) for item in row])
              for row in self.board]))

    def getBoardHash(self):
        if self.board is not None:
            flatBoard = [ y for x in self.board for y in x]
            stringBoard = ''.join(map(str,flatBoard))
            return hash(stringBoard)

    def getNewHValue(self, car, tile1, tile2):
        newCars = self.makeNewCars()
        child_board = Table(newCars, self.goal_state)
        car_to_move = child_board.getCar(car.sign)
        move_params = car_to_move.getStep(tile1, tile2)
        car_to_move.Move(move_params[0], move_params[1])
        child_board.updateBoard()
        print("during")
        child_board.printBoard()
        print('h(n) = ', child_board.getCarsBlocking())

    def makeNewCars(self):
        newCars = []
        for car in self.cars:
            newCars.append(Car(car.x, car.y, car.lie, car.len, car.sign))
        return newCars

    def findAllNewStates(self):
        board_size = len(self.board)
        for car in self.cars:
            if(car.lie == 'h'):
                print(car.sign)
                if(car.x > 0):
                    for i in range(1, car.x + 1):
                        if(self.board[car.y][car.x - i] == 0):
                            print("before")
                            self.printBoard()
                            self.getNewHValue(car, [car.x, car.y],[car.x - i, car.y])
                            print("after")
                            self.printBoard()
                        else:
                            break
                if(car.x + car.len < board_size):
                    for i in range(1, board_size - (car.x + car.len) + 1):
                        print("i: ", i)
                        if(self.board[car.y][car.x + car.len - 1 + i] == 0):
                            print("before")
                            self.printBoard()
                            self.getNewHValue(car, [car.x, car.y],[car.x + car.len - 1 + i, car.y])
                            print("after")
                            self.printBoard()
                        else:
                            break
            else:
                print(car.sign)
                if(car.y > 0):
                    for i in range(1, car.y + 1):
                        if(self.board[car.y - i][car.x] == 0):
                            # print("before")
                            # self.printBoard()
                            self.getNewHValue(car, [car.x, car.y],[car.x, car.y - i])
                            # print("after")
                            # self.printBoard()
                        else:
                            break
                if(car.y + car.len < board_size):
                    for i in range(1, board_size - (car.y + car.len) + 1):
                        print("i: ", i)
                        if(self.board[car.y + car.len - 1 + i][car.x] == 0):
                            # print("before")
                            # self.printBoard()
                            self.getNewHValue(car, [car.x, car.y],[car.x, car.y + car.len - 1 + i])
                            # print("after")
                            # self.printBoard()
                        else:
                            break

main()



# method that goes through all cars and checks forward and backward up to n calling getStep on each potential tile
