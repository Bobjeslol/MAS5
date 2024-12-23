"""
setup_tree.py
Author: Timo Doherty
Student-id: 2656315
Description:
- Implementation of the search space setup for assignment 5.1.
"""

import numpy as np
import random as rd
import math

LEFT = 0
RIGHT = 1

class BinaryTree:
    def __init__(self, depth=20, assign_func = rd.random()):
        self.depth = depth # default value for the assignment
        self.assign_func = assign_func
        self.origin = None
        self.target = None
        self.nodes = {}

    def create_tree(self):
        """
        Initialises the binary tree given the depth.
        """
        self.origin = Node()
        self.nodes[""] = self.origin
        level = 1
        parents = [self.origin]
        while parents:
            level += 1
            new_parents = []
            for parent in parents:
                child1 = Node(address = parent.address + "L", parent = parent)
                parent.left = child1
                self.nodes[parent.address + "L"] = child1
                child2 = Node(address = parent.address + "R", parent = parent)
                parent.right = child2
                self.nodes[parent.address + "R"] = child2
                new_parents.append(child1)
                new_parents.append(child2)

            parents = new_parents

            if level == self.depth:
                break
    
        
    def assign_vals(self, b, tau_divisor):
        """
        Chooses a random leaf node to be the target node and assigns the values in the tree.
        """
        
        def edit_distance(addr1, addr2):
            """
            Given two node addresses, returns the edit distance between them.
            """
            distance = 0
            for i, char in enumerate(addr1):
                if char == addr2[i]:
                    pass
                else:
                    distance += 1
            return distance

        leaf_nodes = [addr for addr in self.nodes.keys() if len(addr) == self.depth - 1]
        self.target = self.nodes[rd.choice(leaf_nodes)]
        print("Target address:")
        print(self.target.address)
        tau = self.depth / tau_divisor

        for leaf_addr in leaf_nodes:
            e_i = np.random.normal(0, 1)
            val = b*math.e**((-1 * edit_distance(self.target.address, leaf_addr)) / tau) + e_i
            self.nodes[leaf_addr].set_value(val)


    def display_tree(self):
        """
        Displays the tree with addresses and values.
        """
        def traverse(node, depth=0):
            if node:
                marker = " *" if node == self.target else ""
                print("  " * depth + f"Address: {node.address}, Value: {node.value}{marker}")
                traverse(node.left, depth + 1)
                traverse(node.right, depth + 1)

        traverse(self.origin)


class Node:
    def __init__(self, address: list[int] = "", value: float = 0, parent = None):
        self.value = value
        self.address = address
        self.parent = parent
        self.left = None
        self.right = None

    def set_address(self, address: list[int]):
        self.address = address

    def set_value(self, value: float):
        self.value = value
        
    def set_child(self, child):
        if self.child:
            self.child = (self.child[0], child)
        else:
            self.child(child, None)
