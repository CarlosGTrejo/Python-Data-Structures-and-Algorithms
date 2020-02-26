# flake8: noqa
from itertools import cycle

import pytest

import singly_linked_list

llist = None

def setup_function(function):
    global llist
    llist = singly_linked_list.LinkedList()


def test_iter():
    """Iterating over the list should trigger __iter__ and return Nodes"""
    for c in 'abc': llist.append(c)

    for letter, node in zip('abc', llist):
        assert node.data == letter


def test_contains():
    """Doing Node in llist should return True if the Node is in the linked list, False otherwise
    If it's not a Node, then it should return True if the data/object is in the linked list, False otherwise."""
    x = singly_linked_list.Node('data')
    assert x not in llist

    for c in 'abc': llist.append(c)

    assert x not in llist
    node = llist[1]  # b
    assert node in llist
    assert 'a' in llist
    assert 'z' not in llist


def test_append_len():
    """Doing llist.append(obj) should add obj at the end of the linked list."""
    assert len(llist) == 0
    objects = ('a', 1, object(), ['list'], ('tuple',), {0: 'dict'}, {'set'})
    for length, o in enumerate(objects, start=1):
        llist.append(o)
        assert len(llist) == length
        assert llist.tail.data == o


def test_str_repr():
    """Calling str() and repr() on a linked list should output the data in a tuple as a string."""
    assert str(llist) == '()'
    assert repr(llist) == '()'
    llist.append('a')
    llist.append(123)
    assert str(llist) == "('a', 123)"
    assert repr(llist) == "('a', 123)"


def test_getitem():
    """Given an integer, n, llist[n] should return the node at position n"""
    with pytest.raises(TypeError):
        llist['a']

    with pytest.raises(IndexError):
        llist[0]

    with pytest.raises(NotImplementedError):
        llist[:]

    for c in 'abcdefg': llist.append(c)

    assert llist[0].data == 'a'
    assert llist[1].data == 'b'

    assert llist[-1].data == 'g'
    assert llist[-3].data == 'e'
    assert len(llist) == len('abcdefg')


def test_setitem():
    """llist[n] == obj should insert obj at index n"""
    with pytest.raises(IndexError):
        llist[0] = 'new data'

    llist.append('a')

    with pytest.raises(TypeError):
        llist['a'] = 'new data'

    with pytest.raises(TypeError):
        llist[2:3] = 'new data'

    llist[0] = 'new data'

    assert len(llist) == 1
    assert llist[0].data == 'new data'

    for c in 'abc': llist.append(c)

    llist[1] = 'x'

    assert len(llist) == 4
    assert str(llist) == "('new data', 'x', 'b', 'c')"

    llist[-1] = 'tail'

    assert len(llist) == 4
    assert str(llist) == "('new data', 'x', 'b', 'tail')"


def test_prepend():
    """Doing llist.prepend(obj) should add a new node with data, obj, at the beginning of the linked list."""
    objects = ('a', 1, object(), ['list'], ('tuple',), {0: 'dict'}, {'set'})
    for length, o in enumerate(objects, start=1):
        llist.prepend(o)
        assert len(llist) == length
        assert llist.head.data == o


def test_append_at_node():
    """Doing llist.append_at_node(node, obj), should add a new node containing data, obj, after the given node."""
    for o in (1, 'a', [], {}, ()):
        with pytest.raises(TypeError):
            llist.append_at_node(o, 'DATA')

    outside_node = singly_linked_list.Node('new node data')
    with pytest.raises(KeyError):
        llist.append_at_node(outside_node, 'New-er node data')

    for c in 'abc':
        llist.append(c)

    llist.append_at_node(llist[1], 'X')
    assert str(llist) == "('a', 'b', 'X', 'c')"


def test_insert_at_index():
    """Doing llist.insert_at_index(n) should insert a new node at the given index, n."""
    for c in 'abc': llist.append(c)

    with pytest.raises(TypeError):
        llist.insert_at_index('index', 'new data')

    with pytest.raises(ValueError):
        llist.insert_at_index(-2, 'new data')

    llist.insert_at_index(1, 'X')
    assert str(llist) == "('a', 'X', 'b', 'c')"

    llist.insert_at_index(400, 'tail')
    assert str(llist) == "('a', 'X', 'b', 'c', 'tail')"

    llist.insert_at_index(0, 'head')
    assert str(llist) == "('head', 'a', 'X', 'b', 'c', 'tail')"

    llist.insert_at_index(4, '3')
    assert str(llist) == "('head', 'a', 'X', 'b', '3', 'c', 'tail')"
    assert len(llist) == 7


