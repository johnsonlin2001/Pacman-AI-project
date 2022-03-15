# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from curses import newpad
import dis
from re import A
from shutil import move
from util import manhattanDistance
from game import Directions
import random, util
import statistics

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)
        legalMoves.remove("Stop")

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        score=0
        successorGameState = currentGameState.generatePacmanSuccessor(self.index, action)
        newPos = successorGameState.getPacmanPosition(self.index)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        ghostStates = currentGameState.getGhostStates()
        newGhostPositions = successorGameState.getGhostPositions()
        currentPos = currentGameState.getPacmanPosition(self.index)
        distances = []
        for position in newGhostPositions:
            distances.append(manhattanDistance(newPos,position))
        
        nearestGhostDis = min(distances)
        if(nearestGhostDis<2):#very dangerous
           score-=100
        elif(nearestGhostDis<3):#quite dangerous
           score-=50
        elif(nearestGhostDis<4):#less dangerous
           score-=25
        elif(nearestGhostDis<5):#less dangerous
            score-=10
        food = successorGameState.getFood()
        foodCoordinates = food.asList()#generates a list of coordinates with remaining food
        distancesToFood = []
        #print(pacPos)
        foodRemaining = successorGameState.getNumFood()
        for foodpos in foodCoordinates:
            distancesToFood.append(manhattanDistance(foodpos,newPos))
        if(foodRemaining>=1):
            nearestFoodDis = min(distancesToFood)
            score+=10/nearestFoodDis
        if(foodRemaining<3):
            score+=25/nearestFoodDis
            score=score

        currentFoodCount = currentGameState.getNumFood()
        newFoodCount = successorGameState.getNumFood()
        if(newFoodCount<currentFoodCount):
            score+=5

        remainingCapPos = successorGameState.getCapsules() #positions of remaining capsules
        numRemainingCaps = len(remainingCapPos) #number of capsules remaining
        #score-=25*numRemainingCaps #the less capsules remaining, the better
        distancesToCaps = []
        #score += 0.1*intgamestate.getScore()
        for cappos in remainingCapPos:
            distancesToCaps.append(manhattanDistance(cappos,newPos))
            #print(manhattanDistance(cappos,pacPos))
        if(numRemainingCaps>=1):
            nearestCapDistance = min(distancesToCaps)
            score += 20/nearestCapDistance


        capsules = currentGameState.getCapsules()
        newcapsules = successorGameState.getCapsules()
        closestCapsuleDis = 999999
        closestCapsulePos = (0,0)
        for cap in capsules:
            olddistocap = manhattanDistance(currentPos,cap)
            if(olddistocap<closestCapsuleDis):
                closestCapsuleDis=olddistocap
                closestCapsulePos=cap
        olddistocap=manhattanDistance(closestCapsulePos,currentPos)
        newdistocap = manhattanDistance(closestCapsulePos,newPos)
        print(olddistocap)
        print(newdistocap)
        foods = currentGameState.getFood()
        if(len(newcapsules)>=1):
            
            if(newdistocap<olddistocap):
                #score+=1000
                print("YESSS")
        elif(newFoodCount==currentFoodCount):
            closestFoodPos = (0,0)
            closesfoodDis = 99999
            #for x in range(0,len(foods)):
            #    for y in range(0,len(foods[x])):
            #        if(currentGameState.hasFood(x,y)):
            #            if(manhattanDistance((x,y),currentPos)<closesfoodDis):
            #                closesfoodDis=manhattanDistance((x,y),currentPos)
            #                closestFoodPos=(x,y)
            #if(manhattanDistance(closestFoodPos,newPos)<closestFoodPos):
            #    score+=5
            #get closer to next available food
        if((len(capsules)-len(newcapsules))>=1):
            score+=10*(newFoodCount)
        
        #if len(newFood.asList()):
        #    fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
        #else:
        #    fooddist = 0
        print(action)
        print(score)
        return score

def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()[index]

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index = 0, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = index # Pacman is always agent index 0
        self.evaluationFunction = lambda state:util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)
    






