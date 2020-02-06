import  sys, random

# set up the board
BOARDWIDTH = 6  # number of columns in the board
BOARDHEIGHT = 6 # number of rows in the board

def main ():
    print("main")
    board = readPuzzle(sys.argv[1])
    guy = board.getStringRep()
    visited = {guy}
    print(visited)
    print(guy in visited)
    red_car = board.getRedCar()
    print(red_car.getStep([red_car.x, red_car.y],[3,0]))
    # test_car = board.getCar('F')
    # print(test_car.x)
    # print(test_car.y)
    # print(test_car.getStep([test_car.y, test_car.x],[4,3]))
    # print
# if RedCar.x == 4:
	#"We're done"

def readPuzzle(puzzle):
    cars = []
    with open(puzzle, "r") as puzzle:
        for sor in puzzle:
            c = sor.split()
            cars.append(Car(int(c[0]), int(c[1]), c[2], int(c[3]), c[4]))
    return Table(cars, (0,3))
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
        #This decides if the tile1 is in the same direction as tile2
        # might not need
    # def isValidDirect(self, tile1, tile2):
    #     fixindex = {'h':1,'v':0}
    #     return tile1[fixindex[self.lie]] == tile2[fixindex[self.lie]]
        #This decides the direction and the number of steps between tile1 and tile2 but we just need to make sure first they're in the same direction first to use this
    def getStep(self, tile1, tile2):
        movingindex = {'h':0,'v':1}
        # map of all available coordinates
        movingcoords = map(lambda t: t[movingindex[self.lie]], self.GetCoordinates())
        # if ((tile2[movingindex[self.lie]] > tile1[movingindex[self.lie]]) and (tile2[1] == tile1[1])):
        if tile2[movingindex[self.lie]] > tile1[movingindex[self.lie]]:
            direction = 'f'
            steps = tile2[movingindex[self.lie]] - max(movingcoords)
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
        self.cars_blocking = self.getCarsBlocking()
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
        red_car = self.getRedCar()
        diff = red_car.x - self.goal_state[0] if (red_car.lie == 'h') else red_car.y - self.goal_state[1]

    def getStringRep(self):
        board = [[0]*self.size for _ in range(self.size)]
        for car in self.cars:
            isTruck = (car.len == 3)
            char = 't' if isTruck else 'c'
            if(car.lie == 'h'):
                board[car.y][car.x] = char.capitalize()
                board[car.y][car.x + 1] = char
                if(isTruck):
                    board[car.y][car.x + 2] = char
            else:
                board[car.y][car.x] = char.capitalize()
                board[car.y + 1][car.x] = char
                if(isTruck):
                    board[car.y + 2][car.x] = char
        print('\n'.join([''.join(['{:1}'.format(item) for item in row])
              for row in board]))
        flatBoard = [ y for x in board for y in x]
        stringBoard = ''.join(map(str,flatBoard))
        return hash(stringBoard)

main()



# method that goes through all cars and checks forward and backward up to n calling getStep on each potential tile
