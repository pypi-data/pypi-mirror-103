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
    Definition of class `CompressedFile` which implements reading of f. n. tomonoids
    from a "compressed" text file.
"""

# TODO if the file is too large then do not load the whole content to memory
# but rather read the tomonoids directly from the file changing its current
# offset by `fh.seek(offset, from_what)` where `from_what` is one of:
# * os.SEEK_SET - beginning of the file
# * os.SEEK_CUR - current position
# * os.SEEK_END - end of file

__all__ = ["CompressedFile"]

import fntom

class CompressedFile:
    """
    Implements reading of f. n. tomonoids from a "compressed" text file.

    Syntax:
        Lines that start by `"#"` are ignored.
        Each line defines one tomonoid and has the syntax:

            <tomonoid_id><delimiter><parent_id>:<tomonoid_definition>

          * `<tomonoid_id>` ... identifier of the tomonoid as a number in the
              Base62 encoding
          * `<delimiter>` ... delimits the tomonoid identifier and the
              identifier of its parent;
              can be `","` or `";"`;
              `","` refers to the fact that the tomonoid is "closed" (that is,
              all its co-extensions are present in the file)
              `";"` refers to the fact that the tomonoid is "not closed"
          * `<parent_id>` ...  identifier of the parent of the tomonoid
              represented by the currnt line of the file; it is a number in the
              Base62 encoding, as well
          * `:` ... colon delimits the identifier part and the definition part;
              omitted if the definition part is empty (the "zero" co-extension)
          * `<tomonoid_definition>` ... the tomonoid can be defined either by a
              Cayley table or by differences when compared to its parent tomonoid:

              - if the first character is "T" then the Cayley table of the
                tomonoid follows as a sequence of `n` rows delimited by `";"`
                where each row is a sequence of `n` tomonoid elements;
                `n` is the size of the tomonoid;
                the tomonoid elements are positive integers from `0` (the unit
                element of the tomonoid) to `n-1` (the unit element of the
                tomonoid) written in Base62 encoding;
              - otherwise, the definition consists of an **even** sequence of
                Base62 one-digit numbers that represents a number of pairs of
                the tomonoid;
                these pairs are those that are evaluated by the tomonoid
                operation to the atom (the second lowest element) of the
                tomonoid;
                the other pairs that are supposed to be evaluated to the atom,
                too, are given by the tomonoid monotonicity;
                the rest of the pairs are evaluated to the zero of the tomonoid

    Example:
        What follows is a "compressed" text file that contains all the
        tomonoids starting from the trivial monoid up to all the tomonoids of
        the size 4:

            1,-:T0
            2,1
            4,2
            3,2:11
            6;4
            7;4:11
            5;4:22
            9;3
            A;3:12
            B;3:21
            C;3:1221
            8;3:22

    Attributes:
        path (str): path to the file
        lines (list of str): the content of the file;
            each list item contains one (unmodified) line of the file
        report (list of dict): report on numbers of the generated f. n.
            tomonoids;
            output of the method `createReport`
    """

    def __init__(self, lines = None, path = None):
        """
        Raises:
            FileNotFoundError: if the file specified by `path` cannot be found
        """
        self.path = None
        if lines != None:
            self.lines = lines
        elif path != None:
            self.load(path)
        else:
            self.lines = []

    def load(self, path):
        """
        Loads a file given by the path.

        The content of the file is loaded, as it is, to the attribute `lines`,
        however, the lines introduced by `"#"` are subsequently removed from
        the list.

        Args:
            path (str): path to the file

        Raises:
            FileNotFoundError: if the file specified by `path` cannot be found
        """
        self.path = path
        # read the whole file
        with open(path, "r") as inFile:
            self.lines = inFile.readlines()
        # and, subsequently, remove commented lines (that start by "#")
        index = 0
        while index < len(self.lines):
            if self.lines[index][0] == "#":
                del(self.lines[index])
            else:
                index += 1

    def save(self, path, displayProgress = False, includeReport = True):
        """
        Saves the current content given by the attribute `lines` to a
        "compressed" file given by the path.

        Args:
            path (str): path to the file
            displayProgress (bool): if `True` then a progres bar will be
                displayed on the terminal during the saving of the file
            includeReport (bool): if `True` then the table returned by
                `CompressedFile.exportReportToText` will be written to the head
                of the created file
        """
        with open(path, "w") as outFile:
            if includeReport:
                self.createReport(displayProgress = displayProgress)
                outFile.write(self.exportReportToText(self.report))
            numLines = len(self.lines)
            for i in range(numLines):
                if displayProgress:
                    progress = (i + 1) / numLines
                    if len(path) > 30:
                        trimmedPath = path[:26] + "..."
                    else:
                        trimmedPath = path
                    fntom.drawProgress(progress, msg = "Writing " + trimmedPath + ":")
                outFile.write(self.lines[i])
            if displayProgress:
                print()

    def saveAsUncompressed(
            self,
            path,
            indices = None,
            identifiers = None,
            separator = "",
            endLine = "\n",
            tableSymbols = "base62",
            identifierSymbols = "base62",
            addOriginal = False,
            displayProgress = False):
        """
        Saves the current content given by the attribute `lines` to an
        "uncompressed" file given by the path.

        Args:
            path (str): path to the file

            indices (list of int, optional): specifies by the indices which
                items of the list `lines` shall be saved to the file

            identifiers (list of int, optional): specifies by the identifiers which
                tomonoids in the list `lines` shall be saved to the file

            separator (str, optional): string that separates the values in the
                table

            endLine (str, optional): string that separates the rows of the
                table

            tableSymbols (str, optional): one of the following three values:

                * "base62" (default) ... the element of the tomonoid will be
                    written as symbols from the number system 62, that is, the
                    characters from
                    `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`
                    where `0` represents the neutral element (unit)
                * "int" ... the element of the tomonoid will be written as
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
                copy, will be added to the head of each definition of a
                tomonoid

            displayProgress(bool): if `True` then a progres bar will be
                displayed on the terminal during the saving of the file
        """
        # TODO optimization needed
        with open(path, "w") as outFile:
            if indices != None:
                numLines = len(indices)
                for i in range(numLines):
                    if displayProgress:
                        progress = (i + 1) / numLines
                        fntom.drawProgress(progress, msg = "Writing file:")
                    index = indices[i]
                    tom = self.getFNTOMonoid(tomIndex = index)
                    tomText = tom.exportToText(
                            separator = separator,
                            endLine = endLine,
                            tableSymbols = tableSymbols,
                            identifierSymbols = identifierSymbols,
                            addOriginal = addOriginal)
                    outFile.write(tomText + "\n")
                if displayProgress:
                    print()
            elif identifiers != None:
                numLines = len(identifiers)
                for i in range(numLines):
                    if displayProgress:
                        progress = (i + 1) / numLines
                        fntom.drawProgress(progress, msg = "Writing file:")
                    identifier = identifiers[i]
                    tom = self.getFNTOMonoid(tomIdentifier = identifier)
                    tomText = tom.exportToText(
                            separator = separator,
                            endLine = endLine,
                            tableSymbols = tableSymbols,
                            identifierSymbols = identifierSymbols,
                            addOriginal = addOriginal)
                    outFile.write(tomText + "\n")
                if displayProgress:
                    print()
            else:
                numLines = len(self.lines)
                for index in range(numLines):
                    if displayProgress:
                        progress = (index + 1) / numLines
                        fntom.drawProgress(progress, msg = "Writing file:")
                    tom = self.getFNTOMonoid(tomIndex = index)
                    tomText = tom.exportToText(
                            separator = separator,
                            endLine = endLine,
                            tableSymbols = tableSymbols,
                            identifierSymbols = identifierSymbols,
                            addOriginal = addOriginal)
                    outFile.write(tomText + "\n")
                if displayProgress:
                    print()
    
    def getIdentifierFromLine(self, index):
        """
        Auxiliary method used in `CompressedFile.getIndexAccordingToIdentifier`.

        Args:
            index (int): index of a line (a f. n. tomonoid) in the list `lines`

        Returns:
            int: the identifier of a f. n. tomonoid in list `lines` specified
                by its index
        """
        line = self.lines[index]
        charIndex = 0
        if line[charIndex] == "-":
            return None
        else:
            tomIdBase62 = ""
            while line[charIndex].isalnum():
                tomIdBase62 += line[charIndex]
                charIndex += 1
            return fntom.convertBase62ToDecimal(tomIdBase62)

    def getIndexAccordingToIdentifier(self, tomIdentifier):
        """
        Auxiliary method used in `CompressedFile.getFNTOMonoid`.

        Args:
            tomIdentifier (int): identifier of a f. n. tomonoid in the list
                `lines`

        Returns:
            int: index of line in `lines` that contains the given f. n.
                tomonoid identifier 
        """
        left = 0
        if self.getIdentifierFromLine(left) == tomIdentifier:
            return left
        right = len(self.lines) - 1
        if self.getIdentifierFromLine(right) == tomIdentifier:
            return right
        middle = (left + right) // 2
        while left < middle < right:
            currentIdentifier = self.getIdentifierFromLine(middle)
            if currentIdentifier == tomIdentifier:
                return middle
            elif currentIdentifier < tomIdentifier:
                left = middle
            elif currentIdentifier > tomIdentifier:
                right = middle
            middle = (left + right) // 2
        return None

    def getFNTOMonoid(self, tomIdentifier = None, tomIndex = None):
        """
        Constructs and returns the tomonoid specified by its identifier or by
        its index.

        The line in `lines` that corresponds to the tomonoid is first found.
        Then, recursively, the parent of the tomonoid (and its parent, and so
        on) is constructed while the current tomonoid is constructed as a
        one-element co-extension of its parent setting its corresponding pairs
        to be evaluated to its atom.

        Args:
            tomIdentifier (int): if specified then the tomonoid is found in
                `lines` according to its identifier
            tomIndex (int): if specified then the tomonoid is found in `lines`
                according to its list index
        """
        #
        # determine tomonoid index:
        # -------------------------
        if tomIdentifier != None:
            tomIndex = self.getIndexAccordingToIdentifier(tomIdentifier)
        if tomIndex == None or tomIndex >= len(self.lines):
            return None
        if tomIndex < 0:
            tomIndex += len(self.lines)
        if tomIndex < 0:
            return None
        #
        # start reading tomonoid:
        # -----------------------
        lineNum = tomIndex + 1
        tomLine = self.lines[tomIndex]
        charIndex = 0
        # read tomonoid identifier
        if tomLine[charIndex] == "-":
            tomIdBase62 = None
            tomId = None
            charIndex += 1
        else:
            tomIdBase62 = ""
            while tomLine[charIndex].isalnum():
                tomIdBase62 += tomLine[charIndex]
                charIndex += 1
            tomId = fntom.convertBase62ToDecimal(tomIdBase62)
        # read whether the tomonoid is closed
        if tomLine[charIndex] == ";":
            closed = False
        elif tomLine[charIndex] == ",":
            closed = True
        else:
            raise fntom.Error.FileSyntax(
                    lineNum,
                    "EXPECTED ';' OR ',' BUT FOUND '" + str(tomLine[charIndex] + "'"))
        charIndex += 1
        # read identifier of the parent of this tomonoid
        if tomLine[charIndex] == "-":
            parentIdBase62 = None
            parentId = None
            charIndex += 1
        else:
            parentIdBase62 = ""
            while tomLine[charIndex].isalnum():
                parentIdBase62 += tomLine[charIndex]
                charIndex += 1
            parentId = fntom.convertBase62ToDecimal(parentIdBase62)
        # colon ":" or newline "\n" is expected
        if tomLine[charIndex] == ":":
            charIndex += 1
            if tomLine[charIndex] == "T":
                definedByTable = True
            else:
                definedByTable = False
        elif tomLine[charIndex] == "\n":
            definedByTable = False
        else:
            raise fntom.Error.FileSyntax(
                    lineNum,
                    "EXPECTED ':' OR NEW LINE BUT FOUND '" + str(tomLine[charIndex] + "'"))
        if definedByTable:
            # if the first character after ":" is "T" then this tomonoid is
            # defined by a Cayley table
            base62Table = []
            for row in tomLine[charIndex + 1:-1].split(";"):
                base62Table.append(list(row))
            tom = fntom.FNTOMonoid(tomId, base62Table = base62Table)
            tom.closed = closed
            return tom
        else:
            # ... otherwise it is defined by those pairs of tomonoid values
            # that are evaluated to the atom
            atomPairs = []
            while tomLine[charIndex] != "\n":
                if not tomLine[charIndex].isalnum():
                    raise fntom.Error.FileSyntax(
                            lineNum,
                            "LEFT VALUE OF A PAIR IS NOT ALPHANUMERIC: '" + tomLine[charIndex] + "'")
                leftValueBase62 = tomLine[charIndex]
                charIndex += 1
                if tomLine[charIndex] != "\n":
                    rightValueBase62 = tomLine[charIndex]
                else:
                    raise fntom.Error.FileSyntax(
                            lineNum,
                            "UNEXPECTED EOF WHEN READING PAIRS")
                if not tomLine[charIndex].isalnum():
                    raise fntom.Error.FileSyntax(
                            lineNum,
                            "RIGHT VALUE OF A PAIR IS NOT ALPHANUMERIC: '" + tomLine[charIndex] + "'")
                charIndex += 1
                leftValue = fntom.convertBase62ToDecimal(leftValueBase62)
                rightValue = fntom.convertBase62ToDecimal(rightValueBase62)
                atomPairs.append((leftValue, rightValue))
            parent = self.getFNTOMonoid(tomIdentifier = parentId)
            tom = fntom.FNTOMonoid(tomId, parent = parent)
            for pair in atomPairs:
                tom.setPairToAtom(pair)
            tom.setRestToZero()
            tom.setIdempotents()
            tom.closed = closed
            return tom

    def getFirstFNTOMonoid(self):
        """
        Constructs and returns the first f. n. tomonoid in the list.

        The f. n. tomonoid is constructed from the first item of `lines`
        utilizing `CompressedFile.getFirstFNTOMonoid`.
        Furthermore, the value of the attribute `currentTomIndex` is set to
        zero (for future calling of `CompressedFile.getNextFNTOMonoid`).

        Returns:
            FNTOMonoid: the first f. n. tomonoid in the list `lines`
        """
        self.currentTomIndex = 0
        return self.getFNTOMonoid(tomIndex = self.currentTomIndex)

    def getNextFNTOMonoid(self):
        """
        Constructs and returns the next f. n. tomonoid in the list.

        The f. n. tomonoid is constructed, utilizing
        `CompressedFile.getFirstFNTOMonoid`, from the item of the list `lines`
        given by the index `currentTomIndex + 1`.
        Furthermore, the value of the attribute `currentTomIndex` is increased
        by one.

        Returns:
            FNTOMonoid: the next f. n. tomonoid in the list `lines`
        """
        self.currentTomIndex += 1
        return self.getFNTOMonoid(tomIndex = self.currentTomIndex)

    def getSizes(self):
        """
        Computes and returns sizes of the f. n. tomonoids contained in `lines`.

        Returns:
            list of int: the list is of the same length as `lines` and contains
                the sizes of the corresponding f. n. tomonoids
        """
        sizes = len(self.lines) * [ 0 ]
        for i in range(len(self.lines)):
            tomLine = self.lines[i]
            if "T" in tomLine:
                sizes[i] = self.getFNTOMonoid(tomIndex = i).size
            else:
                # skip tomonoid identifier
                charIndex = 0
                while tomLine[charIndex] != "," and tomLine[charIndex] != ";":
                    charIndex += 1
                charIndex += 1
                # read identifier of the parent of this tomonoid
                if tomLine[charIndex] == "-":
                    sizes[i] = None
                else:
                    parentIdBase62 = ""
                    while tomLine[charIndex].isalnum():
                        parentIdBase62 += tomLine[charIndex]
                        charIndex += 1
                    parentId = fntom.convertBase62ToDecimal(parentIdBase62)
                    parentIndex = self.getIndexAccordingToIdentifier(parentId)
                    sizes[i] = sizes[parentIndex] + 1
        return sizes

    def getReport(self, displayProgress = False):
        """
        Returns the information on sizes and numbers of stored f. n. tomonoids.

        Args:
            displayProgress (bool): if `True` then a progres bar will be
                displayed on the terminal during the saving of the file

        Returns:
            list of dict: the index of a list item corresponds with the size of
                f. n. tomonoids;
                dict keys:

                * `"number"` ... number of the f. n. tomonoids of the size
                    given by the index
                * `"number of closed"` ... number of those f. n. tomonoids that
                    are closed
        """
        report = [ {"number": 0, "number of closed": 0, "from id": -1, "to id": -1} ]
        numLines = len(self.lines)
        sizes = numLines * [ 0 ]
        currentSize = -1
        for i in range(numLines):
            if displayProgress:
                progress = (i + 1) / numLines
                fntom.drawProgress(progress, msg = "Creating report:")
            tomLine = self.lines[i]
            if "T" in tomLine:
                tom = self.getFNTOMonoid(tomIndex = i)
                tomId = tom.identifier
                tomSize = tom.size
                tomClosed = tom.closed
                currentSize = tomSize
            else:
                # read tomonoid identifier
                charIndex = 0
                if tomLine[charIndex] == "-":
                    tomIdBase62 = None
                    tomId = None
                    charIndex += 1
                else:
                    tomIdBase62 = ""
                    while tomLine[charIndex].isalnum():
                        tomIdBase62 += tomLine[charIndex]
                        charIndex += 1
                    tomId = fntom.convertBase62ToDecimal(tomIdBase62)
                if tomLine[charIndex] == ",":
                    tomClosed = True
                else:
                    tomClosed = False
                charIndex += 1
                # read identifier of the parent of this tomonoid
                if tomLine[charIndex] == "-":
                    tomSize = None
                else:
                    parentIdBase62 = ""
                    while tomLine[charIndex].isalnum():
                        parentIdBase62 += tomLine[charIndex]
                        charIndex += 1
                    parentId = fntom.convertBase62ToDecimal(parentIdBase62)
                    tomSize = None
                    if currentSize > 0:
                        if report[currentSize - 1]["from id"] > 0 and parentId >= report[currentSize - 1]["from id"]:
                            if report[currentSize - 1]["to id"] > 0 and parentId <= report[currentSize - 1]["to id"]:
                                tomSize = currentSize
                        if tomSize == None: # and report[currentSize]["to id"] <= 0:
                            if report[currentSize]["from id"] > 0 and parentId >= report[currentSize]["from id"]:
                                currentSize += 1
                                tomSize = currentSize
                    if tomSize == None:
                        parentIndex = self.getIndexAccordingToIdentifier(parentId)
                        tomSize = sizes[parentIndex] + 1
                        currentSize = tomSize
            sizes[i] = tomSize
            if tomSize >= len(report):
                report.extend((tomSize - len(report) + 1) * [ {"number": 0, "number of closed": 0, "from id": -1, "to id": -1} ])
            report[tomSize]["number"] += 1
            if tomClosed:
                report[tomSize]["number of closed"] += 1
            if report[tomSize]["from id"] < 0: # or tomId < report[tomSize]["from id"]:
                report[tomSize]["from id"] = tomId
            if tomId > report[tomSize]["to id"]:
                report[tomSize]["to id"] = tomId
        if displayProgress:
            print()
        return report

    def createReport(self, displayProgress = False):
        """
        Creates report on sizes and numbers of stored f. n. tomonoids and saves
        it to the attribute `report`.

        Args:
            displayProgress (bool): if `True` then a progres bar will be
                displayed on the terminal during the saving of the file
        """
        self.report = self.getReport(displayProgress = displayProgress)

    def exportReportToText(self, report):
        """
        Converts the list returned by `CompressedFile.getReport` to a MarkDown
        table.

        Each line of the resulting text starts by `"#"`, hence the text is
        suitable to be included to the compressed file.

        Args:
            report (list of dict): see `CompressedFile.getReport` for the
                details

        Returns:
            str: content of `report` formated to a MarkDown table
        """
        tableHead = [ "size", "number", "closed", "from id", "to id" ]
        cellWidth = []
        for item in tableHead:
            cellWidth.append(len(item))
        if len(str(len(report) - 1)) > cellWidth[0]:
            cellWidth[0] = len(str(len(report) - 1))
        for item in report:
            wn = len(str(item["number"]))
            if wn > cellWidth[1]:
                cellWidth[1] = wn
            wc = len(str(item["number of closed"]))
            if wc > cellWidth[2]:
                cellWidth[2] = wc
            fi = len(str(item["from id"]))
            if fi > cellWidth[3]:
                cellWidth[3] = fi
            ti = len(str(item["to id"]))
            if ti > cellWidth[4]:
                cellWidth[4] = ti
        text = ""
        text += "#"
        for i in range(len(tableHead)):
            text += " | "
            text += f"{tableHead[i]:<{cellWidth[i]}}"
        text += " |\n"
        text += "# "
        for i in range(len(tableHead)):
            text += "| "
            for i in range(cellWidth[i]):
                text += "-"
            text += ":"
        text += "|\n"
        for size in range(len(report)):
            if report[size]["number"] > 0:
                text += "# | "
                text += f"{size:>{cellWidth[0]}}"
                text += " | "
                text += f"{report[size]['number']:>{cellWidth[1]}}"
                text += " | "
                text += f"{report[size]['number of closed']:>{cellWidth[2]}}"
                text += " | "
                text += f"{report[size]['from id']:>{cellWidth[3]}}"
                text += " | "
                text += f"{report[size]['to id']:>{cellWidth[4]}}"
                text += " |\n"
        return text

    def getLastIdentifier(self):
        """
        Returns:
            int: the identifier of the last f. n. tomonoids in the list `lines`
        """
        last = self.getFNTOMonoid(tomIndex = -1)
        return last.identifier

