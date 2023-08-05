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
    Definition of class `FNTOMonoid` which represents a finite, negative,
    totally ordered monoid.
"""

__all__ = ["FNTOMonoid"]

import copy
import fntom

class FNTOMonoid(fntom.LevelEquivalence):
    """
    Represents a finite, negative, totally ordered monoid which has an abiity
    to generate its one-element Rees co-extensions.

    Attributes:
        identifier (int): unique positive integer identifying this f. n.
            monoid; can be equal to `None`
        extensions (list of FNTOMonoid): list of co-extensions of this
            f. n. tomonoid
        idempotents (list of int): non-zero idempotents of the monoid
        parent (FNTOMonoid): parent f. n. monoid from which this monoid has
            been created as its co-extension (`parent` is the Rees quotient of
            this monoid)
        original (FNTOMonoid): sibling f. n. monoid from which this one has
            been created as a (possibly altered) copy
        closed (bool): indicates whether the co-extension of this f. n.
            tomonoid have been found, already
    """

    def __init__(self,
                 identifier = None,
                 size = None,
                 parent = None,
                 original = None,
                 xyzTable = None,
                 intTable = None,
                 base62Table = None):
        """
        At maximum, one of the arguments `size`, `original`, `table` can be
        specified.
        If none of them is specified, this monoid is initialized as the trivial
        monoid.

        Args:
            size (int): must be greater or equal to 1; if specified, this
                monoid will be initialized as the _drastic_ f. n. tomonoid of
                the given size; that is:

                  * x*y=x if y=1,
                  * x*y=y if x=1,
                  * x*y=0 otherwise

            parent (FNTOMonoid): if specified, this monoid will be creates as a
                zero-doubling extension of `parent`
                (see `LevelEquivalence.performZeroDoublingExtension()`)

            original (FNTOMonoid): if specified, this monoid will be creates as
                a (deep) copy of `original`

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
        """
        self.setIdentifier(identifier)
        if parent != None:
            super().__init__(original = parent)
            self.performZeroDoublingExtension()
            self.parent = parent
            self.original = None
            self.idempotents = copy.deepcopy(parent.idempotents)
        elif original != None:
            super().__init__(original = original)
            self.parent = original.parent
            self.original = original
            self.idempotents = copy.deepcopy(original.idempotents)
        else:
            super().__init__(
                    size = size,
                    xyzTable = xyzTable,
                    intTable = intTable,
                    base62Table = base62Table)
            self.parent = None
            self.original = None
            self.setIdempotents()
        self.extensions = []
        self.closed = False

    def setIdempotents(self):
        """
        Sets the attribute `idempotents` to contain all the idempotents of the
        f. n. tomonoid apart from `zero`.
        """
        self.idempotents = self.findIdempotents() + [ self.unit ]

    def setIdentifier(self, identifier):
        """
        Sets the value of the attribute `identifier`.
        """
        self.identifier = identifier

    def getCopy(self, identifier = None):
        """
        Creates and returns a copy of this f. n. tomonoid.

        Args:
            identifier (int): identifier of the newly created `FNTOMonoid`

        Returns:
            FNTOMonoid: a deep copy of this instance
        """
        return FNTOMonoid(identifier = identifier, original = self)

    def getZeroDoublingExtension(self, identifier = None):
        """
        Creates and returns a zero-doubling extensions of this f. n. tomonoid.

        Args:
            identifier (int, optional): identifier of the newly created
                `FNTOMonoid`

        Returns:
            FNTOMonoid: a zero-doubling extensions of this f. n. tomonoid

        See:
            `LevelEquivalence.performZeroDoublingExtension()`
        """
        return FNTOMonoid(identifier, parent = self)

    def computeCoExtensionsBrute(self, counter, onlyCommutative = False, onlyArchimedean = False):
        """
        Finds all the one-element co-extensions of this tomonoid by the brute
        force method.

        The found co-extensions are subsequently stored to the attribute
            `extensions`.
        Subsequently, reference to `extensions` is returned

        Args:
            counter (fntom.Counter): serves to assign unique identifiers
                to the generated f. n. tomonoids
            onlyCommutative (bool): if `True` then only commutative
                co-extensions will be constructed
                (it is, however, not checked whether this monoid is
                commutative)
            onlyArchimedean (bool): if `True` then only Archimedean
                co-extensions will be constructed
                (it is, however, not checked whether this monoid is
                Archimedean)

        Returns:
            list of FNTOMonoid: the value of the attribute `extensions` which
                is a list of the co-extensions of this f. n. tomonoid
        """
        ext = self.getZeroDoublingExtension(counter.getNew())
        self.extensions = ext.goThroughAllEvaluationsBrute(
                                    counter,
                                    onlyCommutative = onlyCommutative,
                                    onlyArchimedean = onlyArchimedean)
        return self.extensions

    def goThroughAllEvaluationsBrute(self, counter, onlyCommutative = False, onlyArchimedean = False):
        """
        Recursively generates all the potential one-element coextensions of this tomonoid
        and tests whether they meet the axioms of a finite, negative tomonoid.

        This method is called by the method `FNTOMonoid.computeCoExtensionsBrute`.

        Args:
            counter (fntom.Counter): serves to assign unique identifiers
                to the generated f. n. tomonoids
            onlyCommutative (bool): if `True` then only commutative
                co-extensions will be returned
                (it is, however, not checked whether this monoid is
                commutative)
            onlyArchimedean(bool): if `True` then only Archimedean
                co-extensions will be returned
                (it is, however, not checked whether this monoid is
                Archimedean)

        Returns:
            list of FNTOMonoid: the co-extensions of this f. n. tomonoid
        """
        if len(self.eqClasses) > self.size:
            tomZero = self
            tomAtom = self.getCopy(counter.getNew())
            tomZeroValid = True
            tomAtomValid = True
            try:
                tomZero.mergeEqClassWithZero(self.size)
            except fntom.Error.NotTOMPartition:
                tomZeroValid = False
            try:
                tomAtom.mergeEqClassWithAtom(self.size)
            except fntom.Error.NotTOMPartition:
                tomAtomValid = False
            if tomZeroValid:
                extensionsZero = tomZero.goThroughAllEvaluationsBrute(
                                            counter,
                                            onlyCommutative = onlyCommutative,
                                            onlyArchimedean = onlyArchimedean)
            else:
                extensionsZero = []
            if tomAtomValid:
                extensionsAtom = tomAtom.goThroughAllEvaluationsBrute(
                                            counter,
                                            onlyCommutative = onlyCommutative,
                                            onlyArchimedean = onlyArchimedean)
            else:
                extensionsAtom = []
            extensionsZero.extend(extensionsAtom)
            return extensionsZero
        else:
            if onlyCommutative and self.performCommutativityTest() != None:
                return []
            if onlyArchimedean and self.performArchimedeanicityTest() != None:
                return []
            if self.performMonotonicityTest() != None:
                return []
            if self.performAssociativityTest() != None:
                return []
            return [self]

    def computeCoExtensions(
            self,
            counter,
            commutative = False,
            archimedean = False):
        """
        Computes all the one-element coextensions of this tomonoid by the introduced
        level set based method.

        The computed co-extensions are stored to the attribute `coextensions`.

        Args:
            counter (fntom.Counter): serves to assign unique identifiers
                to the generated f. n. tomonoids

        commutative (bool, optional): if `True`, only commutative co-extensions
            are found;
            it is supposed that the starting f. n. tomonoid is commutative

        archimedean (bool, optional): if `True`, only Archimedean co-extensions
            are found;
            it is supposed that the starting f. n. tomonoid is Archimedean

        Returns:
            list of FNTOMonoid: reference to the attribute `extensions`;
                list of one-element co-extensions of this f. n. tomonoid
        """
        if self.size == 1:
            # trivial monoid has one co-extension only
            zeroDblExt = self.getZeroDoublingExtension(counter.getNew())
            self.extensions = [ zeroDblExt ]
        else:
            zeroDblExt = self.getZeroDoublingExtension()
            if commutative:
                for i in range(zeroDblExt.coatom, zeroDblExt.zero):
                    for j in range(zeroDblExt.coatom, i):
                        zeroDblExt.relatePairs((i, j), (j, i))
            zeroDblExt.performE2(commutative = commutative)
            if archimedean:
                zeroDblExt.performE3Archimedean(commutative = commutative)
                zeroDblExt.performE4Archimedean()
                self.extensions = zeroDblExt.goThroughAllEvaluations(counter)
            else:
                self.extensions = []
                numIdempotents = len(zeroDblExt.idempotents)
                # needed to call `isUsablePairOfIdempotents`
                boundaryOfLeft = numIdempotents * [None]
                boundaryOfRight = numIdempotents * [None]
                for i in range(numIdempotents):
                    definingIdempotentLeft = zeroDblExt.idempotents[i]
                    definingIdempotentRight = zeroDblExt.idempotents[i]
                    boundaryOfLeft[i] = zeroDblExt.getLeftDefiningIdempotentBoundary(definingIdempotentLeft)
                    boundaryOfRight[i] = zeroDblExt.getRightDefiningIdempotentBoundary(definingIdempotentRight)
                # (try to) generate co-extensions for every defining pair of idempotents
                for indexLeft in range(numIdempotents):
                    for indexRight in range(numIdempotents):
                        definingIdempotentLeft = zeroDblExt.idempotents[indexLeft]
                        definingIdempotentRight = zeroDblExt.idempotents[indexRight]
                        if zeroDblExt.isUsablePairOfIdempotents(
                                definingIdempotentLeft,
                                definingIdempotentRight,
                                boundaryOfRight[indexRight],
                                boundaryOfLeft[indexLeft]):
                            tom = zeroDblExt.getCopy()
                            tom.definingIdempotentLeft = definingIdempotentLeft
                            tom.definingIdempotentRight = definingIdempotentRight
                            tom.performE3bGeneral()
                            try:
                                tom.performE4General()
                                tom.performE3aGeneral(commutative = commutative)
                                extensions = tom.goThroughAllEvaluations(counter)
                            except fntom.Error.NotTOMPartition:
                                pass
                            else:
                                self.extensions.extend(extensions)
                zeroDblExt.setPairToAtom((zeroDblExt.atom, zeroDblExt.atom))
                zeroDblExt.idempotents.append(zeroDblExt.atom)
                zeroDblExt.setIdentifier(counter.getNew())
                self.extensions.append(zeroDblExt)
        return self.extensions

    def goThroughAllEvaluations(self, counter):
        """
        Generates and returns all the valid one-element Rees co-extensions
        of this f. n. tomonoid.

        This method is called by `FNTOMonoid.computeCoExtensions`.

        Args:
            counter (fntom.Counter): serves to assign unique identifiers
                to the generated f. n. tomonoids

        Returns:
            list of FNTOMonoid: list of one-element co-extensions of this f. n.
                tomonoid, however, the greatest one-element co-extension (where
                `(atom, atom)` is evaluated to `atom`) is not included to the list
        """
        if len(self.eqClasses) > self.size:
            tomZero = self
            tomAtom = self.getCopy()
            try:
                tomZero.mergeEqClassWithZero(self.size)
                extensionsZero = tomZero.goThroughAllEvaluations(counter)
            except fntom.Error.NotTOMPartition:
                extensionsZero = []
            try:
                tomAtom.mergeEqClassWithAtom(self.size)
                extensionsAtom = tomAtom.goThroughAllEvaluations(counter)
            except fntom.Error.NotTOMPartition:
                extensionsAtom = []
            extensionsZero.extend(extensionsAtom)
            return extensionsZero
        else:
            self.setIdentifier(counter.getNew())
            return [ self ]

    def performE2(self, commutative = False):
        """
        Performs Property (E2).

        For the detailed description, see Definition 4.2 in
        the paper
        [[PeVe17]](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

        Relates pairs `(a,e)` and `(d,c)` such that there is `b` such that the
        pairs `(a,b)` and `(b,c)` belong to the support of the f. n. tomonoid
        and, furthermore, `(a,b)` is related to `d` and `(b,c)` is related to
        `e`.

        Args:
            commutative (bool): if `True` then the optimization for
                commutative f. n.  tomonoids is turned on
            archimedean (bool): if `False` then the optimization for
                non-Archimedean f. n.  tomonoids is turned on
        """
        for k in range(self.coatom, self.atom):
            for pair in self.eqClasses[k]:
                # discard the pairs that have unit coordinate
                if self.isNotOnBorder(pair):
                    (a, b) = pair
                    # a simple optimization for commutative f. n. tomonoids
                    if not commutative or a <= b:
                        d = self.getValue((a,b))
                        # find c such that (b,c) is evaluated strictly higher than
                        # the atom and relate (a,e)~(d,c)
                        for c in range(self.coatom, self.atom):
                            e = self.getValue((b,c))
                            if self.isZeroOrAtomOrNotElement(e):
                                break
                            self.relatePairs((d,c), (a,e))

    def performE3Archimedean(self, commutative = False):
        """
        Performs Property (E3).

        For the detailed description, see Definition 4.2 in
        the paper
        [[PeVe17]](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

        Relates particular pairs with zero.

        Args:
            commutative (bool): if `True` then the optimization for
                commutative f. n.  tomonoids is turned on
        """
        i = self.coatom
        j = self.atom
        while i < self.atom:
            # An optimization for Archimedean f. n. tomonoids:
            # The program considers only those pairs (i,j) such that:
            #     i * j = zero or atom,
            #     Succ(i) * j > atom, and
            #     i * Succ(j) > atom,
            # where Succ(.) is the f. n. tomonoid element that is by one closer
            # to the unit
            while i < self.atom and not self.isZeroOrAtomOrNotElement(self.getValue((i, j))):
                i += 1
            while j >= self.unit and self.isZeroOrAtomOrNotElement(self.getValue((i, j))):
                j -= 1
            j += 1
            # a simple optimization for commutative Archimedean f. n. tomonoids
            if commutative and i > j:
                break
            # (E3) first part
            a = i
            b = j
            c = self.coatom
            e = self.getValue((b, c))
            if self.isHigherThanAtom(e):
                self.setPairToZero((a, e))
            # (E3) second part
            a = self.coatom
            b = i
            c = j
            d = self.getValue((a, b))
            if self.isHigherThanAtom(d):
                self.setPairToZero((d, c))
            if j <= self.coatom:
                break
            j -= 1

    def performE3aGeneral(self, commutative = False):
        """
        Performs Property (E3')(a).

        For the detailed description, see Definition 5.2 in
        the paper
        [[PeVe17]](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

        According to the chosen defining pair of idempotents, relates the
        corresponding pairs with zero.

        Args:
            commutative (bool): if `True` then the optimization for
                commutative f. n.  tomonoids is turned on
        """
        i = self.coatom
        j = self.atom
        while i < self.atom:
            # An optimization:
            # The program considers only those pairs (i,j) such that:
            #     i * j = zero or atom,
            #     Succ(i) * j > atom, and
            #     i * Succ(j) > atom,
            # where Succ(.) is the f. n. tomonoid element that is by one closer
            # to the unit
            while i < self.atom and not self.isZeroOrAtomOrNotElement(self.getValue((i, j))):
                i += 1
            while j >= self.unit and self.isZeroOrAtomOrNotElement(self.getValue((i, j))):
                j -= 1
            j += 1
            # a simple optimization for commutative f. n. tomonoids
            if commutative and i > j:
                break
            # (E3')(a) first part
            if i > self.definingIdempotentLeft:
                a = i
                b = j
                c = self.definingIdempotentRight + 1
                e = self.getValue((b, c))
                if self.isHigherThanAtom(e):
                    self.setPairToZero((a, e))
            # (E3')(a) second part
            if j > self.definingIdempotentRight:
                a = self.definingIdempotentLeft + 1
                b = i
                c = j
                d = self.getValue((a, b))
                if self.isHigherThanAtom(d):
                    self.setPairToZero((d, c))
            if j <= self.coatom:
                break
            j -= 1

    def performE3bGeneral(self):
        """
        Performs Property (E3')(b).

        For the detailed description, see Definition 5.2 in
        the paper
        [[PeVe17]](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

        Relates pairs `(a,e)` and `(d,c)` such that there is `b` such that the
        pairs `(a,b)` and `(b,c)` belong to the support of the f. n. tomonoid
        and, furthermore, `(a,b)` is related to `d` and `(b,c)` is related to
        `e`.

        According to the chosen defining pair of idempotents, relates pairs
        `(a,b)` and `(a,e)` (and pairs `(b,a)` and `(e,a)`) in the complement
        of the support of the f. n. tomonoid.
        """
        if self.definingIdempotentRight > self.unit:
            c = self.definingIdempotentRight
            finish = False
            for b in range(self.coatom, self.atom):
                e = self.getValue((b, c))
                if b < e:
                    if not self.isElement(e):
                        e = self.atom
                        finish = True
                    for a in range(self.atom - 1, self.unit, -1):
                        if self.isHigherThanAtom(self.getValue((a, b))):
                            break
                        self.relateColumn(a, b, e)
                    if finish:
                        break
        if self.definingIdempotentLeft > self.unit:
            a = self.definingIdempotentLeft
            finish = False
            for b in range(self.coatom, self.atom, 1):
                d = self.getValue((a,b))
                if b < d:
                    if not self.isElement(d):
                        d = self.atom
                        finish = True
                    for c in range(self.atom-1, self.unit, -1):
                        if self.isHigherThanAtom(self.getValue((b,c))):
                            break
                        self.relateRow(b, d, c)
                    if finish:
                        break

    def performE4Archimedean(self):
        """
        Performs Property (E4).

        For the detailed description, see Definition 4.2 in
        the paper
        [[PeVe17]](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

        Relates the pairs `(atom, coatom)` and `(coatom, atom)` to `zero`.
        """
        self.setPairToZero((self.coatom, self.atom))
        self.setPairToZero((self.atom, self.coatom))

    def performE4General(self):
        """
        Performs Property (E4').

        For the detailed description, see Definition 5.2 in
        the paper
        [[PeVe17]](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

        According to the chosen defining pair of idempotents, relates the
        corresponding pairs with zero or atom.
        """
        self.setPairToZero((self.definingIdempotentLeft + 1, self.atom))
        self.setPairToZero((self.atom, self.definingIdempotentRight + 1))
        if self.definingIdempotentLeft != self.unit:
            self.setPairToAtom((self.definingIdempotentLeft, self.atom))
        if self.definingIdempotentRight != self.unit:
            self.setPairToAtom((self.atom, self.definingIdempotentRight))

    def getRightDefiningIdempotentBoundary(self, definingIdempotentRight):
        """
        Auxiliary method.

        Its result is utilized in `FNTOMonoid.computeCoExtensions` to perform
        the test whether a chosen pair of defining idempotents will yield any
        co-extensions by calling `FNTOMonoid.isUsablePairOfIdempotents`.

        Args:
            definingIdempotentRight (int): one of the idempotents of the f. n.
                tomonoid

        Returns:
            int: the highest value `boundaryOfRight` such that the pair
                `(boundaryOfRight, definingIdempotentRight)` belongs to the atom
                level equivalence class or to no level equivalence class.
        """
        boundaryOfRight = self.atom
        for i in range(self.coatom, self.zero, 1):
            value = self.getValue((i, definingIdempotentRight))
            if self.isAtomOrNotElement(value):
                boundaryOfRight = i
                break
        return boundaryOfRight

    def getLeftDefiningIdempotentBoundary(self, definingIdempotentLeft):
        """
        Auxiliary method.

        Its result is utilized in `FNTOMonoid.computeCoExtensions` to perform
        the test whether a chosen pair of defining idempotents will yield any
        co-extensions by calling `FNTOMonoid.isUsablePairOfIdempotents`.

        Args:
            definingIdempotentLeft (int): one of the idempotents of the f. n.
                tomonoid

        Returns:
            int: the highest value `boundaryOfLeft` such that the pair
                `(boundaryOfLeft, definingIdempotentLeft)` belongs to the atom
                level equivalence class or to no level equivalence class.
        """
        boundaryOfLeft = self.atom
        for i in range(self.coatom, self.zero, 1):
            value = self.getValue((definingIdempotentLeft, i))
            if self.isAtomOrNotElement(value):
                boundaryOfLeft = i
                break
        return boundaryOfLeft

    def isUsablePairOfIdempotents(
            self,
            definingIdempotentLeft,
            definingIdempotentRight,
            boundaryOfRight,
            boundaryOfLeft):
        """
        Tests whether the chosen pair of defining idempotents fulfills the
        necessary requirements.

        Auxiliary method utilized by `FNTOMonoid.computeCoExtensions`.

        It is, actually, not necessary to use this test, however, it speeds the
        algorithm up (there is a lower number of tracebacks).

        This optiomization is programmed according to Proposition 4.11 in the
        paper
        [[PeVe19]](../../papers/Petrik_Vetterlein__Pomonoids__preprint.pdf).

        Args:
            definingIdempotentLeft (int): the left value in the pair of
                defining idempotents
            definingIdempotentRight (int): the right value in the pair of
                defining idempotents
            boundaryOfRight (int): value returned by
                `FNTOMonoid.getRightDefiningIdempotentBoundary`
            boundaryOfLeft (int): value returned by
                `FNTOMonoid.getLeftDefiningIdempotentBoundary`

        Returns:
            bool: `False` if the given pair of defining idempotents cannot
                yield any co-extensions;
                `True` if it may yield some co-extensions (not granted, though)
        """
        value = self.getValue((definingIdempotentLeft+1, boundaryOfRight))
        if self.isAtomOrHigher(value):
            return False
        value = self.getValue((boundaryOfLeft, definingIdempotentRight+1))
        if self.isAtomOrHigher(value):
            return False
        return True

    def exportToText(
            self,
            separator = "",
            endLine = "\n",
            tableSymbols = "base62",
            identifierSymbols = "base62",
            addOriginal = False):
        """
        Exports the Cayley table of this f. n. tomonoid to a string.

        Suitable for saving to a text file.

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

            identifierSymbols (str, optional): in which set of symbols shall
                the f. n. tomonoid identifiers be written;

                * "base62" (default) ... the identifiers will be written as
                    numbers in the number system with 62 digits
                * "int" ... the identifiers will be written as decimal numbers

            addOriginal (bool, optional): if `True` then the identifier of the
                tomonoid, from which this tomonoid has been initialized as its
                copy, will be added to the head of the returned table

        Returns:
            str: Cayley table of the monoid with a head containing the tomonoid
                identifier, the size of the tomonoid, and the identifier of the
                parent of the tomonoid
        """
        text = ""
        text += "@"
        if self.identifier == None:
            text += "?"
        else:
            if identifierSymbols == "base62" or identifierSymbols == "Base62":
                text += fntom.convertDecimalToBase62(self.identifier)
            elif identifierSymbols == "int":
                text += str(self.identifier)
            else:
                text += "!"
        text += ","
        text += str(self.size)
        text += ","
        if self.parent == None:
            text += "-"
        else:
            if identifierSymbols == "base62" or identifierSymbols == "Base62":
                text += fntom.convertDecimalToBase62(self.parent.identifier)
            elif identifierSymbols == "int":
                text += str(self.parent.identifier)
            else:
                text += "?"
        if addOriginal:
            text += ","
            if self.original == None:
                text += "-"
            else:
                if identifierSymbols == "base62" or identifierSymbols == "Base62":
                    text += fntom.convertDecimalToBase62(self.original.identifier)
                elif identifierSymbols == "int":
                    text += str(self.original.identifier)
                else:
                    text += "?"
        text += "\n"
        text += self.exportTableToText(
            separator = separator,
            endLine = endLine,
            tableSymbols = tableSymbols)
        return text

    def exportToCompressedText(self, parentId = None):
        """
        Exports the line that defines this f. n tomonoid in a "compressed" file.

        See:
            fntom.CompressedFile

        Args:
            parentId (int, optional): identifier of the parent of this f. n.
                tomonoid; if not specified, the identifier will be obtained from
                the attribute `parent`;
                this argument is handy if the parent is not created but its
                identifier is known (for example, when compressing a file with
                generated f. n. tomonoids)

        Returns:
            str: the line that defines this f. n tomonoid in a "compressed"
                file
        """
        text = ""
        text += fntom.convertDecimalToBase62(self.identifier)
        if self.closed == None or self.closed:
            text += ","
        else:
            text += ";"
        if parentId != None:
            text += fntom.convertDecimalToBase62(parentId)
        elif self.parent != None:
            text += fntom.convertDecimalToBase62(self.parent.identifier)
        else:
            text += "-"
        if self.parent == None and parentId == None:
            text += ":"
            text += "T"
            text += self.exportTableToText(separator = "", endLine = ";", tableSymbols = "base62")
        else:
            #text += ":"
            i = self.coatom
            j = self.atom
            first = True
            while i < self.zero and j > self.unit:
                value = self.getValue((i, j))
                if value == self.zero:
                    j -= 1
                elif self.isHigherThanAtom(value):
                    i += 1
                elif value == self.atom:
                    iValue = self.getValue((i + 1, j))
                    jValue = self.getValue((i, j + 1))
                    if iValue == self.zero and jValue == self.zero:
                        if first:
                            first = False
                            text += ":"
                        text += fntom.convertDecimalToBase62(i)
                        text += fntom.convertDecimalToBase62(j)
                    if iValue == self.atom:
                        i += 1
                    else:
                        j -= 1
        return text

    def show(self, separator = ", ", endLine = "\n", tableSymbols = "base62"):
        """
        Prints the values of the attributes of this instance to the terminal
            output.

        This method serves mostly to debugging purposes.
        """
        print("Identifier:", end = " ")
        print(fntom.convertDecimalToBase62(self.identifier), end = " ")
        print("(" + str(self.identifier) + ")", end = ", ")
        print("parent:", end = " ")
        if self.parent == None:
            print("-")
        else:
            print(fntom.convertDecimalToBase62(self.parent.identifier), end = " ")
            print("(" + str(self.parent.identifier) + ")")
        print("co-extensions:", end = " ")
        if self.extensions == None or len(self.extensions) == 0:
            print("empty")
        else:
            first = True
            for coext in self.extensions:
                print(fntom.convertDecimalToBase62(coext.identifier), end = "")
                print("(" + str(coext.identifier) + ")", end = " ")
            print()
        print("idempotents:", self.idempotents)
        print(self.exportTableToText(separator = separator, endLine = endLine, tableSymbols = tableSymbols))
