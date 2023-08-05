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
    Contains all the package-defined exceptions.
"""

__all__ = ["FileSyntax", "NotTOMPartition"]

class FileSyntax(Exception):
    """
    Implements the exception that is raised when the content of the input file
    is corrupted.
    """
    def __init__(self, lineNumber, text):
        """
        Args:
            lineNumber (int): number of the line in the input file where the
                error has occured
            text (str): error message
        """
        super().__init__("FILE SYNTAX ERROR ON LINE " + str(lineNumber) + ": " + text)

class NotTOMPartition(Exception):
    """
    Implements the exception referring to the fact, that there are assigned
    multiple values to one level equivalence class of a tomonoid.
    """
    def __init__(self, values, tomonoid):
        """
        Args:
            values (list of int): list of the multiple values that are assigned to
                one class
            tomonoid (LevelEquivalence): reference to the tomonoid partition
        """
        super().__init__("ERROR: ATTEMPT TO MERGE CLASSES WITH VALUES: " + str(values))

