#ifndef KPOINTLATTICEGENERATOR_H
#define KPOINTLATTICEGENERATOR_H

#include <vector>
#include <string>
#include <limits>
#include "msmath.h"
#include "kPointLattice.h"

enum INCLUDE_GAMMA { TRUE, AUTO, FALSE };

template <typename T> int sgn(T val);

class KPointLatticeGenerator {

private:
  //---------------------------------------Member attributes--------------------------------------//

  /*
   * Value used to address numerical errors. Distance with an absolute value below "precision"
   * is treated as if it's zero.
   */
  double PRECISION = 3e-6;

  /*
   * Estimated maximum length of the shortest lattice vector parallel with the c3 vector.
   */
  double m_MaxZDistance;

  Tensor<double> m_PrimVectors;          // {a1, a2, a3}
  Tensor<double> m_ConventionalVectors;  // {c1, c2, c3}
  Tensor<double> m_CartesianToPrim;
  double m_NumConventionalPrimCells; // Keep this as a double to avoid integer division issues.
  double m_PrimCellSize;  // volume of the primitive unit cell.

  /*
   * Matrix representation of point operations in the basis of primitive lattice vectors.
   */
  std::vector<Tensor<int> > m_PointOperators3D;

  /*
   * Matrix representation of point operations in the basis of {c1, c2}, i.e. the conventional
   * lattice vectors normal to the third one, c3. They are derived in constructor from
   * m_PointOpeartors3D.
   */
  std::vector<Tensor<int> > m_PointOperators2D;

  /*
   * Matrix representation of point operations in the basis of reciprocal primitive lattice.
   * They change as transformation matrices of superlattices change. Hence, they are re-calculated
   * each time in function "numDistinctKPoints" when the distinct k-points are to be calculated.
   *
   * It is declared as global just so we don't need to reallocate this array each time.
   */
  std::vector<Tensor<int> > m_KPointOperators;

  /*
   * A wrapper variable for m_Hexagonal2DShifts and m_Other2DShifts. Assigned to either of these
   * two depending on the input structure in the constructor.
   */
  Tensor<double> m_Shifts2D;

  /*
   * Three-dimensional shifts of the gamma points.
   */
  Tensor<double> m_KPointShifts;

  /*
   * Two-dimensional shifts between stackings for hexagonal and trigonal.
   */
  Tensor<double> m_Hexagonal2DShifts;

  /*
   * Two-dimensional shifts between stackings for lattices other than hexagonal and trigonal.
   */
  Tensor<double> m_Other2DShifts;

  /*
   *  A parameter to control the usage of scale factor. A scale factor, n, if larger than 1,
   *  will divide the input MINDISTANCE by n, and return a k-point grid corresponding to a
   *  "n x n x n" superlattice of the found superlattice. When scale factor is used, the code
   *  uses 729 and 1728 as default search depth for triclinic and monoclinic structures. For
   *  cubic and other crystal systems, the search depth in 46656 (36x36x36) and 5832 (18x18x18).
   */
  int m_MaxScaleFactor = 1;
  int m_MaxAllowedKPoints = std::numeric_limits<int>::max();

  //--------------------------------------Member Functions----------------------------------------//

  /*
   * The wrapper function of getKPointLatticeTriclnic() and getKPointLatticeOrthogonal().
   * It parses the minDisance and minSize and controls the loop for an exhaustive search.
   * It implements the dynamic generation algorithm in section 2.1 of our paper.
   */
  KPointLattice getKPointLattice(double minScaledDistance, int scaledMinSize, int scaledMaxSize,
                                 int scaleFactor);

  /*
   * The actual grid generation function for triclinic lattices.
   *
   * @param scaledSize                The size of the k-point grids to be searched for.
   * @param minAllowedScaledDistance  The minimum allowed distance between any points on
   *                                  superlattices.
   * @param bestKnownLattice          The best grid found so far.
   * @param scaleFactor               Kept here as an option to scale structures when
   *                                  there is a maximum search depth. By "scale structures",
   *                                  see section II.D of our first paper:
   *                      https://journals.aps.org/prb/abstract/10.1103/PhysRevB.93.155109.
   */
  KPointLattice getKPointLatticeTriclinic(int scaledSize, double minAllowedDistance,
                                          KPointLattice &bestKnownLattice, int scaleFactor);

  /*
   * The actual grid generation function for lattices other than triclinic.
   *
   * @param scaledSize                The size of the k-point grids to be searched for.
   * @param minAllowedScaledDistance  The minimum allowed distance between any points on
   *                                  superlattices.
   * @param bestKnownLattice          The best grid found so far.
   * @param scaleFactor               Kept here as an option to scale structures when
   *                                  there is a maximum search depth. By "scale structures",
   *                                  see section II.D of our first paper:
   *                      https://journals.aps.org/prb/abstract/10.1103/PhysRevB.93.155109.
   */
  KPointLattice getKPointLatticeOrthogonal(int scaledSize, double minAllowedScaledDistance,
                                           KPointLattice &bestKnownLattice, int scaleFactor);

