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


import random
import util
from game import Agent
from util import Queue


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (new_food) and Pacman position after moving (new_pos).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        score = successorGameState.getScore()

        if successorGameState.isWin(): return float("inf")
        if successorGameState.isLose(): return float("-inf")

        ghostDists = []
        for ghost in newGhostStates:
            ghostDists.append(util.manhattan_distance(ghost.getPosition(), newPos))
        if len(ghostDists) > 0:
            minGhostDist = min(ghostDists)
            if minGhostDist < 3:
                score -= 50 / minGhostDist

        foodDists = []
        foodList = newFood.asList()

        for food in foodList:
            foodDists.append(util.manhattan_distance(newPos, food))

        if len(foodDists) > 0:
            minFoodDist = min(foodDists)
            score += 2 / minFoodDist

        return score


def score_evaluation_function(current_game_state):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search game
      (not reflex game).
    """

    return current_game_state.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search game.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='score_evaluation_function', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def get_action(self, game_state):
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
            Returns the total number of game in the game
        """
        "*** YOUR CODE HERE ***"
        agentCount = game_state.getNumAgents()

        def multiminimax(state, depth, agentIndex):
            legalActions = state.getLegalActions(agentIndex)
            if depth == 0 or len(legalActions) == 0:
                return None, self.evaluationFunction(state)

            nextAgentIndex = (agentIndex + 1) % agentCount
            nextDepth = depth
            if nextAgentIndex == 0:
                nextDepth -= 1

            bestAction = None
            if agentIndex == 0:
                bestScore = float('-inf')
                for action in legalActions:
                    succState = state.generateSuccessor(agentIndex, action)
                    (_, succScore) = multiminimax(succState, nextDepth, nextAgentIndex)
                    if succScore > bestScore:
                        bestScore = succScore
                        bestAction = action

            else:
                bestScore = float('inf')
                for action in legalActions:
                    succState = state.generateSuccessor(agentIndex, action)
                    (_, succScore) = multiminimax(succState, nextDepth, nextAgentIndex)
                    if succScore < bestScore:
                        bestScore = succScore
                        bestAction = action
            return bestAction, bestScore

        result = multiminimax(game_state, self.depth, 0)
        return result[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent witlh alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        agentCount = game_state.getNumAgents()

        def alphabeta(state, depth, agentIndex, alpha, beta):
            legalActions = state.getLegalActions(agentIndex)
            if depth == 0 or len(legalActions) == 0:
                return None, self.evaluationFunction(state)

            nextAgent = (agentIndex + 1) % agentCount
            nextDepth = depth
            if nextAgent == 0:
                nextDepth -= 1

            bestAction = None
            if agentIndex == 0:
                bestScore = float('-inf')
                for action in legalActions:
                    succState = state.generateSuccessor(agentIndex, action)
                    (_, succScore) = alphabeta(succState, nextDepth, nextAgent, alpha, beta)
                    if succScore > bestScore:
                        bestScore = succScore
                        bestAction = action
                    if bestScore >= beta: break
                    alpha = max(alpha, bestScore)

            else:
                bestScore = float('inf')
                for action in legalActions:
                    succState = state.generateSuccessor(agentIndex, action)
                    (_, succScore) = alphabeta(succState, nextDepth, nextAgent, alpha, beta)
                    if succScore < bestScore:
                        bestScore = succScore
                        bestAction = action
                    if bestScore <= alpha: break
                    beta = min(beta, bestScore)
            return bestAction, bestScore

        result = alphabeta(game_state, self.depth, 0, float('-inf'), float('inf'))
        return result[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        numAgents = gameState.getNumAgents()

        def expectimax(state, depth, agentIndex):
            legalActions = state.getLegalActions(agentIndex)
            if depth == 0 or len(legalActions) == 0:
                return None, self.evaluationFunction(state)

            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth
            if nextAgent == 0:
                nextDepth = depth - 1

            bestAction = None
            if agentIndex == 0:
                bestScore = float('-inf')
                for action in legalActions:
                    successorState = state.generateSuccessor(agentIndex, action)
                    (_, successorScore) = expectimax(successorState, nextDepth, nextAgent)
                    if successorScore > bestScore:
                        bestScore = successorScore
                        bestAction = action
            else:
                totalScore = 0
                numActions = len(legalActions)
                for action in legalActions:
                    successorState = state.generateSuccessor(agentIndex, action)
                    (_, successorScore) = expectimax(successorState, nextDepth, nextAgent)
                    totalScore += successorScore
                bestScore = totalScore / numActions

            return bestAction, bestScore

        result = expectimax(gameState, self.depth, 0)
        return result[0]


def bfs_distance(startPosition, targets, gameState):
    """
    Finds the shortest distance between startPosition and one of the target points
    using breadth-first search (BFS).
    """
    if not targets:
        return float('inf')
    walls = gameState.getWalls()
    visited = set()
    queue = Queue()
    queue.push((startPosition, 0))
    visited.add(startPosition)

    while not queue.is_empty():
        position, dist = queue.pop()

        if position in targets:
            return dist

        x, y = position
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nextPos = (x + dx, y + dy)

            if nextPos not in visited and not walls[nextPos[0]][nextPos[1]]:
                queue.push((nextPos, dist + 1))
                visited.add(nextPos)

    return float('inf')


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      """
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsuleList = currentGameState.getCapsules()
    currentScore = currentGameState.getScore()

    ghostScaredDist = bfs_distance(pacmanPos, [ghost.getPosition() for ghost in ghostStates if ghost.scaredTimer > 0],
                                   currentGameState)
    ghostDangerousDist = bfs_distance(pacmanPos,
                                      [ghost.getPosition() for ghost in ghostStates if ghost.scaredTimer == 0],
                                      currentGameState)

    foodDist = bfs_distance(pacmanPos, foodList, currentGameState)

    capsuleDist = bfs_distance(pacmanPos, [capsule for capsule in capsuleList], currentGameState)

    if ghostDangerousDist < 3:
        currentScore -= 500

    if ghostScaredDist != float('inf'):
        currentScore += 100 / (ghostScaredDist + 1)

    if foodDist != float('inf'):
        currentScore += 1 / (foodDist + 1)

    if capsuleDist != float('inf'):
        currentScore += 20 / (capsuleDist + 1)

    return currentScore


# Abbreviation

better = betterEvaluationFunction
