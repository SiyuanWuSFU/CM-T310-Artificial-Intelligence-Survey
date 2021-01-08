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


from util import manhattanDistance
from game import Directions
import random, util

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

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
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
          
        Foodlist = newFood.asList()
        min_fdistance =100
        food_score =0
        beside_score = 0

        for ghost in newGhostStates:
            gdistance = manhattanDistance(newPos, successorGameState.getGhostPositions()[0])
            if gdistance ==1:
                beside_score =1

        for food in Foodlist:
            
            food_distance = manhattanDistance(newPos, food)
            if food_distance <= min_fdistance:
                min_fdistance = food_distance
                

        food_score = (1/float(min_fdistance))


        
        return successorGameState.getScore()+food_score - beside_score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
 
        agent_Pac = 0
        agent_Ghost = 1
        highest = float("-inf")
       


        def minimax(depth,turn,newState):
            agent_Number = newState.getNumAgents()
            maxscore = float("-inf")
            minscore = float("inf")
            if newState.isLose() or newState.isWin() or depth == self.depth:
                return self.evaluationFunction(newState)
             
            
            if turn == 0:
                for state in newState.getLegalActions(turn):
                    max_result = minimax(depth,1,newState.generateSuccessor(turn, state))
                    if max_result >= maxscore:
                        maxscore = max_result
                        
                return maxscore
            
            else:

                next_agent = turn+1
                if next_agent == agent_Number:
                    next_agent = 0
                    depth +=1
                
                    
                for state in newState.getLegalActions(turn):
                    min_result = minimax(depth,next_agent,newState.generateSuccessor(turn, state))


                    if min_result <= minscore:
                        minscore = min_result

                return minscore
                         
        for agentState in gameState.getLegalActions(0):
            final_Score = minimax(0, agent_Ghost, gameState.generateSuccessor(0, agentState))
            
            if final_Score> highest:
                highest = final_Score
                movement = agentState
                
        return movement
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agent_Pac = 0
        agent_Ghost = 1
        highest = float("-inf")
        max_score = float("-inf")
        min_score = float("inf")
       
        def minimax_p(depth,turn,newState,p_max,p_min):
            maxscore = float("-inf")
            minscore = float("inf")
       
            agent_Number = newState.getNumAgents()

            if newState.isLose() or newState.isWin() or depth == self.depth:
                return self.evaluationFunction(newState)
             
            
            if turn == 0:
                for state in newState.getLegalActions(turn):
                    max_result = minimax_p(depth,1,newState.generateSuccessor(turn, state),p_max,p_min)
                        



                    if max_result > maxscore:
                        maxscore = max_result
                    if max_result>p_min:
                        return max_result
                    p_max = max(p_max,max_result)

                return maxscore
            
            else:

                next_agent = turn+1
                if next_agent == agent_Number:
                    next_agent = 0
                    depth +=1
                
                    
                for state in newState.getLegalActions(turn):
                    min_result = minimax_p(depth,next_agent,newState.generateSuccessor(turn, state),p_max,p_min)


                    if min_result < minscore:
                        minscore = min_result
                    if min_result<p_max:
                        return min_result
                    p_min = min(p_min,min_result)

                        

                return minscore
                         
        for agentState in gameState.getLegalActions(0):
            final_Score = minimax_p(0, agent_Ghost, gameState.generateSuccessor(0, agentState),max_score,min_score)
            
            if final_Score> highest:
                highest = final_Score
                movement = agentState
            if final_Score>min_score:
                return final_Score
            max_score = max(final_Score,max_score)
                
        return movement
            
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        agent_Pac = 0
        agent_Ghost = 1
        highest = float("-inf")
       
        def minimax_exp(depth,turn,newState):
            exp = 0
            agent_Number = newState.getNumAgents()
            maxscore = float("-inf")
            minscore = float("inf")
            if newState.isLose() or newState.isWin() or depth == self.depth:
                return self.evaluationFunction(newState)
             
            
            if turn == 0:
                for state in newState.getLegalActions(turn):
                    max_result = minimax_exp(depth,1,newState.generateSuccessor(turn, state))
                    if max_result >= maxscore:
                        maxscore = max_result
                        
                return maxscore
            
            else:

                next_agent = turn+1
                if next_agent == agent_Number:
                    next_agent = 0
                    depth +=1
                
                    
                for state in newState.getLegalActions(turn):
                    min_result = minimax_exp(depth,next_agent,newState.generateSuccessor(turn, state))
                    exp+= min_result

  #                  if min_result <= minscore:
 #                       minscore = min_result

                return exp
                         
        for agentState in gameState.getLegalActions(0):
            final_Score = minimax_exp(0, agent_Ghost, gameState.generateSuccessor(0, agentState))
            
            if final_Score> highest:
                highest = final_Score
                movement = agentState
                
        return movement
        util.raiseNotDefined()








        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
 
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    pellet = currentGameState.getCapsules()
    Foodlist = newFood.asList()
    min_fdistance =100
    min_pdistance = 100
    food_score =0
    beside_score = 0
    ghost_score = 0
    pellet_score = 0
    
    for ghost in newGhostStates:
        gdistance = manhattanDistance(newPos, currentGameState.getGhostPositions()[0])
        if gdistance ==1:
            beside_score =5
        elif gdistance!=0:
            ghost_score +=( 1/float(gdistance))

    for food in Foodlist:
            
        food_distance = manhattanDistance(newPos, food)
        if food_distance <= min_fdistance:
            min_fdistance = food_distance

    pellet_score = len(pellet)
        



    food_score = (1/float(min_fdistance))

    total_score = food_score - beside_score-ghost_score-pellet_score
        
    return currentGameState.getScore()+total_score
        

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

