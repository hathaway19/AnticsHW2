  # -*- coding: latin-1 -*-
import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *

#Constants
currentPlayerWon = 1
currentPlayerLost = -1
gameIsStillRunning = 0
Depth_Limit = 2

##
# Authors: Justin Hathaway, Logan Simpson
#
# Assignment: Homework #2: Search AI
#
# Due Date: Febuary 13th, 2017
#
# Description: This class interacts with the rest of the game
# to make a search AI. This search AI checks the surrounding states resulting from
# different moves and makes a move based on the best scores from those states.
##

##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "TheSearchForFood")

        # Variable to know that the game is still running
        self.statusOfGame = gameIsStillRunning

        self.rankList = []
        self.allMoveList = []

    ##
    #getPlacement
    #
    #Description: The getPlacement method corresponds to the
    #action taken on setup phase 1 and setup phase 2 of the game.
    #In setup phase 1, the AI player will be passed a copy of the
    #state as currentState which contains the board, accessed via
    #currentState.board. The player will then return a list of 11 tuple
    #coordinates (from their side of the board) that represent Locations
    #to place the anthill and 9 grass pieces. In setup phase 2, the player
    #will again be passed the state and needs to return a list of 2 tuple
    #coordinates (on their opponent's side of the board) which represent
    #Locations to place the food sources. This is all that is necessary to
    #complete the setup phases.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is
    #       requesting a placement from the player.(GameState)
    #
    #Return: If setup phase 1: list of eleven 2-tuples of ints -> [(x1,y1), (x2,y2),…,(x10,y10)]
    #       If setup phase 2: list of two 2-tuples of ints -> [(x1,y1), (x2,y2)]
    ##
    def getPlacement(self, currentState):
        # Resets the variable to check if someone won
        self.statusOfGame = gameIsStillRunning

        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: The getMove method corresponds to the play phase of the game 
    #and requests from the player a Move object. All types are symbolic 
    #constants which can be referred to in Constants.py. The move object has a 
    #field for type (moveType) as well as field for relevant coordinate 
    #information (coordList). If for instance the player wishes to move an ant, 
    #they simply return a Move object where the type field is the MOVE_ANT constant 
    #and the coordList contains a listing of valid locations starting with an Ant 
    #and containing only unoccupied spaces thereafter. A build is similar to a move 
    #except the type is set as BUILD, a buildType is given, and a single coordinate 
    #is in the list representing the build location. For an end turn, no coordinates 
    #are necessary, just set the type as END and return.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is 
    #       requesting a move from the player.(GameState)   
    #
    #Return: Move(moveType [int], coordList [list of 2-tuples of ints], buildType [int]
    ##
    def getMove(self, currentState):
        # Empty the lists that hold the evaluation values and the moves
        self.rankList = []
        self.allMoveList = []

        # Tries to get a move
        try:
            return self.nodeExpand(currentState, 0)
        # If it fails, the move ends
        except:
            print "method nodeExpand didn't return a valid move. Not moving"
            return Move(END,None,None)
    ##
    #getAttack
    #Description: The getAttack method is called on the player whenever an ant completes
    #a move and has a valid attack. It is assumed that an attack will always be made
    #because there is no strategic advantage from withholding an attack. The AIPlayer
    #is passed a copy of the state which again contains the board and also a clone of
    #the attacking ant. The player is also passed a list of coordinate tuples which
    #represent valid locations for attack. Hint: a random AI can simply return one of
    #these coordinates for a valid attack.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is requesting
    #       a move from the player. (GameState)
    #   attackingAnt - A clone of the ant currently making the attack. (Ant)
    #   enemyLocation - A list of coordinate locations for valid attacks (i.e.
    #       enemies within range) ([list of 2-tuples of ints])
    #
    #Return: A coordinate that matches one of the entries of enemyLocations. ((int,int))
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #Description: The last method, registerWin, is called when the game ends and simply 
    #indicates to the AI whether it has won or lost the game. This is to help with 
    #learning algorithms to develop more successful strategies.
    #
    #Parameters:
    #   hasWon - True if the player has won the game, False if the player lost. (Boolean)
    ##
    def registerWin(self, hasWon):
        if hasWon:
            self.statusOfGame = currentPlayerWon
        else:
            self.statusOfGame = currentPlayerLost
        pass

    def pickBetweenCoords(self, currentState, startCoords, endGoals):
        closestGoal = endGoals[0]
        distToClosestGoal = approxDist(startCoords, closestGoal)

        for goalCoord in endGoals:
            distFromCurrentGoal = approxDist(startCoords, goalCoord)
            if distFromCurrentGoal < distToClosestGoal:
                distToClosestGoal = distFromCurrentGoal
                closestGoal = goalCoord
        return goalCoord

    ##
    # evaluation
    # Description: This method evaluates the game state and sees if the AI
    # is currently winning or loosing against its opponent.
    #
    # Parameters:
    #   currentState - The current state of the game.
    #
    # Returns: A double that shows how well the AI is performing at a given state. 1.0
    # means the AI has already won, 0.0 means the AI has already lost. Anything in the middle
    # means that the game is still running with everything above 0.5 meaning the AI is winning
    # and anything lower than 0.5 means the AI is loosing.
    ##
    def evaluation(self, currentState):
        # Checks to see if the game is already over
        # Returns 1.0 if our AI has already won
        if self.statusOfGame == currentPlayerWon:
            return 1.0
        # Returns 0.0 if our AI has already lost
        elif self.statusOfGame == currentPlayerLost:
            return 0.0

        # Gets my id
        me = currentState.whoseTurn
        # Gets my inventory
        myInv = getCurrPlayerInventory(currentState)

        # Variable to hold all 4 foods
        myFoods = getConstrList(currentState, None, (FOOD,))
        # Variable to hold the food locations from myFoods
        myFoodCoords = []
        # Adds each foods coordinates to the coordinate list
        for food in myFoods:
            myFoodCoords.append(food.coords)

        # Variable to hold a list of my constructs (the anthill and the tunnel)
        myConstructs = getConstrList(currentState, me, (ANTHILL, TUNNEL,))
        # Variable to hold the coordinates of the constructs in myConstructs
        myConstructsCoords = []
        # Adds both the tunnel and the anthill coordinates to the list of construct coordinates
        myConstructsCoords.append(myConstructs[0].coords)
        myConstructsCoords.append(myConstructs[1].coords)

        # Variable to hold a list of my workers
        myWorkers = getAntList(currentState, me, (WORKER,))

        # Variable to hold total amount of distance ants have from their goal
        rankFromDistToGoal = 0.0

        # Calculate the rank gained from food in inventory
        rankFromFood = ((float(myInv.foodCount)) / float(FOOD_GOAL)) * 5.0

        # Goes through all the workers and trys to guide them to food or constructs through use of score
        for worker in myWorkers:
            # If the worker is carrying, they should head to tunnel or anthill
            if worker.carrying:
                # Finds the closest construct (tunnel or anthill) and guides ant there
                myClosestConstruct = self.pickBetweenCoords(currentState, worker.coords, myConstructsCoords)
                # Finds the distance from the ant to the construct
                distToClosestConstruct = stepsToReach(currentState, worker.coords, myClosestConstruct)
                # Begins to calculate how it will effect overall score
                rankFromDistToGoal += distToClosestConstruct / 2.0
            # Worker isn't carrying, move towards a food source
            else:
                # Finds closest food and sets path
                closestFood = self.pickBetweenCoords(currentState, worker.coords, myFoodCoords)
                # Gets food distance from ant
                foodDistance = stepsToReach(currentState, worker.coords, closestFood)
                # Calculates distance into score
                rankFromDistToGoal += foodDistance / 2.0

        # There's no workers, score goes down (since it's necessary)
        notEnoughWorkersResult = 0.0
        # If there's no workers, no distance goal necessary. Need to build more
        if len(myWorkers) < 1:
            notEnoughWorkersResult = 0.2
            rankFromDistToGoal = 0.0
        else:
            rankFromDistToGoal = 1.0 - rankFromDistToGoal / (len(myWorkers) * 20.00)

        if rankFromDistToGoal < 0.0:
            rankFromDistToGoal = 0.0

        # weight all considerations - higher multipliers = higher weight
        result = (rankFromFood + rankFromDistToGoal - notEnoughWorkersResult) / 5.00

        # Make sure the rank stays in the boundaries that make sense
        # (can't be 1 or 0 yet since we've yet to win or loose)
        print result
        return result

    ##
    # nodeExpand
    #
    ##
    # nodeExpand
    #
    def nodeExpand(self, currentState, depth):
        # A copy of the current state
        state = currentState
        # Compiles a list of all legal moves in the current state
        allMoves = listAllLegalMoves(state)

        rankList = []
        allMovesList = []

        for move in allMoves:
            childNode = getNextState(state, move)
            rank = self.evaluation(childNode)
            if rank == 1.0:
                return move
            if depth < Depth_Limit:
                pass
                # self.nodeExpand(childNode, depth + 1)
            else:
                pass
            rankList.append(rank)
            allMovesList.append(move)
            self.rankList.append(rankList)
            self.allMoveList.append(allMovesList)

        overallEval = self.getTheBestMove(rankList)

        if depth == 0:
            return allMovesList[overallEval]
        else:
            return allMovesList[overallEval]

    # Helper method to find the max value in a given list
    def getTheBestMove(self, rankList):
        return rankList.index(max(rankList))
