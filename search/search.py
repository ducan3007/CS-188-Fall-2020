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


def commonSearch(problem, Fringe):
    # Fringe (rìa) được hiểu là một cấu trúc dữ liệu, lưu trưu các node sẽ được duyệt (rìa - nằm ở rìa của cây tìm kiếm, các nút tiếp theo)
    # Các node sẽ được thêm vào dần dần.
    # Các Node có thể trùng lặp.
    # Vậy dùng một [] để lưu các node đã duyệt, tránh việc lặp vô hạn
    # Nếu node không trong [] thì ta thêm vào Fringe (push)
    # Các phần tử trùng sẽ được loại bỏ (pop) dần dần khỏi Fringe
    # khi Fringe rỗng thì thuật toán kết thúc.

    # Lấy startState là tọa độ ban đầu của agent có dạng (x, y)
    startState = problem.getStartState()

    # Push startState vào fringe. StartState là vị trí ban đầu nên đường đi đến chính nó là một mảng rỗng.
    Fringe.push((startState, []))

    # Các state đã từng duyệt sẽ được lưu trong mảng visited, đảm bảo không duyệt lại.
    visited = []

    while not Fringe.isEmpty():

        currentState, actionArr = Fringe.pop()

        # Nếu state hiện tại là goalState thì trả về đường dẫn tới nó.
        if problem.isGoalState(currentState):

            return actionArr

        # Nếu state hiện tại chưa duyệt thì đánh dấu là đã duyệt (thêm vào mảng visited)
        # Đồng thời thêm các state liền kề với nó vào fringe.
        # Ngược lại, sate đã duyệt sẽ được bỏ qua.

        if currentState not in visited:
            # đánh dấu là đã duyệt
            visited.append(currentState)

            # từ đỉnh đó, lấy các đỉnh kề, (nhiều đỉnh kề)
            successors = problem.getSuccessors(currentState)

            for nextSate, action, cost in successors:
                # Đường đi từ startState đến nextState (successor) bằng tổng đường đi từ start đến current và current đến next
                actionOfNextState = actionArr + [action]
                Fringe.push((nextSate, actionOfNextState))

    # Khi đã duyệt hết state mà không tìm được goalState thì trả về mảng trống
    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    In DFS, we use a stack data structure to store the fringe.


    Trong DFS, Fringe là một Stack (LIFO).
    Các Node vào trước sẽ được duyệt sau cùng.

    """

    "*** YOUR CODE HERE ***"

    stack = util.Stack()
    return commonSearch(problem, stack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first.

    Trong BFS, Fringe là một Queue (FIFO).
    Node nào vào trước sẽ được duyệt trước.


    """

    queue = util.Queue()

    return commonSearch(problem, queue)


def uniformCostSearch(problem):
    '''
    Cấu trúc dữ liệu chính là một PriorityQueue.
    Mỗi phần tử trong PriorityQueue là một tuple ((node, actions[ from node to startState ]), actionsCost)
    '''

    prorityQueue = util.PriorityQueue()

    startState = problem.getStartState()
    prorityQueue.push((startState, []), problem.getCostOfActions([]))

    visited = []

    while not prorityQueue.isEmpty():

        currentState, actionArr = prorityQueue.pop()

        if problem.isGoalState(currentState):
            return actionArr

        if currentState not in visited:
            visited.append(currentState)
            for nextSate, action, cost in problem.getSuccessors(currentState):
                actionOfNextState = actionArr + [action]
                prorityQueue.push((nextSate, actionOfNextState), problem.getCostOfActions(actionOfNextState))

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
   # Chi phí cost của A* được tính bởi chi phí từ startState tới state hiện tại cộng với chi phí dự
   # đoán từ state hiện tại tới goalState.
    fringe = util.PriorityQueue()
    startState = problem.getStartState()

    """ 
     Sử dụng hàm getCostOfActions để tính chi phí dựa trên Actions từ startState đến state hiện tại.

     Sử dụng heuristic(state, problem) để tính chi phí dự đoán tới goalState.

     Chi phí dự đoán được tính như sau: 
     + tọa độ hiện tại : (x1, y1)
     + tọa độ đích: (x2, y2)

     => Chi phí dự đoán là đường thắng nối giữa 2 điểm:
        => cost =  |x1 - x2| + |y1 - y2| ( công thức Manhattan Distance)
     
    """
    fringe.push((startState, []), problem.getCostOfActions([]) + heuristic(startState, problem))

    # Các state đã từng duyệt sẽ được lưu trong mảng visited.
    visited = []

    while not fringe.isEmpty():
        import time

        # Lấy ra state với chi phí thấp nhất.
        currentState, actionArr = fringe.pop()

        # Nếu state hiện tại là goalState thì trả về đường dẫn tới nó.
        if problem.isGoalState(currentState):
            return actionArr

        # Nếu state hiện tại chưa duyệt thì đánh dấu là đã duyệt (thêm vào mảng visited)
        # Đồng thời thêm các state liền kề với nó vào fringe.

        if currentState not in visited:
            visited.append(currentState)

            for nextState, action, cost in problem.getSuccessors(currentState):
                actionOfNextState = actionArr + [action]

                fringe.push((nextState, actionOfNextState), problem.getCostOfActions(
                    actionOfNextState) + heuristic(nextState, problem))

    # Khi đã duyệt hết state mà không tìm được goalState thì trả về mảng trống
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
