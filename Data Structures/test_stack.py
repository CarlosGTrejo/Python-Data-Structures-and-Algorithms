# flake8: noqa
import pytest

import stack

s = None

def setup_function(function):
    global s
    s = stack.Stack()


def test_push():
    """Test push() items."""
    items = ('a', 1, False, None, object(), ['list'], {1,2,3}, dict(a=1), stack.Stack())
    for item in items:
        s.push(item)
    assert s.size == len(items)


def test_push_missing_item():
    """Test push() without passing item."""
    with pytest.raises(TypeError):
        s.push()


def test_peek():
    """Test peek() with items."""
    s.push('b')
    s.push('a')
    assert s.peek() == 'a'


def test_peek_empty():
    """Test peek() when stack is empty."""
    assert s.peek() == None


def test_pop_empty():
    """Test pop() when stack is empty."""
    assert s.size == 0
    with pytest.raises(IndexError):
        s.pop()


def test_pop():
    """Test pop() with items in stack."""
    for c in 'abc':
        s.push(c)
    for c in 'cba':
        assert s.pop() == c


def test_get_stack_empty():
    """Test get_stack() on empty stack."""
    assert s.get_stack() == []


def test_get_stack():
    """Test get_stack() on stack w/ items."""
    for c in 'abc':
        s.push(c)
    else:
        assert s.get_stack() == list('abc')


def test_is_empty_empty():
    """Test is_empty() on empty stack."""
    assert s.is_empty() == True


def test_is_empty():
    """Test is_empty() on stack w/ items."""
    s.push('a')
    assert s.is_empty() == False


def test_clear_empty():
    """Test clear() on empty stack."""
    s.clear()
    assert s.items == []


def test_clear():
    """Test clear() on stack w/ items."""
    s.push('a')
    s.clear()
    assert s.is_empty() == True


def test_len():
    """Test len() on stack."""
    for c in 'abc':
        s.push(c)
    else:
        assert len(s) == 3


def test_len_empty():
    """Test len_empty() on empty stack."""
    assert len(s) == 0


def teardown_function(function):
    global s
    del s
