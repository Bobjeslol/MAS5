"""
rollout.py
Author: Timo Doherty
Student-id: 2656315
Description:
- Implements MCTS to find the optimal path in a binary tree.
"""

from setup_tree import BinaryTree
import math

def UCB(node, tree_stats, C):
    """
    Calculates the UCB score of a given node.
    """
    if node not in tree_stats.keys():
        tree_stats[node] = [0, node.value, node.value, node.value]
    
    avg_val = tree_stats[node][1]
    parent_node_visits = tree_stats[node.parent][0]
    child_node_visits = tree_stats[node][0]
    
    if child_node_visits == 0 or parent_node_visits == 0:
        return float('inf')
    
    explore_term = math.sqrt(math.log(parent_node_visits)/child_node_visits)
    return avg_val + C * explore_term


def rollout(tree, tree_stats, C):
    # Rollout
    current_node = tree.origin
    tree_stats[tree.origin] = [1, 0, 0, 0]
    for _ in range(tree.depth - 1):
        left_UCB = UCB(current_node.left, tree_stats, C)
        right_UCB = UCB(current_node.right, tree_stats, C)
        if left_UCB >= right_UCB: # On ties, always just pick left.
            tree_stats[current_node.left][0] += 1
            current_node = current_node.left
        else:
            tree_stats[current_node.right][0] += 1
            current_node = current_node.right

    # Backpropagate
    found_val = current_node.value
    for _ in range(tree.depth - 1):
        current_node = current_node.parent
        tree_stats[current_node][2] = max(tree_stats[current_node][2], found_val)
        tree_stats[current_node][3] += found_val
        tree_stats[current_node][1] = tree_stats[current_node][3] / tree_stats[current_node][0]
    

def MCTS(tree, C):
    iterations = 50
    tree_stats = {} # Maps node to [visit_count, avg_val, max_val, sum_vals]
    for iter in range(1, iterations + 1):
        rollout(tree, tree_stats, C)
    return tree_stats


def main():
    """
    Initialises the tree using the function given in the assignment.
    """
    tree = BinaryTree(5)
    tree.create_tree()
    tree.assign_vals(b = 10, tau_divisor = 5)
    tree.display_tree() # TODO: Remove
    
    
    C = 4
    tree_stats = MCTS(tree, C)
    
    # Testing purposes
    for node in tree_stats:
        node.value = tree_stats[node][2]
    tree.display_tree()
    

if __name__  == "__main__":
    main()