class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    You implementation here
    """
    def heuristic(self,gamestate):
        if(gamestate.isWin()):
            return 99999999
        elif(gamestate.isLose()):
            return -9999999
        score = 0
        index = self.index #index of pacman
        pacPos = gamestate.getPacmanPosition(index) #position of pacman
        foodRemaining = gamestate.getNumFood() #amount of food remaining in the game
        #score -= 2*foodRemaining #the less food remaining, the better
        food = gamestate.getFood()
        foodCoordinates = food.asList()#generates a list of coordinates with remaining food
        distancesToFood = []
        #print(pacPos)
        for foodpos in foodCoordinates:
            distancesToFood.append(manhattanDistance(foodpos,pacPos))
        if(foodRemaining>=1):
            nearestFoodDis = min(distancesToFood)
            score+=10/nearestFoodDis
        if(foodRemaining<3):
            score+=25/nearestFoodDis
            score=score
        ghostPositions = gamestate.getGhostPositions()
        distancesToGhost = []
        for ghostpos in ghostPositions:
            distancesToGhost.append(manhattanDistance(ghostpos,pacPos))
            
        nearestGhostDis = min(distancesToGhost)

        if(nearestGhostDis<2):#very dangerous
           score-=50
        elif(nearestGhostDis<3):#quite dangerous
           score-=25
        elif(nearestGhostDis<4):#less dangerous
           score-=10
        #elif(nearestGhostDis<5):#less dangerous
        #    score-=10
        averageGhostdis = statistics.mean(distancesToGhost)
        #score +=2*averageGhostdis
        remainingCapPos = gamestate.getCapsules() #positions of remaining capsules
        numRemainingCaps = len(remainingCapPos) #number of capsules remaining
        #score-=25*numRemainingCaps #the less capsules remaining, the better
        distancesToCaps = []
        #score += 0.1*intgamestate.getScore()
        for cappos in remainingCapPos:
            distancesToCaps.append(manhattanDistance(cappos,pacPos))
            #print(manhattanDistance(cappos,pacPos))
        if(numRemainingCaps>=1):
            nearestCapDistance = min(distancesToCaps)
            score += 30/nearestCapDistance #incentivize capsules before food raised to 30 from 20
        score+=100/(foodRemaining+1)
        score+=250/(numRemainingCaps+1) #raised from 200 to 250
        score+=scoreEvaluationFunction(gamestate,index) #incentivize eating food faster and avoiding idle states

        return score






    #My implementation extends the minmax algo for multiple minimizing agents. By splitting the search into three functions, I'm
    #able to compute the min and max scores for each action and then return the action with the highest score.
    
    def minimumSearchAgent(self,gamestate,index,depth):
        if((gamestate.isWin())): #depth reached or game is over
            return 9999999
        if(gamestate.isLose()):
            return -999999
        if(depth==self.depth):
            return self.heuristic(gamestate) #must cut search slightly early to avoid timeout on gradescope
        lowestScore = float('inf') # set the initial lowest score to infinity so that all scores are worse
        nextagent = ""
        for i in range(0,len(gamestate.getLegalActions(index))):
            nextState = gamestate.generateSuccessor(index,gamestate.getLegalActions(index)[i])
            if(index<gamestate.getNumAgents()-1): #iterate for next ghost
                lowestScore = min(lowestScore,self.minimumSearchAgent(nextState,index+1,depth))
            elif(index>=gamestate.getNumAgents()-1): #iterated for all ghosts, return to maxsearch
                lowestScore = min(lowestScore,self.maximumSearchAgent(nextState,0,depth)) #pass control back to maxsearch
        return lowestScore


    def maximumSearchAgent(self,gamestate,index,depth):
        if((gamestate.isWin())): #depth reached or game is over
            return 9999999
        if(gamestate.isLose()):
            return -999999
        if(depth==self.depth):
            return self.heuristic(gamestate)
        greatestScore = float('-inf') #set the initial best score to negative infinity so all scores are better
            
        for i in range(0,len(gamestate.getLegalActions(self.index))):
            nextState = gamestate.generateSuccessor(index,gamestate.getLegalActions(self.index)[i])
            greatestScore = max(self.minimumSearchAgent(nextState,index+1,depth+1),greatestScore)
        return greatestScore 
    
    def minmaxSearch(self,gamestate,index,depth):
        bestScore = float('-inf') #initialize the initial best score to be better than all possible scores
        for i in range(0,len(gamestate.getLegalActions(index))):
            scores = []
            scoresandmoves = []
            nextstate = gamestate.generateSuccessor(index,gamestate.getLegalActions(index)[i]) #evaluate for all possible pacman moves
            if(nextstate.isWin()):
                return gamestate.getLegalActions(index)[i]
            currentGameScore = self.minimumSearchAgent(nextstate,index+1,depth) #pacman just moved so evaluate ghost actions next
            scores.append(currentGameScore)
            scoresandmoves.append([currentGameScore,move])
            if(currentGameScore>bestScore):     #choose the best state at the end of the search
                bestScore, bestmove=currentGameScore, gamestate.getLegalActions(index)[i]
            

        return bestmove,bestScore #return the move with the highest score and corresponging score

 





    def getAction(self, gameState):
        index = self.index # pacman index
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        Some functions you may need:
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legalMoves = gameState.getLegalActions(agent)
        legalNextState = [gameState.generateSuccessor(agent, action)
                          for action in legalMoves]
        """
        "*** YOUR CODE HERE ***"
        #print("Number of Pacmans:", gameState.getNumPacman(), ", Number of ghosts:", gameState.getNumGhosts())
        pos = gameState.getPacmanPosition(self.index)
        legalmoves = gameState.getLegalActions(self.index)
        for move in legalmoves:
            if(gameState.generateSuccessor(self.index,move).isWin()):
                return move
        

        return self.minmaxSearch(gameState,index,1)[0]
        


        util.raiseNotDefined()

        
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




