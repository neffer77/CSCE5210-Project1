# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# algorith which decide the next action
class agentFunction:
    
    
    
    def __init__(self, agentLocation, percept, customerOrder,actuator,randRange,basket,visited):
        self.location = agentLocation
        self.percept = percept
        self.order = customerOrder
        self.orderShelfLocations = []
        self.actuator = actuator
        self.random = randRange
        self.basket = basket
        self.visited = visited
        #need to collect and check if an item has already been collected
        
    
    def addShelfLocation(self,location):
        if (location not in self.orderShelfLocations):
            self.orderShelfLocations.append(location)
        
    def removeShelfLocation(self,location,fake):
        loc = location.copy()
        c = 0
        d = -1
        for i in self.orderShelfLocations:
            if (i[0] == loc[0] and i[1] == loc[1]):
                d = c
            c = c + 1
        if (d != -1):
            self.orderShelfLocations.pop(d)
            if (fake):
                return True
            
        return False
            
    
    def getCurrentShelfLocation(self):
        return self.currentShelf
    
    def setCurrentShelfLocation(self,location):
        self.currentShelf = location
    #how to handle movement
    #have a current movement?
    def determineIfOnFakeShelf(self):
        location = self.percept.getCurrentLocation()
        if (self.percept.percepts['current']['value'] == -1):
            return self.removeShelfLocation(location,True)

    #Loads percepts and decides where to move
    
    #Questions: How do I keep track of shelves already collected items from?
    def determineAction(self):
        print("onOrderShelf: " + str(self.percept.onOrderShelf()))
        
        #is agent on top of a Shelf?
        if (self.percept.onOrderShelf()):
            self.actuator.collectItem()
            self.removeShelfLocation(self.percept.getCurrentLocation(), False)
            self.currentShelf = ""
        print("shelf count: " + str(self.percept.shelfCount(self.basket.getCoords())))
        
        fake = self.determineIfOnFakeShelf()
        #Are there any shelves around me?
        if (self.percept.shelfCount(self.basket.getCoords()) == 0):
            
            #Have I detected any shelves in the past that I have not collected from?
            if (len(self.orderShelfLocations) == 0):
                
                #Random move
                print("Random Move")
                self.bestMove(self.percept.getCurrentLocation())
            else:
                
                #Is there a current shelf I am targeting?
                if (self.currentShelf != ""):
                    if (fake):
                        self.currentShelf = self.orderShelfLocations[0]
                    print("Moving Towards: " + str(self.currentShelf))
                    print("Order Shelf Locations: " +  str(self.orderShelfLocations))
                    self.actuator.move(self.currentShelf)
                    
                #Load shelf from list of shelves that need to be visited
                else:
                    print("Previous Order Shelf Locations: " +  str(self.orderShelfLocations))
                    self.setCurrentShelfLocation(self.orderShelfLocations[0])
                    
                    print("Moving Towards: " + str(self.currentShelf))
                    print("Order Shelf Locations: " +  str(self.orderShelfLocations))
                    self.actuator.move(self.currentShelf)
                    
        #One or more shelves are around the agent
        elif (self.percept.shelfCount(self.basket.getCoords()) >= 1):
            print("Shelf Count Detected: " + str(self.percept.shelfCount(self.basket.getCoords())))
            #get the shelf Coodinates
            shelfLocations = self.percept.getShelfLocations(self.basket.getCoords())
            
            print("Previous Order Shelf Locations: " +  str(self.orderShelfLocations))    
            #add cooordinates to list of shelves that need to be visited
            
            for i in shelfLocations:
                c = 0 
                for j in self.orderShelfLocations:
                    if (i[0] == j[0] and i[1] == j[1]):
                            c = c-1
                    c = c + 1
                if (c == len(self.orderShelfLocations)):
                    self.addShelfLocation(i)
                
            
            #Set next shelf that needs to be visited
            self.currentShelf = self.orderShelfLocations[0]
            
            print("Order Shelf Locations: " +  str(self.orderShelfLocations))
            
            print("Moving Towards: " + str(self.currentShelf))
            #move to that shelf
            self.actuator.move(self.currentShelf)
            
    
    def determineRandomMove(self):
        success = False
        #add a best move function, determines if there are unvisited options and if not pick random
        while not success:
            move = self.random.randint(0,3)
            print(self.actuator.movePossible('left'))
            if (move == 0):
                if (self.actuator.movePossible('left')):
                    self.actuator.left()
                    success = True
            elif (move == 1):
                if (self.actuator.movePossible('right')):
                    self.actuator.right()
                    success = True
            elif (move == 2):
                if (self.actuator.movePossible('up')):
                    self.actuator.up()
                    success = True
            elif (move == 3):
                if (self.actuator.movePossible('down')):
                    self.actuator.down()
                    success = True
            
    def bestMove(self,location):
        
        moves = []
        if (self.actuator.movePossible('left')):
            left = location.copy()
            left[1] = left[1]-1
            if(not self.visited.hasVisited(left)):
                   moves.append('left')
        if (self.actuator.movePossible('right')):
            right = location.copy()
            right[1] = right[1]+1
            if(not self.visited.hasVisited(right)):
                   moves.append('right') 
        if (self.actuator.movePossible('up')):
            up = location.copy()
            up[0] = up[0]-1
            if(not self.visited.hasVisited(up)):
                   moves.append('up')
        if (self.actuator.movePossible('down')):
            down = location.copy()
            down[0] = down[0]+1
            if(not self.visited.hasVisited(down)):
                   moves.append('down')
        
        if (len(moves) == 0):
            self.determineRandomMove()
        else:
            bestMoveNum = self.random.randint(0,(len(moves)-1))
            if (moves[bestMoveNum] == 'left'):
                self.actuator.left()
            elif (moves[bestMoveNum] == 'right'):
                self.actuator.right()
            elif (moves[bestMoveNum] == 'up'):
                self.actuator.up()
            elif (moves[bestMoveNum] == 'down'):
                self.actuator.down()
            else:
                print("Error")
    #returns true if customer order is complete
    def hasCollectedAllItems(self):
        if (len(self.order) == len(self.basket.getBasket())):
            print("WIN!: " + str(self.basket.getBasket()))
            return True
        return False
 
