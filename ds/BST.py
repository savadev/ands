#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Nelson Brochado
Creation: July, 2015
Last update: 11/09/2015

Basic class to represent binary search trees (BSTs).

NAMES' CONVENTIONS
In general, if a variable name has more than one word,
those words are separated by _ (underscores).
Functions' names should roughly describe what the function does.
Names of functions' local variables are usually short,
and not so self-descriptive, but, on the other hand,
comments are usually provide on the first occurrence of the name,
in order to explain the purpose of such a variable.

FUNCTIONS:
- Methods that start with _ should not be called.
They are usually helper functions.

- Methods that start with __ should definitely NOT be called.
They are helper functions that usually are not independent from other functions.

PARAMETERS:
- u and v are used to usually indicate that a BSTNode object is expected.
- s is used to indicate that a source node (which is also BSTNode object) is expected.
- x is used when the parameter's expected type can either be a BSTNode object
or any other comparable object to represent keys.
- ls is usually used to indicate that a list or a tuple is expected.

LOCAL VARIABLES:
- c usually indicates some "current" changing variable.
- p is usually c's parent.

DOC-STRINGS:
Under methods' signatures, h in O(h) is the height of the tree.
Note that the height of a BST varies
depending on how elements are inserted and removed.

Other names are self-descriptive.
For example, "key" and "value" are self-descriptive.


Want to know more about BSTs?

- https://en.wikipedia.org/wiki/Binary_search_tree
- Introduction to Algorithms (3rd edition) by CLRS, chapter 12.
- http://algs4.cs.princeton.edu/32bst/
- http://www.cs.princeton.edu/courses/archive/spr04/cos226/lectures/bst.4up.pdf
- http://algs4.cs.princeton.edu/32bst/BST.java.html


