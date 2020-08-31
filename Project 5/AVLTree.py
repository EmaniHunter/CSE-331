"""
PROJECT 5 - AVL Trees
Name: Emani Hunter
"""
import queue


class TreeNode:
    # DO NOT MODIFY THIS CLASS #
    __slots__ = 'value', 'parent', 'left', 'right', 'height'

    def __init__(self, value, parent=None, left=None, right=None):
        """
        Initialization of a node
        :param value: value stored at the node
        :param parent: the parent node
        :param left: the left child node
        :param right: the right child node
        """
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0

    def __eq__(self, other):
        """
        Determine if the two nodes are equal
        :param other: the node being compared to
        :return: true if the nodes are equal, false otherwise
        """
        if type(self) is not type(other):
            return False
        return self.value == other.value

    def __str__(self):
        """String representation of a node by its value"""
        return str(self.value)

    def __repr__(self):
        """String representation of a node by its value"""
        return str(self.value)


class AVLTree:

    def __init__(self):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Initializes an empty Binary Search Tree
        """
        self.root = None
        self.size = 0

    def __eq__(self, other):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Describe equality comparison for BSTs ('==')
        :param other: BST being compared to
        :return: True if equal, False if not equal
        """
        if self.root is None and other.root is None:
            return True

        if self.size != other.size or self.root != other.root:
            return False  # size & root comp

        return self._is_equal(self.root.left, other.root.left) and self._is_equal(self.root.right, other.root.right)

    def _is_equal(self, root1, root2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Checks if rootts are both not None then calls _compare, otherwise checks their equality.
        :param root1: root node of first tree
        :param root2: root node of second tree
        :return: True if equal, False if not
        """
        return self._compare(root1, root2) if root1 and root2 else root1 == root2

    def _compare(self, t1, t2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Recursively compares two trees, used in __eq__.
        :param t1: root node of first tree
        :param t2: root node of second tree
        :return: True if equal, False if not
        """
        if t1 is None or t2 is None:
            return t1 == t2
        if t1 != t2:
            return False
        return self._compare(t1.left, t2.left) and self._compare(t1.right, t2.right)

    def __str__(self):
        """
        Collects a visual representation of AVL tree
        :return: string of AVL tree
        """
        if not self.root:
            return "Empty AVL Tree..."

        root = self.root
        ans = ""
        bfs_queue = []
        track = {}
        bfs_queue.append((root, 0, root.parent))
        h = AVLTree.height(self.root)

        for i in range(h+1):
            track[i] = []

        while bfs_queue:
            node = bfs_queue.pop(0)
            if node[1] > h:
                break
            track[node[1]].append(node)

            if node[0] is None:
                bfs_queue.append((None, node[1] + 1, None))
                bfs_queue.append((None, node[1] + 1, None))
                continue

            if node[0].left:
                bfs_queue.append((node[0].left, node[1] + 1, node[0]))
            else:
                bfs_queue.append((None,  node[1] + 1, None))

            if node[0].right:
                bfs_queue.append((node[0].right, node[1] + 1, node[0]))
            else:
                bfs_queue.append((None,  node[1] + 1, None))

        spaces = pow(2, h) * 12
        ans += "\n"
        ans += "\t\tVisual Level Order Traversal of AVL Tree - Node (Parent Height)".center(spaces)
        ans += "\n\n"
        for i in range(h+1):
            ans += f"Level {i}: "
            for node in track[i]:
                level = pow(2, i)
                space = int(round(spaces / level))
                if node[0] is None:
                    ans += " " * space
                    continue
                ans += "{} ({} {})".format(node[0], node[2], node[0].height).center(space, " ")
            ans += "\n"
        return ans

    # ------- Implement/Modify the functions below ------- #

    def insert(self, node, value):
        '''
        Takes in value to be added in the form of a node to the tree
        :param node: root of (sub)tree
        :param value: value to be added to tree
        :return: nothing
        '''
        # TIME COMPLEXITY: O(log(n)) ; SPACE COMPLEXITY: O(1)
        if node is None:
            node = TreeNode(value)
            self.size = self.size + 1
            if self.root is None:
                self.root = TreeNode(value)

            self.update_height(node)
            self.update_height(self.root)
        else:
            if node.value > value:
                if node.left is None:
                    new_node = TreeNode(value)
                    node.left = new_node  # set the node left to be the node created
                    self.size = self.size + 1
                    new_node.parent = node  # set the node created's parent to the current node
                else:
                    self.insert(node.left, value)

            elif node.value < value:
                if node.right is None:
                    new_node = TreeNode(value)
                    node.right = new_node
                    self.size = self.size + 1  # change the size when assigning a new node
                    new_node.parent = node
                else:
                    self.insert(node.right, value)
            elif node.value == value:
                return

            self.update_height(node)
            self.update_height(self.root)
            self.rebalance(node)

    def remove(self, node, value):
        '''
        Takes in value to remove from the tree
        :param node: root of (sub) tree
        :param value: value to be removed
        :return: root of subtree
        '''
        # TIME COMPLEXITY: O(log(n)) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return None
        node = self.search(node, value)  # creates new node with this search on each call to remove
        parent = node.parent  # violates space complexity. Space complexity is supposed to be: O(1)

        if node.left is not None and node.right is not None:  # internal node with 2 children
            successor = node.right
            if successor.left is not None:
                successor = self.max(successor.left)

            self.remove(node, successor.value)
            if node != self.root:
                if self.root.value < successor.value:
                    self.root.right = successor
                    node = None

            if node is not None:
                node.value = node.left.value
                node.right = successor
                node.left = None
            return self.root

        elif node == self.root:  # root node with 1 or 0 children
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right
            if self.root:
                self.root.parent = None
                self.size = self.size - 1

            if node.left is None and node.right is None:
                self.root = None
                self.size = self.size - 1
            return node.parent

        elif node.left is not None:  # internal node with left child only
            self.replace_child(parent, node, node.left)
            self.size = self.size - 1

        else:  # internal node with right child only or leaf
            self.replace_child(parent, node, node.right)
            self.size = self.size - 1

        node = parent
        if node is not None:
            self.rebalance(node)
            node = node.parent
            self.update_height(node)
            self.update_height(self.root)
        return node

    @staticmethod
    def height(node):
        '''
        Returns height of given node
        :param node: node to find height of
        :return: height of node
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return -1
        else:
            return node.height

    @staticmethod
    def update_height(node):
        '''
        Updates the height of the node based on its children's heights
        :param node: node to update height of
        :return: updated height of node
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if node is None:  # if node does not exist at all in tree, height = -1
            return
        node.height = 1 + max(AVLTree.height(node.left), AVLTree.height(node.right))

    def depth(self, value):
        '''
        Returns the depth of the node with the given value
        :param value: value to find to get depth of
        :return: depth of node with given value
        '''
        # TIME COMPLEXITY: O(height) ; SPACE COMPLEXITY: O(1)
        cur = self.root
        count = 0
        while cur is not None:
            if value == cur.value:
                return count
            count += 1
            if value < cur.value:
                cur = cur.left
            elif value > cur.value:
                cur = cur.right
        return -1

    def search(self, node, value):
        '''
        Takes in value to search for and a node which is the root of a given (sub)tree
        :param node: root of given subtree
        :param value: value to find
        :return: node with given value if found, if not found, returns potential parent node
        '''
        # TIME COMPLEXITY: O(log(n)) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return

        if value == node.value:
            return node
        elif value < node.value:
            if node.left is not None:
                return self.search(node.left, value)
        elif value > node.value:
            if node.right is not None:
                return self.search(node.right, value)
        return node

    def inorder(self, node):  # left root right
        '''
        Returns a generator object of the tree traversed using the
        inorder method of traversal starting at the given node
        :param node: node to start traversal
        :return: generator object of tree traversed inorder
        '''
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
        if node is None:
            return
        if node.left is not None: # DO YIELD FROM INSTEAD OF LOOPS
            yield from self.inorder(node.left)
        yield node
        if node.right is not None:
            yield from self.inorder(node.right)

    def preorder(self, node):  # root left root
        '''
         Returns a generator object of the tree traversed using the
        preorder method of traversal starting at the given node
        :param node: node to start traversal
        :return: generator object of tree traversed preorder
        '''
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
        if node is None:
            return
        yield node
        if node.left is not None:
            yield from self.preorder(node.left)
        if node.right is not None:
            yield from self.preorder(node.right)

    def postorder(self, node):  # left right root
        '''
         Returns a generator object of the tree traversed using the
        postorder method of traversal starting at the given node
        :param node: node to start traversal
        :return: generator object of tree traversed postorder
        '''
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
        if node is None:
            return
        if node.left is not None:
            yield from self.postorder(node.left)
        if node.right is not None:
            yield from self.postorder(node.right)
        yield node

    def bfs(self):
        '''
        Returns a generator object of the tree traversed using the
        breadth-first method of traversal using a queue
        :return: generator object of tree traversed bfs
        '''
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
        if self.root is not None:
            bfs_queue = queue.Queue()
            bfs_queue.put(self.root)
            while bfs_queue.qsize() != 0:
                p = bfs_queue.get()
                yield p

                if p.left is not None:
                    bfs_queue.put(p.left)
                if p.right is not None:
                    bfs_queue.put(p.right)

    def min(self, node):
        '''
        Gets the minimum of the tree rooted at the given node
        :param node: root of (sub)tree
        :return: minimum of the tree
        '''
        # TIME COMPLEXITY: O(log(n)) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return None
        else:
            cur = node
            if node.left is not None:
                look_left = self.min(node.left)
                if cur.value > look_left.value:
                    cur = look_left
            return cur

    def max(self, node):
        '''
        Gets the maximum of the tree rooted at the given node
        :param node: root of (sub)tree
        :return: maximum of the tree
        '''
        # TIME COMPLEXITY: O(log(n)) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return None
        else:
            cur = node
            if node.left is not None:
                look_right = self.max(node.right)
                if cur.value < look_right.value:
                    cur = look_right
            return cur

    def get_size(self):
        '''
        Gets the number of nodes in the AVL Tree
        :return: returns number of nodes
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        return self.size

    @staticmethod
    def get_balance(node):
        '''
        Gets the balance factor of the node passed in
        :param node: node to find balance factor of
        :return: balance factor of node computed
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return 0
        balance_fac = AVLTree.height(node.left) - AVLTree.height(node.right)
        return balance_fac

    @staticmethod
    def set_child(parent, child, is_left):
        '''
        Sets the parent node's child to the child node
        :param parent: parent of child
        :param child: child node, child of parent
        :param is_left: a boolean that determines where the child is to be placed in relation
         to the parent where True is left and False is right
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if child is not None:
            child.parent = parent
        if is_left is not True and is_left is not False: # if not given any parameter
            return False
        if is_left is True:
            parent.left = child
        if is_left is False:
            parent.right = child
        AVLTree.update_height(parent)
        AVLTree.update_height(child)

    @staticmethod
    def replace_child(parent, current_child, new_child):
        '''
        Makes the new_child node a child of the parent node
        in place of the current_child node
        :param parent: parent of current child
        :param current_child: current_child of parent in tree
        :param new_child: new_child to replace current_child
        :return: recursive call of new_child being set in tree
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if parent.left == current_child:
            return AVLTree.set_child(parent, new_child, True)
        if parent.right == current_child:
            return AVLTree.set_child(parent, new_child, False)

    def left_rotate(self, node):
        '''
        Performs an AVL left rotation on the subtree rooted at node
        :param node: root of subtree
        :return: root of new subtree
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        right_left = node.right.left
        if node.parent is not None:
            self.replace_child(node.parent, node, node.right)
        else:
            self.root = node.right
            self.root.parent = None
        self.set_child(node.right, node, True)
        self.set_child(node, right_left, False)
        self.update_height(node.parent)
        return node.parent
        # pass

    def right_rotate(self, node):
        '''
        Performs an AVL right rotation on the subtree rooted at node
        :param node: root of subtree
        :return: root of new subtree
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        left_right = node.left.right
        if node.parent is not None:
            self.replace_child(node.parent, node, node.left)
        else:
            self.root = node.left
            self.root.parent = None
        self.set_child(node.left, node, False)
        self.set_child(node, left_right, True)
        self.update_height(node.parent)
        return node.parent
        # pass

    def rebalance(self, node):
        '''
        Rebalances the subtree rooted at the node if needed
        :param node: root of subtree
        :return: the root of the new, balanced subtree
        '''
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if node is None:
            return
        self.update_height(node)
        if self.get_balance(node) == -2:
            if self.get_balance(node.right) == 1:
                self.right_rotate(node.right) # double rotation
            self.left_rotate(node)
        elif self.get_balance(node) == 2:
            if self.get_balance(node.left) == -1:
                self.left_rotate(node.left)
            self.right_rotate(node)

        self.update_height(self.root)
        return self.root
        # pass


# ------- Application Problem ------- #
def height_helper(node):
    '''
    Helper function to get height of node outside of AVLTree class
    :param node: root of (sub)tree
    :return: height of node
    '''
    if node is None:
        return -1
    else:
        return 1 + max(height_helper(node.left), height_helper(node.right))


def is_avl_tree(node):
    '''
    Checks if tree is a balanced avl tree
    :param node: root of binary search tree
    :return: True if the given tree is a valid AVL tree, otherwise False
    '''
    # TIME COMPLEXITY: O(nlog(n)) ; SPACE COMPLEXITY: O(1)
    if node is None:  # empty tree always balanced
        return True

    if node and node.left is None and node.right is None:
        return True

    left_height = height_helper(node.left)  # get heights of nodes in left subtree
    right_height = height_helper(node.right)
    balance_fac = left_height-right_height
    if abs(balance_fac) <= 1:
        if is_avl_tree(node.left) is not False:  # check if it is  truly balanced
            if is_avl_tree(node.right) is not False:
                return True
    return False