#import libraries
import numpy as np
import random
#Generates warehouse environment
class Environment:
    
    def __init__(self):
        self.line_sep = '\n~~~~~~~~~~~~~~~~~~\n'

        #Define the environment
        self.environment_rows = 6
        self.environment_columns = 6
        self.item_A = 'A'
        self.item_B = 'B'
        self.item_C = 'C'
        self.item_D = 'D'
        self.item_E = 'E'
        self.item_F = 'F'
        self.item_G = 'G'
        self.item_H = 'H'
        self.item_I = 'I'
        self.item_J = 'J'
        
    def print_grid(self,rewards,ordered_items):
        #print itemes ordered
        print(self.line_sep)

        print('Items ordered:',ordered_items)

        print (self.line_sep)
            
        #Print rewards matrix
        for row in rewards:
            print(row)
            
        print(self.line_sep)
    
    def genRandOrder(self):
        x = random.randint(1,10)
        #Give items their single character name
        items = [self.item_A,self.item_B, self.item_C, self.item_D, self.item_E, self.item_F, self.item_G, self.item_H, self.item_I, self.item_J]
        
        #Generate random orders containing items A-J
        ordered_items = random.sample(items,x)
        return ordered_items
    
    #Define rewards
    def buildEnv(self):
        rewards = np.full((self.environment_rows, self.environment_columns), -1)
        ordered_items = self.genRandOrder()
        shelfArray = np.full((self.environment_rows, self.environment_columns), "")
        
        if self.item_A in ordered_items:
                rewards [1,1] = 3
                shelfArray[1,1] = 'A'
        else:
            rewards[1,1] = -1

        if self.item_B in ordered_items:
            rewards [2,2] = 3
            shelfArray[2,2] = 'B'
        else:
            rewards[2,2] = -1

        if self.item_C in ordered_items:
            rewards [3,1] = 3
            shelfArray[3,1] = 'C'
        else:
            rewards[3,1] = -1

        if self.item_D in ordered_items:
            rewards [0,2] = 3
            shelfArray[0,2] = 'D'
        else:
            rewards[0,2] = -1

        if self.item_E in ordered_items:
            rewards [2,0] = 3
            shelfArray[2,0] = 'E'
        else:
            rewards[2,0] = -1

        if self.item_F in ordered_items:
            rewards [4,2] = 3
            shelfArray[4,2] = 'F'
        else:
            rewards[4,2] = -1
            
        if self.item_G in ordered_items:
            rewards [1,4] = 3
            shelfArray[1,4] = 'G'
        else:
            rewards[1,4] = -1

        if self.item_H in ordered_items:
            rewards [4,5] = 3
            shelfArray[4,5] = 'H'
        else:
            rewards[4,5] = -1

        if self.item_I in ordered_items:
            rewards [2,4] = 3
            shelfArray[2,4] = 'I'
        else:
            rewards[2,4] = -1
            
        if self.item_J in ordered_items:
            rewards [5,3] = 3
            shelfArray[5,3] = 'J'
        else:
            rewards[5,3] = -1
        
        return rewards,ordered_items,shelfArray

    #need to build random layout case after static shelf testing to make sure agen works in any shelf situation.
    #def randomShelfOrganization(self):

