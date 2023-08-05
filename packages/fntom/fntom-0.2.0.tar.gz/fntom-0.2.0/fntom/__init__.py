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
This package contains an implementation of the algorithm that serves to find
all the one-element Rees co-extensions of a given finite, negative totally
ordered monoid (abbreviated by f. n. tomonoid).

Note that a commutative f. n. tomonoid represents a conjunction in the
semantics of a many-valued (fuzzy) logic that has finitely many totally ordered
logical values.


Representation of a finite set of logical values
------------------------------------------------

An example of a totally ordered finite set of (five) logical values is:

    0, 1/4, 2/4, 3/4, 1

where `1` is the "unit element" of the f. n. tomonoid and the "Truth" of the
corresponding fuzzy logical semantics while `0` is the "zero element" and the
logical "Falsity".

In the papers (see **References** below), that are the foundation of this
program, such a set would be described as

    0, x, y, z, 1

since letters, compared to fractions, are easier to read.

However, in order to work with these values in this program, it has turned out
to be the best solution to represent them by non-negative integers such that
`0` represents the unit and the greatest element represents the "zero".
Hence the previous set of logical values is represented, in the program, by:

    4, 3, 2, 1, 0


Many-valued conjunctions
------------------------

A conjunction on a totally ordered set of finite set of logical values is every
binary operation * such that:

  - `*` is associative, i.e, `(x*y)*y = x*(y*z)` for every `x`, `y`, and `z`
    from the set,
  - `*` is commutative , i.e, `x*y = y*x` for every `x` and `y` from the set,
  - `*` is monotone, i.e, `x <= y` implies `x*z <= y*z` for every `x`, `y`, and
    `z` from the set,
  - `1` is the neutral (unit) element of *, i.e, `x*1 = 1*x = x` for every `x`
    from the set.

Hence the operation of the conjunction is not unique like in the case of the
classical logic with two truth values.
For example, in the case of four logical values there are four distinct
conjunctions given by the following Cayley tables:

| 0 | y | z | 1 |  | 0 | y | z | 1 |  | 0 | y | z | 1 |  | 0 | y | z | 1 |  | 0 | y | z | 1 |  | 0 | y | z | 1 |
| - | - | - | - |  | - | - | - | - |  | - | - | - | - |  | - | - | - | - |  | - | - | - | - |  | - | - | - | - |
| 0 | 0 | 0 | z |  | 0 | 0 | y | z |  | 0 | y | y | z |  | 0 | 0 | z | z |  | 0 | y | z | z |  | 0 | y | z | z |
| 0 | 0 | 0 | y |  | 0 | 0 | 0 | y |  | 0 | y | y | y |  | 0 | 0 | 0 | y |  | 0 | 0 | y | y |  | 0 | y | y | y |
| 0 | 0 | 0 | 1 |  | 0 | 0 | 0 | 1 |  | 0 | 0 | 0 | 1 |  | 0 | 0 | 0 | 1 |  | 0 | 0 | 0 | 1 |  | 0 | 0 | 0 | 1 |

Note that these Cayley tables are modified: they are left-right flipped.
This way of depicting conjunctions is utilized in the referenced papers since
it corresponds with the way of depicting *triangular norms* which represents
many-valued conjunctions defined on the real unit interval `[0,1]`.

However, the inner prepresentation of the logical values is done by the
non-negative integers.
If the program exports conjunctions in this representation, two changes are
being made:

  - the logical values are written as numbers in the Base62 number system (the
    numbers system with 62 digits:
    `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`),
  - the Cayley tables **are not** left-right flipped compared to the previous
    case.

Hence the six four-valued conjunctions would be exprted as:

