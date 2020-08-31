"""
Implemented by: Yash Vesikar and Brandon Field
"""

class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key, value, deleted=False):
        self.key = key
        self.value = value
        self.deleted = deleted

    def __repr__(self):
        return f"HashNode({self.key}, {self.value})"

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other):
        self.value += other


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity=8):
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other):
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __repr__(self):
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    def _hash_1(self, key):
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key):
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param x: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    def __len__(self):
        """
        don't edit this plz
        Getter for size
        :return: size
        """
        return self.size

    ########## EDIT BELOW ##########

    def __setitem__(self, key, value):
        '''
        Creates a node in the hash table that has the key and value that are passed in as parameters
        :param key: [Str] key for HashNode
        :param value: [int] value for HashNode
        '''
        self._insert(key, value)

    def __getitem__(self, key):
        '''
        Gets the item with the key denoted by the item parameter
        :param key: [Str] key that helps find node in table
        :return: the node's value that was found with input key
        '''
        if key is None:
            raise KeyError
        node = self._get(key)
        if node is None:
            raise KeyError
        return node.value

    def __delitem__(self, key):
        '''
        Deletes the node that has the value denoted by the key parameter
        :param key: [Str] key to find node to delete
        '''
        if key is None:
            raise KeyError
        self._delete(key)

    def __contains__(self, key):
        '''
        Determines if a node with the key denoted by the item parameter exists in the table
        :param key: [Str] key to find node in table
        :return: [bool] true if node with key is in table, false otherwise
        '''
        if self.size == 0:
            return False
        if key is not None:
            key_index = self.hash(key)
            if self.table[key_index] is None:
                return False
            if self.table[key_index].key == key and self.table[key_index] is not None:
                return True

    def hash(self, key, inserting=False):
        '''
        Given a key string return an index in the hash table.
        :param key: [Str] key to find node in table
        :param inserting: False when performing deletion/ lookup, True otherwise if inserting node
        :return: [int] the index of the node with the key
        '''
        index = 0
        initial_hash = self._hash_1(key)
        step_size = self._hash_2(key)

        if self.table[initial_hash] is None:
            return initial_hash
        if self.table[initial_hash].key == key:
            return initial_hash
        if self.table[initial_hash].key != key:
            while index < self.capacity:
                if inserting is True:
                    double_hash = (initial_hash + index * step_size) % self.capacity
                    if self.table[double_hash] is None:
                        return double_hash
                    if self.table[initial_hash] == HashNode(None, None, True):
                        return double_hash
                else:
                    double_hash = (initial_hash + index * step_size) % self.capacity
                    if self.table[double_hash] is None:
                        return double_hash
                    if self.table[double_hash].key == key:
                        return double_hash
                index += 1

    def _insert(self, key, value):
        '''
        Use the key and value parameters to add a HashNode to the hash table.
        :param key: [Str] key to place in new node
        :param value: [int] value of node to insert/ overwrite
        '''
        if key is not None:
            key_index = self.hash(key, inserting=True)
            new_node = HashNode(key, value)
            if self.table[key_index] is None:
                self.table[key_index] = new_node
                self.size += 1
            else:
                node_key = self.table[key_index].key
                if node_key is not None:
                    if node_key == key:
                        self.table[key_index].value = value
            if self.size >= self.capacity // 2:
                self._grow()

    def _get(self, key):
        '''
        Find the HashNode with the given key in the hash table.
        :param key: key to find node in table
        :return: [Node] return node with given key
        '''
        key_index = self.hash(key)

        if key_index is None:
            return None
        if self.table[key_index] is not None:
            if self.table[key_index].key == key:
                return self.table[key_index]
        else:
            return None

    def _delete(self, key):
        '''
        Removes the HashNode with the given key from the hash table .
        :param key: [Str] key to find node in table to delete
        '''
        key_index = self.hash(key)
        if self.table[key_index] is not None:
            if self.table[key_index].key == key:
                self.table[key_index].key = None
                self.table[key_index].value = None
                self.table[key_index].deleted = True
                self.size -= 1
        else:
            return None

    def _grow(self):
        '''
        Double the capacity of the existing hash table.
        '''
        if self.size >= self.capacity // 2:
            copy_table = self.table
            self.capacity = self.capacity * 2
            self.table = [None] * self.capacity
            self.size = 0

            i = 0
            while HashTable.primes[i] < self.capacity:
                i += 1
            self.prime_index = i - 1

            for i in copy_table:
                if i is not None and i.deleted is False:
                    if i.value is not None:  # None is valid for key in setitem
                        self._insert(i.key, i.value)

    def update(self, pairs=[]):
        '''
        Updates the hash table using an iterable of key value pairs
        :param pairs: [iterable] list of pairs to update hash table with
        '''
        for i in pairs:
            k, v = i
            self._insert(k, v)

    def setdefault(self, key, default=None):
        '''
        Sets the default value for the key denoted by the key parameter using the default parameter
        :param key: [Str] key to find node in table
        :param default: default value to set for key
        :return: if node's value is none return default parameter otherwise return node's value
        '''
        key_index = self.hash(key)
        if key_index is None:
            return None

        if self.table[key_index] is None:
            self._insert(key, default)
            return default

        if self.table[key_index].key == key:
            return self.table[key_index].value

    def keys(self):
        '''
        Returns a generator object that contains all of the keys in the table
        :return: generator object of all keys in table
        '''
        for node in self.table:
            if node is not None:
                yield node.key

    def values(self):
        '''
        Returns a generator object that contains all of the values in the table
        :return: generator object of all values in table
        '''
        for node in self.table:
            if node is not None and node.value is not None:
                yield node.value

    def items(self):
        '''
        Returns a generator object that contains all of the items in the table
        :return: generator object tuple of all items (key/value pairs) in table
        '''
        for item in self.table:
            if item is not None:
                tuple_pairs = (item.key, item.value)
                yield tuple_pairs

    def clear(self):
        '''
        Clears table of HashNodes
        '''
        for i in range(len(self.table)):
            self.table[i] = None
        self.size = 0


def hurdles(grid):
    '''
    Given a grid that denotes a grid of hurdles, determine the minimum number of hurdles you will
    need to jump over
    :param grid: [list] 2D grid representing rows and hurdles inside
    '''
    new_table = HashTable()
    if len(grid) == 1:
        return len(grid)
    for col in range(len(grid[0])):
        col_width = 1
        hurdle_count = 0
        for row in range(len(grid)):
            col_width = (col_width + row) - 1
            if row < len(grid):
                hurdle_count += 1
            else:
                hurdle_count += 0
            new_table[str(row)] = hurdle_count
            if 0 < col < len(grid):
                new_table[str(row)] += 1

    return min(new_table.values())
    
    # could not pass hidden test case for hurdles
