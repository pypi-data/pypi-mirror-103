#include "kPointLatticeGenerator.h"
#include "kPointLattice.h"
#include <vector>
#include <limits>

void KPointLattice::findDistinctKPoints() {
  if (m_SuperToDirect.empty()) {
    return;
  }
  m_DistinctKPointMap = std::vector<int>(numTotalKPoints());

  // Get the matrix representation of the point operators in the basis of
  // reciprocal primitive lattice vectors.
  Tensor<double> recipSTD = MSMath::simpleLowerTriangularInverse(m_SuperToDirect);
  for (int opNum = 0; opNum < (int) m_Parent->m_KPointOperators.size(); opNum++) {
    Tensor<int> opInverse = MSMath::matrixMultiply<int, int, int>(
        m_SuperToDirect, m_Parent->m_PointOperators3D[opNum]);
    m_Parent->m_KPointOperators[opNum] =
        MSMath::rounded(MSMath::matrixMultiply<double, int, double>(opInverse, recipSTD));
  }

  Tensor<int> kPointCanonical = MSMath::transpose(m_SuperToDirect);
  KPointLatticeGenerator::toHermiteNormalForm(kPointCanonical);

  double shiftedPoint[3] = {0, 0, 0};
  int mappedPointIntArray[3] = {0, 0, 0};

  //Iterate over x first, then y and z.
  for (int k = 0; k < kPointCanonical[2][2]; k++) {
    for (int j = 0; j < kPointCanonical[1][1]; j++) {
      for (int i = 0; i < kPointCanonical[0][0]; i++) {
        int currKPoint[3] = {i, j, k};
        int currIndex = currKPoint[0]
                      + currKPoint[1] * kPointCanonical[0][0]
                      + currKPoint[2] * kPointCanonical[0][0] * kPointCanonical[1][1];

        int minMappedIndex = std::numeric_limits<int>::max();
        for (int opNum = 0; opNum < (int) m_Parent->m_KPointOperators.size();
            opNum++) {
          for (int dimNum = 0; dimNum < 3; dimNum++) {
            shiftedPoint[dimNum] = currKPoint[dimNum] + m_Shift[dimNum];
          }

          // Putting the vector last is faster than taking a transpose of the operators.
          double mappedPoint[3] = {0, 0, 0};
          MSMath::matrixTimesVector(m_Parent->m_KPointOperators[opNum], shiftedPoint, mappedPoint);
          for (int dimNum = 0; dimNum < 3; dimNum++) {
            double newCoord = mappedPoint[dimNum] - m_Shift[dimNum];
            if (fabs(newCoord - round(newCoord)) > 1E-2) { // Not symmetry preserving
              throw "Invalid KPointLattice was created.";
            }
            mappedPointIntArray[dimNum] = (int)round(newCoord);
          }

          KPointLatticeGenerator::getInnerPrimCell(mappedPointIntArray, kPointCanonical);
          int mappedIndex = mappedPointIntArray[0]
                          + mappedPointIntArray[1] * kPointCanonical[0][0]
                          + mappedPointIntArray[2] * kPointCanonical[0][0] * kPointCanonical[1][1];
          minMappedIndex = std::min(minMappedIndex, mappedIndex);
        }
        m_DistinctKPointMap[currIndex] = minMappedIndex;
      }
    }
  }

  return;
}

Tensor<double> KPointLattice::getKPointCoordinates() {
  if (m_SuperToDirect.empty()) {
    return Tensor<double> ();
  } else if (m_DistinctKPointMap.size() == 0) {
    findDistinctKPoints();
  }

  Tensor<double> returnArray(numTotalKPoints(), std::vector<double>());
  Tensor<int> kPointCanonical = MSMath::transpose<int>(m_SuperToDirect);
  KPointLatticeGenerator::toHermiteNormalForm(kPointCanonical);

  // Reciprocal primitive lattice vectors in the basis of the reciprocal superLattice.
  Tensor<double> recipPrimLatticeVectors =
      MSMath::transpose(MSMath::simpleLowerTriangularInverse(m_SuperToDirect));
  int returnIndex = 0;

  // k-point coordinates in the basis of primitive lattice and superlattice vectors.
  // Avoid repetitive allocation.
  std::vector<double> coordPrim(3, 0);
  std::vector<double> coordSuper(3, 0);
  // The sequence of iteration should be the same as the findDistinctKPoints.
  for (int k = 0; k < kPointCanonical[2][2]; k++) {
    for (int j = 0; j < kPointCanonical[1][1]; j++) {
      for (int i = 0; i < kPointCanonical[0][0]; i++) {
        coordPrim[0] = i + m_Shift[0];
        coordPrim[1] = j + m_Shift[1];
        coordPrim[2] = k + m_Shift[2];
        /*
         * Note: we should use the m_SuperToDirect to get the coordinates,
         *       since kPointCanonical defines a different reciprocal lattice.
         */
        MSMath::vectorTimesMatrix(coordPrim, recipPrimLatticeVectors, coordSuper);
        for (int dim = 0; dim < (int) coordSuper.size(); dim++) {
          coordSuper[dim] = coordSuper[dim] - std::floor(coordSuper[dim]);
        }
        // Use copy constructor. Don't pass references.
        returnArray[returnIndex] = std::vector<double>(coordSuper.begin(), coordSuper.end());
        returnIndex++;
      }
    }
  }

  return returnArray;
}

std::vector<int> KPointLattice::getKPointWeights() {
  if (m_SuperToDirect.empty()) {
    return std::vector<int>();
  } else if (m_DistinctKPointMap.size() == 0) {
    findDistinctKPoints();
  }

  std::vector<int> weights = std::vector<int>(numTotalKPoints(), 0);
  for (int i = 0; i < numTotalKPoints(); i++) {
    weights[m_DistinctKPointMap[i]]++;
  }
  return weights;
}

int KPointLattice::numTotalKPoints() {
  return (m_SuperToDirect.empty()) ? -1 : MSMath::determinant(m_SuperToDirect);
}
