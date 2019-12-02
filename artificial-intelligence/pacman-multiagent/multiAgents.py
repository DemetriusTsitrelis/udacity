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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        return successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        def minimax(state, depth, agent):
            if state.isLose() or state.isWin() or (depth == 0):
                return self.evaluationFunction(state), Directions.STOP

            nextAgent = (agent + 1) % numAgents
            if agent == self.index:  # Maximizing player
                v_value = float("-inf")
                v_action = Directions.STOP
                for action in state.getLegalActions(agent):
                    mm = minimax(state.generateSuccessor(agent, action), depth - 1, nextAgent)
                    if mm[0] > v_value:
                        v_value = mm[0]
                        v_action = action
                return v_value, v_action

            else:  # Minimizing player
                v_value = float("inf")
                v_action = Directions.STOP
                for action in state.getLegalActions(agent):
                    mm = minimax(state.generateSuccessor(agent, action), depth - 1, nextAgent)
                    if mm[0] < v_value:
                        v_value = mm[0]
                        v_action = action
                return v_value, v_action

        numAgents = gameState.getNumAgents()
        v_value, v_action = minimax(gameState, self.depth * numAgents, self.index)
        return v_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def alphabeta(state, depth, alpha, beta, agent):
            # Note from Q3 that:
            # alpha is Max's best option on path to root
            # beta is Min's best option on path to root

            if state.isLose() or state.isWin() or (depth == 0):
                return self.evaluationFunction(state), Directions.STOP

            nextAgent = (agent + 1) % numAgents
            if agent == self.index:  # Maximizing player
                v_value = float("-inf")
                v_action = Directions.STOP
                for action in state.getLegalActions(agent):
                    mm = alphabeta(state.generateSuccessor(agent, action), depth - 1, alpha, beta, nextAgent)
                    if mm[0] > v_value:
                        v_value = mm[0]
                        v_action = action
                    if v_value > beta:  # Per Q3 do not prune on >=
                        return v_value, v_action
                    alpha = max(alpha, v_value)
                return v_value, v_action

            else:  # Minimizing player
                v_value = float("inf")
                v_action = Directions.STOP
                for action in state.getLegalActions(agent):
                    mm = alphabeta(state.generateSuccessor(agent, action), depth - 1, alpha, beta, nextAgent)
                    if mm[0] < v_value:
                        v_value = mm[0]
                        v_action = action
                    if v_value < alpha:  # Per Q3 do not prune on <=
                        break
                    beta = min(beta, v_value)
                return v_value, v_action

        numAgents = gameState.getNumAgents()
        v_value, v_action = alphabeta(gameState, self.depth * numAgents, float("-inf"), float("inf"), self.index)
        return v_action


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

        def expectimax(state, depth, agent):
            if state.isLose() or state.isWin() or (depth == 0):
                return self.evaluationFunction(state), Directions.STOP

            nextAgent = (agent + 1) % numAgents
            if agent == self.index:  # Maximizing player
                v_value = float("-inf")
                v_action = Directions.STOP
                for action in state.getLegalActions(agent):
                    mm = expectimax(state.generateSuccessor(agent, action), depth - 1, nextAgent)
                    if mm[0] > v_value:
                        v_value = mm[0]
                        v_action = action
                return v_value, v_action

            else:  # Chance player
                v_values = []
                v_action = Directions.STOP
                for action in state.getLegalActions(agent):
                    mm = expectimax(state.generateSuccessor(agent, action), depth - 1, nextAgent)
                    v_values.append(mm[0])
                v_value = sum(v_values) / len(v_values)
                return v_value, v_action

        numAgents = gameState.getNumAgents()
        v_value, v_action = expectimax(gameState, self.depth * numAgents, self.index)
        return v_action


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
