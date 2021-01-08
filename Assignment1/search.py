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

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 0
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>
48+ hour spend on assignment:(
"""
#####################################################
#####################################################

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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    start = problem.getStartState()
    visited = []

    #from util import Stack
    curdirect = []
    pos = util.Stack()
 
    pos.push((start,[]))
    while not pos.isEmpty():
        
        position, direction = pos.pop()
        print(direction)
        print("xd")
        if problem.isGoalState(position):
            break
        visited.append(position)
        sus = problem.getSuccessors(position)
        for i in sus:
            coor = i[0]
            if coor not in visited:
                curdirect = i[1]
                
                pos.push((coor,direction+[curdirect]))
                
    return direction       

def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    visited = []
    visited.append(start)
    curdirect = []
    pos = util.Queue()
    pos.push((start,[]))
    while not pos.isEmpty():
        
        position, direction = pos.pop()
  

        if problem.isGoalState(position):
            return direction
        
        sus = problem.getSuccessors(position)
        for i in sus:
            coor = i[0]
            if coor not in visited:
                curdirect = i[1]
                pos.push((coor,direction+[curdirect]))
                visited.append(coor)
                
                
    return direction       



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    start = problem.getStartState()
   
    pos = util.PriorityQueue()
    h_dis = heuristic(start,problem)
    pos.push((problem.getStartState(),[],0), h_dis)
    (position, direction,cost)= pos.pop()
    visited = []
    
    visited.append((start, h_dis) )
    
    while not problem.isGoalState(position):
        
        
        sus = problem.getSuccessors(position)
        for i in sus:
            
            flag = False
            newCost = cost+i[2]
            coor = i[0]
            curdirect = i[1]
            for (state,viscost) in visited:

                if (state == coor) and (newCost>=viscost):
                    flag = True
            if not flag:
                actioncost = direction + [curdirect]
                h_dis = heuristic(coor,problem)
                g_dis = problem.getCostOfActions(actioncost)
                f_dis = h_dis + g_dis

                pos.push((coor,direction + [curdirect],g_dis),f_dis)
                visited.append((coor,newCost))
        (position, direction,cost)= pos.pop()
                
        
    return direction


    
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"

def priorityQueueDepthFirstSearch(problem):
    """
    Q1.4a.
    Reimplement DFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    visited = []
    visited.append(start)
    #from util import Stack
    curdirect = []
    pos = util.PriorityQueue()
    pos.push((start,[]),0)
    
    while not pos.isEmpty():
        
        position, direction = pos.pop()
        if problem.isGoalState(position):
            break
        visited.append(position)
        sus = problem.getSuccessors(position)
        for i in sus:
            coor = i[0]
            if coor not in visited:
                curdirect = i[1]
                priorith = len(direction)
                pos.push((coor,direction+[curdirect]),priorith)
                
    return direction + [curdirect] 

def priorityQueueBreadthFirstSearch(problem):
    """
    Q1.4b.
    Reimplement BFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    visited = []
    visited.append(start)
    curdirect = []
    pos = util.PriorityQueue()
    priority = 0
    pos.push((start,[]),priority)

    while not pos.isEmpty():
        
        position, direction = pos.pop()
        if problem.isGoalState(position):
            break
        visited.append(position)
        sus = problem.getSuccessors(position)
        for i in sus:
            coor = i[0]
            if coor not in visited:
                priority+=1
                curdirect = i[1]
                pos.push((coor,direction+[curdirect]),priority)
                
    return direction       

#####################################################
#####################################################
# Discuss the results of comparing the priority-queue
# based implementations of BFS and DFS with your original
# implementations.

"""
<Your discussion goes here>
"""



#####################################################
#####################################################



# Abbreviations (please DO NOT change these.)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bfs2 = priorityQueueBreadthFirstSearch
dfs2 = priorityQueueDepthFirstSearch