TODO
- Implement a recursive version of insert_key (just for educational purposes).
- Decide which functions are static and which are not, and why.
- Improve the "randomness" of insertion into the bst.
"""

from ands.ds.BSTNode import *
from random import *


class BST:

    def __init__(self, root=None, name="BST"):
        self.root = None
        self.name = name
        self.n = 0  # Number of nodes.

        if root is not None:
            self._initialise(root)

    # INITIALISE

    def _initialise(self, u: BSTNode):
        """Sets u as the new root of this tree."""
        self.root = u
        self.root.parent = None
        self.root.left = None
        self.root.right = None
        self.n = 1

    def size(self):
        """Returns the total number of nodes."""
        return self.n

    def is_empty(self):
        """Returns True if this tree has 0 nodes."""
        return self.size() == 0

    def is_the_root(self, u):
        """Checks if u is a reference pointing to the root object."""
        if u == self.root:
            return True
        return False

    def clear(self):
        """Removes all nodes from this tree."""
        self.root = None
        self.n = 0

    @staticmethod
    def check_arg(x):
        """Raises a TypeError if x is None."""
        if x is None:
            raise TypeError("x cannot be None.")

    # INSERTIONS

    def insert(self, x, value=None):
        """Inserts x into this tree.

        x can either be a BSTNode object,
        or it can be a key of any other type,
        but it should be of the same type of the other keys,
        and these keys should be comparable objects.

        Note that the height of a BST varies
        depending on how elements are inserted and removed.
        For example, if we insert a list of numbers in increasing order,
        the resulting BST object will look like a chain with height n - 1,
        where n is the number of elements inserted.
        In general, the optimal height is logarithmic,
        and to get closer to the optimal height,
        randomly insertion of numbers usually is used.

        If we have n keys to insert, there are n! (n-factorial)
        ways of inserting those n keys into the binary search tree.
        When we randomly insert them, those permutations are equally likely.

        So, the expected height of a tree created with randomly insertions is O(log_2(n)).
        For a proof, see chapter 12 of Introduction to Algorithms (3rd ed.) by CLRS.

        This function does a pseudo-random insertion of keys."""
        r = randint(0, self.size() * 3 // 8)  # * 3 // 8 is just a random operation XD
        if r == 0:
            self.root_insert(x, value)
        else:
            self.tail_insert(x, value)

    def insert_many(self, ls):
        """Calls self.tail_insert for all elements of ls.

        Therefore the elements of ls should either be
        BSTNode objects or they should represent keys.

        Time complexity: O(len(ls)*h)"""
        for i in ls:
            self.insert(i)

    def tail_insert(self, x, value=None):
        """Inserts x into this BST object.

        x can either be a BSTNode object,
        or it can be a key of any other type,
        but it should be of the same type of the other keys,
        and these keys should be comparable objects.
        Note that if you tail_insert x as a key,
        you can also pass a value to associate with x.

        Time complexity: O(h)"""
        if x is None:
            raise TypeError("x cannot be None.")

        if not isinstance(x, BSTNode):
            x = BSTNode(x, value)

        if self.root is None:
            self._initialise(x)
        else:
            c = self.root  # c is the current node.
            p = self.root.parent  # Parent of c.

            while c is not None:
                p = c
                if x.key < c.key:
                    c = c.left
                else:  # x.key >= c.key
                    c = c.right

            if x.key < p.key:
                p.left = x
            else:
                p.right = x

            x.parent = p

            self.n += 1

    def root_insert(self, x, value=None):
        """Inserts x as the root of this tree.

        x can either be a key or a BSTNode object.
        In the former case, a BSTNode object is first created to host x.
        If x is a key, you can also provide a value,
        which is then associated with the BSTNode object with key x.

        Time complexity: O(h)"""
        if x is None:
            raise TypeError("x cannot be None.")

        if not isinstance(x, BSTNode):
            x = BSTNode(x, value)

        if self.root is None:
            self._initialise(x)
        else:
            self._root_insert(self.root, x)
            self.n += 1

    def _root_insert(self, u: BSTNode, v: BSTNode):
        """Helper method for self.root_insert

        Time complexity: O(h)"""
        if u is None:
            return v
        if v.key < u.key:
            u.left = self._root_insert(u.left, v)
            u = self.right_rotate(u)
        else:
            u.right = self._root_insert(u.right, v)
            u = self.left_rotate(u)
        return u

    # SEARCH

    def search(self, key, s: BSTNode=None) -> BSTNode:
        """Searches for the key in the tree.
        If s is specified, then this procedure starts searching from s.

        key must be a comparable object of the same type as the other keys.

        Time complexity: O(h)"""
        if s is None:
            return self.search_i(key)
        else:
            return BST._search_i(key, s)

    def search_r(self, key) -> BSTNode:
        """Searches recursively for key starting from the root.
        
        Time complexity: O(h)"""
        return self._search_r(key, self.root)

    def _search_r(self, key, s: BSTNode) -> BSTNode:
        """Searches recursively for key in the subtree rooted at s.

        key must be a comparable object of the same type as the other keys.

        Time complexity: O(m),
        where m is the height of the subtree rooted at s,
        if s is not None. Else the time complexity is O(1)."""
        if s is None or key == s.key:
            return s
        elif key < s.key:
            return self._search_r(key, s.left)
        else:  # key > root_node.key
            return self._search_r(key, s.right)

    def search_i(self, key) -> BSTNode:
        """Searches iteratively for key starting from the root.

        Time complexity: O(h)"""
        return BST._search_i(key, self.root)

    @staticmethod
    def _search_i(key, s: BSTNode):
        """Searches iteratively for key in the subtree rooted at root_node.

        Time complexity: O(m),
        where m is the height of the subtree rooted at s,
        if s is not None. Else the time complexity is constant."""
        c = s  # c is the current node
        while c is not None:
            if key == c.key:
                return c
            elif key < c.key:
                c = c.left
            else:  # key > c.key:
                c = c.right

    # CONTAINS

    def contains(self, key):
        """Returns True if a BSTNode object with key exists in the tree."""
        return self.search_r(key) is not None

    # SELECT

    def rank(self, key):
        """Returns the number of keys strictly less than key."""
        if self.root is None:
            return 0
        else:
            r = 0
            return self._rank(self.root, key, r)

    def _rank(self, u: BSTNode, key, r: int):
        if u is None:
            return r
        if u.key < key:
            r += 1
        r = self._rank(u.left, key, r)
        r = self._rank(u.right, key, r)
        return r

    def height(self):
        """Returns the maximum depth or height of the tree."""
        if self.root is None:
            return 0
        return self._height(self.root)

    def _height(self, u: BSTNode):
        if u is None:
            return -1
        return 1 + max(self._height(u.left), self._height(u.right))

    # TRAVERSALS

    def in_order_traversal(self):
        """See BST._in_order_traversal"""
        self._in_order_traversal(self.root)
        print("\n")

    def _in_order_traversal(self, u: BSTNode, e=", "):
        """Prints the elements of the tree in increasing order.

        Time complexity: theta(m),
        where m is the number of elements rooted under u (included)."""
        if u is not None:
            self._in_order_traversal(u.left)
            print(u, end=e)
            self._in_order_traversal(u.right)

    def pre_order_traversal(self):
        """See BST._pre_order_traversal"""
        self._pre_order_traversal(self.root)
        print("\n")

    def _pre_order_traversal(self, u: BSTNode, e=", "):
        """Prints the keys in pre-order starting from u.
        In other words, it prints first u,
        then its left child node and then its right child node.
        It keeps doing this recursively.

        Time complexity: theta(m),
        where m is the number of elements rooted under u (included)."""
        if u is not None:
            print(u, end=e)
            self._pre_order_traversal(u.left)
            self._pre_order_traversal(u.right)

    def post_order_traversal(self):
        """See self._post_order_traversal"""
        self._post_order_traversal(self.root)
        print("\n")

    def _post_order_traversal(self, u: BSTNode, e=", "):
        """Prints the keys in post-order.

        It does the opposite of BST._pre_order_traversal

        Time complexity: theta(m),
        where m is the number of elements rooted under u (included)."""
        if u is not None:
            self._post_order_traversal(u.left)
            self._post_order_traversal(u.right)
            print(u, end=e)

    def reverse_in_order_traversal(self):
        """See self._reverse_in_order_traversal"""
        self._reverse_in_order_traversal(self.root)
        print("\n")

    def _reverse_in_order_traversal(self, u: BSTNode, e=", "):
        """Prints the keys in decreasing order.

        It does the opposite of BST._in_order_traversal

        Time complexity: theta(m),
        where m is the number of elements rooted under u (included)."""
        if u is not None:
            self._reverse_in_order_traversal(u.right)
            print(u, end=e)
            self._reverse_in_order_traversal(u.left)

    # ROTATIONS

    def left_rotate(self, x):
        """Left rotates the subtree rooted at node x.

        x can be a BSTNode object, and in that case,
        this function performs in constant time O(1);
        else, if node is not a BSTNode object,
        it tries to search for a BSTNode object with key=x,
        and, in that case, it performs in O(h) time.

        Returns the node which is at the previous position of x,
        that is it returns the parent of x."""

        c = None  # It will rotate the subtree rooted at c.

        if not isinstance(x, BSTNode):
            c = self.search(x)
            if c is None:
                raise Exception("key node was not found in the tree.")
        else:  # x should be a BSTNode object
            c = x

        if c is None:
            raise Exception("x cannot be None.")

        # To left rotate a node, its right child must exist.
        if c.right is None:
            raise Exception("Left rotation cannot be performed on " + str(c) +
                            " because it does not have a right child.")

        c.right.parent = c.parent

        # If the following expression is evaluated to True,
        # then this implies that c is the root
        # and the new root becomes the right child.
        if c.parent is None:
            self.root = c.right

        # Checking if c is a left or a right child,
        # in order to set the new left or right child (respectively) of its parent.
        elif c.is_left_child():
            c.parent.left = c.right

        else:  # c.is_right_child():
            c.parent.right = c.right

        # Setting the new parent of c,
        # which is its right child.
        c.parent = c.right

        # Setting the new right child of c
        # Note that the current parent of c
        # is what was its previous right child
        # So, basically, the new right child of c
        # becomes what is the left child of its previous right child.
        c.right = c.parent.left

        # Checking if the new right child of c is None,
        # because, if it is not, we need to set its parent to be c
        if c.right is not None:
            c.right.parent = c

        # Now, we can set c to be the new left child
        # of its new parent (which was its previous right child).
        c.parent.left = c

        return c.parent

    def right_rotate(self, x):
        """Right rotates the subtree rooted at node x.

        See doc-strings of left_rotate."""
        c = None

        if not isinstance(x, BSTNode):
            c = self.search(x)
            if c is None:
                raise Exception("key node was not found in the tree.")
        else:
            c = x

        if c is None:
            raise Exception("x cannot be None.")

        if c.left is None:
            raise Exception("Right rotation cannot be performed on " + str(c) +
                            " because it does not have a left child.")

        c.left.parent = c.parent

        # If the following expression is evaluated to True,
        # then this implies that c is the root
        # and the new root becomes the right child.
        if c.parent is None:
            self.root = c.left
        # Checking if c is a left or a right child,
        # in order to set the new left or right child (respectively) of its parent.
        elif c.is_left_child():
            c.parent.left = c.left
        else:  # c.is_right_child():
            c.parent.right = c.left

        # Setting the new parent of c
        c.parent = c.left

        # Setting the new right child of c
        c.left = c.parent.right

        if c.left is not None:
            c.left.parent = c

        c.parent.right = c
        return c.parent

    # MINIMUM AND MAXIMUM

    def minimum(self):
        """Calls BST._minimum_r(self.root) if self.root is not None."""
        if self.root is not None:
            return self._minimum_r(self.root)

    def _minimum_r(self, u: BSTNode):
        """Recursive version of the BST._minimum(u) function.

        Time complexity: O(h)"""
        if u.left is not None:
            u = self._minimum_r(u.left)
        return u

    @staticmethod
    def _minimum(u: BSTNode):
        """Returns the node (rooted at u) with the minimum key."""
        while u.left is not None:
            u = u.left
        return u

    def maximum(self):
        """Calls BST._maximum_r(self.root) if self.root is not None."""
        if self.root is not None:
            return self._maximum_r(self.root)

    def _maximum_r(self, u: BSTNode):
        """Recursive version of BST._maximum.

        Time complexity: O(h)"""
        if u.right is not None:
            u = self._maximum_r(u.right)
        return u

    @staticmethod
    def _maximum(u: BSTNode):
        """Returns the node (rooted at u) with the maximum key."""
        while u.right is not None:
            u = u.right
        return u

    # SUCCESSOR AND PREDECESSOR

    def successor(self, u: BSTNode):
        """Finds the successor of u.

        If u has a right subtree,
        then the successor of u is the minimum of that right subtree.

        Otherwise it is the first ancestor, lets call it A, of u
        such that u falls in the left subtree of A.

        Time complexity: O(h)"""

        if not isinstance(u, BSTNode):
            u = self.search(u)
            if not u:
                raise Exception("BSTNode object with key node was not found.")

        if u.right is not None:
            return BST._minimum_r(u.right)

        p = u.parent

        # The comparison node == p.right
        # compares basically if they are the same object.
        # See the BaseNode class.
        while p is not None and p.right == u:
            u = p
            p = u.parent

        return p

    def predecessor(self, u: BSTNode):
        """Finds the successor of the node u.
        Opposite operation of successor(u)

        Time complexity: O(h)"""
        if not isinstance(u, BSTNode):
            u = self.search_r(u)
            if not u:
                raise Exception("BSTNode object with key node was not found.")

        if u.left is not None:
            return BST._maximum_r(u.left)

        p = u.parent

        # The comparison node == p.left
        # compares basically if they are the same object,
        # See the BaseNode class.
        while p is not None and u == p.left:
            u = p
            p = u.parent

        return p

    # REMOVALS AND DELETIONS

    # REMOVALS

    def remove_max(self):
        """Removes and returns the maximum element of the tree, if it is not empty."""
        if self.n > 0:
            return self._remove_max(self.root)

    def _remove_max(self, u: BSTNode):
        """Removes the maximum element of the subtree rooted at u.

        Note that the maximum element is all the way to the right,
        and it cannot have a right child,
        but it can still have a left subtree.

        If u is None, exceptions will be thrown.

        Time complexity: O(h)"""
        m = self._maximum_r(u)

        if m.left is not None:  # m has a left subtree.
            if self.is_the_root(m):  # m is the root.
                self.root = m.left
                m.left.parent = None  # self.root.parent = None
            else:  # m is NOT the root.
                m.left.parent = m.parent
                m.parent.right = m.left
        else:  # m has NO children
            if self.is_the_root(m):
                self.root = None
            else:
                m.parent.right = None

        m.parent = m.left = None
        self.n -= 1
        return m

    def remove_min(self):
        """Removes and returns the minimum element of the tree, if it is not empty."""
        if self.n > 0:
            return self._remove_min(self.root)

    def _remove_min(self, u: BSTNode):
        """Removes and returns the minimum element of the subtree rooted at u.

        If u is None, exceptions will be thrown.

        Time complexity: O(h)"""

        m = self._minimum_r(u)

        if m.right is not None:
            if self.is_the_root(m):
                self.root = m.right
                m.right.parent = None
            else:
                m.right.parent = m.parent
                m.parent.left = m.right
        else:  # m has not right subtree.
            if self.is_the_root(m):
                self.root = None
            else:  # m is an internal node with no right subtree.
                m.parent.left = None

        m.right = m.parent = None
        self.n -= 1
        return m

    # DELETIONS

    def delete(self, x):
        """Deletes x from self (if it exists).

        x can either be the key of a node,
        or it can be a reference to an actual BSTNode object.

        There are 3 cases of deletion:
            1. the node has no children
            2. the node has one child
            3. the node has the left and right subtrees"""
        if x is None:
            raise TypeError("x cannot be None.")

        if not isinstance(x, BSTNode):
            x = self.search_r(x)

        if x is None:
            raise LookupError("No node was found with key=x.")

        if x.parent is None and x != self.root:
            raise LookupError("x was not found.")

        self.n -= 1
        return self.__delete(x)

    def __delete(self, u: BSTNode):
        """This is a helper method to the delete method,
        thus it should not be called by clients.

        When deleting a node u from a BST, we have basically to consider 3 cases:
        1. u has no children
        2. u has one child
        3. u has two children

        1. u has no children, then we simply remove it
        by modifying its parent to replace u with None.
        If u.parent is None, then u must be the root,
        and thus we simply set the root to None.

        2. u has just one child, but we first need to decide which one.
        Then we elevate this child to u's position in the tree
        by modifying u's parent to replace u by u's child.

        But if u's parent is None, that means u was the root,
        and the new root becomes u's child.

        3. u has two children, then we search for u's successor s,
        which must be in the u's right subtree (it's the minimum),
        which takes u's position in the tree.
        The rest of the u's subtree becomes the s's right subtree,
        and the u's left subtree becomes the new s's left subtree.
        This case is a little bit tricky,
        because it matters whether s is u's right child.

        Suppose s is the right child of u, then we replace u by s,
        which might or not have a right subtree, but no left subtree.

        Suppose s is not the right child of u,
        in this case, we replace s by its own right child,
        and then we replace u by s.
        
        Note that "self.__delete__two_children" does NOT exactly do that,
        but instead it simply replaces the positions of u and s,
        as if s was u and u was s.
        
        After that, self.__delete is called again on u,
        but note that u is now in the previous s's position,
        and thus u has now no left subtree, but at most a right subtree."""

        if u.has_two_children():
            self.__delete__two_children(u)
        else:  # Note that  u could also not have any child.
            self.__delete__at_most_one_child(u)

        u.right = u.left = u.parent = None
        return u

    def __delete__at_most_one_child(self, u: BSTNode):
        """Removes u from the tree, when u has at most one child.
        This means that u could have 0 or 1 child."""
        child = u.right
        if u.left is not None:
            child = u.left

        if u.parent is None:  # u is the root.
            self.root = child
        else:  # u has a parent, so it is not the root.
            if u.is_left_child():
                u.parent.left = child
            else:
                u.parent.right = child

        # child is None iff u.right and u.left are None.
        if child is not None:
            child.parent = u.parent

    def __delete__two_children(self, u: BSTNode):
        """Call by __delete when a node has two children."""
         # Replace u with its successor s.
        self.__replace(u, self.successor(u))
        # Recursively calls the function that should have called this function.
        # This is done because u is now in a new position,
        # where it simply has at most one right subtree.
        self.__delete(u)

    def __replace(self, u: BSTNode, s: BSTNode):
        # TODO: Check if this function would switch u and s correctly in all cases of u and s...
        """Switches the roles and positions of u nad s,
        which must be the successor of u.
        s, the u's successor, can either be u's right child or
        it could also be the minimum of the left subtree
        of u's right child, in case u's right child has a left subtree.

        Note that this function assumes that
        the successor of u is in its right subtree!"""

        sp = s.parent  # sp=s's initial parent
        src = s.right  # src=s's right child

        # SET NEW PARENT OF THE SUCCESSOR
        # Set s's new parent to be u's parent.
        s.parent = u.parent

        # u is not the root iff u's parent is not None.
        if u.parent is not None:
            # If u is the left child, then u.parent's left child becomes s.
            if u.is_left_child():
                u.parent.left = s
            else:  # u.parent's right child becomes s.
                u.parent.right = s
        else:  # u.parent is None, then u was the root.
            self.root = s  # No need to set self.root.parent to None!

        # SET NEW LEFT CHILD OF THE SUCCESSOR
        # Set s's left child to be u's left child.
        s.left = u.left

        # If u has a left child y, make y's parent be s.
        if u.left is not None:
            u.left.parent = s

        # SET NEW THE RIGHT CHILD OF THE SUCCESSOR
        # If s is not the right child of u.
        if s != u.right:
            # Note that we have stored the previous s's right child in src.
            s.right = u.right
            u.right.parent = s  # Note that u.right cannot be None.
        else:  # u.right == s
            s.right = u

        # SET THE NEW PARENT OF u
        # If the previous s's parent is not u,
        # that means that s was not the right child of u.
        if sp != u:
            # Set u's parent to be the initial s's parent.
            u.parent = sp
            # Note that since s was not the right child of u,
            # then s was the minimum of u's initial left subtree,
            # and therefore s couldn't have a left subtree.
            # and s was indeed the left child of its parent.
            sp.left = u
        else:  # u was the parent of s.
            u.parent = s

        # SET THE NEW RIGHT SUBTREE OF u
        # The previous s's right subtree becomes the new u's right subtree.
        u.right = src

        # If s's initial right child src was not None,
        # then set the new parent of src to be u.
        if src is not None:
            src.parent = u

        # SET THE NEW LEFT SUBTREE OF u
        # Since s was the successor,
        # then it had to left subtree or child,
        # and thus also u, in its new position (the previous s's position),
        # cannot have a left child or subtree too.
        u.left = None

    def show(self):
        """Calls self.__str__()"""
        print(self)

    def __str__(self):
        """Source:
        http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/readings/binary-search-trees/bst.py"""
        if self.root is None:
            return 'Nothing to print: tree is empty.'

        def recurse(node):
            """Pretty-prints this BST object."""
            if node is None:
                return [], 0, 0

            fill = "_"

            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(node.label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos

            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)

            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)

            if (middle - len(node.label)) % 2 == 1 and node.parent is not None and \
               node is node.parent.left and len(node.label) < middle:
                node.label += fill

            node.label = node.label.center(middle, fill)

            if node.label[0] == fill:
                node.label = ' ' + node.label[1:]

            if node.label[-1] == fill:
                node.label = node.label[:-1] + ' '

            lines = [' ' * left_pos + node.label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle - 2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
                [left_line + ' ' * (width - left_width - right_width) +

                 right_line

                 for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self.root)[0]) + "\n"

    def __repr__(self):
        return self.__str__()


def test_bst():
    b = BST()

    def show():
        print(b)
        print("Size:", b.size())
        print("Height:", b.height())
        # input()

    for i in range(40):
        b.insert(i)

    a = BSTNode(21, "Hello World!")
    b.insert(a)
    print(repr(b.search(17)))

    # b.delete(BSTNode(100))
    show()

if __name__ == "__main__":
    test_bst()