#Performs action determined by agent function left, right, up, down, collect item        
class actuator:
    def __init__(self,percept,basket,env,moveMem,rand):
        self.coord = percept.getCurrentLocation()
        self.percept = percept
        self.basket = basket
        self.env = env
        self.moveMem = moveMem
        self.rand = rand
        
    def collectItem(self):
        self.coord = self.percept.getCurrentLocation()
        item = self.coord.copy()
        if (self.env[item[0]][item[1]] != ''):
            if (self.env[item[0]][item[1]] not in self.basket.getBasket()):
                self.basket.addToBasket(self.env[item[0]][item[1]])
                self.basket.addCoords(item)
                print("Collected Item: " + str(self.env[item[0]][item[1]]) + " Basket: " + str(self.basket.getBasket()))
    def move(self,nextShelf):
        potentialMoves = []
        self.coord = self.percept.getCurrentLocation()
        print("Shelf We are Trying to Approach: " + str(nextShelf))
        print("Current Coords: " + str(self.coord))
        if(nextShelf[1] < self.coord[1]):
            left = self.coord.copy()
            left[1] = left[1]-1
            potentialMoves.append(left)
        if(nextShelf[1] > self.coord[1]):
            right = self.coord.copy()
            right[1] = right[1]+1
            potentialMoves.append(right)
        if(nextShelf[0] < self.coord[0]):
            up = self.coord.copy()
            up[0] = up[0]-1
            potentialMoves.append(up)
        if(nextShelf[0] > self.coord[0]):
            down = self.coord.copy()
            down[0] = down[0]+1
            potentialMoves.append(down)
        notVisited = []
        for i in potentialMoves:
            if (not self.moveMem.hasVisited(str(i))):
                notVisited.append(i)
        print("Potential Moves Not Visited Yet" + str(notVisited))        
        print("Potential Moves Added: " + str(potentialMoves))
        if (len(notVisited) == 0):
            move = potentialMoves[self.rand.randint(0,(len(potentialMoves)-1))]
            self.percept.setCurrentLocation(move)
        elif (len(notVisited) == 2):
            self.percept.setCurrentLocation(notVisited[self.rand.randint(0,1)])
            self.addVisitedSpace(notVisited[0])
            self.addVisitedSpace(notVisited[1])
        elif (len(notVisited) == 1):
            self.percept.setCurrentLocation(notVisited[0])
            self.addVisitedSpace(notVisited[0])
        else:
            print("Error: more than two moves")
            
        
        
    def left(self):
        self.coord = self.percept.getCurrentLocation()
        left = self.coord.copy()
        left[1] = left[1]-1
        self.percept.setCurrentLocation(left)
        self.addVisitedSpace(left)
    def right(self):
        self.coord = self.percept.getCurrentLocation()
        right = self.coord.copy()
        right[1] = right[1]+1
        self.percept.setCurrentLocation(right)
        self.addVisitedSpace(right)
    def up(self):
        self.coord = self.percept.getCurrentLocation()
        up = self.coord.copy()
        up[0] = up[0]-1
        self.percept.setCurrentLocation(up)
        self.addVisitedSpace(up)
    def down(self):
        self.coord = self.percept.getCurrentLocation()
        down = self.coord.copy()
        down[0] = down[0]+1
        self.percept.setCurrentLocation(down)
        self.addVisitedSpace(down)
        
    def addVisitedSpace(self, coord):
        self.moveMem.addVisited(coord)
        
    def movePossible(self, move):
        self.coord = self.percept.getCurrentLocation()
        if move == 'left' and (self.coord[1]-1) < 0:
            return False
        if move == 'right' and (self.coord[1]+1) > 5:
            return False
        if move == 'up' and(self.coord[0]-1)  < 0:
            return False
        if move == 'down' and (self.coord[0]+1) > 5:
            return False
        return True


