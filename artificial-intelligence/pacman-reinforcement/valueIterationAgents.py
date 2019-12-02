# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Initialize state values
        for _ in range(iterations):
            """
            Per Q1 note, use "batch" version of value iteration.  Sutton & Barto, Chapter 4.1, paragraph 6 says
            'To write a sequential computer program to implement iterative policy evaluation, as given by (4.5),
            you would have to use two arrays, one for the old values, V_k(s), and one for the new values, V_k+1(s).
            This way, the new values can be computed one by one from the old values without the old values being changed.'
            """

            newValues = util.Counter()

            # Initialize state values to 0 or to computed value
            for state in self.mdp.getStates():
                maxValue = float("-inf")
                for action in self.mdp.getPossibleActions(state):
                    maxValue = max(maxValue, self.computeQValueFromValues(state, action))
                newValues[state] = 0 if maxValue == float("-inf") else maxValue

            # Copy over new values
            for state in newValues:
                self.values[state] = newValues[state]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """

        # Bellman optimality equation (Sutton & Barto, eq 4.1)
        q = 0
        for (nextState, probability) in self.mdp.getTransitionStatesAndProbs(state, action):
            q += probability * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
        return q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        maxAction = None
        actions = self.mdp.getPossibleActions(state)
        if len(actions) != 0:
            maxQ = float("-inf")
            for action in actions:
                q = self.computeQValueFromValues(state, action)
                if q > maxQ:  # I won't worry about breaking ties
                    maxQ, maxAction = q, action

        return maxAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