| 0 | 1 | 2 | 3 |  | 0 | 1 | 2 | 3 |  | 0 | 1 | 2 | 3 |  | 0 | 1 | 2 | 3 |  | 0 | 1 | 2 | 3 |  | 0 | 1 | 2 | 3 |
| - | - | - | - |  | - | - | - | - |  | - | - | - | - |  | - | - | - | - |  | - | - | - | - |  | - | - | - | - |
| 1 | 3 | 3 | 3 |  | 1 | 2 | 3 | 3 |  | 1 | 2 | 2 | 3 |  | 1 | 1 | 3 | 3 |  | 1 | 1 | 2 | 3 |  | 1 | 1 | 2 | 3 |
| 2 | 3 | 3 | 3 |  | 2 | 3 | 3 | 3 |  | 2 | 2 | 2 | 3 |  | 2 | 3 | 3 | 3 |  | 2 | 2 | 3 | 3 |  | 2 | 2 | 2 | 3 |
| 3 | 3 | 3 | 3 |  | 3 | 3 | 3 | 3 |  | 3 | 3 | 3 | 3 |  | 3 | 3 | 3 | 3 |  | 3 | 3 | 3 | 3 |  | 3 | 3 | 3 | 3 |

This way of exporting the conjunctions matches with their inner
representation by the program.


Finite, negative, totally ordered monoids (f. n. tomonoids)
-----------------------------------------------------------

A _finite, negative, totally ordered monoid_ (abbreviated as _f. n. tomonoid_)
of a size `n` (where `n` is a natural number) is a set `S` of `n` elements,
denoted and ordered as:

    0 < ... < x < y < z < 1

Hence, `0` is the bottom element and `1` is the top element.
Furthermore, this set is endowed with a binary operation `*` that satisfies,
for every `a`, `b`, and `c` from the set `S`:

  - `(a*b)*b = a*(b*c)` (associativity),
  - if `a <= b` then `a*c <= b*c` (monotonicity, or also, compatibility with
    the total order),
  - `a*1 = 1*a = a` (the top element `1` is also the neutral (unit) element of
    `*`).

An element `a` of a f. n. tomonoid is called _idempotent_ if `a*a=a`.
The elements `0` and `1` are always idempotent and the are called the _trivial
idempotents_.

A f. n. tomonoid is called:

  - _commutative_ if `a*b=b*a` for every `a` and `b` from the set `S`,
  - _Archimedean_ if `0` and `1` are the only idempotents.

Clearly, a f. n. tomonoid represents a totally ordered set of truth values
together with a conjunction which is represented by the monoidal binary
operation.


One-element Rees quotients
--------------------------

Given a f. n. tomonoid `S`, its one-element Rees quotient can be constructed by
"merging" its lowest element `0` and its second lowest element &alpha; (which
is called the _atom_) into a new bottom element.
For example, the one-element Rees quotient of the f. n. tomonoid:

| 0 | u | v | w | x | y | z | 1 |
| - | - | - | - | - | - | - | - |
| 0 | 0 | v | w | x | y | z | z |
| 0 | 0 | v | w | w | y | y | y |
| 0 | 0 | 0 | 0 | 0 | v | x | x |
| 0 | 0 | 0 | 0 | 0 | v | w | w |
| 0 | 0 | 0 | 0 | 0 | v | v | v |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | u |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

is the f. n. tomonoid:

| 0 | v | w | x | y | z | 1 |
| - | - | - | - | - | - | - |
| 0 | v | w | x | y | z | z |
| 0 | v | w | w | y | y | y |
| 0 | 0 | 0 | 0 | v | x | x |
| 0 | 0 | 0 | 0 | v | w | w |
| 0 | 0 | 0 | 0 | v | v | v |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Further, the one-element Rees quotient of the latter f. n. tomonoid is the f.
n. tomonoid:

| 0 | w | x | y | z | 1 |
| - | - | - | - | - | - |
| 0 | w | x | y | z | z |
| 0 | w | w | y | y | y |
| 0 | 0 | 0 | 0 | x | x |
| 0 | 0 | 0 | 0 | w | w |
| 0 | 0 | 0 | 0 | 0 | 0 |