  /*
   * Get the number of symmetrically irreducible k-points of the input grid. Note: to get the
   * k-point coordinates after found the best grid, use KPointLattice::getKPointsCoordinates().
   * The implementations of the two are pretty similar, though.
   *
   * @param superToDirect   The real-space transformation matrix in Hermite Normal Form.
   * @param shiftArray      Shift vector of the gamma point in the basis of reciprocal primitive
   *                        vectors.
   * @return The number of symmetrically irreducible k-points in this grid.
   */
  int numDistinctKPoints(const Tensor<int> &superToDirect,
                         const std::vector<double> &shiftArray);

  /**
   * It applies Minkowski reduction to calculation the minimum periodic distances in superlattices.
   */
  static double getMinDistance(std::vector<std::vector<double> > superVectors, const int numDimensions);

  // Transform a matrix to its Hermite Normal Form. For the definition of HNF, see our paper.
  static void toHermiteNormalForm(std::vector<std::vector<int> > &superToDirect);
  static void toHermiteNormalForm(int size, int *superToDirect);

  /**
   * A quick way to determine the rectangular coordinates of a lattice point
   * relative to the location of corresponding lattice point in the SuperLattice.
   * Assumes superToDirect is in Hermite Normal Form.
   *
   * @param primCellLocation
   * @param superToDirect     Transformation matrix in Hermite Normal Form.
   */
  static void getInnerPrimCell(int *primCellLocation,
                               const Tensor<int> &superToDirect);

  /**
   * Determine whether the superlattice defined by the superToDirect matrix is symmetry preserving.
   * This works in any dimensions.
   *
   * @param superToDirect   Transformation matrix in Hermite Normal Form.
   * @param pointOperators  The point operations to be checked.
   */
  static bool isSymmetryPreserving(const Tensor<int> &superToDirect,
                                   const std::vector<Tensor<int> > &pointOperators);

  std::vector<Tensor<int> > getSymPreservingLattices2D(int size);

  bool isTriclinic();
  static bool isInverse(const Tensor<int> &operation);
  static bool isIdentity(const Tensor<int> &operation);

  // To grant access to point operators and some utility functions, e.g. toHermiteNormalForm().
  friend class KPointLattice;

public:

  // Wrapper function of the corresponding private functions.
  KPointLatticeGenerator(const double primVectorsArray[3][3],
                         const double conventionalVectorsArray[3][3],
                         const int latticePointOperatorsArray[][3][3],
                         const int numOperators,
                         const bool isConventionalHexagonal);
  
  // C++ version of the constructor
  KPointLatticeGenerator(Tensor<double> primVectors,
                         Tensor<double> conventionalVectors,
                         std::vector<Tensor<int>> latticePointOperators,
                         const bool isConventionalHexagonal);

  /*
   * Wrapper function of the private getKPointLattice(). This is the function that users should call
   * when using this interface. This only requires the minimum inputs from users.
   *
   * @param minDistance The minimum distance between any lattice points on superlattices.
   *                    The superlattice corresponding to the returned grid should have at least
   *                    a periodic distance of this value.
   * @param minSize     The minimum size of k-point grids.
   * @return            The best grid from our exhaustive search.
   */
  KPointLattice getKPointLattice(const double minDistance, const int minSize);

  /*
   * Generate gamma-centered grids or shifted grids.
   */
  void includeGamma(INCLUDE_GAMMA includeGamma);

  /*
   * Optional functionality.
   *
   * This function activates the scale factor functionality. It sets a finite value of
   * m_MaxAllowedKPoints. When the requested grid size exceeds m_MaxAllowedKPoints, the code
   * tries to find a superlattice with minimum periodic distance < MINDISTANCE / scale factor.
   * Currently, 3 is the maximum allowed scaling factor.
   *
   * The space group number is required since the maximum allowed k-points for different
   * crystal systems are different. If user changes the code to set a uniform search depth, then
   * he doesn't need the space group number in this function.
   *
   * @param spaceGroupNum 1-230. Note: it should be the group number after symmetry is adjusted.
   *                             For example, if all structural symmetries are removed, the space
   *                             group should be changed to triclinic. The space group number will
   *                             be 2 if it has inversion, and 1 otherwise.
   */
  void useScaleFactor(int spaceGroupNum);
};

#endif // KPOINTLATTICEGENERATOR_H
