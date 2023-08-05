# -*- coding: UTF-8 -*-

# This file is a part of fntom which is a Python3 package that implements a
# finite, negative, totally ordered monoid together with methods to compute its
# one-element Rees co-extensions.
#
# Copyright (C) 2021 Milan Petrík <milan.petrik@protonmail.com>
#
# Web page of the program: <https://gitlab.com/petrikm/fntom>
#
# fntom is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# fntom is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# fntom. If not, see <https://www.gnu.org/licenses/>.

"""
    Definition of class `LevelEquivalence` which implements a finite negative
    tomonoid partition.
"""

__all__ = ["LevelEquivalence"]

import copy
import fntom

class LevelEquivalence:
    """
    Implements level set equivalence of a finite negative tomonoid (i.e. f. n.
    tomonoid partition).

    Attributes:
        size (int): size of the f. n. tomonoid
        eqClasses (list of sets of 2-tuples of int): level set equivalence classes
        zero (int, const): the bottom element of the f. n. tomonoid
        unit (int, const): the unit element of the f. n. tomonoid which is also
            the top element
        atom (int, const): the highest element smaller than the top element
        coatom (int, const): the lowest element higher than the bottom element
    """

    def __init__(self,
                 size = None,
                 original = None,
                 base62Table = None,
                 intTable = None,
                 xyzTable = None):
        """
        At maximum one of the arguments `size`, `original`, `xyzTable`,
        `intTable` can be specified.
        If none of them is specified, the level set equivalence is initialized
        to represent the trivial monoid.

        Args:
            size (int): must be greater or equal to 1; if specified, the level
                set equivalence will represent a f. n. tomonoid of the given size,
                however, all the pairs will form singletons in the equivalence with
                the exception of:

                  * the pairs of the form (1,x) and (x,1) which will be
                    pairwise related
                  * the pairs of the form (0,x) or (x,0) which will be
                    alltogether related

            original (LevelEquivalence): if specified, this level set
                equivalence will be a (deep) copy of the `original`

            base62Table (list of lists of chr): if specified, the level set
                equivalence will be created according to the given Cayley table;
                the values in the table are supposed to be from the set:
                `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`
                where `0` represents the neutral element (unit)

            intTable (list of lists of int): if specified, the level set
                equivalence will be created according to the given Cayley table;
                the values in the table are supposed to be non-negative
                integers starting from `0` (which represents the unit element)

            xyzTable (list of lists of chr): if specified, the level set
                equivalence will be created according to the given Cayley table;
                the values in the table are supposed to be from the set:
                `"0"`, ..., `"x"`, `"y"`, `"z"`, `"1"`
                and the table is supposed to have its second index reversed,
                i.e., the table is left-right flipped (accoding to vertical
                axis)
                This style of depicting the Cayley table corresponds with
                the style used in the referenced papers
                [PeVe14,PeVe16,PeVe17,PeVe19], while the previous two
                styles reflect the inner representation of the tomonoid.

        Example:
            The level equivalence of the Lukasiewicz f. n. tomonoid of the size
            10 could be initialized by:

                base62Table = [
                    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A"],
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "A"],
                    ["2", "3", "4", "5", "6", "7", "8", "9", "A", "A", "A"],
                    ["3", "4", "5", "6", "7", "8", "9", "A", "A", "A", "A"],
                    ["4", "5", "6", "7", "8", "9", "A", "A", "A", "A", "A"],
                    ["5", "6", "7", "8", "9", "A", "A", "A", "A", "A", "A"],
                    ["6", "7", "8", "9", "A", "A", "A", "A", "A", "A", "A"],
                    ["7", "8", "9", "A", "A", "A", "A", "A", "A", "A", "A"],
                    ["8", "9", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
                    ["9", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
                    ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"]]
                lvlEq = fntom.LevelEquivalence(base62Table = base62Table)

            or it could be initialized by:

                intTable = [
                    [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10],
                    [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 10],
                    [ 2,  3,  4,  5,  6,  7,  8,  9, 10, 10, 10],
                    [ 3,  4,  5,  6,  7,  8,  9, 10, 10, 10, 10],
                    [ 4,  5,  6,  7,  8,  9, 10, 10, 10, 10, 10],
                    [ 5,  6,  7,  8,  9, 10, 10, 10, 10, 10, 10],
                    [ 6,  7,  8,  9, 10, 10, 10, 10, 10, 10, 10],
                    [ 7,  8,  9, 10, 10, 10, 10, 10, 10, 10, 10],
                    [ 8,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                    [ 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]]
                lvlEq = fntom.LevelEquivalence(intTable = intTable)

            or it could be initialized by:

                xyzTable = [
                    ["0", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1"],
                    ["0", "0", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
                    ["0", "0", "0", "r", "s", "t", "u", "v", "w", "x", "y"],
                    ["0", "0", "0", "0", "r", "s", "t", "u", "v", "w", "x"],
                    ["0", "0", "0", "0", "0", "r", "s", "t", "u", "v", "w"],
                    ["0", "0", "0", "0", "0", "0", "r", "s", "t", "u", "v"],
                    ["0", "0", "0", "0", "0", "0", "0", "r", "s", "t", "u"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "r", "s", "t"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "r", "s"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "r"]]
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]
                lvlEq = fntom.LevelEquivalence(xyzTable = xyzTable)

        """
        if size != None:
            self.size = size
            self.setDesignatedValues()
            self.eqClasses = self.size * [None]
            for i in range(self.size):
                self.eqClasses[i] = set([])
            # pairs with unit coordinate
            self.eqClasses[self.unit].update(set([(self.unit,self.unit)]))
            for i in range(self.coatom, self.size, 1):
                self.eqClasses[i].update(set([(i,self.unit), (self.unit,i)]))
            # pairs with zero coordinate
            self.eqClasses[self.zero].update(set([(self.zero,self.zero)]))
            for i in range(self.coatom, self.zero, 1):
                self.eqClasses[self.zero].update(set([(i,self.zero), (self.zero,i)]))
            # add all the other pairs - each pair to its own equivalence class
            for i in range(self.coatom, self.zero, 1):
                for j in range(self.coatom, self.zero, 1):
                    self.eqClasses.append(set([(i,j)]))
        elif original != None:
            self.size = original.size
            self.eqClasses = copy.deepcopy(original.eqClasses)
            self.zero = original.zero
            self.unit = original.unit
            self.atom = original.atom
            self.coatom = original.coatom
        elif base62Table != None:
            self.size = len(base62Table)
            self.setDesignatedValues()
            self.eqClasses = self.size * [None]
            for i in range(self.size):
                self.eqClasses[i] = set([])
            for i in range(self.size):
                for j in range(self.size):
                    value = fntom.convertBase62ToDecimal(base62Table[i][j])
                    self.eqClasses[value].add((i, j))
        elif intTable != None:
            self.size = len(intTable)
            self.setDesignatedValues()
            self.eqClasses = self.size * [None]
            for i in range(self.size):
                self.eqClasses[i] = set([])
            for i in range(self.size):
                for j in range(self.size):
                    value = intTable[i][j]
                    self.eqClasses[value].add((i, j))
        elif xyzTable != None:
            self.size = len(xyzTable)
            self.setDesignatedValues()
            self.eqClasses = self.size * [None]
            for i in range(self.size):
                self.eqClasses[i] = set([])
            for i in range(self.size):
                for j in range(self.size):
                    char = xyzTable[i][j]
                    #value = self.getElementCode(char)
                    value = fntom.convert0xyz1ToDecimal(char, self.size)
                    self.eqClasses[value].add((i, self.size - 1 - j))
        else:
            self.size = 1
            self.setDesignatedValues()
            self.eqClasses = [ set([ (self.unit,self.unit) ]) ]

    def setDesignatedValues(self):
        """
        According to the value of the attribute `size`, sets the values of
        `zero`, `unit`, `atom`, and `coatom`.
        """
        if self.size == 1:
            self.zero = self.unit = self.atom = self.coatom = 0
        else:
            self.zero = self.size - 1
            self.unit = 0
            self.atom = self.size - 2
            self.coatom = 1

    def getCopy(self):
        """
            Returns:
                LevelEquivalence: a deep copy of this instance
        """
        return LevelEquivalence(original = self)

    def findIdempotents(self):
        """
        Finds and returns all the non-trivial idempotents.

        An element x is an idempotent if x*x=x (where * is the monoidal
            operation).

        Hence if an equivalence class indexed by x that contains the pair (x,x)
        is found then the value x is an idempotent.

        Note that the top element 1 and the bottom element 0 is an idempotent
        of every f. n. tomonoid; these values are called trivial idempotents.
        These values are not included in the returned list of idempotents.

        Returns:
            list of int: list of the non-trivial idempotents
        """
        idempotents = []
        for x in range(self.coatom, self.zero, 1):
            if self.getValue((x,x)) == x:
                idempotents.append(x)
        return idempotents

    def performZeroDoublingExtension(self):
        """
        Performs the zero-doubling extension on this tomonoid.

          * Removes all the pairs from the level set equivalence that are
            equivalent with (0, 1) and (1, 0).
          * Enlarges the size of the tomonoid by one adding a new bottom
            element.
          * Recomputes the values of `zero`, `unit`, `atom`, and `coatom`.
        """
        formerSize = self.size

        self.size += 1
        self.setDesignatedValues()

        numEqClasses = len(self.eqClasses)
        if numEqClasses > formerSize:
            # move the last class behind former zero to the end of the list
            self.eqClasses.append(self.eqClasses[self.zero])
            # add (1,0), (0,1), and (0,0) to the zero class
            self.eqClasses[self.zero] = set([(self.unit, self.zero), (self.zero, self.unit), (self.zero, self.zero)])
        else:
            # add (1,0), (0,1), and (0,0) to the zero class
            self.eqClasses.append(set([(self.unit, self.zero), (self.zero, self.unit), (self.zero, self.zero)]))

        # add pairs of type (x,0) and (0,x) to the zero class
        for i in range(self.coatom, self.zero, 1):
            self.eqClasses[self.zero].add((self.zero,i))
            self.eqClasses[self.zero].add((i,self.zero))

        # atom class (former zero class) is used to determine all the single
        # pair undefined equivalence classes
        if self.size > 2:
            for pair in self.eqClasses[self.atom]:
                if self.isNotOnBorder(pair):
                    self.eqClasses.append(set([pair]))

        # setting the atom class to (1,at)~(at,1)
        self.eqClasses[self.atom] = set([(self.unit, self.atom), (self.atom, self.unit)])

    def findEqClass(self, pair):
        """
        Finds the class to which the given pair belongs.

        Args:
            pair (2-tuple of int): the searched pair

        Returns:
            2-tuple: `(class, index)` where `class` is the reference to the
                class containing the `pair` while `index` is the index in the
                list `eqClasses`

        Raises:
            Exception: if the pair has not been found
        """
        numEqClasses = len(self.eqClasses)
        for i in range(numEqClasses):
            if pair in self.eqClasses[i]:
                return (self.eqClasses[i], i)
        raise Exception("ERROR: Pair", pair, "has not been found")

    def isElement(self, value):
        """
        Args:
            value (int): index of level equivalence class in `eqClasses`

        Returns:
            bool: `True` if `value` is an element of the monoid
        """
        return self.unit <= value <= self.zero

    def isAtomOrHigher(self, value):
        """
        Args:
            value (int): index of level equivalence class in `eqClasses`

        Returns:
            bool: `True` if `value` is an element of the monoid that is not
                equal to `zero`
        """
        return self.unit <= value < self.zero

    def isHigherThanAtom(self, value):
        """
        Args:
            value (int): index of level equivalence class in `eqClasses`

        Returns:
            bool: `True` if `value` is an element of the monoid that is neither
                equal to `zero` nor to `atom`
        """
        return self.isElement(value) and value < self.atom

    def isZeroOrAtomOrNotElement(self, value):
        """
        Args:
            value (int): index of level equivalence class in `eqClasses`

        Returns:
            bool: `True` if `value` is equal to `zero` or to `atom` or if it is
                not an element of the monoid
        """
        return value == self.zero or value == self.atom or not self.isElement(value)

    def isAtomOrNotElement(self, value):
        """
        Args:
            value (int): index of level equivalence class in `eqClasses`

        Returns:
            bool: `True` if `value` is equal to `atom` or if it is not an
                element of the monoid
        """
        return value == self.atom or not self.isElement(value)

    def isNotOnBorder(self, pair):
        """
        Args:
            value (2-tuple of int): pair of monoid elements

        Returns:
            bool: `True` if the pair does lie neither on the axis given by the
                zero element nor on the axis given by the unit element
        """
        return self.zero > pair[0] > self.unit and self.zero > pair[1] > self.unit

    def setValue(self, pair, value):
        """
        Defines the value to which the given pair is supposed to be evaluated
        by the monoidal operation.

        It, actually, merges (relates) the class that contains `pair` with the
        class that contains the pairs `(1,value)` and `(value,1)`.

        Args:
            pair (2-tuple of int): the pair
            value (int): to which value is the pair supposed to be evaluated
                (the index of the class)
        """
        (cla, ind) = self.findEqClass(pair)
        if ind != value:
            if self.isElement(ind):
                raise fntom.Error.NotTOMPartition([ind, value], self)
            else:
                self.eqClasses[value].update(cla)
                self.eqClasses.remove(cla)

    def getValue(self, pair):
        """
        Returns the value of the given pair according to the monoidal
        operation.

        A value outside of the range of the monoidal values may be returned if
        the pair belongs to a class that does not contain pairs of the type
        `(1,x)`, `(x,1)`.

        Args:
            pair (2-tuple of int): the pair

        Returns:
            int: the value of the pair according to the monoidal operation
                (i.e., the index of the level equivalence class to which the
                pair belongs)
        """
        (cla, ind) = self.findEqClass(pair)
        return ind

    def relateClasses(self, ind1, ind2):
        """
        Merges two level equivalence classes into one.

        Args:
            ind1 (int): index of the first class in `eqClasses`
            ind2 (int): index of the second class in `eqClasses`

        Raises:
            fntom.Error.NotTOMPartition: if both the classes contain pairs of
                the types (1,x) and (x,1)
        """
        if ind1 != ind2:
            if self.isElement(ind2):
                if self.isElement(ind1):
                    raise fntom.Error.NotTOMPartition([ind1, ind2], self)
                else:
                    self.eqClasses[ind2].update(self.eqClasses[ind1])
                    self.eqClasses.remove(self.eqClasses[ind1])
            else:
                self.eqClasses[ind1].update(self.eqClasses[ind2])
                self.eqClasses.remove(self.eqClasses[ind2])

    #TODO !!! neni resen pripad, kdy pair1 nebo pair2 neni v zadne tride
    def relatePairs(self, pair1, pair2):
        """
        Merges the level equivalence classes that contain the given pairs.

        Args:
            pair1 (2-tuple of int): first pair
            pair2 (2-tuple of int): second pair

        Raises:
            fntom.Error.NotTOMPartition: if both the classes contain pairs of
                the types (1,x) and (x,1)
        """
        if pair1 != pair2:
            (cla1, ind1) = self.findEqClass(pair1)
            (cla2, ind2) = self.findEqClass(pair2)
            self.relateClasses(ind1, ind2)

    def setPairToZero(self, pair):
        """
        Adds the given pair to the zero equivalence class.

        Merges the class that contains the pair with the class that contains
        (1,0) and (0,1).
        Furthermore, the monotonicity of the tomonoid is taken into account,
        i.e., all the pairs that are closer to (0,0) are added to the zero
        equivalence class, as well.

        Args:
            pair (2-tuple of int): the pair that is to be evaluated to zero by
                the monoidal operation
        """
        if self.isNotOnBorder(pair):
            for i in range(pair[0], self.zero, 1):
                for j in range(pair[1], self.zero, 1):
                    (cla, ind) = self.findEqClass(pair)
                    self.mergeEqClassWithZero(ind)

    def mergeEqClassWithZero(self, ind):
        """
        Merges the given level equivalence class with the zero equivalence
            class.

        Merges the given class with the class that contains (1,0) and (0,1).
        Furthermore, the monotonicity of the tomonoid is taken into account,
        i.e., all the pairs that are closer to (0,0) (compared to the pairs of
        the given class) are added to the zero equivalence class, as well.

        Args:
            ind (int): index of the class in `eqClasses`

        Raises:
            fntom.Error.NotTOMPartition: if both the classes contain pairs of
                the types (1,x) and (x,1)
        """
        if not self.isElement(ind):
            cla = self.eqClasses[ind]
            self.eqClasses[self.zero].update(cla)
            self.eqClasses.remove(cla)
            for pair in cla:
                self.setPairToZero((pair[0]+1,pair[1]))
                self.setPairToZero((pair[0],pair[1]+1))
        elif self.isAtomOrHigher(ind):
            raise fntom.Error.NotTOMPartition([self.zero, ind], self)

    def setPairToAtom(self, pair):
        """
        Adds the given pair to the atom equivalence class.

        Merges the class that contains the pair with the class that contains
        (1,atom) and (atom,1).
        Furthermore, the monotonicity of the tomonoid is taken into account,
        i.e., all the pairs that are closer to (1,1) are added to the atom
        equivalence class, as well.

        Args:
            pair (2-tuple of int): the pair that is to be evaluated to atom by
                the monoidal operation
        """
        if self.isNotOnBorder(pair):
            for i in range(pair[0], self.unit, -1):
                for j in range(pair[1], self.unit, -1):
                    (cla, ind) = self.findEqClass(pair)
                    self.mergeEqClassWithAtom(ind)

    def mergeEqClassWithAtom(self, ind):
        """
        Merges the given level equivalence class with the atom equivalence
            class.

        Merges the given class with the class that contains (1,atom) and (atom,1).
        Furthermore, the monotonicity of the tomonoid is taken into account,
        i.e., all the pairs that are closer to (1,1) (compared to the pairs of
        the given class) are added to the atom equivalence class, as well.

        Args:
            ind (int): index of the class in `eqClasses`

        Raises:
            fntom.Error.NotTOMPartition: if both the classes contain pairs of
                the types (1,x) and (x,1)
        """
        if not self.isElement(ind):
            cla = self.eqClasses[ind]
            self.eqClasses[self.atom].update(cla)
            self.eqClasses.remove(cla)
            for pair in cla:
                self.setPairToAtom((pair[0]-1,pair[1]))
                self.setPairToAtom((pair[0],pair[1]-1))
        elif ind == self.zero:
            raise fntom.Error.NotTOMPartition([self.zero, self.atom], self)

    def setRestToZero(self):
        """
        Sets all the undetermined pairs to zero.

        Undetermined pairs are those that are contained in the equivalence
        classes with their indices out of the range of the tomonoid values.
        """
        numClasses = len(self.eqClasses)
        for ind in range(numClasses - 1, self.size - 1, -1):
            self.relateClasses(ind, self.zero)

    def relateColumn(self, x, yFrom, yTo):
        """
        Makes the pairs in a bounded column of the Cayley table level
        equivalent.

        This involves the pairs in the range from `(x, yFrom)` to `(x, yTo)`.

        The value of `yFrom` does not need to be lower than `yTo` (or vice
        versa).

        Args:
            x (int): an element of the monoid
            yFrom (int): an element of the monoid
            yTo (int): an element of the monoid
        """
        if yFrom == yTo:
            return
        elif yFrom < yTo:
            rang = range(yFrom, yTo+1, 1)
        elif yFrom > yTo:
            rang = range(yTo, yFrom+1, 1)
        first = None
        for y in rang:
            if first == None:
                first = (x,y)
            else:
                self.relatePairs(first, (x,y))

    def relateRow(self, xFrom, xTo, y):
        """
        Makes the pairs in a bounded row of the Cayley table level equivalent.

        This involves the pairs in the range from `(xFrom, y)` to `(xTo, y)`.

        The value of `xFrom` does not need to be lower than `xTo` (or vice
        versa).

        Args:
            xFrom (int): an element of the monoid
            xTo (int): an element of the monoid
            y (int): an element of the monoid
        """
        if xFrom == xTo:
            return
        elif xFrom < xTo:
            ran = range(xFrom, xTo+1, 1)
        elif xFrom > xTo:
            ran = range(xTo, xFrom+1, 1)
        first = None
        for x in ran:
            if first == None:
                first = (x,y)
            else:
                self.relatePairs(first, (x,y))

    def getTable(self):
        """
        Constructs the Cayley table of the tomonoid.

        The table is constructed according to the level set equivalence.

        Returns:
            list of list of int: the Cayley table
        """
        table = []
        for i in range(self.size):
            table.append(self.size * [-1])
        for eqClassIndex in range(len(self.eqClasses)):
            for pair in self.eqClasses[eqClassIndex]:
                (i, j) = pair
                table[i][j] = eqClassIndex
        return table

    def performAssociativityTest(self):
        """
        Tests whether the operaration defined by the level set equivalence is
        associative.

        Returns:
            3-tuple of int: `None` if it is associative, `(x, y, z)` if it is
                not associative; the triplet `(x, y, z)` contains the values on
                which the associativity test has failed
        """
        table = self.getTable()
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    xy = table[x][y]
                    yz = table[y][z]
                    if table[xy][z] != table[x][yz]:
                        return (x, y, z)
        return None

    def performMonotonicityTest(self):
        """
        Tests whether the operaration defined by the level set equivalence is
        monotone.

        Returns:
            2-tuple of int: `None` if it is monotone, `(x, y)` if it is not
                monotone; the pair `(x, y)` contains the values on which the
                monotonicity test has failed
        """
        table = self.getTable()
        for x in range(0, self.size-1, 1):
            for y in range(0, self.size-1, 1):
                if table[x+1][y] < table[x][y] or table[x][y+1] < table[x][y]:
                    return (x, y)
        return None

    def performArchimedeanicityTest(self):
        """
        Tests whether the operaration defined by the level set equivalence is
        Archimedean.

        Returns:
            int: `None` if it is Archimedean, a single integer value if it is
                not Archimedean; the value is one of the non-trivial idempotents of
                the monoid
        """
        table = self.getTable()
        for x in range(1, self.size-1, 1):
            if table[x][x] <= x:
                return x
        return None

    def performCommutativityTest(self):
        """
        Tests whether the operaration defined by the level set equivalence is
        commutative.

        Returns:
            2-tuple of int: `None` if it is commutative, `(x, y)` if it is not
                commutative; the pair `(x, y)` contains the values on which the
                commutativity test has failed
        """
        table = self.getTable()
        for x in range(self.size):
            for y in range(self.size):
                if table[x][y] != table[y][x]:
                    return (x, y)
        return None

    def exportClassesToText(self):
        """
        Returns:
            str: description of the level equivalence classes; suitable to be
                printed to the terminal output
        """
        text = ""
        numClasses = len(self.eqClasses)
        for i in range(numClasses):
            textPart = str(i) + ": "
            initialLength = len(textPart)
            lineLength = initialLength
            text += textPart
            first = True
            for (a, b) in self.eqClasses[i]:
                if first:
                    first = False
                else:
                    text += " "
                    lineLength += 1
                textPart = "(" + str(a) + "," + str(b) + ")"
                if lineLength + len(textPart) > 78:
                    text += "\n"
                    text += initialLength * " "
                    text += textPart
                    lineLength = initialLength + len(textPart)
                else:
                    text += textPart
                    lineLength += len(textPart)

            text += "\n"
        return text

    def exportTableToText(self, separator = ", ", endLine = "\n", tableSymbols = "base62"):
        """
        Args:
            separator (str, optional): string that separates the values in the
                table

            endLine (str, optional): string that separates the rows of the
                table

            tableSymbols (str, optional): one of the following three values:

                * "base62" (default) ... the element of the tomonoid will be
                    diplayed as symbls from the number system 62, that is, the
                    characters from
                    `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`
                    where `0` represents the neutral element (unit)
                * "int" ... the element of the tomonoid will be diplayed as
                    non-negative integers starting from `0` which will represent
                    the neutral element (unit)
                * "0xyz1" ...  the element of the tomonoid will be diplayed as
                    the characters from the set:
                    `"0"`, ..., `"x"`, `"y"`, `"z"`, `"1"`
                    In this case, the table will be left-right flipped
                    (according to the vertical axis).
                    This style of depicting the Cayley table corresponds with
                    the style used in the referenced papers
                    [PeVe14,PeVe16,PeVe17,PeVe19], while the previous two
                    styles reflect the inner representation of the tomonoid.

        Returns:
            str: Cayley table of the monoid;
                suitable be written to a text file or to the terminal output
        """
        table = self.getTable()
        text = ""
        if tableSymbols == "int":
            width = len(str(len(self.eqClasses) - 1))
        else:
            width = 1
        for i in range(self.size):
            if i > 0:
                text += endLine
            first = True
            for j in range(self.size):
                if first:
                    first = False
                else:
                    text += separator
                if tableSymbols == "0xyz1":
                    value = table[i][self.size - 1 - j]
                else:
                    value = table[i][j]
                if tableSymbols == "base62":
                    if value == None:
                        text += "?"
                    else:
                        text += fntom.convertDecimalToBase62(value)
                elif tableSymbols == "int":
                    text += f'{value:>{width}}'
                elif tableSymbols == "0xyz1":
                    text += fntom.convertDecimalTo0xyz1(value, self.size)
        return text

    def show(self):
        """
        Prints the values of the attributes of this instance to the terminal
            output.

        Mostly for debugging purposes.
        """
        print(self.exportTableToText())
        print(self.exportClassesToText())
