#ifndef SRC_KPOINTLATTICE_H_
#define SRC_KPOINTLATTICE_H_

#include "msmath.h"
#include <vector>

class KPointLatticeGenerator; // Forward declaration to solve circular dependency.

/**
 * This is a class for holding data about the best k-point grid the algorithm has found so far.
 */
class KPointLattice {

private:
  // The real-space transformation matrix.
  Tensor<int> m_SuperToDirect;

  // The number of symmetrically irreducible k-points of the grid.
  int m_NumDistinctKPoints;

  // The minimum distance between any two lattice points on the corresponding superlattice.
  double m_MinPeriodicDistance;

  // Shift vector of the gamma point in the basis of primitive lattice vectors.
  std::vector<double> m_Shift;

  // To access the point operations in the KPointLatticeGenerator.
  KPointLatticeGenerator *m_Parent;

  // A map of the indices of the distinct k-points in the coordinates and the weights array.
  std::vector<int> m_DistinctKPointMap;

  /*
   * The function to identify the symmetrically irreducible k-points. The algorithm is similar to
   * that of KPointLatticeGenerator::numDistinctKPoints.
   */
  void findDistinctKPoints();

public:

  /**
   * Constructor.
   *
   * @param superToDirect   Real-space transformation matrix in Hermite Normal Form.
   * @param shift           Shift vector in the basis of generating vectors, i.e. reciprocal
   *                        primitive lattice vectors.
   * @param numDistinctKPoints
   * @param minDistance     Minimum distance between any points on the superlattice corresponding
   *                        to this k-point grid.
   */

  KPointLattice() {}
  
  KPointLattice(Tensor<int> superToDirect, std::vector<double> shift,
      int numDistinctKPoints, double minDistance, KPointLatticeGenerator *parent) {
    m_SuperToDirect = superToDirect;
    m_Shift = shift;
    m_NumDistinctKPoints = numDistinctKPoints;
    m_MinPeriodicDistance = minDistance;
    m_Parent = parent;  // To access the point group operators;
    m_DistinctKPointMap = std::vector<int>();
  }

  // Straight forward query functions.
  Tensor<int> getSuperToDirect() { return m_SuperToDirect; }
  std::vector<double> getShift() { return m_Shift; }
  double getMinPeriodicDistance() { return m_MinPeriodicDistance; }
  int getNumDistinctKPoints() { return m_NumDistinctKPoints; }
  int numTotalKPoints();

  /*
   * Get k-point coordinates of all k-points in the basis of reciprocal lattice vectors.
   * The coordinates of the symmetrically irreducible ones can be picked out by checking the
   * weights array. The distinct ones have weights larger than zero.
   *
   * @return Array of fractional coordiantes for all k-points.
   */
  Tensor<double> getKPointCoordinates();

  /*
   * A weight of zero indicates the corresponding point is not symmetrically distinct.
   *
   * @return An array of weights for the corresponding k-points.
   */
  std::vector<int> getKPointWeights();
};

#endif /* SRC_KPOINTLATTICE_H_ */
