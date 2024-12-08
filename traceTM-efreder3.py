#!/usr/bin/env python3
import sys 

def read_file(file):
    """
    Reads and parses the input file to extract the machine's configuration. It returns the name of the 
    machine, the start state, accept state, reject state, and an empty dict with transitons. 
    
    """
    # check if the file exists 
    try: 
        with open(file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Invalid file name: {file}")
        sys.exit(1)

    # parse data from file
    name = lines[0].strip()
    start = lines[4].strip()
    accept = lines[5].strip().split(',')  # list of accepting states
    reject = lines[6].strip()  # single rejecting state
    transitions = {} 

    # parse transitions from the file
    for line in lines[7:]:
        if line.strip():
            curr, r, next_state, w, direction = line.strip().split(',')
            transitions.setdefault((curr, r), []).append((next_state, w, direction))

    return name, start, accept, reject, transitions

def move(left, right, write_char, direction):
    """
    Simulates the movement of the Turing machine's head and updates the tape. Returns the left 
    and right parts of the tape after the move. 

    """

    # write character
    if not right:
        right = write_char
    else:
        right = write_char + right[1:]

    # move the head based on direction
    if direction == 'R':
        if len(right) > 1:
            left += right[0]
            right = right[1:]
        else:
            left += right[0]
            right = "_"
    else:  # move left
        if left:
            if not right or right == "_":
                right = "_"
            else:
                right = left[-1] + right
                left = left[:-1]
        else:
            right = "_" + right

    return left, right

def trace(transition, parent):
    """
    Traces the path from the initial configuration to the current configuration by following 
    the parents. Returns configurations 

    """

    # trace the path from the start to the current state
    path = [transition]
    while transition in parent:
        transition = parent[transition]
        path.append(transition)
    return list(reversed(path))

def bfs(start, accept, reject, transitions, input, max_steps):
    """
    Performs a breadth-first search (BFS) to simulate the Turing machine's operation. The function 
    will return if it finds an accepting state or exhausts all possible configurations 
    
    """

    total = 0
    queue = [[("", start, input)]]
    before = {}

    # perform breadth-first search (BFS)
    for depth in range(max_steps):
        if not queue[depth]:  # end loop when there are no more possible configurations
            return False, depth, total, []
        queue.append([])

        for transition in queue[depth]:
            left, state, right = transition

            # check if the current state is an accepting state
            if state in accept:
                path = trace(transition, before)
                return True, depth, total, path

            # skip if reject state
            if state == reject:
                continue

            # het the current character being read
            curr = right[0] if right else "_"

            # get possible transitions
            moves = transitions.get((state, curr), [])

            # if no possible moves, reject
            if not moves:
                next_transition = (left, reject, right)
                queue[depth + 1].append(next_transition)
                before[next_transition] = transition
                total += 1
                continue

            # use transitions to generate new states
            for next_state, write, direction in moves:
                new_left, new_right = move(left, right, write, direction)
                next_transition = (new_left, next_state, new_right)
                queue[depth + 1].append(next_transition)
                before[next_transition] = transition
                total += 1

    return False, max_steps, total, []

def main():
    # get the Turing Machine file name interactively
    file = input("Enter Turing machine file name: ")
    name, start, accept, reject, transitions = read_file(file)

    while True:
        # ask the user for an input string and maximum depth
        input_string = input("\nEnter input string (or type 'exit' to quit): ")
        if input_string.lower() == 'exit':
            print("Exiting program.")
            break
        
        max_steps = input("Enter maximum steps for the simulation: ")
        
        # check if max_steps is a valid integer
        try:
            max_steps = int(max_steps)
        except ValueError:
            print("Invalid input for steps, please enter a number.")
            continue

        # [erform breadth-first search (BFS)
        check, steps, total, path = bfs(start, accept, reject, transitions, input_string, max_steps)

        # output results
        print(f"\nMachine: {name}")
        print(f"Initial input string: {input_string}")
        print(f"Depth of the tree of configurations: {steps}")
        print(f"Total transitions: {total}")

        if check:
            print(f"\nString accepted in {steps} steps.")
            print("Accepting path:")
            for left, state, right in path:
                left = ''.join(left)  # left part as a string
                right = ''.join(right)  # right part as a string
                print(f"{left},{state},{right}")
        else:
            print(f"\nString rejected in {steps} steps.")

if __name__ == "__main__":
    main()