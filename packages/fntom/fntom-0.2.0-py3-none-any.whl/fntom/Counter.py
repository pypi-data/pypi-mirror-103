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
    Definition of class `Counter` which serves to give the increasing sequence
    of natural numbers starting from `1`.
"""

__all__ = ["Counter"]

import timeit
import datetime

class Counter:
    """
    Gives the sequence of increasing natural numbers starting from `1`.

    These numbers are utilized to give unique names to the generated f. n.
    tomonoids.

    Attributes:
        number (int): the current value of the counter
        report (bool): if `True` then the value of the counter will be printed
            on the terminal output everytime it reaches a value which is a
            natural multiple of the attribute `period`
        period (int): determines in which steps the values of the counter will
            be printed on the terminal output; see the attribute `report`
        time (float): timestamp of the last output of the counter value on the
            terminal; to give the user some idea, how quick the computation is
    """
    def __init__(self, number = 0, report = False, period = 10000):
        self.number = number
        self.report = report
        self.period = period
        self.time = timeit.default_timer()

    def set(self, number):
        """
        Sets the current value of the counter.
        """
        self.number = number

    def getNew(self):
        """
        Increases the value of the counter by 1 and returns it.

        If `report == True` then this method writes a short report to the
        terminal output everytime the value reaches a multiple of `period`.

        Returns:
            int: the new number of the counter
        """
        self.number = self.number + 1
        if self.report and self.number % self.period == 0:
            newTime = timeit.default_timer()
            print(datetime.datetime.today(), end = " ")
            print("counter has reached", self.number, end = " ")
            print("in", round(newTime - self.time, 2), "seconds")
            self.time = newTime
        return self.number

    def getCurrent(self):
        """
        Returns the current number of the counter without increasing it.

        Returns: 
            int: the current number of the counter
        """
        return self.number