and so on.
This way we eventually end up with the trivial monoid which is a set that
consists of the unit element, only.

Instead of one-element Rees quotient we say just _one-element quotient_.


One-element Rees co-extensions
------------------------------

If a f. n. tomonoid `T` is the one-element Rees quotient of a f. n. tomonoid
`S` then `S` is a _one-element Rees co-extension_ of `T`.
Hence, in the previous section, the first f. n. tomonoid is a one-element Rees
co-extension of the second one and the second f. n. tomonoid is a one-element
Rees co-extension of the third one.

Instead of one-element Rees co-extension we say just _one-element
co-extension_, or just _co-extension_.

Note that, while one-element quotients are unique, one-element co-extensions
are not.
For example, the f. n. tomonoid:

| 0 | x | y | z | 1 |
| - | - | - | - | - |
| 0 | 0 | 0 | x | z |
| 0 | 0 | 0 | 0 | y |
| 0 | 0 | 0 | 0 | x |
| 0 | 0 | 0 | 0 | 0 |

has 8 co-extensions:

| 0 | w | x | y | z | 1 |   | 0 | w | x | y | z | 1 |   | 0 | w | x | y | z | 1 |   | 0 | w | x | y | z | 1 |
| - | - | - | - | - | - |   | - | - | - | - | - | - |   | - | - | - | - | - | - |   | - | - | - | - | - | - |
| 0 | 0 | 0 | 0 | x | z |   | 0 | 0 | 0 | 0 | x | z |   | 0 | 0 | 0 | w | x | z |   | 0 | 0 | 0 | w | x | z |
| 0 | 0 | 0 | 0 | 0 | y |   | 0 | 0 | 0 | 0 | w | y |   | 0 | 0 | 0 | 0 | 0 | y |   | 0 | 0 | 0 | 0 | w | y |
| 0 | 0 | 0 | 0 | 0 | x |   | 0 | 0 | 0 | 0 | 0 | x |   | 0 | 0 | 0 | 0 | 0 | x |   | 0 | 0 | 0 | 0 | 0 | x |
| 0 | 0 | 0 | 0 | 0 | w |   | 0 | 0 | 0 | 0 | 0 | w |   | 0 | 0 | 0 | 0 | 0 | w |   | 0 | 0 | 0 | 0 | 0 | w |
| 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |

| 0 | w | x | y | z | 1 |   | 0 | w | x | y | z | 1 |   | 0 | w | x | y | z | 1 |   | 0 | w | x | y | z | 1 |
| - | - | - | - | - | - |   | - | - | - | - | - | - |   | - | - | - | - | - | - |   | - | - | - | - | - | - |
| 0 | 0 | 0 | w | x | z |   | 0 | 0 | w | w | x | z |   | 0 | 0 | w | w | x | z |   | 0 | w | w | w | x | z |
| 0 | 0 | 0 | w | w | y |   | 0 | 0 | 0 | 0 | w | y |   | 0 | 0 | 0 | w | w | y |   | 0 | w | w | w | w | y |
| 0 | 0 | 0 | 0 | 0 | x |   | 0 | 0 | 0 | 0 | w | x |   | 0 | 0 | 0 | 0 | w | x |   | 0 | w | w | w | w | x |
| 0 | 0 | 0 | 0 | 0 | w |   | 0 | 0 | 0 | 0 | 0 | w |   | 0 | 0 | 0 | 0 | 0 | w |   | 0 | w | w | w | w | w |
| 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |

Notice that the second and the third one are non-commutative while the rest is
commutative.


Description of the program
--------------------------

The aim of this package is to find all the one-element Rees co-extensions
of a given f. n. tomonoid.
For this purpose, the algorithm introduced in the referenced papers is
utilized.
It is performed by the method `fntom.FNTOMonoid.FNTOMonoid.computeCoExtensions`.

