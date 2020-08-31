"""
PROJECT 2 - Linked List Recursion
Name: Emani Hunter
PID: A55714733
"""


class LinkedNode:
    # DO NOT MODIFY THIS CLASS #
    __slots__ = '_value', '_next'

    def __init__(self, value, next=None):
        """
        DO NOT EDIT
        Initialize a node
        :param value: value of the node
        :param next: pointer to the next node in the LinkedList, default is None
        """
        self._value = value  # element at the node
        self._next = next  # reference to next node in the LinkedList

    def __repr__(self):
        """
        DO NOT EDIT
        String representation of a node
        :return: string of value
        """
        return str(self._value)

    __str__ = __repr__

    def get_value(self):
        return self._value

    def get_next(self):
        return self._next

    def set_value(self, value):
        self._value = value

    def set_next(self, next):
        self._next = next


# IMPLEMENT THESE FUNCTIONS - DO NOT MODIFY FUNCTION SIGNATURES #


def insert(value, node=None):
    """
    Inserts a value into the back of the list
    :param value: the value to insert
    :param node: the head node in the list
    :return: [LinkedNode] the starting node in the list
    """
    if node is None:
        return LinkedNode(value)
    if node is not None:
        node._next = insert(value, node._next)
    return node


def to_string(node):
    """
    Generates a string representation of the list
    :param node: the head node in the list
    :return: a string representation of the list
    """

    if node is None:
        return ""

    if node._value is not None:
        if node._next is not None:
            list_string = to_string(node._next)
            return str(node._value) + ", " + list_string

        if node._next is None:
            list_string = to_string(node._next)
            return str(node._value)


def remove(value, node):
    """
    Removes first occurrence of node with given value
    :param value: value to remove
    :param node: head node of the list
    :return: [LinkedNode] the starting node of the list
    """

    if node is None:
        return None
    if node._value is not None:
        if node._value == value:
            next_node = node._next
            return next_node
        node._next = remove(value, node._next)

    return node


def remove_all(value, node):
    """
    Remove all occurrences of nodes with given value
    :param value: value to remove
    :param node: head node of the list
    :return: [LinkedNode] the starting node of the list
    """

    if node is None:
        return None
    if node._value is not None:
        if node._value == value:
            return remove_all(value, node._next)
        node._next = remove_all(value, node._next)
    return node


def search(value, node):
    """
    Searches for value in list
    :param value: value to find
    :param node: head node of list
    :return: [Bool] True if value is found, false if value is not found
    """
    if node is None:
        return False
    if node._value is not None:
        if node._value == value:
            return True
    return search(value, node._next)


def length(node):
    """
    Computes the length of list
    :param node: the head node of list
    :return: [int] the length of the list
    """
    if node is None:
        return 0
    if node is not None:
        count_len = length(node._next)
        count_len = count_len + 1
        return count_len


def sum_list(node):
    """
    Computes the sum of the list
    :param node: the head of list
    :return: [int] the sum of the list
    """
    if node is None:
        return 0
    if node is not None:
        sum_of_nodes = sum_list(node._next)
        return sum_of_nodes + node._value


def count(value, node):
    """
    Counts how many times the given value occurs
    :param value: value to find
    :param node: the head node
    :return: [int] the number of times the value occurs
    """

    if node is None:
        return 0
    if node is not None:
        if node._value == value:
            return count(value, node._next) + 1
        else:
            return count(value, node._next)


def reverse(node):
    """
    Reverse the list
    :param node: the head node
    :return: [LinkedNode] the starting node of the list
    """
    if node is None:
        return None

    if node is not None:
        if node._next is not None:
            reverse_node = reverse(node._next)
            node._next._next = node
            node._next = None
        else:
            return node
        return reverse_node


def list_percentage(node, percentage, counter=0):
    """
    Given list, find first node of subset of that list  based on input percentage
    :param node: the starting node of list
    :param percentage: percentage of entire list
    :param counter: count number of nodes in list
    :return: [LinkedNode] first node of subset
    """

    if node is None:
        return None

    if percentage == 0:
        return None

    if percentage == 1:
        return node

    counter += 1
    if node is not None:
        if node._next is not None:
            count_list = list_percentage(node._next, percentage, counter)
            if isinstance(count_list, LinkedNode):
                return count_list
            else:
                if count_list == counter:
                    return node

        if node._next is None:
            count_sublist = counter - (counter * percentage) + 1
            count_sublist = int(count_sublist)
            return count_sublist


# ***unable to pass list percentage hidden test case***
