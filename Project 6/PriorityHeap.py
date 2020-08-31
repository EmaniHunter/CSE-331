"""
PROJECT 6 - Priority Queues and Heaps
Name: Emani Hunter
"""


class Node:
    """
    This class represents a node object with k (key) and v (value)
    Node definition should not be changed in any way
    """

    def __init__(self, k, v):
        """
        Initializes node
        :param k: key to be stored in the node
        :param v: value to be stored in the node
        """
        self.key = k
        self.value = v

    def __lt__(self, other):
        """
        Less than comparator
        :param other: second node to be compared to
        :return: True if the node is less than other, False otherwise
        """
        return self.key < other.key or (self.key == other.key and self.value < other.value)

    def __gt__(self, other):
        """
        Greater than comparator
        :param other: second node to be compared to
        :return: True if the node is greater than other, False otherwise
        """
        return self.key > other.key or (self.key == other.key and self.value > other.value)

    def __eq__(self, other):
        """
        Equality comparator
        :param other: second node to be compared to
        :return: True if the nodes are equal, False otherwise
        """
        return self.key == other.key and self.value == other.value

    def __str__(self):
        """
        Converts node to a string
        :return: string representation of node
        """
        return '({0},{1})'.format(self.key, self.value)

    __repr__ = __str__


class PriorityHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """

    def __init__(self, is_min=True):
        """
        Initializes the priority heap
        """
        self._data = []
        self.min = is_min

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self._data)

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self._data)

    __repr__ = __str__

#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Modify below this line

    def empty(self):
        """
        Checks if the priority queue is empty
        :return: [Bool] true if empty, false otherwise
        """
        if len(self) == 0:
            return True
        else:
            return False

    def top(self):
        """
        Gives the root value of heap
        :return: [Node._value] the root's values
        """
        if len(self._data) == 0:
            return None
        else:
            root = self._data[0]
            return root.value

    def push(self, key, val):
        """
        Add a node to the heap
        :param key: key of node to be added
        :param val: value of node to be added
        """
        if key is None:
            return
        if val is None:
            return
        self._data.append(Node(key, val))
        self.percolate_up(len(self._data)-1)

    def pop(self):
        """
        Removes the top element from the priority queue
        :return: [Node] return a node element
        """
        if self.empty():
            return
        self.swap(0, len(self._data) - 1)  # put min or max item at end
        item = self._data.pop()
        item = Node(item.key, item.value)
        self.percolate_down(0)
        return item

    def _left(self, j):
        """
        Helper function, grab left child
        :return: [Index] index of left child
        """
        return 2*j + 1

    def _right(self, j):
        """
        Helper function, grab right child
        :return: [Index] index of right child
        """
        return 2*j + 2

    def _has_left(self, j):
        """
        Helper function, check if there is left child
        :return: [Bool]
        """
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        """
        Helper function, check if there is right child
        :return: [Bool]
        """
        return self._right(j) < len(self._data)

    def min_child(self, index):
        """
        Given an index of a node, return the index of the smaller child
        :param index: index of node
        :return: [int] index of smaller child
        """
        if not self._has_left(index):
            if not self._has_right(index):
                return None
        if self._has_left(index):
            left = self._left(index)
            small_child = left
            if self._has_right(index):
                right = self._right(index)
                if self._data[right] < self._data[left]:
                    small_child = right
                if self._data[right] == self._data[left]:
                    small_child = right
            return small_child

    def max_child(self, index):
        """
        Given an index of a node, return the index of the larger child
        :param index: index of node
        :return: [int] index of larger child
        """
        if not self._has_left(index):
            if not self._has_right(index):
                return None
        if self._has_left(index):
            left = self._left(index)
            large_child = left
            if self._has_right(index):
                right = self._right(index)
                if self._data[right] > self._data[left]:
                    large_child = right
                if self._data[right] == self._data[left]:
                    large_child = right
            return large_child

    def swap(self, i, j):
        """
        Helper function, swap indexes when needed
        """
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def percolate_up(self, index):
        """
        Given the index of a node, move the node up to its valid spot in the heap
        :param index: index of node
        """
        if index <= 0:
            return
        parent = (index - 1) // 2
        if self.min is True:
            if index > 0 and self._data[index] < self._data[parent]:
                self.swap(index, parent)
                self.percolate_up(parent)
        if self.min is False:
            if index > 0 and self._data[index] > self._data[parent]:
                self.swap(index, parent)
                self.percolate_up(parent)

    def percolate_down(self, index):
        """
        Given the index of a node, move the node down to its valid spot in the heap
        :param index: index of node
        """
        if self.min is True:
            if self._has_left(index):
                left = self._left(index)
                small_child = left
                if self._has_right(index):
                    right = self._right(index)
                    if self._data[right] < self._data[left]:
                        small_child = right
                    if self._data[right] == self._data[left]:
                        small_child = right
                if self._data[small_child] < self._data[index]:
                    self.swap(index, small_child)
                    self.percolate_down(small_child)
        else:
            if self._has_left(index):
                left = self._left(index)
                large_child = left
                if self._has_right(index):
                    right = self._right(index)
                    if self._data[right] > self._data[left]:
                        large_child = right
                    if self._data[right] == self._data[left]:
                        large_child = right
                if self._data[large_child] > self._data[index]:
                    self.swap(index, large_child)
                    self.percolate_down(large_child)


def heap_sort(array):
    """
    Given a list of data, use heap sort to sort the data
    :param array: list of data to sort
    :return: [List] list of sorted data
    """
    heap = PriorityHeap(False)
    if len(array) == 0:  # no elements
        return array
    new_list = [None] * len(array)
    for i in array:
        heap.push(i, 1)  # max heap
    for i in range(len(array)-1, -1, -1):  # remove max value by: move to end of heap, remove
        if len(array) == 1:  # single elements
            new_list[0] = array[0]
        if i >= 0:
            items = heap.pop()
            new_list[i] = items.key
    return new_list


def current_medians(values):
    """
    Keep track of the current median after each value of list is read in
    :param values: list of values
    :return: [List] list containing current median after each value has been read
    """
    min_heap = PriorityHeap()
    max_heap = PriorityHeap(False)
    medians = []
    current_median = 0
    if len(values) == 0:
        return medians
    for i in values:
        if len(values) % 2 == 0 or len(values) % 2 != 0:
            if i < current_median:
                max_heap.push(1, i)
            if i == current_median:
                max_heap.push(1, i)
            if i > current_median:
                min_heap.push(1, i)

            if len(max_heap) < len(min_heap):
                max_heap.push(1, min_heap.top())
                min_heap.pop()

            if len(min_heap) < len(max_heap):
                min_heap.push(1, max_heap.top())
                max_heap.pop()

            if len(min_heap) == len(max_heap):
                current_median = (max_heap.top() + min_heap.top()) / 2
                medians.append(current_median)
            if len(max_heap) > len(min_heap):
                current_median = max_heap.top()
                medians.append(current_median)
            if len(max_heap) < len(min_heap):
                current_median = min_heap.top()
                medians.append(current_median)

    return medians