Once the co-extensions of a given f. n. tomonoid can be all found, one can,
starting from the trivial, single-element, f. n. tomonoid, find all the f. n.
tomonoids up to a given size.
The package implements this task, as well, by the method
`fntom.Utils.generateFNTomonoids`.

The number of f. n. tomonoids grows rapidly with their size (see the table in
the next section).
For this reason, a clever way of saving the generated f. n. tomonoids is
needed.
This package therefore contain a module `fntom.CompressedFile` which
implements a text file format where each saved f. n. tomonoid is decribed by
its differences when compared to its parent (i.e., to the f. n. tomonoid from
which it has been created as a co-extension).


Table with numbers of finite, negative tomonoids
------------------------------------------------

Running this program on a personal computer, the following numbers of f. n.
tomonoids have been achieved.

| size |    all, | Archimedean, | commutative, | Archimedean and commutative |
| ----:| -------:| ------------:| ------------:| ---------------------------:|
|    1 |       1 |            1 |            1 |                           1 |    
|    2 |       1 |            1 |            1 |                           1 |    
|    3 |       2 |            1 |            2 |                           1 |    
|    4 |       8 |            2 |            6 |                           2 |    
|    5 |      44 |            8 |           22 |                           6 |    
|    6 |     308 |           44 |           94 |                          22 |   
|    7 |    2641 |          333 |          451 |                          95 |   
|    8 |   27120 |         3543 |         2386 |                         471 |  
|    9 |  332507 |        54954 |        13775 |                        2670 | 
|   10 | 5035455 |      1297705 |        86417 |                       17387 |


References
----------

For the theoretical description of the problem and for the description of the
algorithm se the paper:

* [PeVe17] M. Petrík and Th. Vetterlein. 
    *Rees coextensions of finite, negative tomonoids.*
    Journal of Logic and Computation 27 (2017) 337-356. 
    DOI: [10.1093/logcom/exv047](https://doi.org/10.1093/logcom/exv047),
    [PDF](../../papers/Petrik_Vetterlein__Coextensions__preprint.pdf).

For a more detailed description of the algorithm see the papers:

* [PeVe16] M. Petrík and Th. Vetterlein. 
    *Algorithm to generate finite negative totally ordered monoids.*
    In: IPMU 2016: 16th International Conference on Information Processing 
        and Management of Uncertainty in Knowledge-Based Systems.
    Eindhoven, Netherlands, June 20-24, 2016.
    [PDF](../../papers/Petrik_Vetterlein__IPMU_2016__preprint.pdf).

* [PeVe14] M. Petrík and Th. Vetterlein. 
    *Algorithm to generate the Archimedean, finite, negative tomonoids.*
    In: Joint 7th International Conference on Soft Computing 
        and Intelligent Systems and 15th International Symposium on Advanced Intelligent Systems.
    Kitakyushu, Japan, Dec. 3-6, 2014.
    DOI: [10.1109/SCIS-ISIS.2014.7044822](https://doi.org/10.1109/SCIS-ISIS.2014.7044822).
    [PDF](../../papers/Petrik_Vetterlein__SCIS_ISIS_2014__preprint.pdf).
    
For more details on one-element co-extensions of finite, negative, tomonoids see the paper:

* [PeVe19] M. Petrík and Th. Vetterlein. 
    *Rees coextensions of finite tomonoids and free pomonoids.*
    Semigroup Forum 99 (2019) 345-367. 
    DOI: [10.1007/s00233-018-9972-z](https://doi.org/10.1007/s00233-018-9972-z),
    [PDF](../../papers/Petrik_Vetterlein__Pomonoids__preprint.pdf).
"""

import fntom.Error
from fntom.Constants import *
from fntom.Counter import *
from fntom.Utils import *
from fntom.LevelEquivalence import *
from fntom.FNTOMonoid import *
from fntom.CompressedFile import *
