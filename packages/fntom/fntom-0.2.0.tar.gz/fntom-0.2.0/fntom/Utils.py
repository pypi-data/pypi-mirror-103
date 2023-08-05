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
    Various utility functions.
"""

__all__ = [
        "convertBase62ToDecimal",
        "convertDecimalToBase62",
        "convert0xyz1ToDecimal",
        "convertDecimalTo0xyz1",
        "generateFNTomonoids",
        "drawProgress",
        "saveToCompressed",
        "saveToUncompressed"]

import timeit
import datetime
import fntom

# Encoding between Base62 and the other number systems.
BASE62_ALPH = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE62_DICT = dict((character, index) for (index, character) in enumerate(BASE62_ALPH))
BASE62_LEN = len(BASE62_ALPH)

def convertBase62ToDecimal(base62):
    """
    Converts the number given in the Base62 system to its counterpart in the
    decimal system.

    Base62 is the number system with 62 symbols:

        0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    Hence, for example,

      * `0` is equivalent to `"0"`
      * `10` is equivalent to `"A"`
      * `20` is equivalent to `"K"`
      * `36` is equivalent to `"a"`
      * `61` is equivalent to `"z"`
      * `62` is equivalent to `"10"`
      * `620` is equivalent to `"A0"`
        
    Args:
        base62 (str): number in the Base62 system

    Returns:
        int: number in the decimal system
    """
    decimal = 0
    for character in base62:
        decimal = decimal * BASE62_LEN + BASE62_DICT[character]
    return decimal

def convertDecimalToBase62(decimal):
    """
    Converts the number given in the decimal system to its counterpart in the
    Base62 system.

    Base62 is the number system with 62 symbols:

        0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    Hence, for example,

      * `0` is equivalent to `"0"`
      * `10` is equivalent to `"A"`
      * `20` is equivalent to `"K"`
      * `36` is equivalent to `"a"`
      * `61` is equivalent to `"z"`
      * `62` is equivalent to `"10"`
      * `620` is equivalent to `"A0"`
        
    Args:
        decimal (int): number in the decimal system

    Returns:
        str: number in the Base62 system
    """
    base62 = ""
    while decimal != 0:
        (decimal, remainder) = divmod(decimal, BASE62_LEN)
        base62 = BASE62_ALPH[remainder] + base62
    if base62 == "":
        return BASE62_ALPH[0]
    else:
        return base62

def convert0xyz1ToDecimal(element, size):
    """
    Converts the name of the given f. n. tomonoid element in the "0xyz1" system
    to its decimal representation.

    The system "0xyz1" is how the elements of a f. n. tomonoid are denoted in
    the referenced papers [PeVe14,PeVe16,PeVe17,PeVe19].

    The bottom element is denoted as `"0"`, the top element is denoted by
    `"1"`, and the rest of the elements is denoted by lower-case letters such
    that the second greates element is denoted by `"z"`, the third greates
    element is denoted by `"y"`, and so on.

    Hence the elements of a f. n. tomonoid of size `5` would be:

            `"0"`, `"x"`, `"y"`, `"z"`, `"1"`

    In this case:

      * `"0"` corresponds to decimal number `4`
      * `"x"` corresponds to decimal number `3`
      * `"y"` corresponds to decimal number `2`
      * `"z"` corresponds to decimal number `1`
      * `"1"` corresponds to decimal number `0`

    Args:
        element (str): the name of the f. n. tomonoid element in the "0xyz1"
            system (one character)

        size (int): number of the elements of the f. n. tomonoid

    Returns:
        int: number in the decimal system
    """
    if element == "1":
        return 0
    elif element == "0":
        return size - 1
    else:
        return ord("z") - ord(element) + 1

def convertDecimalTo0xyz1(decimal, size):
    """
    Converts the number given in the decimal system to its counterpart in the
    "0xyz1" system.

    The system "0xyz1" is how the elements of a f. n. tomonoid are denoted in
    the referenced papers [PeVe14,PeVe16,PeVe17,PeVe19].

    The bottom element is denoted as `"0"`, the top element is denoted by
    `"1"`, and the rest of the elements is denoted by lower-case letters such
    that the second greates element is denoted by `"z"`, the third greates
    element is denoted by `"y"`, and so on.

    Hence the elements of a f. n. tomonoid of size `5` would be:

            `"0"`, `"x"`, `"y"`, `"z"`, `"1"`
        
    In this case:

      * `"0"` corresponds to decimal number `4`
      * `"x"` corresponds to decimal number `3`
      * `"y"` corresponds to decimal number `2`
      * `"z"` corresponds to decimal number `1`
      * `"1"` corresponds to decimal number `0`

    Args:
        decimal (int): number in the decimal system

        size (int): number of the elements of the f. n. tomonoid

    Returns:
        str: the name of the f. n. tomonoid element in the "0xyz1" system (one
            character)
    """
    if decimal == 0:
        return "1"
    elif decimal == size - 1:
        return "0"
    elif 0 < decimal < size - 1:
        return chr(ord("z") - decimal + 1)
    else:
        return str(decimal)

def generateFNTomonoids(
        method = "levelset",
        startingFNTOMonoid = None,
        upToSize = None,
        depth = None,
        archimedean = False,
        commutative = False,
        displayProgress = False,
        counter = None):
    """
    Generates recursively all the one-element Rees co-extensions of a given
    f. n. tomonoid up to the given depth.

    Args:
        method (str, optional): can be `"levelset"` or `"brute"`;
            if not specified, `"levelset"` is used

              * `"levelset"` denotes the new method described in the referenced
                papers [PeVe14,PeVe16,PeVe17,PeVe19]
              * `"brute"` denotes "a bit intelligent" brute force method based
                on generating all the potential one-element co-extensions of a
                given tomonoid and testing whether they meet the axioms of a f.n.
                tomonoid (i.e. associativity)

        startingFNTOMonoid (fntom.FNTOMonoid, optional): the f. n.
            tomonoid for which the co-extensions are supposed to be found;
            if not specified, the trivial (one-element) monoid is used

        upToSize (int, optional): up to which size the co-extensions are
            recursively supposed to be found;
            if not specified, the depth of value `1` is used which means that
            only co-extensions of the size greater by one are found

        depth (int, optional): up to which size, compared to the size of this
            f. n. tomonoid, the co-extensions are recursively supposed to be found;
            for example: if the size is `5` and `depth` is `3` then the
            co-extensions are supposed to be generated up to size `8`;
            if not specified, the depth of value `1` is used which means that
            only co-extensions of the size greater by one are found

        archimedean (bool, optional): if `True`, only Archimedean co-extensions
            are found;
            it is supposed that the starting f. n. tomonoid is Archimedean

        commutative (bool, optional): if `True`, only commutative co-extensions
            are found;
            it is supposed that the starting f. n. tomonoid is commutative

        displayProgress (bool): if `True` then a progres bar will be
            displayed on the terminal during the computation of the
            co-extensions

        counter (fntom.Counter, optional): counter that will be used to
            give unique identifiers to the generated f. n. tomonoids;
            if not specified, the function will create its own instance of
            `fntom.Counter`

    Returns:
        list of fntom.FNTOMonoid: the generated f. n. tomonoids
    """
    if counter == None:
        counter = fntom.Counter()
    if startingFNTOMonoid == None:
        # create the trivial monoid
        startingFNTOMonoid = fntom.FNTOMonoid(counter.getNew(), size = 1)
    monoids = [ startingFNTOMonoid ]
    if upToSize == None:
        if depth == None:
            upToSize = startingFNTOMonoid.size + 1
        else:
            upToSize = startingFNTOMonoid.size + depth
    sizeWidth = len(str(upToSize))
    currentSize = startingFNTOMonoid.size
    monoidsProcessed = 0
    monoidsTotal = 1
    numCoExtWidth = len(str(monoidsTotal))
    report = startingFNTOMonoid.size * [ {"number": None, "time": None} ]
    report.append( {"number": 1, "time": 0.0} )
    index = 0
    timeStart = timeit.default_timer()
    numCoExt = 0
    while index < len(monoids):
        while monoids[index].closed:
            index += 1
            monoidsProcessed += 1
        if monoids[index].size > currentSize:
            if displayProgress:
                currentMsg = "Size " + f"{currentSize + 1:>{sizeWidth}}" + ":"
                drawProgress(monoidsProcessed / monoidsTotal, msg = currentMsg)
                timeEnd = timeit.default_timer()
                timePassed = timeEnd - timeStart
                print("", datetime.timedelta(seconds=timePassed), end = " ")
                for k in range(2 * numCoExtWidth + 1):
                    print(end = " ")
                for k in range(2 * numCoExtWidth + 1):
                    print(end = "\b")
                print(numCoExt)
            currentSize += 1
            monoidsProcessed = 0
            monoidsTotal = numCoExt
            numCoExtWidth = len(str(monoidsTotal))
            timeEnd = timeit.default_timer()
            timePassed = timeEnd - timeStart
            report.append( {"number": numCoExt, "time": timePassed} )
            numCoExt = 0
            timeStart = timeEnd
        if index < len(monoids) and monoids[index].size < upToSize:
            if displayProgress:
                currentMsg = "Size " + f"{currentSize + 1:>{sizeWidth}}" + ":"
                drawProgress(monoidsProcessed / monoidsTotal, msg = currentMsg)
                if monoidsProcessed > 0:
                    timeEnd = timeit.default_timer()
                    timePassed = timeEnd - timeStart
                    timeEstTotal = monoidsTotal * timePassed / monoidsProcessed
                    timeEstRemaining = timeEstTotal - timePassed
                    print("", datetime.timedelta(seconds=timeEstRemaining), end = " ")
                    print(f"{monoidsProcessed:>{numCoExtWidth}}" + "/" + str(monoidsTotal), end = " ")
            coextensions = monoids[index].computeCoExtensions(
                    counter,
                    archimedean = archimedean,
                    commutative = commutative)
            monoids.extend(coextensions)
            monoids[index].closed = True
            numCoExt += len(coextensions)
        index += 1
        monoidsProcessed += 1
    return (monoids, report)

def drawProgress(progress, barSize = 20, msg = None, showBar = True, showPercentage = True):
    """
    Draws a progress bar to the terminal output.

    The output is not ended by new line, hence it will be overwritten with a new
    call of this method.

    Additional message can be also attached to the end of the drawn progress bar.

    Args:
        progress (float): a number in the range from `0.0` to `1.0`
        barSize (int): how many `"#"` characters the progress bar shall have
        msg (str): the message displayed before the percentage and the progress bar
        showBar (bool): if `True` the progress bar will be displayed
        showPercentage (bool): if `True` the percentage will be displayed
    """
    # delete all the characters on the active terminal line
    for i in range(80):
        print("\b", end="")
    # write initial message
    if msg != None:
        print(msg, end = " ")
    # write percentage
    percentage = round(100 * progress)
    print(f"{percentage:>{3}}" + "% ", end = "")
    # draw progress bar
    numSquares = round(barSize * progress)
    print("[", end = "")
    for i in range(numSquares):
        print("#", end = "")
    for i in range(barSize - numSquares):
        print(" ", end = "")
    print("]", end = "", flush = True)

def exportReportToText(report):
    """
    Auxiliary method to convert the content of `report`, returned by
    `generateFNTomonoids` to text that can be written to the output file.

    Note that all the lines of the returned text start by `"#"`;
    hence they are supposed to be ignored when the file is read.
    """
    text = ""
    sizeWidth = len(str(len(report) - 1))
    numberWidth = len(str(report[-1]["number"]))
    for i in range(len(report)):
        if report[i]["number"] != None:
            text += "# "
            text += "size: " + f"{i:>{sizeWidth}}" + " "
            text += "number: " + f"{report[i]['number']:>{numberWidth}}" + " "
            text += "time:" + str(datetime.timedelta(seconds=report[i]["time"]))
            text += "\n"
    return text

def saveToCompressed(path, fntomonoids, displayProgress = False, report = None):
    """
    Saves a list of f. n. tomonoids to a "compressed" file given by the path.

    Args:
        path (str): path to the file

        fntomonoids (list of coextensions.FNTOMonoid): list of f. n. tomonoids
            (as, e. g., generaed by `generateFNTomonoids`)

        displayProgress (bool): if `True` then a progres bar will be
            displayed on the terminal during the saving of the file
    """
    with open(path, "w") as outFile:
        if report != None:
            outFile.write(exportReportToText(report))
        numTomonoids = len(fntomonoids)
        for i in range(numTomonoids):
            if displayProgress:
                progress = (i + 1) / numTomonoids
                drawProgress(progress, msg = "Writing output file:")
            outFile.write(fntomonoids[i].exportToCompressedText() + "\n")
        if displayProgress:
            print()

def saveToUncompressed(
        path,
        fntomonoids,
        displayProgress = False,
        separator = "",
        endLine = "\n",
        tableSymbols = "base62",
        identifierSymbols = "base62",
        addOriginal = False,
        report = None):
    """
    Saves a list of f. n. tomonoids to an "uncompressed" file given by the
    path.

    Args:
        path (str): path to the file

        fntomonoids (list of coextensions.FNTOMonoid): list of f. n. tomonoids
            (as, e. g., generaed by `generateFNTomonoids`)

        displayProgress (bool): if `True` then a progres bar will be
            displayed on the terminal during the saving of the file

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
    """
    with open(path, "w") as outFile:
        if report != None:
            outFile.write(exportReportToText(report))
        numTomonoids = len(fntomonoids)
        for i in range(numTomonoids):
            if displayProgress:
                progress = (i + 1) / numTomonoids
                drawProgress(progress, msg = "Writing output file:")
            outFile.write(fntomonoids[i].exportToText(
                                        separator = separator,
                                        endLine = endLine,
                                        tableSymbols = tableSymbols,
                                        identifierSymbols = identifierSymbols,
                                        addOriginal = addOriginal))
            outFile.write("\n")
        if displayProgress:
            print()
