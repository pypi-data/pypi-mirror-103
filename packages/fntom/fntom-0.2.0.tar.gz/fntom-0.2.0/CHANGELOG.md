
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2021-04-21
### Added
 *  class `CompressedFile` to read f. n. tomonoids from a "compressed" file
 *  script genall.py that generates as many f. n. tomonoids, as possible (up
    to a given limit of the size of the output files)

## [0.1.0] - 2021-04-17
 *  The package fntom is able to:
    - define a f. n. tomonoid and to find all its one-element Rees
      co-extensions; these co-extensions can be restricted to commutative or
      Archimedean,
    - display progress bars when computing the co-extensions (this is handy
      since the process may take a signficantly long time),
    - save the generated f. n. tomonoids to a "compressed" or "uncompressed"
      text file; the compression is based on saving only differences from
      the corresponding parent f. n. tomonoid
 *  Includes script genfntom.py which serves to run from the command line the
    methods of the package fntom in order to generate, starting from the
    trivial monoid, all the specified f. n. tomonoids up to a given size.

[0.2.0]: https://gitlab.com/petrikm/fntom/-/tags/0.2.0
[0.1.0]: https://gitlab.com/petrikm/fntom/-/tags/0.1.0