def test_remove_node():
    """Doing llist.remove_node(data) should remove the first occurence of the node containing the given data."""
    with pytest.raises(ValueError):
        llist.remove_node('a')

    for c in 'abccd': llist.append(c)

    node_3 = llist[2]
    llist.remove_node('c')
    assert llist[2] != node_3
    assert len(llist) == len('abccd') - 1
    assert str(llist) == "('a', 'b', 'c', 'd')"

    with pytest.raises(ValueError):
        llist.remove_node('data')


def test_reverse():
    """Doing llist.reverse() should reverse the data in the list"""
    llist.reverse()

    for c in 'abcde':
        llist.append(c)

    llist.reverse()
    assert str(llist) == "('e', 'd', 'c', 'b', 'a')", f"List Content: {llist}"


def test_copy():
    """llist.copy() should return an exact copy of the data in the list"""
    for c in 'abc': llist.append(c)

    l_copy = llist.copy()
    assert str(l_copy) == str(llist)


def test_swap_small():
    """Doing llist.swap(N1,N2) in a list of length 0 or 1 should return ValueError"""
    with pytest.raises(ValueError):
        llist.swap('a', 'b')

    llist.append('a')

    with pytest.raises(ValueError):
        llist.swap('a','b')

def test_swap():
    """Doing llist.swap(N1, N2) should swap nodes N1 and N2."""
    for c in 'abcde': llist.append(c)

    llist.swap('a', 'a')
    assert str(llist) == str(tuple('abcde'))

    with pytest.raises(IndexError):
        N1 = singly_linked_list.Node('data1')
        N2 = 'data2'
        llist.swap(N1, N2)

    # Head-Tail swap
    cases = (
        ('a', 'e'),  # Neither is node
        (llist.head, llist.tail.data),  # One is node
        (llist.tail, llist.head),  # Both are nodes
        (llist.tail.data, llist.head)  # Switching order back to normal
    )
    for i,case in enumerate(cases, start=1):
        llist.swap(*case)
        assert {llist.head.data, llist.tail.data} == {'e', 'a'}, f"\n  Case #{i}: {case}\n{'='*20}"

        assert sorted((n.data for n in llist)) == list('abcde')

    # list data = a b c d e
    llist.swap('b', 'c')
    assert llist[1].data == 'c' and llist[2].data == 'b'
    assert str(llist) == str(tuple('acbde'))

    llist.swap('c', 'b')

    llist.swap('b', 'd')
    # a d c b e
    assert llist[1].data == 'd' and llist[-2].data == 'b'
    assert str(llist) == str(tuple('adcbe'))


    # Swapping by Node content
    # list data: a d c b e
    N1 = singly_linked_list.Node('x')
    llist.swap(N1, 'b')
    assert llist[-2].data == 'x', f"List Contents: {llist}"

    llist.swap('b', N1)
    assert llist[-2].data == 'b', f"List Contents: {llist}"

    llist.swap('x', 'b')
    assert llist[-2].data == 'x', f"List Contents: {llist}"

    llist.swap('b', 'x')
    assert llist[-2].data == 'b', f"List Contents: {llist}"
    assert str(llist) == str(tuple('adcbe'))


    # Head Swapping
    N2 = singly_linked_list.Node('H')
    old_head = llist[0]
    llist.swap(N2, llist[0])
    assert llist[0] == N2, f"List Contents: {llist}"

    llist.swap(N2, old_head)
    assert llist[0] == old_head, f"List Contents: {llist}"
    # list data: a d c b e
    assert str(llist) == str(tuple('adcbe'))


    # Tail swapping
    # ++Both keys are nodes++
    # Key1 is Node and not in list
    new_tail = singly_linked_list.Node('tail')
    og_tail = llist.tail
    llist.swap(new_tail, llist[-1])
    assert llist[-1].data == new_tail.data, f"List Contents: {llist}"

    llist.swap(llist[-1], og_tail)
    assert llist[-1] == og_tail, f"List Contents: {llist}"
    assert str(llist) == str(tuple('adcbe')), "List contents are not correct"


    # Key2 is Node and not in list
    N5 = singly_linked_list.Node('-2')
    old_node = llist[-2]
    llist.swap(old_node.data, N5)
    assert llist[-2] == N5, breakpoint()
    llist.swap(old_node, N5)
    assert str(llist) == str(tuple('adcbe'))


    # Key2 is NOT Node and not in list
    old_node = 'b'
    llist.swap(llist[-2], 'not node')
    assert llist[-2].data == 'not node'

    llist.swap(llist[-2], old_node)
    assert str(llist) == str(tuple('adcbe')), f"List Contents: {llist}"


    # Both keys are in list
    # Head swap
    old_head = llist.head
    new_head = llist.head.next
    llist.swap(llist.head, llist.head.next)
    assert llist.head == new_head

    # contents: d a c b e

    old_node = llist[-2]
    # breakpoint()
    llist.swap(old_node, llist.head)
    assert llist.head == old_node

    assert str(llist) == str(tuple('bacde'))


def teardown_function(function):
    global llist
    del llist