#determines current and surrounding locations, and values associated with it    
class percept:
    def __init__(self,currentLocation, envArray):
        self.percepts = dict(left=dict(coord=[],value=""), right=dict(coord=[],value=""), up=dict(coord=[],value=""), down=dict(coord=[],value=""), current=dict(coord=[],value=""))
        self.envArray = envArray
        self.setCurrentLocation(currentLocation)
        
    def determine(self):
        
        
        if (self.getCurrentLocation()[0] == 0):
            self.percepts["up"]["coord"] = []
            self.percepts["up"]["value"] = ""
        else:
            self.percepts["up"]["coord"] = [(self.percepts['current']['coord'][0]-1),self.percepts['current']['coord'][1]]
            self.percepts["up"]["value"] = self.envArray[self.percepts['up']['coord'][0]][self.percepts['up']['coord'][1]]
        
        if (self.getCurrentLocation()[0] == 5):
            self.percepts["down"]["coord"] = []
            self.percepts["down"]["value"] = ""
        else:
            self.percepts["down"]["coord"] = [(self.percepts['current']['coord'][0]+1),self.percepts['current']['coord'][1]]
            self.percepts["down"]["value"] = self.envArray[self.percepts['down']['coord'][0]][self.percepts['down']['coord'][1]]
        
        if (self.getCurrentLocation()[1] == 0):
            self.percepts["left"]["coord"] = []
            self.percepts["left"]["value"] = ""
        else:
            self.percepts["left"]["coord"] = [self.percepts['current']['coord'][0],(self.percepts['current']['coord'][1]-1)]
            self.percepts["left"]["value"] = self.envArray[self.percepts['left']['coord'][0]][self.percepts['left']['coord'][1]]
        
        if (self.getCurrentLocation()[1] == 5):
            self.percepts["right"]["coord"] = []
            self.percepts["right"]["value"] = ""
        else:
            self.percepts["right"]["coord"] = [self.percepts['current']['coord'][0],(self.percepts['current']['coord'][1]+1)]
            self.percepts["right"]["value"] = self.envArray[self.percepts['right']['coord'][0]][self.percepts['right']['coord'][1]]
        print("Current Percept: " + str(self.percepts))
        
        
        
    def onOrderShelf(self):
        if (self.percepts["current"]["value"] == 3):
            return True;
        return False
    
    def shelfCount(self, basket):
        count = 0
        for i in self.percepts:
            if self.percepts[i]["value"] == 3:
                if (i != 'current'):
                    if ((self.percepts[i]["coord"] not in basket)):
                        count = count + 1
        return count
        
    def getShelfLocations(self, basket):
        shelves = []
        for i in self.percepts:
            if self.percepts[i]["value"] == 3:
                if (self.percepts[i]["coord"] not in basket):
                    shelves.append(self.percepts[i]["coord"])
        return shelves
        
    def getPercepts(self):
        return self.percepts
    
    def setValue(self, key, value):
        self.percepts[key]['value'] = value
        
    def setCurrentLocation(self,coord):        
        self.percepts['current']['coord'] = coord
        self.percepts['current']['value'] = self.envArray[coord[0]][coord[1]]
        
    def getCurrentLocation(self):
        return self.percepts['current']['coord']  

