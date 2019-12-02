# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def solution(node):
    """
    As defined in section 3.3.1
    Returns list of actions leading to node
    """
    actions = []
    while node.parent:
        actions.insert(0, node.action)
        node = node.parent
    return actions


class ChildNode:
    """
    Based upon figure 3.10 with the exception that the problem
    (i.e. SearchProblem) class does not have result() or stepCost()
    methods so search for matching action in getSuccessors() instead.
    """

    def __init__(self, state, parent=None, action=None, step_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = parent.path_cost + step_cost if parent else 0


def graphSearch(problem, frontier):
    """
    Based up figure 3.7
    """
    node = ChildNode(problem.getStartState())
    frontier.push(node)
    explored = set()

    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return solution(node)

        if node.state not in explored:
            explored.add(node.state)

            for (successor, action, step_cost) in problem.getSuccessors(node.state):
                frontier.push(ChildNode(successor, node, action, step_cost))

    return 'failure'


def depthFirstSearch(problem):
    return graphSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    return graphSearch(problem, util.Queue())


def uniformCostSearch(problem):
    return graphSearch(problem, util.PriorityQueueWithFunction(lambda node: node.path_cost))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    return graphSearch(problem,
                       util.PriorityQueueWithFunction(lambda node: node.path_cost + heuristic(node.state, problem)))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
