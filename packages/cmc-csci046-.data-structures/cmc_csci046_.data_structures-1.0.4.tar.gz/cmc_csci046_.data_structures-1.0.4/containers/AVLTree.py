'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST


class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()
        if xs is not None:
            for x in xs:
                self.insert(x)

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        ret = True
        if node is None:
            return ret
        if not AVLTree._is_bst_satisfied(node):
            return False
        else:
            if AVLTree._balance_factor(node) in [-1, 0, 1]:
                left = AVLTree._is_avl_satisfied(node.left)
                right = AVLTree._is_avl_satisfied(node.right)
                return ret & left & right
            else:
                return False

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        tmp = node.value
        tmp2 = node.right
        if tmp2:
            tmp3 = tmp2.left
        else:
            tmp3 = None
        node.value = tmp2.value
        node.right = tmp2.right
        tmp2 = node.left
        node.left = Node(tmp, left=tmp2, right=tmp3)
        return node

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        tmp = node.value
        tmp2 = node.left
        if tmp2:
            tmp3 = tmp2.right
        else:
            tmp3 = None
        node.value = tmp2.value
        node.left = tmp2.left
        tmp2 = node.right
        node.right = Node(tmp, left=tmp3, right=tmp2)
        return node

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of how to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code for your insert function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        if not self.root:
            self.root = Node(value)
            return
        if value == self.root.value:
            return
        else:
            self._insert(value, self.root)
            if not self.is_avl_satisfied():
                self.root = self.rebalance(self.root)
                if not self.is_avl_satisfied():
                    self.root = self.rebalance(self.root)
            return

    @staticmethod
    def _insert(value, node):
        '''
        FIXME:
        Implement this function.
        '''
        if node.value == value:
            return
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
                return
            else:
                return AVLTree._insert(value, node.left)
        else:
            if node.right is None:
                node.right = Node(value)
                return
            else:
                return AVLTree._insert(value, node.right)

    def rebalance(self, start):
        if start is None:
            return
        if self._balance_factor(start) in [-2, 2]:
            start = self._rebalance(start)
        else:
            start.left = self.rebalance(start.left)
            start.right = self.rebalance(start.right)
        return start

    @staticmethod
    def _rebalance(node):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        if node is None:
            return
        balance = AVLTree._balance_factor(node)
        if balance < 0:
            if AVLTree._balance_factor(node.right) > 0:
                node.right = AVLTree._right_rotate(node.right)
                node = AVLTree._left_rotate(node)
            else:
                node = AVLTree._left_rotate(node)
            return node
        elif balance > 0:
            if AVLTree._balance_factor(node.left) < 0:
                node.left = AVLTree._left_rotate(node.left)
                node = AVLTree._right_rotate(node)
            else:
                node = AVLTree._right_rotate(node)
            return node