#agent sensor which determines success of percept
class sensor:
    def __init__(self, random, agentlocation,percept):
        self.random = random
        self.agentlocation = agentlocation
        self.percept = percept
        
    def sensorRoll(self):
        roll = self.random.randint(1,10)
        if roll == 9:
            percepts = self.percept.getPercepts()
            percepts = self.setEmptyShelf()   
        elif roll == 10:
            percepts = self.percept.getPercepts()
            percepts = self.setShelf()
            
    
    #need the percept to be an array of dictionaries
    def setEmptyShelf(self):
        shelves = []
        for i in self.percept.getPercepts():
            if (self.percept.getPercepts()[i]['value'] == 3):
                if(i != 'current'):
                    shelves.append(i)
        if (len(shelves) > 0):  
            roll = self.random.randint(0,(len(shelves)-1))
            key = shelves[roll]
            self.percept.setValue(key, -1) 
    
    def setShelf(self):
        empty = []
        for i in self.percept.getPercepts():
            if (self.percept.getPercepts()[i]['value'] == -1):
                if(i != 'current'):
                    empty.append(i)
        if (len(empty) > 0):    
            roll = self.random.randint(0,(len(empty)-1))
            key = empty[roll]
            self.percept.setValue(key, 3) 
 
#collects score of one episode            
class stats:
    def __init__(self, env, percept):
        self.env = env
        self.percept = percept
        self.score = 0
        self.path = []
        
    def updateScore(self):
        location = self.percept.getCurrentLocation()
        value = self.env[location[0]][location[1]]
        self.score = self.score + value
        
    def getScore(self):
        return self.score
    
    def printScore(self):
        print("Score: " + str(self.score))
        
    def updatePath(self,coord):
        self.path.append(coord)
        
    def getPath(self):
        return self.path

#stores collected items
class basket:
    def __init__(self):
        self.basket = []
        self.coords = []
        
    def addToBasket(self,item):
        self.basket.append(item)
        
    def getBasket(self):
        return self.basket
    
    def addCoords(self,item):
        self.coords.append(item)
        
    def getCoords(self):
        return self.coords

#Tracks already visited locations    
class movementMemory:
    def __init__(self):
        self.visited = {}
        
    def addVisited(self, coord):
        self.visited[str(coord)] = True
    
    def hasVisited(self, coord):
        if str(coord) in self.visited.keys():
            return True
        return False
    
import random as rand
#main function
def main():
    
    #set up environment
    env = Environment()
    warehouse,ordered_items,shelfLocations = env.buildEnv()
    env.print_grid(warehouse,ordered_items)
    print(shelfLocations)
    
    
    #agentLocation starts at 0,0 in first episode
    
    #set up percept
    agentLocation = [0,0]
    prcpt = percept(agentLocation,warehouse)
    
    #determine surrounding tiles
    prcpt.determine()
    score = stats(warehouse,prcpt)
    score.updateScore()
    score.updatePath(agentLocation)
    
    #Roll for sensor Accuracy
    snsr = sensor(rand, agentLocation, prcpt)
    snsr.sensorRoll()
    
    #initiate empty basket of items
    currentCollected = basket()
    
    #initiate new movement memory
    moveMem = movementMemory()
    
    moveMem.addVisited(agentLocation)
    
    #initiate acutuator
    act = actuator(prcpt,currentCollected,shelfLocations,moveMem,rand)
    
    #initiate agent
    agent = agentFunction(agentLocation, prcpt, ordered_items,act,rand,currentCollected,moveMem)
    #need to purge fake list of visited when they visit the space
    while(not agent.hasCollectedAllItems()): 
        agent.determineAction()
        prcpt.determine()
        score.updateScore()
        score.updatePath(prcpt.getCurrentLocation().copy())
        snsr.sensorRoll()
    
    score.printScore()
    print(score.getPath())
        
       
    
    
if __name__ == "__main__":
    main()