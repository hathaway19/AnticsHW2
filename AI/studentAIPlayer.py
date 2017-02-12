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
        super(AIPlayer,self).__init__(inputPlayerId, "SearchAI")

        self.statusOfGame = gameIsStillRunning

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
        # temp variable to test the values evaluation method returns
        #cur = evaluation(self, currentState)

        #dfdf = self.compileListOfNodes(currentState)
        tempVariable = self.nodeExpand(currentState, 0)
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0, len(moves) - 1)];

        # don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0, len(moves) - 1)];

        return selectedMove
    
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

        # Variables to hold the player's Ids
        me = currentState.whoseTurn
        opponent = (currentState.whoseTurn + 1) % 2
        # Gets both player's inventories
        myInv = getCurrPlayerInventory(currentState)
        oppInv = currentState.inventories[opponent]

        # Variables to hold the number of ants on the board and the one's that belong to us
        antCountOurs = float(len(getAntList(currentState, me,
                                            (QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER,))))
        allAntCount = float(len(getAntList(currentState, opponent,
                                           (QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER,))))

        # Variables to hold our and our opponent's worker ants
        myWorkers = getAntList(currentState, me, (WORKER,))
        oppWorkers = getAntList(currentState, opponent, (WORKER,))

        # Scoring method: Get the ratio of ants that belong to us
        # Weight: 30%
        ourRank = (antCountOurs / allAntCount) * 3 / 7

        # Scoring method: Adds score based on ratio of food we control compared to opponent
        # Weight: 45%
        # Adds 22.5% of score if we have same amount of food as opponent
        if myInv.foodCount == oppInv.foodCount:
            ourRank += 0.225
        else:
            ourRank += (myInv.foodCount / (myInv.foodCount + oppInv.foodCount)) * 9 / 20

        # Finds and compares the amount of food each player is carrying
        count = 0
        # Goes through all of our workers to see amount of food that's being carried
        for worker in myWorkers:
            if worker.carrying:
                count += 1
        grabbedFoodOurs = float(count)
        # # Goes through all of our opponents' workers to see amount of food that's being carried
        for worker in oppWorkers:
            if worker.carrying:
                count += 1
        grabbedFoodOpp = float(count)

        # Scoring method: Add to score depending on amount of food being carried
        # Weight: 20%
        # If tied, we get half the weight, 10%
        if grabbedFoodOurs == grabbedFoodOpp:
            ourRank += .1
        # Otherwise we add based on ratio of us versus opponents' food being carried
        else:
            ourRank += (grabbedFoodOurs / (grabbedFoodOurs + grabbedFoodOpp)) * 1 / 5

        print "ourRank: ", ourRank
        # Returns the rank our AI currently scored (a double)
        return ourRank

    ##
    # nodeExpand
    #
    def nodeExpand(self, currentState, depth):
        depthLimit = 0
        state = currentState
        allMoves = listAllLegalMoves(state)
        rankList = []

        allMovesList = []
        for move in allMoves:
            childNode = getNextState(state, move)
            rank = self.evaluation(childNode)
            if rank == 1.0:
                return move
            if depth < depthLimit:
                self.nodeExpand(childNode, depth + 1)
            else:
                pass
            rankList.append(rank)
            allMovesList.append(move)

        overallEval = self.getTheBestMove(rankList)

        if depth == 0:
            return allMovesList[overallEval]
        else:
            return allMovesList[overallEval]

    def getTheBestMove(self, rankList):
        return rankList.index(max(rankList))

    def compileListOfNodes(self, currentState):
        # A copy of the current state
        state = currentState
        allMoves = listAllLegalMoves(state)

        listOfAllMoveNodes = {}

        for move in allMoves:
            key = str(move)
        listOfAllMoveNodes['df'] = Node(state, move)
        listOfAllMoveNodes['dfdfd'] = Node(state, move)
        print listOfAllMoveNodes
        #listOfAllMoveNodes['df'] = Node(state, move)

        return listOfAllMoveNodes
#         return key
# #ToDo: Implement a dictionary (look that up)
# #It could take: key: coordinate value: node class (create a class for a single node
#
class Node:
    def __init__(self, state, move):
        # The move it took to reach a given state
        self.move = move
        self.newState = getNextState(state, move)
        #self.score = AIPlayer.evaluation(self, self.newState)