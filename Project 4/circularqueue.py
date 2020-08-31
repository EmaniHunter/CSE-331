"""
Project 4 - Circular Queues
Name: Emani Hunter
"""
from collections import defaultdict


class CircularQueue:
    """
    Circular Queue Class.
    """

    # DO NOT MODIFY THESE METHODS
    def __init__(self, capacity=4):
        """
        Initialize the queue with an initial capacity
        :param capacity: the initial capacity of the queue
        """
        self.capacity = capacity
        self.size = 0
        self.data = [None] * capacity
        self.head = 0
        self.tail = 0

    def __eq__(self, other):
        """
        Defines equality for two queues
        :return: true if two queues are equal, false otherwise
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False

        if self.head != other.head or self.tail != other.tail:
            return False

        for i in range(self.capacity):
            if self.data[i] != other.data[i]:
                return False

        return True

    def __str__(self):
        """
        String representation of the queue
        :return: the queue as a string
        """
        if self.is_empty():
            return "Empty queue"

        str_list = [str(self.data[(self.head + i) % self.capacity]) for i in range(self.size)]
        return "Queue: " + ", ".join(str_list)

    # -----------MODIFY BELOW--------------

    def is_empty(self):
        """
        Returns whether or not the queue is empty (bool)
        :return: boolean, true if empty, false otherwise
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.size == 0:
            return True
        else:
            return False

    def __len__(self):
        """
        Overrides the len() method.
        :return: size of queue
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        return self.size

    def head_element(self):
        """
        Returns head element of queue
        :return: the front element of the queue or none if queue is empty
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.is_empty is not True:
            return self.data[self.head]
        else:
            return None

    def tail_element(self):
        """
        Returns tail element of queue
        :return: the last element of the queue or none if queue is empty
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.is_empty is not True:
            return self.data[self.tail-1]
        else:
            return None

    def grow(self):
        """
        Doubles the capacity of the queue immediately when capacity is reached to
        make room for new elements; Moves the head to the front of the
        newly allocated list
        """
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
        if self.capacity == self.size:
            count = 0
            new_list = [None] * (2 * self.capacity)
            for i in range(self.head, self.head + self.size):
                new_list[count] = self.data[i % self.capacity]
                count = count + 1
            self.head = 0
            self.tail = self.size
            self.capacity = 2 * self.capacity
            self.data = new_list

    def shrink(self):
        """
        Halves the capacity of the queue immediately if the
        size is 1/4 or less of the capacity
        """
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
        if self.size <= (self.capacity // 4):
            if (self.capacity // 2) >= 4:
                count = 0
                new_list = [None] * (self.capacity // 2)
                for i in range(self.head, self.head + self.size):
                    new_list[count] = self.data[i % self.capacity]
                    count = count + 1
                self.head = 0
                self.tail = self.size
                self.capacity = self.capacity // 2
                self.data = new_list

    def enqueue(self, val):
        """
        Add an element val to the back of the queue
        :param val: value to enqueue
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.is_empty is True:
            self.tail = 1
            self.data[self.tail] = val
            self.size += 1
            return None
        else:
            self.data[self.tail] = val
            self.tail = (self.tail + 1) % self.capacity
            self.size += 1
            if self.size == len(self.data):
                self.grow()

    def dequeue(self):
        """
        Remove an element from the front of a queue.
        :return: element popped. If empty, return None
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.is_empty is True:
            return None

        ele_pop = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        if self.size <= (self.capacity // 4):
            self.shrink()
        return ele_pop


class QStack:
    """
    Stack class, implemented with underlying Circular Queue
    """
    # DO NOT MODIFY THESE METHODS
    def __init__(self):
        self.cq = CircularQueue()
        self.size = 0

    def __eq__(self, other):
        """
        Defines equality for two QStacks
        :return: true if two stacks are equal, false otherwise
        """
        if self.size != other.size:
            return False

        if self.cq != other.cq:
            return False

        return True

    def __str__(self):
        """
        String representation of the QStack
        :return: the stack as a string
        """
        if self.size == 0:
            return "Empty stack"

        str_list = [str(self.cq.data[(self.cq.head + i) % self.cq.capacity]) for i in range(self.size)]
        return "Stack: " + ", ".join(str_list)

    # -----------MODIFY BELOW--------------
    def push(self, val):
        """
        Adds an element, val, to the top of the stack.
        :param val: value to push
        """
        # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(1)
        if self.size == 0:
            self.cq.enqueue(val)
            self.size = self.size + 1
        else:
            self.cq.enqueue(val)
            for i in range(0, (len(self.cq))-1):
                ele_pop = self.cq.dequeue()
                self.cq.enqueue(ele_pop)
            self.size = self.size + 1

    def pop(self):
        """
        Removes an element from the top of the stack,
        :return: element popped. If empty, return None.
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.size == 0:
            return None
        top_ele = self.cq.dequeue()
        self.size = self.size - 1
        if top_ele is None:
            return None
        return top_ele

    def top(self):
        """
        Returns top element of the stack.
        :return: top element of stack, none if stack is empty
        """
        # TIME COMPLEXITY: O(1) ; SPACE COMPLEXITY: O(1)
        if self.size == 0:
            return None
        return self.cq.head_element()


def digit_swap(nums, replacements):
    """
     Return the length of the longest substring of "nums" that contains the same character,
     given that you are allowed to swap "replacements" amount of characters
     :param nums: string of numbers to swap elements
     :param replacements: number of swaps that you are permitted to make
     :return: length of longest substring
    """
    # TIME COMPLEXITY: O(n) ; SPACE COMPLEXITY: O(n)
    dict_of_nums = defaultdict(int)
    current_max = 0
    new_max = 0
    cq = CircularQueue()

    if nums == '':
        return
    if replacements == len(nums):
        return len(nums)
    if replacements > 0 and replacements != len(nums):
        for i in nums:
            cq.enqueue(i)
            dict_of_nums[i] = dict_of_nums[i] + 1
            current_max = max(current_max, dict_of_nums[i])
            lengths_diff = len(cq) - current_max
            if replacements < lengths_diff:
                ele_pop = cq.dequeue()
                dict_of_nums[ele_pop] = dict_of_nums[ele_pop] - 1
            new_max = max(new_max, len(cq))
        return new_max
