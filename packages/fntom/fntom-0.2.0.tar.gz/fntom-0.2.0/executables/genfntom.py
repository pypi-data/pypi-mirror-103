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
    This script serves to run from the command line the methods of the package
    fntom in order to generate f. n. tomonoids up to a given size.

      * The f. n. tomonoids can be either computed as one-element Rees
        co-extensions of the trivial monoid (that contains one element only).
      * Or, if an input file is given, the script reads the contained f. n.
        tomonoids that are not closed, computes their co-extensions up to the
        given size and writes the resulting f. n. tomonoids to the end of the
        same file.
        Note, however, that this second option, IS NOT IMPLEMENTED, yet.

    The description of the command line arguments can be listed by typing:

        python genfntom.py --help
"""

import sys
import datetime
import fntom

def printHelpMessage():
    print()
    print("-----------------------------------------------------------------------")
    print("Generates finite, negative, totally ordered monoids")
    print("This script is a part of the package fntom, version", fntom.Constants.__version__)
    print("-----------------------------------------------------------------------")
    print()
    print("Command line arguments:")
    print()
    print("    -h, --help")
    print("        ... print this help message")
    print("    -i path, --input path")
    print("        (NOT IMPLEMENTED)")
    print("        ... path to input file containing definitions")
    print("            of f. n. tomonoids;")
    print("            can be in \"compressed\" or in \"uncompressed\" format")
    print("    -o path, --output path")
    print("        ... path to output file where the generated f. n. tomonoids")
    print("            will be written in \"compressed\" format")
    print("    -u path, --uoutput path, --uncompressedoutput path")
    print("        ... path to output file where the generated f. n. tomonoids")
    print("            will be written in \"uncompressed\" format")
    print("    -m, --mute")
    print("        ... the generated f. n. tomonoids will not be written")
    print("            to the standard output")
    print("    -s n, --uptosize n")
    print("        ... up to which size the f. n. tomonoids will be generated")
    print("    -c, --commutative")
    print("        ... the program will generate commutative f. n. tomonoids, only")
    print("    -a, --archimedean")
    print("        ... the program will generate Archimedean f. n. tomonoids, only")
    print("    -r, --report")
    print("        ... when finished, write a report to the standard output on times")
    print("            and numbers of generated f. n. tomonoids")
    print("    -p, --progress")
    print("        ... turns on displaying of the progress")
    print()
    print("    If an output file is not specified, the generted f. n. tomonoids")
    print("    are written in the \"0xyz1\" format to the standard output, unless")
    print("    the --mute option is given.")
    print()
    print("Examples:")
    print()
    print("    Generate f. n. tomonoids up to size 4 and write them")
    print("    to the standard output:")
    print()
    print("        python genfntom.py -s 4")
    print()
    print("    Generate Archimedean f. n. tomonoids up to size 5 and write them")
    print("    to an uncompressed file named \"out_u.txt\":")
    print()
    print("        python genfntom.py -a -s 5 -u out_u.txt")
    print()
    print("    Generate commutative f. n. tomonoids up to size 9 and write them")
    print("    to a compressed file named \"out_c.txt\"; display progress bars:")
    print()
    print("        python genfntom.py -c -p -s 9 -o out_c.txt")
    print()

def parseCommandLineArguments(argv):
    """
    Args:
        argv (list of str): value of `sys.argv`

    Returns:
        dict: options read from the command line arguments; the keys are:
            * "input" ... path to input file
            * "output" ... path to compressed output file
            * "uncompressedoutput" ... path to uncompressed output file
            * "uptosize" ... up to which size the f. n. tomonoids are supposed
                to be generated
            * "mute" ... if `True` then the generated f. n. tomonoids will not
                be written to standard output
            * "commutative" ... only commutative f. n. tomonoids will be
                generated
            * "archimedean" ... only Archimedean f. n. tomonoids will be
                generated
            * "report" ... when finished, write a report to the standard output
                on times and numbers of generated f. n. tomonoids
            * "progress" ... if `True`, progress bars will be displayed during
                the run of the program
    """
    options = {
        "input":                None,
        "output":               None,
        "uncompressedoutput":   None,
        "uptosize":             None,
        "mute":                 False,
        "commutative":          False,
        "archimedean":          False,
        "report":               False,
        "progress":             False,
    }
    if len(argv) == 1:
        print("No arguments given. For help, type:")
        print()
        print("    python", argv[0], "--help")
        print()
        return None
    else:
        i = 1
        while i < len(argv):
            # ----------------
            # read an argument
            # ----------------
            thisOption = None
            if argv[i][0] == "-":
                if len(argv[i]) == 1:
                    print("Unknown argument:", argv[i])
                    print("For help, type:")
                    print()
                    print("    python", argv[0], "--help")
                    print()
                    return None
                elif argv[i][1] == "-":
                    thisOption = argv[i][2:]
                    if thisOption == "uoutput":
                        thisOption = "uncompressedoutput"
                else:
                    if len(argv[i]) == 2:
                        o = argv[i][1]
                        if o == "h":
                            thisOption = "help"
                        elif o == "i":
                            thisOption = "input"
                        elif o == "o":
                            thisOption = "output"
                        elif o == "u":
                            thisOption = "uncompressedoutput"
                        elif o == "s":
                            thisOption = "uptosize"
                        elif o == "m":
                            options["mute"] = True
                        elif o == "c":
                            options["commutative"] = True
                        elif o == "a":
                            options["archimedean"] = True
                        elif o == "r":
                            options["report"] = True
                        elif o == "p":
                            options["progress"] = True
                        else:
                            print("Unknown argument:", argv[i])
                            print("For help, type:")
                            print()
                            print("    python", argv[0], "--help")
                            print()
                            return None
                    else:
                        for o in argv[i][1:]:
                            if o == "m":
                                options["mute"] = True
                            elif o == "c":
                                options["commutative"] = True
                            elif o == "a":
                                options["archimedean"] = True
                            elif o == "r":
                                options["report"] = True
                            elif o == "p":
                                options["progress"] = True
                            else:
                                print("Unknown argument:", argv[i])
                                print("For help, type:")
                                print()
                                print("    python", argv[0], "--help")
                                print()
                                return None
            else:
                print("Unknown argument:", argv[i])
                print("For help, type:")
                print()
                print("    python", argv[0], "--help")
                print()
                return None
            # ----------------------
            # interpret the argument
            # ----------------------
            if thisOption == None:
                pass
            elif thisOption == "help":
                printHelpMessage()
                return None
            elif thisOption == "input":
                i += 1
                if i < len(argv):
                    options["input"] = argv[i]
                else:
                    print("Path to a file after --input (or -i) is missing. The usage is:")
                    print()
                    print("    python", argv[0], "--input path")
                    print()
                    return None
            elif thisOption == "output":
                i += 1
                if i < len(argv):
                    options["output"] = argv[i]
                else:
                    print("Path to a file after --output (or -o) is missing. The usage is:")
                    print()
                    print("    python", argv[0], "--output path")
                    print()
                    return None
            elif thisOption == "uncompressedoutput":
                i += 1
                if i < len(argv):
                    options["uncompressedoutput"] = argv[i]
                else:
                    print("Path to a file after --uncompressedoutput (or -u) is missing. The usage is:")
                    print()
                    print("    python", argv[0], "--uncompressedoutput path")
                    print()
                    return None
            elif thisOption == "uptosize":
                i += 1
                if i < len(argv):
                    if argv[i].isdecimal() and int(argv[i]) > 0:
                        options["uptosize"] = int(argv[i])
                    else:
                        print("Expected positive integer after --uptosize (or -s). The usage is:")
                        print()
                        print("    python", argv[0], "--uptosize positive_integer")
                        print()
                        return None
                else:
                    print("Positive integer after --uptosize (or -s) is missing. The usage is:")
                    print()
                    print("    python", argv[0], "--uptosize positive_integer")
                    print()
                    return None
            elif thisOption == "mute":
                options["mute"] = True
            elif thisOption == "commutative":
                options["commutative"] = True
            elif thisOption == "archimedean":
                options["archimedean"] = True
            elif thisOption == "report":
                options["report"] = True
            elif thisOption == "progress":
                options["progress"] = True
            else:
                print("Unknown argument:", argv[i])
                print("For help, type:")
                print()
                print("    python", argv[0], "--help")
                print()
                return None
            i += 1
    return options

#
# Beginning of the program
#

options = parseCommandLineArguments(sys.argv)

if options != None:
    if options["uptosize"] == None:
        print("Specify size, up to which the f. n. tomonoids are supposed to be generated.")
        print("Use the option -s or --uptosize. For help, type:")
        print()
        print("    python", sys.argv[0], "--help")
        print()
    else:
        if options["input"] == None:
            fntomonoids, report = fntom.generateFNTomonoids(
                    upToSize = options["uptosize"],
                    commutative = options["commutative"],
                    archimedean = options["archimedean"],
                    displayProgress = options["progress"],
                    counter = fntom.Counter())
            if options["output"] != None:
                fntom.saveToCompressed(
                        options["output"],
                        fntomonoids,
                        displayProgress = options["progress"],
                        report = report)
            elif options["uncompressedoutput"] != None:
                fntom.saveToUncompressed(
                        options["uncompressedoutput"],
                        fntomonoids,
                        displayProgress = options["progress"],
                        separator = "",
                        endLine = "\n",
                        tableSymbols = "0xyz1",
                        identifierSymbols = "base62",
                        report = report)
            elif not options["mute"]:
                for tom in fntomonoids:
                    print(tom.exportToText(
                        separator = " ",
                        endLine = "\n",
                        tableSymbols = "0xyz1",
                        identifierSymbols = "base62",
                        addOriginal = False))
            if options["report"]:
                sizeWidth = len(str(len(report) - 1))
                numberWidth = len(str(report[-1]["number"]))
                print("Report:")
                for i in range(len(report)):
                    if report[i]["number"] != None:
                        print("size:", f"{i:>{sizeWidth}}", end = " ")
                        print("number:", f'{report[i]["number"]:>{numberWidth}}', end = " ")
                        print("time:", datetime.timedelta(seconds=report[i]["time"]))
