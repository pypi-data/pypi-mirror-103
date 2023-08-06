# Release Note

## Version 2019.09.17
Main features:
* Implemented dynamic generation scheme described in the pre-print: [Algorithms for the Generation of Generalized Monkhorst-Pack Grids](https://arxiv.org/abs/1907.13610).
* The algorithms implemented in this version are consistent with the ones used to generate the database for version `2019.08.01` of the *K*-Point Grid Generator and the *K*-Point Server.
* When specifying MINDISTANCE, kpLib can generate optimized grids in 0.19 seconds at 50 angstroms and within 5 seconds at 100 angstroms, on average over 102 structures randomly selected from Inorganic Crystal Structure Database (ICSD).
* Wrapped kpLib in a Python module `kpGen` verion `0.0.1`. Thanks for the work by Shyam!
* Added a flag `USESCALEFACTOR` to control whether or not scale factor technique is used. `TRUE` will activate it, while `FALSE` and the default behavior is to turn it off. When scale factor is used, the explicit search limits are 729, 1728, 46656 and 5632 for triclinic, monoclinic, cubic and other crystal systems, respectively. Above these limits, scale factor will be used to accelerate the generation. Grids using scale factor will have slightly higher number of symmetrically irreducible *k*-point, since kpLib doesn't perform an exhaustive search in this case.
