# kplib

[![pipeline status](https://gitlab.com/muellergroup/kplib/badges/master/pipeline.svg)](https://gitlab.com/muellergroup/kplib/commits/master)


KpLib is a C++ library for finding the optimal Generalized Monkhorst-Pack k-points grid. It can be imported into electronic-structure packages as a generator of efficient generalized *k*-point grids, or be integrated into user scripts through the python interface.

For questions of kpLib and underlying algorithms, you are welcomed to check our paper at [here](https://doi.org/10.1016/j.commatsci.2020.110100) or send emails to kpoints@jhu.edu.

# Usage

## Route I: Integrate kpLib as a C++ library
---
### Compile kpLib
We use `cmake` to detect native build environment and generate native build files. For Unix-like operating systems, users can build the project by:

    $ git clone https://gitlab.com/muellergroup/kplib.git
    $ cd kplib
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make

Then you can find a static library `libkpoints.a` and a dynamic library `libkpoints.so` in the `./build` directory.

### Use kpLib in your code

There are basically two steps:

1. copy the header file `src/kPointLatticeGenerator.h` to your `include` folder, and add the following line to your source code

        #include "kPointLatticeGenerator.h"

2. link the library at the linking stage.

    For example, to link the static library and compile the object `myapp.o` to the final executable `myapp`, you can

        $ g++ myapp.o -L /path/to/lib libkpoints.a -o myapp

    If you want to use the dynamic library, you can

        $ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/lib
        $ g++ myapp.o -L /path/to/lib -lkpoints -o myapp

    The first line tells the loader, `ld`, where to find the shared library at runtime, since the dynamic linkage only puts a reference of the library in the executable.

Then you are ready to go!

## Route II: Integrate KpLib through Python Interface
---

### Installation

The source code is downloaded at https://gitlab.com/muellergroup/kplib .

```
$ git clone https://gitlab.com/muellergroup/kplib.git
```

In order to install this package use pip:

```
$ pip install "kplib"
```

### Command-line interface `kpgen`

You can use the command line interface to generate Generalized Monkhorst-Pack k-points grid by calling `kpGen` in terminal.

`kpGen` reads the input file by using `pymatgen`, so it in principle support all kinds
of structure format supported by `pymatgen`. By default, it reads POSCAR as input file.
Currently, the output file which contain the k-points is writen as VASP's KPOINTS file.

Users can check and see the details of the arguments and options by `kpGen --help`.

### Python API reference and examples

For users who wants to use `kplib` in their python packages, the recommended method is to use the `get_kpoints` function. It returns a dict, the keys of which are:

- `min_periodic_distance`: The minimum distance between lattice points on the real-space superlattice.
- `num_distinct_kpts`: The number of distinct k-points reduced by lattice symmetry.
- `num_total_kpts`: The number of total k-points.
- `coords`: The coordinates of k-points, represented in refraction coordinate.
- `weights`: The weights of corresponding k-points.


```python
import numpy as np
from kplib import get_kpoints

struc = ...

kpts = get_kpoints(struc, minDistance=24.9, include_gamma=include_gamma)
```

# How to cite
If you use the kplib in generating generalized *k*-point grids, please cite the following article:

Wang, Y., Wisesa, P., Balasubramanian, A., Dwaraknath, S. & Mueller, T. Rapid generation of optimal generalized Monkhorst-Pack grids. Comp Mater Sci, 110100, doi:https://doi.org/10.1016/j.commatsci.2020.110100 (2020).

# Documentation
## C++ API

#### Class: `kPointLatticeGenerator`

    template <typename T>
    using Tensor = std::vector<std::vector<T>>;

    /**
     * Constructor.
     *
     * To see how the variables are defined, check the "Conventions" section below)
     *
     * @param primVectorsArray            primitive lattice vectors in rows.
     * @param conventionalVectorsArray    conventional lattice vectors in rows.
     * @param latticePointOperatorsArray  point operators of the Laue Class
                                          of the input structure, expressed
                                          in the basis of primitive lattice vectors
     * @param numOperators                number of point operators in above array
     * @param isConventionalHexaognal     whether the conventional lattice is
                                          hexagonal
     */
    KPointLatticeGenerator(const double primVectorsArray[3][3],
	                       const double conventionalVectorsArray[3][3],
	                       const int latticePointOperatorsArray[][3][3],
	                       const int numOperators,
	                       const bool isConventionalHexagonal);

    /*
     * Specify whether to generate a gamma-centered grid or a shifted grid.
     * The available shifts are:
     *     {{0.0, 0.0, 0.5}, {0.0, 0.5, 0.0}, {0.5, 0.0, 0.0}, {0.5, 0.5, 0.0},
     *      {0.5, 0.0, 0.5}, {0.0, 0.5, 0.5}, {0.5, 0.5, 0.5}}
     * Basiclly, side centers, face centers and the body center.
     *
     * @param includeGamma   TRUE:  gamma-centered grid
     *                       FALSE: grid with one of the above shift
     *                       AUTO:  search both shifted and gamma-centered grid
     *                              and return the best one.
     */
    enum INCLUDE_GAMMA { TRUE, FALSE, AUTO };
    void includeGamma(INCLUDE_GAMMA includeGamma);

    /*
     * @param minDistance  The returned grid should have a corresponding
     *                     real-space superlattice whose "minimum periodic distance"
     *                     is no smaller than this value.
     * @param minSize      Minimum number of total k-points of grids returned.
     */
    KPointLattice getKPointLattice(const double minDistance,
                                   const int minSize);

#### Class: `KPointLattice`

It's meant to hold the found k-point grid and provide query functions.


The main query routines of this type:

	double getMinPeriodicDistance();

    int getNumDistinctKPoints();

    int numTotalKPoints();

    /*
     * @return Tensor<double> 2D arrays of coordinates. It's basically a wrapper
     *                        of "double coords[][3]".
     */
	Tensor<double> getKPointCoordinates();

    /*
     * @return vector<int>  1D array of k-points weights.
     */
	std::vector<int> getKPointWeights();


## Conventions

This section specifies the conventions we use for the variables used in `kPointLatticeGenerator` constructor:
i.e. `primVectors`, `conventionalVectors`, `latticePointOperators` and `isConventionalHexagonal`.

#### Lattice Vectors

Lattice vectors are expressed as row vectors of the lattice matrix:

    double primtiveVectors[3][3] = {{a_x, a_y, a_z},
                                    {b_x, b_y, b_z},
                                    {c_a, c_z, c_y}}

#### Point Operators

Each operation is a 3x3 integral matrix, representing how a **fractional coordinate** in the **primitive lattice basis** is transformed under this operation.

    int latticePointOperations[][3][3];

Because of the lattice vectors are expressed as rows, each symmetry operation is done through "x' = x<sup>T</sup> . R", i.e. vector times matrix.

#### Conventional Lattice Vectors

Becuase of the algorithm we use to efficiently iterate symmetry-preserving superlattice, the conventional lattice vectors should follow the below requirements:

* For all lattice systems, except for **triclinic**, the c-vector should be along the axis of the highest order rotational operation, i.e the 4-fold, 6-fold, 3-fold, 4-fold, any 2-fold, and 2-fold rotation for  **cubic**, **hexagonal**, **trigonal**, **tetragonal**, **orthorhombic**, and **monoclinic** lattices, respectively. This direction is commonly referred as the "primary symmetry direction" in crystallography textbooks.

* For **trigonal** lattices, the conventional lattices should be primitive hexagonal lattices, i.e. the trigonal-centered hexagonal.

The algorithm doesn't put constraints on triclinic system, or on the centering type of lattices in the **2/m** and the **mmm** Laue class.

(Note: User could get the primary directions from the point symmetry opeartions.)

## Example of using kplib -- `demo_kplib`

To demonstrate the usage of the kpbib, we implement a simple C++ application to find Generalised Monkhorst-Pack k-point grids. It use `spglib` to determine symmetries ([Togo and Tanaka, 2010](https://atztogo.github.io/spglib/index.html)) and output the k-point grid in the format of VASP KPOINTS file.

It's under the folder `demo_kplib`. To build this application, user should build [`spglib`](https://atztogo.github.io/spglib/index.html) and replace the library file `libsymspg.a` in `./lib`. Then the executable `demo_kplib` can be built by

    $ cd demo_kplib
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make

The binary is placed at `./build/demo_kplib`. To call it, use:

    $ demo_kplib /path/to/POSCAR /path/to/PRECALC > KPOINTS

The POSCAR is one of the standard VASP input file. The PRECALC file is the input file of `demo_kplib` and users can find its specifications on our [website](http://muellergroup.jhu.edu/K-Points.html). Since it's for demonstration purposes, only the parameters `MINDISTANCE`, `MINTOTALKPOINTS`, and `INCLUDEGAMMA` are valid.

There are some examples of using this application in `demo_kplib/examples`.

For a more complete application, check our ***K*-point Grid Generator** and ***K*-point Server**.

#### Code snippet of demo_kpib

Below are excerpts from the application to show how to use the kplib API.

`main.cpp`:

    #include "kPointLatticeGenerator.h"
    #include "utils.h"
    #include "precalc.h"
    #include "poscar.h"
    #include <iostream>

    int main(int argc, char **argv) {
        if (argc < 3) {
            std::cerr << "Usage: ./main /path/to/POSCAR /path/to/PRECALC"
                      << std::endl;
            return 1;
        }
        // Parse POSCAR and PRECALC.
        Poscar poscar;
        poscar.readFromPoscar(std::string(argv[1]));
        Precalc precalc(argv[2]);

        // Execute the main routines.
        KPointLatticeGenerator generator = initializeKPointLatticeGeneratorObject(
            poscar.primitiveLattice, poscar.coordinates, poscar.atomTypes);

        if (precalc.getIncludeGamma() == "TRUE") {
            generator.includeGamma(TRUE);
        } else if (precalc.getIncludeGamma() == "FALSE") {
            generator.includeGamma(FALSE);
        } else if (precalc.getIncludeGamma() == "AUTO") {
            generator.includeGamma(AUTO);
        }

        KPointLattice latticeGamma = generator.getKPointLattice(
            precalc.getMinDistance(), precalc.getMinTotalKpoints());

        outputLattice(latticeGamma);
    }

`utils.cpp`:

    #include "utils.h"
    #include "spglib.h"
    ... // other includes and functions

    // Wrapper of the kPointLatticeGenerator constructor.
    KPointLatticeGenerator initializeKPointLatticeGeneratorObject(
            Tensor<double> primitiveLattice,
            Tensor<double> coordinates,
            std::vector<int> atomTypes) {

        double primLatticeArray[3][3] = {0};
        double conventionalLatticeArray[3][3] = {0};
        int rotation[192][3][3] = {0};
        int size = 0;
        bool isConventionalHexagonal = false;

        // use spglib to get necessary parameters for the consturctor
        // of kPointLatticeGenerator.
        ...

        KPointLatticeGenerator generator = KPointLatticeGenerator(primLatticeArray,
                conventionalLatticeArray, rotation, size, isConventionalHexagonal);
        return generator;

    }



