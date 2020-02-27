class Node:
    __slots__ = ("data", "next")

    def __init__(self, data: object, _next: "Node" = None):
        self.data, self.next = data, _next

    def __repr__(self):
        return repr((self.data))


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def __str__(self) -> str:
        """Returns the content of the linked list."""
        current_node = self.head
        data = ()  # Using tuple because it uses less memory
        while current_node:
            data += (current_node.data,)
            current_node = current_node.next

        return str(data)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        """Used whenever linked list needs to be iterated (for-loops, unpacking, etc.)
        Also gets rid of a lot of while-loops that were used in:
            * __getitem__
            * __setitem__
            * insert_at_index
            * etc."""
        curr = self.head
        while curr:
            yield curr
            curr = curr.next

    def __getitem__(self, key: int) -> Node:
        """Returns nodes on given key (index).
        Does not support negative indexing smaller than -1 or slices."""
        if isinstance(key, slice):
            raise NotImplementedError("Slices are not supported")
        if not isinstance(key, int):
            raise TypeError("indices must be integers")

        pre_tests = (
            (key >= self.length),  # index out of max range
            (key < 0 - self.length)  # index out of min range
        )

        if any(pre_tests):
            raise IndexError("linked list index out of range")

        if key in (0, 0 - self.length):
            return self.head
        elif key in (-1, self.length - 1):
            return self.tail
        else:  # if index is negative...
            node = self.head.next
            # Because head was returned, there is no need to
            # have index start at 0 or the min negative index
            index = 1 - self.length if key < 0 else 1
            while index != key:
                node = node.next
                index += 1

            return node  # On index and key match, return node

    def __setitem__(self, key, value):
        """Replaces the node's data at index, 'key', with 'value'."""
        if isinstance(key, slice):
            raise TypeError("indices must be integers, not slices")

        self[key].data = value

    def __contains__(self, item):
        for node in self:
            if item in (node, node.data):
                return True
        return False

    def append(self, data) -> None:
        """Adds (appends) a node to the end of the list."""
        new_node = Node(data)
        if self.length == 0:  # Add first node if list is empty
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next, self.tail = new_node, new_node

        self.length += 1

    def prepend(self, data) -> None:
        """Adds a node to the beginning of the list (prepend)."""
        self.head = Node(data, _next=self.head)
        self.length += 1

    def append_at_node(self, node: Node, data):
        """Inserts a new node after the given node."""
        if not isinstance(node, Node):
            raise TypeError("Argument 1 is not a node.")

        if node not in self:
            raise KeyError("Node not in linked list.")

        node.next = Node(data, _next=node.next)
        self.length += 1

    def insert_at_index(self, index: int, data) -> None:
        """Inserts a node at the given index.
        If the index is out of range, then it appends it to the end."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer.")
        if index < 0:
            raise ValueError("index must be non-negative")

        if index == 0:
            self.prepend(data)
        elif index >= self.length:
            self.append(data)
        else:
            # Not starting at head, 2nd if statment handled it
            node = self.head.next
            last_node = self.head
            node_index = 1
            while node_index != index:
                last_node = node
                node = node.next
                node_index += 1

            # Node indexes matched, so insert node
            last_node.next = Node(data, _next=node)
            self.length += 1

    def remove_node(self, data) -> None:
        """Removes a node that matches the given data."""
        if self.length == 0:
            raise ValueError(f"Data {data} not in linked list")
        last_node = cur_node = self.head
        while cur_node.next:
            if cur_node.data == data:
                break  # break if node data matches given data
            else:
                last_node, cur_node = cur_node, cur_node.next
        else:  # node NOT found
            raise ValueError(f"Data {data} not in linked list")
        # node found
        last_node.next = cur_node.next
        cur_node.data = cur_node.next = None  # GC will take care of it
        self.length -= 1

    def reverse(self):
        """Reverses the linked list order."""
        if self.length == 0: return

        curr, last = self.head, None
        while True:
            if curr is None: break
            curr.next, last = last, curr.next
            if last is None: break
            last.next, curr = curr, last.next
        self.tail, self.head = self.head, self.tail

    def copy(self):
        """Returns a copy of the linked list."""
        llist_copy = type(self)()
        for node in self:
            llist_copy.append(node.data)

        return llist_copy

    def swap(self, key1, key2) -> None:
        if self.length == 0: raise ValueError("Can't perfrom swap on an empty list")
        if self.length == 1: raise ValueError("Can't perform swap on a list of length 1")

        if key1 == key2:
            return

        head_tail = (
            {self.head, self.tail},
            {self.head.data, self.tail.data},
            {self.head.data, self.tail},
            {self.head, self.tail.data},
        )

        if {key1, key2} in head_tail:  # if either key1 or key2 is head and the other tail
            # then swap list head and list tail
            penultimate = self[-2]  # The node before the tail
            # swap head tail pointers first
            self.head, self.tail = self.tail, self.head
            self.head.next = self.tail.next
            self.tail.next = None
            penultimate.next = self.tail
            return

        prev_1, curr_1 = None, self.head
        prev_2, curr_2 = None, self.head
        found_key1, found_key2 = False, False

        for node in self:  # Key searching
            if key1 in (node, node.data) and not found_key1:  # 1st key found
                curr_1 = node
                found_key1 = True
            elif key2 in (node, node.data) and not found_key2:  # 2nd key found
                curr_2 = node
                found_key2 = True

            if found_key1 and found_key2:
                break  # No need to go through llist in vain if both keys are found
            else:  # Update prev nodes if keys not found yet
                prev_1 = node if not found_key1 else prev_1  # Update prev1 if key1 not found
                prev_2 = node if not found_key2 else prev_2  # Update prev2 if key2 not found
        else:  # One or more keys was not found
            if not any((found_key1, found_key2)):  # if neither key was found...
                raise IndexError(f"{key1} and {key2} are not in linked list.")

            # But if at least 1 key was found...
            if not found_key1:  # key1 is not in llist, swap key2 for key1
                if isinstance(key1, Node):  # perform node swap if key1 is Node
                    if curr_2 == self.head:  # assign new head if key2 is head
                        self.head = key1
                    elif curr_2 == self.tail:  # assign new tail if key2 is tail
                        self.tail = key1
                        prev_2.next = key1  # prev 2 pointer must be fixed for tail too
                    else:  # if key2 is not head, fix prev2 pointer
                        prev_2.next = key1
                    key1.next = curr_2.next
                    curr_2.next = None
                else:  # if key1 is not Node, swap data
                    curr_2.data = key1

                return

            elif not found_key2:  # key2 is not in llist, swap key1 for key2
                if isinstance(key2, Node):  # Node swap since key 2 is Node
                    if curr_1 == self.head:  # assign new head if key1 is head
                        self.head = key2
                    elif curr_1 == self.tail:  # assign new tail if key1 is tail
                        self.tail = key2
                        prev_1.next = key2  # prev 1 pointer must be fixed for tail
                    else:
                        prev_1.next = key2
                    key2.next = curr_1.next
                    curr_1.next = None
                else:  # key2 is not Node, swap key1.data
                    curr_1.data = key2
                return

        # Both keys are in llist, but one could be the head
        if prev_1:
            prev_1.next = curr_2
        else:  # Key 1 is head
            self.head = curr_2

        if prev_2:
            prev_2.next = curr_1
        else:  # Key 2 is head
            self.head = curr_1

        curr_1.next, curr_2.next = curr_2.next, curr_1.next  # swap
