import random


def alpha_beta_pruning(student_id, min_negative_hp, max_negative_hp):
    initial_hp = int(student_id[-1::-1][:3])  # Last 2 digits in reverse
    depth = int(student_id[0]) * 2  # 1st digit of student ID
    branches = int(student_id[2])  # 3rd digit of student ID
    total_leaf_nodes = branches ** depth

    terminal_states = [random.randint(min_negative_hp, max_negative_hp) for _ in range(total_leaf_nodes)]
    visited_leaf_nodes = 0

    def simulate_tree(node_index, depth, alpha, beta, maximizingPlayer):
        nonlocal visited_leaf_nodes

        start_index = node_index * branches
        if depth == 0 or start_index >= total_leaf_nodes:
            visited_leaf_nodes += 1
            return terminal_states[node_index]

        if maximizingPlayer:
            maxEval = float('-inf')
            for i in range(branches):
                child_index = start_index + i
                if child_index < total_leaf_nodes:
                    eval = simulate_tree(child_index, depth - 1, alpha, beta, False)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Alpha Beta Pruning
            return maxEval
        else:
            minEval = float('inf')
            for i in range(branches):
                child_index = start_index + i
                if child_index < total_leaf_nodes:
                    eval = simulate_tree(child_index, depth - 1, alpha, beta, True)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha Beta Pruning
            return minEval

    final_alpha = simulate_tree(0, depth, float('-inf'), float('inf'), True)
    left_life_hp = initial_hp - final_alpha
    comparisons_after_pruning = visited_leaf_nodes

    return depth, branches, terminal_states, left_life_hp, comparisons_after_pruning


with open("22101667_Sakib Rayhan Yeasin_CSE422_07_Lab_Assignment03_InputFile_Spring2024.txt", "r") as input_file:
    student_id = input_file.readline()
    min_negative_hp, max_negative_hp = map(int, input_file.readline().split())

    depth, branches, terminal_states, left_life_hp, comparisons = alpha_beta_pruning(student_id, min_negative_hp, max_negative_hp)

    print(f"Depth and Branches ratio is {depth}:{branches}")
    print(f"Terminal States (Leaf node) are {' '.join(map(str, terminal_states))}")
    print(f"Left life(HP) of the defender after maximum damage caused by the attacker is {left_life_hp if left_life_hp >= 0 else 0}")
    print(f"After Alpha-Beta Pruning Leaf Node Comparisons {comparisons}")
