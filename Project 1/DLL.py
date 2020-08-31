class DLLError(Exception):
    """
    Class representing an error related to the DLL class implemented below.
    """
    pass


class DLLNode:
    """
    Class representing a node in the doubly linked list implemented below.
    """

    def __init__(self, value, next=None, prev=None):
        """
        Constructor
        @attribute value: the value to give this node
        @attribute next: the next node for this node
        @attribute prev: the previous node for this node
        """
        self.next = next
        self.prev = prev
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class DLL:
    """
    Class representing a doubly linked list.
    """

    def __init__(self):
        """
        Constructor
        @attribute head: the head of the linked list
        @attribute tail: the tail of the linked list
        @attribute size: the size of the linked list
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __repr__(self):
        """
        iterates through the linked list to generate a string representation
        :return: string representation of the linked list
        """
        res = ""
        node = self.head
        while node:
            res += str(node)
            if node.next:
                res += " "
            node = node.next
        return res

    def __str__(self):
        """
        iterates through the linked list to generate a string representation
        :return: string representation of the linked list
        """
        res = ""
        node = self.head
        while node:
            res += str(node)
            if node.next:
                res += " "
            node = node.next
        return res

    ######### MODIFY BELOW ##########

    def is_empty(self):
        """
        Determines if the linked list is empty or not
        :return: [boolean] true if DLL is empty, false otherwise
        """
        if self.head is None:  # if linked list is empty
            return True
        else:
            return False

    def insert_front(self, value):  # prepend
        """
        Inserts a value into the front of the list
        :param value: the value to insert
        """
        node_val = DLLNode(value)  # give val node attributes

        if self.head is None:  # if linked list is empty
            self.head = node_val  # head points to newly inserted value
            self.tail = node_val  # tail points to newly inserted val
            self.size = self.size+1
        else:
            node_val.next = self.head  # the values next pointer points to node that head currently points to
            self.head.prev = node_val  # current head node's previous pointer points to new value
            self.head = node_val  # let head point to new value
            self.size = self.size+1

    def insert_back(self, value):  # append
        """
        Inserts a value into the back of the list
        :param value: the value to insert
        """
        node_val = DLLNode(value)  # give val node attributes

        if self.head is None:  # if linked list is empty
            self.head = node_val  # head points to newly inserted value
            self.tail = node_val  # tail points to newly inserted val
            self.size = self.size + 1
        else:
            self.tail.next = node_val  # tail's next pointer points to newly inserted val
            node_val.prev = self.tail  # new value's previous pointer points to tail node
            self.tail = node_val  # tail node pointer updated to point to newly inserted val
            self.size = self.size + 1

    def delete_front(self): # remove first
        """
        Deletes the front node of the list
        """
        if self.head is None:
            raise DLLError

        if self.size == 1:  # accounting for only one item in list
            self.head = None
            self.tail = None
            self.size = self.size - 1

        if self.size > 1:
            self.head = self.head.next  # make head node point to successor node
            self.head.prev = None  # assigning head previous pointer to point to null
            self.size = self.size - 1

    def delete_back(self):  # remove last
        """
        Deletes the back node of the list
        """
        if self.head is None:
            raise DLLError

        if self.size == 1:
            self.head = None
            self.tail = None
            self.size = self.size - 1

        if self.size > 1:
            self.tail = self.tail.prev  # make tail node point to current tail's previous pointer node
            self.tail.next = None  # assigning tail next pointer to point to null because end of list
            self.size = self.size - 1

    def delete_value(self, value):
        """
        Deletes the first instance of the value in the list.
        :param value: The value to remove
        """

        cur_node = self.head
        if self.head is None:
            raise DLLError

        if cur_node.value == value:
            return self.delete_front()

        cur_node = cur_node.next
        while cur_node.next is not None:
            if cur_node.value == value:  # compare values
                cur_node.prev.next = cur_node.next
                cur_node.next.prev = cur_node.prev
                self.size = self.size - 1
                return
            cur_node = cur_node.next

        if cur_node == self.tail:
            if cur_node.value == value:
                return self.delete_back()
            else:
                raise DLLError

    def delete_all(self, value):
        """
        Deletes all instances of the value in the list
        :param value: the value to remove
        """
        cur_node = self.head
        value_exists = False
        if self.head is None:
            raise DLLError

        while cur_node is not None:
            if cur_node.value == value:
                for i in range(self.count(cur_node.value)):
                    self.delete_value(value)
                    value_exists = True
            cur_node = cur_node.next
        if value_exists is False:
            raise DLLError

    def find_first(self, value):  # traverse forward
        """
        Finds the first instance of the value in the list
        :param value: the value to find
        :return: [DLLNode] the first node containing the value
        """
        cur_node = self.head
        first_node = DLLNode(value)
        value_exists = False

        if self.head is None:
            raise DLLError

        while cur_node is not None:
            if cur_node.value == value:  # compare values
                if cur_node == self.head:  # if the current node IS the head node
                    first_node.next = cur_node.next
                    first_node.prev = cur_node.prev
                    value_exists = True
                    return first_node

                if cur_node == self.tail:
                    first_node.next = cur_node.next
                    first_node.prev = cur_node.prev
                    value_exits = True
                    return first_node

                if cur_node != self.head or cur_node != self.tail:
                    first_node.next = cur_node.next
                    first_node.prev = cur_node.prev
                    value_exists = True
                    return first_node

            cur_node = cur_node.next

        if value_exists is False:
            raise DLLError  # if nothing returns then raise error-- flags for not having deleted anything

    def find_last(self, value):  # reverse traverse
        """
        Finds the last instance of the value in the list
        :param value: the value to find
        :return: [DLLNode] the last node containing the value
        """
        cur_node = self.tail
        last_node = DLLNode(value)
        value_exists = False

        if self.head is None:
            raise DLLError

        while cur_node is not None:
            if cur_node.value == value:  # compare values
                if cur_node == self.head:  # if the current node IS the head node
                    last_node.next = cur_node.next
                    last_node.prev = cur_node.prev
                    value_exists = True
                    return last_node

                if cur_node == self.tail:
                    last_node.next = cur_node.next
                    last_node.prev = cur_node.prev
                    value_exists = True
                    return last_node

                if cur_node != self.head or cur_node != self.tail:
                    last_node.next = cur_node.next
                    last_node.prev = cur_node.prev
                    value_exists = True
                    return last_node

            cur_node = cur_node.prev

        if value_exists is False:
            raise DLLError  # if nothing returns then raise error-- flags for not having deleted anything

    def find_all(self, value):
        """
        Finds all of the instances of the value in the list
        :param value: the value to find
        :return: [List] a list of the nodes containing the value
        """
        cur_node = self.head
        list_value_nodes = []
        value_exists = False

        while cur_node is not None:
            if cur_node.value == value:
                list_value_nodes.append(cur_node)
                value_exists = True
            cur_node = cur_node.next

        if self.head is None:
            raise DLLError

        if value_exists is False:
            raise DLLError

        return list_value_nodes

    def count(self, value):
        """
        Finds the count of times that the value occurs in the list
        :param value: the value to count
        :return: [int] the count of nodes that contain the given value
        """
        cur_node = self.head
        count = 0

        if self.head is None:
            return 0

        while cur_node is not None:
            if cur_node.value == value:
                count = count + 1
            cur_node = cur_node.next
        return count

    def sum(self):
        """
        Finds the sum of all nodes in the list
        :param start: the indicator of the contents of the list
        :return: the sum of all items in the list
        """
        if self.head is None:
            return None

        if self.size == 1:
            return self.head.value

        sum_of_items = self.head.value
        self.head = self.head.next
        while self.head is not None:
            sum_of_items = sum_of_items + self.head.value
            self.head = self.head.next
        return sum_of_items


def reverse(LL):
    """
    Reverses a linked list in place
    :param LL: The linked list to reverse
    """
    store_node = None
    cur_node = LL.head

    if LL.size == 0:
        return

    if LL.size == 1:
        LL.head = cur_node
        LL.tail = cur_node

    while cur_node is not None:
        LL.tail = LL.head
        store_node = cur_node.prev
        cur_node.prev = cur_node.next
        cur_node.next = store_node
        cur_node = cur_node.prev

    if store_node is not None:
        LL.head = store_node.prev

    return
