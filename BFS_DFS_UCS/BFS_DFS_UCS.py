import random
import timeit
from collections import deque

goal_state = [1, 8, 7, 2, 0, 6, 3, 4, 5]
# 0 is a placeholder for empty
GoalNode = None
max_front = 0


def main():
    global GoalNode
    choice = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random_state = []
    while len(random_state) < 9:
        temp = random.choice(choice)
        if temp not in random_state:
            random_state.append(temp)

    print("Choose Search Option\n[1] Breath-First Search")
    print("[2] Depth-First Search")
    print("[3] Uniform-Cost Search\n[*] Any Other Value to Quit")
    menu = input()
    print(menu)

    if menu == "1":
        start_time = timeit.default_timer()
        breathFirst(random_state)
        stop_time = timeit.default_timer()
        time_elapsed = stop_time - start_time
    elif menu == "2":
        start_time = timeit.default_timer()
        depthFirst(random_state)
        stop_time = timeit.default_timer()
        time_elapsed = stop_time - start_time
    elif menu == "3":
        start_time = timeit.default_timer()
        uniformCost(random_state)
        stop_time = timeit.default_timer()
        time_elapsed = stop_time - start_time
    else:
        print("QUIT")
        exit()

    turns = []
    try:
        while random_state != GoalNode.state:
            if GoalNode.move == 1:
                turn = 'Up'
            if GoalNode.move == 2:
                turn = 'Down'
            if GoalNode.move == 3:
                turn = 'Left'
            if GoalNode.move == 4:
                turn = 'Right'
            turns.insert(0, turn)
            GoalNode = GoalNode.parent
    except:
        print("No Solution Found")

    print("Goal State: ", goal_state)
    print("Starting State: ", random_state)
    # print("Path Taken:", turns)
    print("Move Cost:", len(turns), "turns")
    print("Time Elapsed:", format(time_elapsed, '.8f'), "sec")


class Puzzle:
    def __init__(puzzle, state, parent, move, depth, cost):
        puzzle.state = state
        puzzle.parent = parent
        puzzle.move = move
        puzzle.depth = depth
        puzzle.cost = cost
        if puzzle.state:
            puzzle.map = ''.join(str(e) for e in puzzle.state)


def breathFirst(start_state):
    global max_front, GoalNode
    visited = set()
    queue = deque([Puzzle(start_state, None, None, 0, 0)])
    # Using queue FIFO
    while queue:
        node = queue.popleft()
        visited.add(node.map)
        if node.state == goal_state:
            GoalNode = node
            return queue
        paths = adjacentNodes(node)
        for path in paths:
            if path.map not in visited:
                queue.append(path)
                visited.add(path.map)
        if len(queue) > max_front:
            queue_size = len(queue)
            max_front = queue_size


def depthFirst(start_state):
    global max_front, GoalNode
    visited = set()
    stack = list([Puzzle(start_state, None, None, 0, 0)])
    # Using stack LIFO
    while stack:
        node = stack.pop()
        visited.add(node.map)
        if node.state == goal_state:
            GoalNode = node
            return stack
        paths = reversed(adjacentNodes(node))
        for path in paths:
            if path.map not in visited:
                stack.append(path)
                visited.add(path.map)
        if len(stack) > max_front:
            max_front = len(stack)


def uniformCost(start_state):
    global max_front, GoalNode
    temp_node = ""
    for poss in start_state:
        temp_node = temp_node + str(poss)
    visited = set()
    queue = []
    queue.append(Puzzle(start_state, None, None, 0, 0))
    visited.add(temp_node)
    # Using priority queue (dijkstra least cost)
    while queue:
        node = queue.pop(0)
        if node.state == goal_state:
            GoalNode = node
            return queue
        paths = adjacentNodes(node)
        for path in paths:
            current_path = path.map[:]
            if current_path not in visited:
                queue.append(path)
                visited.add(path.map[:])


def adjacentNodes(node):
    nodes = []
    paths = []
    new_depth = node.depth + 1
    new_cost = node.cost + 1
    paths.append(Puzzle(makeMove(node.state, 1), node, 1, new_depth, new_cost))
    paths.append(Puzzle(makeMove(node.state, 2), node, 2, new_depth, new_cost))
    paths.append(Puzzle(makeMove(node.state, 3), node, 3, new_depth, new_cost))
    paths.append(Puzzle(makeMove(node.state, 4), node, 4, new_depth, new_cost))
    for path in paths:
        if (path.state != None):
            nodes.append(path)
    return nodes


def makeMove(state, turn):
    new_state = state[:]
    index = new_state.index(0)
    # turn 1 = 'Up'
    # turn 2 = 'Down'
    # turn 3 = 'Left'
    # turn 4 = 'Right'
    if index == 0:
        if turn == 2:
            temp_state = new_state[0]
            new_state[0] = new_state[3]
            new_state[3] = temp_state
        elif turn == 4:
            temp_state = new_state[0]
            new_state[0] = new_state[1]
            new_state[1] = temp_state
        else:
            return None
        return new_state
    elif index == 1:
        if turn == 2:
            temp_state = new_state[1]
            new_state[1] = new_state[4]
            new_state[4] = temp_state
        elif turn == 3:
            temp_state = new_state[1]
            new_state[1] = new_state[0]
            new_state[0] = temp_state
        elif turn == 4:
            temp_state = new_state[1]
            new_state[1] = new_state[2]
            new_state[2] = temp_state
        else:
            return None
        return new_state
    elif index == 2:
        if turn == 2:
            temp_state = new_state[2]
            new_state[2] = new_state[5]
            new_state[5] = temp_state
        elif turn == 3:
            temp_state = new_state[2]
            new_state[2] = new_state[1]
            new_state[1] = temp_state
        else:
            return None
        return new_state
    elif index == 3:
        if turn == 1:
            temp_state = new_state[3]
            new_state[3] = new_state[0]
            new_state[0] = temp_state
        elif turn == 2:
            temp_state = new_state[3]
            new_state[3] = new_state[6]
            new_state[6] = temp_state
        elif turn == 4:
            temp_state = new_state[3]
            new_state[3] = new_state[4]
            new_state[4] = temp_state
        else:
            return None
        return new_state
    elif index == 4:
        if turn == 1:
            temp_state = new_state[4]
            new_state[4] = new_state[1]
            new_state[1] = temp_state
        elif turn == 2:
            temp_state = new_state[4]
            new_state[4] = new_state[7]
            new_state[7] = temp_state
        elif turn == 3:
            temp_state = new_state[4]
            new_state[4] = new_state[3]
            new_state[3] = temp_state
        elif turn == 4:
            temp_state = new_state[4]
            new_state[4] = new_state[5]
            new_state[5] = temp_state
        return new_state
    elif index == 5:
        if turn == 1:
            temp_state = new_state[5]
            new_state[5] = new_state[2]
            new_state[2] = temp_state
        elif turn == 2:
            temp_state = new_state[5]
            new_state[5] = new_state[8]
            new_state[8] = temp_state
        elif turn == 3:
            temp_state = new_state[5]
            new_state[5] = new_state[4]
            new_state[4] = temp_state
        else:
            return None
        return new_state
    elif index == 6:
        if turn == 1:
            temp_state = new_state[6]
            new_state[6] = new_state[3]
            new_state[3] = temp_state
        elif turn == 4:
            temp_state = new_state[6]
            new_state[6] = new_state[7]
            new_state[7] = temp_state
        else:
            return None
        return new_state
    elif index == 7:
        if turn == 1:
            temp_state = new_state[7]
            new_state[7] = new_state[4]
            new_state[4] = temp_state
        elif turn == 3:
            temp_state = new_state[7]
            new_state[7] = new_state[6]
            new_state[6] = temp_state
        elif turn == 4:
            temp_state = new_state[7]
            new_state[7] = new_state[8]
            new_state[8] = temp_state
        else:
            return None
        return new_state
    elif index == 8:
        if turn == 1:
            temp_state = new_state[8]
            new_state[8] = new_state[5]
            new_state[5] = temp_state
        elif turn == 3:
            temp_state = new_state[8]
            new_state[8] = new_state[7]
            new_state[7] = temp_state
        else:
            return None
        return new_state


if __name__ == '__main__':
    main()