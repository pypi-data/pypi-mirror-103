#include <cmath>
#include <cstdlib>
#include <iostream>

#include "kPointLatticeGenerator.h"
#include "msmath.h"

/**
 * Users can get all of the arguments from a SpaceGroup object, but this is more general.
 *
 * @param primVectorsArray
 * @param conventionalVectorsArray The third vector should be orthogonal to the first two.
 * @param latticePointOperatorsArray
 * @param numOperators
 * @param isConventionalHexagonal
 */
KPointLatticeGenerator::KPointLatticeGenerator(const double primVectorsArray[3][3],
                                               const double conventionalVectorsArray[3][3],
                                               const int latticePointOperatorsArray[][3][3],
                                               const int numOperators,
                                               const bool isConventionalHexagonal) {

  const int Ndim = 3;
  Tensor<double> primVectors(Ndim, std::vector<double>(Ndim, 0));
  Tensor<double> conventionalVectors(Ndim, std::vector<double>(Ndim, 0));
  std::vector<Tensor<int>> latticePointOperators(numOperators,
                                                 Tensor<int>(Ndim, std::vector<int>(Ndim, 0)));

  for (int i = 0; i < Ndim; i++) {
    for (int j = 0; j < Ndim; j++) {
      primVectors[i][j] = primVectorsArray[i][j];
      conventionalVectors[i][j] = conventionalVectorsArray[i][j];
    }
  }

  for (int n = 0; n < numOperators; n++) {
    for (int i = 0; i < Ndim; i++) {
      for (int j = 0; j < Ndim; j++) {
        latticePointOperators[n][i][j] = latticePointOperatorsArray[n][i][j];
      }
    }
  }
    KPointLatticeGenerator(primVectors,conventionalVectors,latticePointOperators,isConventionalHexagonal);
}

/**
 * Users can get all of the arguments from a SpaceGroup object, but this is more general.
 *
 * @param primVectors
 * @param conventionalVectors The third vector should be orthogonal to the first two.
 * @param latticePointOperators
 * @param isConventionalHexagonal
 */
KPointLatticeGenerator::KPointLatticeGenerator(Tensor<double> primVectors,
                                               Tensor<double> conventionalVectors,
                                               std::vector<Tensor<int>> latticePointOperators,
                                               const bool isConventionalHexagonal) {

  static const double hexagonal2DShifts[9][2] = {
      {0, 0},
      {1.0 / 3, 1.0 / 3},
      {2.0 / 3, 2.0 / 3},
      {1.0 / 3, 2.0 / 3},
      {2.0 / 3, 1.0 / 3},
      {0, 1.0 / 3},
      {1.0 / 3, 0},
      {0, 2.0 / 3},
      {2.0 / 3, 0},
  };

  static const double other2DShifts[4][2] = {
      {0, 0},
      {0, 0.5},
      {0.5, 0},
      {0.5, 0.5},
  };

  m_Hexagonal2DShifts.resize(9, std::vector<double>(2,0.0));
  for (int i = 0; i < 9; ++i) {
    m_Hexagonal2DShifts[i][0] = hexagonal2DShifts[i][0];
    m_Hexagonal2DShifts[i][1] = hexagonal2DShifts[i][1];
  }

  m_Other2DShifts.resize(4, std::vector<double>(2, 0.0));
  for (int i = 0; i < 4; ++i) {
    m_Other2DShifts[i][0] = other2DShifts[i][0];
    m_Other2DShifts[i][1] = other2DShifts[i][1];
  }

  m_PointOperators3D = latticePointOperators;
  // Make it global to save the dynamic allocation;
  m_KPointOperators = std::vector<Tensor<int> >(m_PointOperators3D.size(), Tensor<int>());

  m_PrimVectors = primVectors;
  m_CartesianToPrim = MSMath::simpleInverse(primVectors);
  m_PrimCellSize = fabs(MSMath::determinant(primVectors));

  // Check to see if we have a face-centered 2D lattice. We need to work with
  // the primitive 2D lattice.
  std::vector<double> faceCenter = MSMath::arrayAdd(conventionalVectors[0], conventionalVectors[1]);
  std::vector<double> directFaceCenter(3, 0);
  MSMath::vectorTimesMatrix(faceCenter, m_CartesianToPrim, directFaceCenter);
  bool isLatticePoint = true;
  for (int dimNum = 0; dimNum < (int) directFaceCenter.size(); dimNum++) {
    int coord = static_cast<int>(MSMath::round(directFaceCenter[dimNum]));
    isLatticePoint &= (coord % 2 == 0);
  }
  if (isLatticePoint) {
    conventionalVectors[0] = MSMath::arrayDivide(faceCenter, 2);
    conventionalVectors[1] = MSMath::arraySubtract(conventionalVectors[0], conventionalVectors[1]);
  }
  m_ConventionalVectors = conventionalVectors;

  if (isConventionalHexagonal) {
    m_Shifts2D = m_Hexagonal2DShifts;
  } else {
    m_Shifts2D = m_Other2DShifts;
  }

  Tensor<double> conventionalToPrim =
      MSMath::matrixMultiply<double, double, double>(conventionalVectors, m_CartesianToPrim);
  Tensor<double> primToConventional = MSMath::simpleInverse(conventionalToPrim);

  // Get the two-dimensional point operations.
  std::vector<Tensor<int> > ops2D(m_PointOperators3D.size(), Tensor<int>());

  // First we get all of the lattice operations in the coordinates of the conventional
  // lattice vectors.
  int keeperIndex = 0;
  for (int opNum = 0; opNum < (int) m_PointOperators3D.size(); opNum++) {
    Tensor<int> op = m_PointOperators3D[opNum];
    Tensor<double> conventionalOp = MSMath::matrixMultiply<double, double, int>(conventionalToPrim,
                                                                                op);
    conventionalOp = MSMath::matrixMultiply<double, double, double>(conventionalOp,
                                                                    primToConventional);
    if (MSMath::round(conventionalOp[0][2]) != 0) {
      continue;
    }
    if (MSMath::round(conventionalOp[1][2]) != 0) {
      continue;
    }
    if (MSMath::round(conventionalOp[2][0]) != 0) {
      continue;
    }
    if (MSMath::round(conventionalOp[2][1]) != 0) {
      continue;
    }

    int op2Darr[2][2] = {
        {static_cast<int>(MSMath::round(conventionalOp[0][0])),
         static_cast<int>(MSMath::round(conventionalOp[0][1]))},
        {static_cast<int>(MSMath::round(conventionalOp[1][0])),
         static_cast<int>(MSMath::round(conventionalOp[1][1]))}};

    Tensor<int> op2D(2, std::vector<int>(2, 0));

    for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 2; j++) {
        op2D[i][j] = op2Darr[i][j];
      }
    }

    bool match = false;
    for (int prevOpNum = 0; prevOpNum < keeperIndex; prevOpNum++) {
      Tensor<int> prevOp = ops2D[prevOpNum];
      match |= (prevOp == op2D);
      if (match) {
        break;
      }
    }
    if (match) {
      continue;
    }
    ops2D[keeperIndex++] = op2D;
  }

  m_NumConventionalPrimCells = fabs(MSMath::determinant(conventionalToPrim)); // maxLayers;
  m_MaxZDistance = MSMath::magnitude(conventionalVectors[2]) / m_NumConventionalPrimCells
      * (isConventionalHexagonal ? 3 : 2);  // 3 is for rhombohedral in primitive hexagonal;
  m_PointOperators2D = ops2D;
  m_PointOperators2D.resize(keeperIndex);
}

void KPointLatticeGenerator::useScaleFactor(int spaceGroupNum) {
  m_MaxScaleFactor = 3;
  if (spaceGroupNum >0 && spaceGroupNum <= 2) {
    m_MaxAllowedKPoints = 729;   // Triclinic;
  } else if (spaceGroupNum >= 3 && spaceGroupNum <= 15) {
    m_MaxAllowedKPoints = 1728;  // Monoclinic;
  } else if (spaceGroupNum >= 16 && spaceGroupNum <= 194) {
    m_MaxAllowedKPoints = 5832;  // Orthorhombic, Tetragonal, Trigonal, Hexagonal;
  } else if (spaceGroupNum >=195 && spaceGroupNum <= 230){
    m_MaxAllowedKPoints = 46656; // Cubic;
  }
}

/*
 * Wrapper function of the private getKPointLattice function to disable the scaleFactor for now,
 * but keep the option.
 */
KPointLattice KPointLatticeGenerator::getKPointLattice(const double minDistance, const int minSize) {

  for (int scaleFactor = 1; scaleFactor <= m_MaxScaleFactor; scaleFactor++) {
    double minScaledDistance = minDistance / scaleFactor;
    int minScaledTotalKPoints = (int) ceil(minSize / pow(scaleFactor, 3));
    KPointLattice lattice = getKPointLattice(minScaledDistance, minScaledTotalKPoints,
        m_MaxAllowedKPoints, scaleFactor);
    if (lattice.getNumDistinctKPoints() == std::numeric_limits<int>::max() ) {
      continue; // Couldn't find a valid grid up to m_MaxAllowedKPoints in this loop.
    }
    if (scaleFactor > 1) { std::cout << "Scale factor is used: " << scaleFactor << ". "; }
    return lattice;
  }

  // No valid grid can be found with sizes smaller than m_MaxAllowedKPoints *  m_MaxScaleFactor^3.
  return KPointLattice(Tensor<int>(), std::vector<double>(), std::numeric_limits<int>::max(), 0, this);
}

KPointLattice KPointLatticeGenerator::getKPointLattice(double minDistance, int minSize, int maxSize,
    int scaleFactor) {
  KPointLattice bestKnownLattice = KPointLattice(Tensor<int>(), std::vector<double>(),
                                                 std::numeric_limits<int>::max(), 0, this);

  // We can't do better than fcc packing.
  int minSizeByDistance = static_cast<int>(
      floor(minDistance * minDistance * minDistance / (m_PrimCellSize * sqrt(2))));
  minSize = std::max(minSize, minSizeByDistance);


  for (int scaledSize = minSize; scaledSize <= maxSize; scaledSize++) {
    if (isTriclinic()) {
      bestKnownLattice = getKPointLatticeTriclinic(scaledSize, minDistance,
          bestKnownLattice, scaleFactor);
    } else {
      bestKnownLattice = getKPointLatticeOrthogonal(scaledSize, minDistance,
          bestKnownLattice, scaleFactor);
    }
    if (bestKnownLattice.getNumDistinctKPoints() == std::numeric_limits<int>::max()) {
      continue;
    }
    maxSize = bestKnownLattice.getNumDistinctKPoints() * m_PointOperators3D.size();
    maxSize = static_cast<int>(floor(1.0 * maxSize / pow(scaleFactor, 3)));
  }

  return bestKnownLattice;
}

KPointLattice KPointLatticeGenerator::getKPointLatticeTriclinic(int scaledSize,
    double minAllowedScaledDistance, KPointLattice &bestKnownLattice, int scaleFactor) {

  bool includeGamma = (m_KPointShifts.size() != 7);
  if (!includeGamma && ((scaledSize * scaleFactor * scaleFactor * scaleFactor)
      % m_PointOperators3D.size() != 0)) {
    return bestKnownLattice;
  }
  double minAllowedDistance = minAllowedScaledDistance * scaleFactor;

  // Figure out what the minimum possible number of k-points is.
  int gammaFactor = (m_KPointShifts.size() == 1) ? 1 : 0;
  int minPossibleKPoints = static_cast<int>(ceil((scaledSize * scaleFactor * scaleFactor *
      scaleFactor - gammaFactor) / (1.0 + m_PointOperators3D.size()))) + gammaFactor;

  if (minPossibleKPoints > bestKnownLattice.getNumDistinctKPoints()) {
    return bestKnownLattice;
  }

  // Loop over all possible superlattices.
  Tensor<int> factorSets = MSMath::getFactorSets(scaledSize, 3);
  Tensor<double> superVectors(3, std::vector<double>(3, 0));
  Tensor<int> superToDirect(3, std::vector<int>(3, 0));

  for (int setNum = 0; setNum < (int) factorSets.size(); setNum++) {
    std::vector<int> &factors = factorSets[setNum];
    for (int i = 0; i < 3; i++) {
      superToDirect[i][i] = factors[i] * scaleFactor;
    }

    MSMath::vectorTimesMatrix(superToDirect[0], m_PrimVectors, superVectors[0]);
    if (MSMath::magnitude(superVectors[0]) < minAllowedDistance) {
      continue;
    }

    for (int ba = 0; ba < factors[0]; ba++) {
      superToDirect[1][0] = ba * scaleFactor;
      MSMath::vectorTimesMatrix(superToDirect[1], m_PrimVectors, superVectors[1]);
      if (getMinDistance(superVectors, 2) < minAllowedDistance) {
        continue;
      }

      for (int ca = 0; ca < factors[0]; ca++) {
        superToDirect[2][0] = ca * scaleFactor;
        for (int cb = 0; cb < factors[1]; cb++) {
          superToDirect[2][1] = cb * scaleFactor;
          MSMath::vectorTimesMatrix(superToDirect[2], m_PrimVectors, superVectors[2]);
          if (MSMath::magnitude(superVectors[2]) < minAllowedDistance) {
            continue;
          }
          double minDistance = getMinDistance(superVectors, 3);
          if (minDistance < minAllowedDistance) {
            continue;
          }

          // Compare this valid lattice with bestKnownLattice.
          if (bestKnownLattice.getNumDistinctKPoints() == minPossibleKPoints
              && minDistance < bestKnownLattice.getMinPeriodicDistance()) {
            continue;
          }

          int numTotalKPoints = MSMath::determinant(superToDirect);

          for (int shiftNum = 0; shiftNum < (int) m_KPointShifts.size(); shiftNum++) {
            std::vector<double> &shift = m_KPointShifts[shiftNum];
            int numDistinctKPointsVal = (m_PointOperators3D.size() == 1)
            							             ? numTotalKPoints
            							             : numDistinctKPoints(superToDirect, shift);
            if (numDistinctKPointsVal < bestKnownLattice.getNumDistinctKPoints()) {
              bestKnownLattice = KPointLattice(superToDirect, shift, numDistinctKPointsVal,
                                               minDistance, this);
            } else if (numDistinctKPointsVal == bestKnownLattice.getNumDistinctKPoints()
                    && minDistance > bestKnownLattice.getMinPeriodicDistance()) {
              bestKnownLattice = KPointLattice(superToDirect, shift, numDistinctKPointsVal,
                                               minDistance, this);
            } else if (numDistinctKPointsVal == bestKnownLattice.getNumDistinctKPoints()
                    && minDistance == bestKnownLattice.getMinPeriodicDistance()
                    && numTotalKPoints > bestKnownLattice.numTotalKPoints()) {
              bestKnownLattice = KPointLattice(superToDirect, shift, numDistinctKPointsVal,
                                               minDistance, this);
            }
            if (numDistinctKPointsVal == minPossibleKPoints) { break; }
          }
        }
      }
    }
  }
  return bestKnownLattice;
}

KPointLattice KPointLatticeGenerator::getKPointLatticeOrthogonal(int scaledSize,
    double minAllowedScaledDistance, KPointLattice &bestKnownLattice, int scaleFactor) {

  // First we generate the 2D lattices
  std::vector<int> factors = MSMath::factor(scaledSize);

  // We don't have to repeatedly dynamically allocate memory in each loop.
  Tensor<double> superVectors(3, std::vector<double>(3, 0));
  Tensor<int> superToDirect(3, std::vector<int>(3, 0));
  for (int factorNum = (int) factors.size() - 1; factorNum >= 0; factorNum--) {
    int factor = factors[factorNum];
    if ((factor * m_MaxZDistance) < minAllowedScaledDistance) {
      continue;
    }
    std::vector<Tensor<int> > lattices2D = getSymPreservingLattices2D(scaledSize / factor);
    for (int latticeNum = 0; latticeNum < (int) lattices2D.size(); latticeNum++) {

      Tensor<int> &lattice2D = lattices2D[latticeNum];
      for (int dimNum = 0; dimNum < 3; dimNum++) {
        superVectors[0][dimNum] = m_ConventionalVectors[0][dimNum] * lattice2D[0][0] +
                                  m_ConventionalVectors[1][dimNum] * lattice2D[0][1];
        superVectors[1][dimNum] = m_ConventionalVectors[0][dimNum] * lattice2D[1][0] +
                                  m_ConventionalVectors[1][dimNum] * lattice2D[1][1];
      }
      if (getMinDistance(superVectors, 2) < minAllowedScaledDistance) {
        continue;
      }
      /**
       * Now we shift the relative layers of the stacked 2D lattices and
       * evaluate the resulting 3D lattice.
       */
      for (int shiftNum = 0; shiftNum < (int) m_Shifts2D.size(); shiftNum++) {

        std::vector<double> shift = m_Shifts2D[shiftNum];
        for (int dimNum = 0; dimNum < 3; dimNum++) {
          superVectors[2][dimNum] = superVectors[0][dimNum] * shift[0] +
                                    superVectors[1][dimNum] * shift[1] +
                                    m_ConventionalVectors[2][dimNum] * (factor / m_NumConventionalPrimCells);
        }

        Tensor<double> superToDirectDouble =
            MSMath::matrixMultiply<double, double, double> (superVectors, m_CartesianToPrim);

        bool allInts = true;
        // Check whether the transformation matrix is integral. If there are non-integral elements,
        // this shift vector doesn't create a valid superlattice.
        for (int rowNum = 0; rowNum < (int) superToDirect.size(); rowNum++) {
          std::vector<double> &rowDouble = superToDirectDouble[rowNum];
          std::vector<int> &row = superToDirect[rowNum];
          for (int colNum = 0; colNum < (int) row.size(); colNum++) {
            row[colNum] = static_cast<int>(MSMath::round(rowDouble[colNum]));
            double delta = fabs(row[colNum] - rowDouble[colNum]);
            allInts &= (delta < 1E-2);
          }
        }
        if (!allInts) {
          continue;
        }

        double minDistance = getMinDistance(superVectors, 3);
        if (minDistance < minAllowedScaledDistance) {
          continue;
        }

        // This is the simplest way to take care of the scale factor.
        for (int rowNum = 0; rowNum < (int) superToDirect.size(); rowNum++) {
          for (int colNum = 0; colNum < (int) superToDirect[rowNum].size(); colNum++) {
            superToDirect[rowNum][colNum] *= scaleFactor;
          }
        }
        minDistance *= scaleFactor;

        toHermiteNormalForm(superToDirect);

        if (!isSymmetryPreserving(superToDirect, m_PointOperators3D)) {
          continue;
        }

        for (int kPointShiftNum = 0; kPointShiftNum < (int) m_KPointShifts.size(); kPointShiftNum++) {
          std::vector<double> &kPointShift = m_KPointShifts[kPointShiftNum];
          int numTotalKPoints = MSMath::determinant(superToDirect);
          int numDistinctKPointsVal = numDistinctKPoints(superToDirect, kPointShift);

          // Compare the new lattice with found lattice.
          // 1. Favor less distinct k-points;
          // 2. Favor larger periodic distance;
          // 3. Favor more total k-points;
          if (numDistinctKPointsVal > bestKnownLattice.getNumDistinctKPoints()) {
            continue;
          } else if (numDistinctKPointsVal == bestKnownLattice.getNumDistinctKPoints()) {
            // Numerical errors sometimes happens
            if (minDistance + PRECISION < bestKnownLattice.getMinPeriodicDistance()) { continue; }
            if (fabs(minDistance - bestKnownLattice.getMinPeriodicDistance()) < PRECISION
                && numTotalKPoints <= bestKnownLattice.numTotalKPoints()) { continue; }
          }

          bestKnownLattice = KPointLattice(superToDirect, kPointShift, numDistinctKPointsVal,
                                           minDistance, this);
        }
      }
    }
  }

  return bestKnownLattice;
}

bool KPointLatticeGenerator::isTriclinic() {
  if (m_PointOperators3D.size() > 2) {
    return false;
  }
  for (int opNum = 0; opNum < (int) m_PointOperators3D.size(); opNum++) {
    if (!(isInverse(m_PointOperators3D[opNum]) || isIdentity(m_PointOperators3D[opNum]))) {
      return false;
    }
  }
  return true;
}

bool KPointLatticeGenerator::isInverse(const Tensor<int> &operation) {
  int trace = operation[0][0] + operation[1][1] + operation[2][2];
  if (trace == -3) {
    return true;
  }
  return false;
}

bool KPointLatticeGenerator::isIdentity(const Tensor<int> &operation) {
  int trace = operation[0][0] + operation[1][1] + operation[2][2];
  if (trace == 3) {
    return true;
  }
  return false;
}

void KPointLatticeGenerator::includeGamma(INCLUDE_GAMMA includeGamma) {

  if (includeGamma == TRUE) {
    static const double kPointShiftsMat[][3] = {{0, 0, 0}};
    m_KPointShifts = Tensor<double> (1, std::vector<double>(3,0));
    for (int i = 0; i < 1; ++i) {
      for (int j = 0; j < 3; j++) {
        m_KPointShifts[i][j] = kPointShiftsMat[i][j];
      }
    }
  } else if (includeGamma == AUTO) {
    static const double kPointShiftsMat[][3] = {
        {0, 0, 0},     {0, 0, 0.5},   {0, 0.5, 0},   {0.5, 0, 0},
        {0.5, 0.5, 0}, {0.5, 0, 0.5}, {0, 0.5, 0.5}, {0.5, 0.5, 0.5},
    };
    m_KPointShifts = Tensor<double> (8, std::vector<double>(3,0));
    for (int i = 0; i < 8; ++i) {
      for (int j = 0; j < 3; j++) {
        m_KPointShifts[i][j] = kPointShiftsMat[i][j];
      }
    }
  } else if (includeGamma == FALSE) {
    static const double kPointShiftsMat[][3] = {
        {0, 0, 0.5},   {0, 0.5, 0},   {0.5, 0, 0},     {0.5, 0.5, 0},
        {0.5, 0, 0.5}, {0, 0.5, 0.5}, {0.5, 0.5, 0.5},
    };
    m_KPointShifts = Tensor<double> (7, std::vector<double>(3,0));
    for (int i = 0; i < 7; ++i) {
      for (int j = 0; j < 3; j++) {
        m_KPointShifts[i][j] = kPointShiftsMat[i][j];
      }
    }
  }


}

/**
 * This is one of the most expensive operations. I try to make it fast by
 * pre-calculating the operators, but it still takes some time.
 */
int KPointLatticeGenerator::numDistinctKPoints(const Tensor<int> &superToDirect,
    const std::vector<double> &shiftArray) {

  // Apply the operation in k-space
  Tensor<double> recipSTD = MSMath::simpleLowerTriangularInverse(superToDirect);

  for (int opNum = 0; opNum < (int) m_KPointOperators.size(); opNum++) {
    Tensor<int> opInverse = MSMath::matrixMultiply<int, int, int>(superToDirect,
                                                                  m_PointOperators3D[opNum]);
    m_KPointOperators[opNum] = MSMath::rounded(
        MSMath::matrixMultiply<double, int, double>(opInverse, recipSTD));
  }

  Tensor<int> kPointCanonical = MSMath::transpose(superToDirect);
  toHermiteNormalForm(kPointCanonical);

  int numDistinctKPoints = 0;
  int currKPoint[3] = {0, 0, 0};
  double shiftedPoint[3] = {0, 0, 0};
  int mappedPointIntArray[3] = {0, 0, 0};

  int mappedIndex = -1;

  for (int k = 0; k < kPointCanonical[2][2]; k++) {
    for (int j = 0; j < kPointCanonical[1][1]; j++) {
      for (int i = 0; i < kPointCanonical[0][0]; i++) {
        currKPoint[0] = i; currKPoint[1] = j; currKPoint[2] = k;

        int currIndex = currKPoint[0]
                      + currKPoint[1] * kPointCanonical[0][0]
                      + currKPoint[2] * kPointCanonical[0][0] * kPointCanonical[1][1] ;

        for (int opNum = 0; opNum < (int) m_KPointOperators.size(); opNum++) {
          for (int dimNum = 0; dimNum < 3; dimNum++) {
            shiftedPoint[dimNum] = currKPoint[dimNum] + shiftArray[dimNum];
          }

          // Putting the vector last is faster than taking the transpose of the operations.
          double mappedPoint[3] = {0, 0, 0};
          MSMath::matrixTimesVector(m_KPointOperators[opNum], shiftedPoint, mappedPoint);

          for (int dimNum = 0; dimNum < 3; dimNum++) {
            double newCoord = mappedPoint[dimNum] - shiftArray[dimNum];
            if (fabs(newCoord - MSMath::round(newCoord)) > 1E-2) { // Not symmetry preserving
              return std::numeric_limits<int>::max();
            }
            mappedPointIntArray[dimNum] = static_cast<int>(MSMath::round(newCoord));
          }
          getInnerPrimCell(mappedPointIntArray, kPointCanonical);
          mappedIndex = mappedPointIntArray[0]
                      + mappedPointIntArray[1] * kPointCanonical[0][0]
                      + mappedPointIntArray[2] * kPointCanonical[0][0] * kPointCanonical[1][1] ;
          if (mappedIndex < currIndex) {
            break;
          }
        }

        if (mappedIndex >= currIndex) {
          numDistinctKPoints++;
        }
      }
    }
  }

  return numDistinctKPoints;
}

void KPointLatticeGenerator::getInnerPrimCell(int* primCellLocation,
                                              const Tensor<int> &canonicalMatrix) {
  for (int i = (int) canonicalMatrix.size()-1; i >= 0; i--) {
    //int quotient = MSMath::divFloor(primCellLocation[i], canonicalMatrix[i][i]);
    int quotient = primCellLocation[i] / canonicalMatrix[i][i] + (primCellLocation[i] % canonicalMatrix[i][i] < 0) * -1;
    // Take modulo of the matrix row vectors
    for (int j = (int) canonicalMatrix.size()-1; j >= 0; j--) {
      primCellLocation[j] -= quotient * canonicalMatrix[i][j];
    }
  }
}

/**
 * Checks to see if a given superlattice preserves symmetry by applying symmetry
 * operations to it and comparing the Hermite normal form of the operated
 * lattice. The dimension could be 2 or 3.
 *
 * @param canonicalSuperToDirect  This must be in Hermite normal form.
 * @param pointOperators
 * @return
 */
bool KPointLatticeGenerator::isSymmetryPreserving(
    const Tensor<int> &canonicalSuperToDirect,
    const std::vector<Tensor<int> > &pointOperators) {


  int size = canonicalSuperToDirect.size();
  int oppedArray[size][size];
  // Initialize variable-sized array.
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      oppedArray[i][j] = 0;
    }
  }

  for (int opNum = 0; opNum < (int) pointOperators.size(); opNum++) {
    const Tensor<int> &pointOperator = pointOperators[opNum];
    MSMath::matrixMultiply<int, int, int>(canonicalSuperToDirect, pointOperator, &oppedArray[0][0]);
    toHermiteNormalForm(size, &oppedArray[0][0]);

    for (int row = 0; row < size; row++) {
      for (int col = 0; col < size; col++) {
        if (canonicalSuperToDirect[row][col] != oppedArray[row][col]) {
          return false;
        }
      }
    }
  }
  return true;
}

/**
 * Simply checks to make sure lattices are symmetry preserving by applying
 * symmetry operations and comparing the Hermite normal form of the transformed
 * lattice to the original.
 *
 * @param size
 * @return
 */
std::vector<Tensor<int> >
KPointLatticeGenerator::getSymPreservingLattices2D(int size) {

  std::vector<int> factors = MSMath::factor(size);
  std::vector<Tensor<int> > returnArray(
      MSMath::arraySum(factors), Tensor<int>());

  Tensor<int> superToDirect(2, std::vector<int>(2, 0));

  int returnIndex = 0;
  for (int factorNum = 0; factorNum < (int) factors.size(); factorNum++) {
    int factor = factors[factorNum];

    // First we build the lattice in Hermite normal form.
    superToDirect[0][0] = factor;
    superToDirect[1][1] = size / factor;
    for (int diagElement = 0; diagElement < factor; diagElement++) {
      superToDirect[1][0] = diagElement;
      if (!isSymmetryPreserving(superToDirect, m_PointOperators2D)) {
        continue;
      }
      returnArray[returnIndex++] = superToDirect;
    }
  }

  returnArray.resize(returnIndex);
  return returnArray;
}

/**
 * This reduces the matrix to lower-triangular Hermite Normal form.  The
 * algorithm is simple -- start from the last column and perform elementary row
 * operations to get the necessary zeroes.  Then do this for the rest of the
 * columns in reverse order.  Once you have a lower triangular matrix, use
 * modulo for the off-diagonal elements.
 */
void KPointLatticeGenerator::toHermiteNormalForm(int size, int *STD) {

  if (size == 0) {
    return;
  }

  // First we make it lower triangular using elementary row operations
  for (int colNum = size - 1; colNum > 0; colNum--) {

    // Find the row with the minimum value in this column
    int minValue = std::numeric_limits<int>::max();
    int minRowNum = -1;
    for (int rowNum = 0; rowNum <= colNum; rowNum++) {
      int rowValue = fabs(*(STD + rowNum*size + colNum));
      if (rowValue < minValue && rowValue != 0) {
        minRowNum = rowNum;
        minValue = rowValue;
      }
    }

    // Swap the minRow so it is the new "last" row
    for (int i = 0; i < size; i++) {
      int temp = *(STD + minRowNum * size + i);
      *(STD + minRowNum * size + i) = *(STD + colNum * size + i);
      *(STD + colNum * size + i) = temp;
    }

    // Make sure the diagonal element on the new minimal row (colNum) is positive.
    if (*(STD + colNum * size + colNum) < 0) {
      for (int prevColNum = 0; prevColNum <= colNum; prevColNum++) {
        *(STD + colNum * size + prevColNum) *= -1;
      }
    }

    // Now keep getting the remainder between the minimum row and other rows
    // and calling that new remainder the new minimum.  Do this until all remainders are zero
    bool allZeroes = true;
    do {
      allZeroes = true;
      for (int rowNum = 0; rowNum < colNum; rowNum++) {
        int quotient = MSMath::divFloor(*(STD + rowNum*size + colNum), minValue);
        int remainder = *(STD + rowNum*size + colNum) - (minValue * quotient);
        if (remainder != 0) {
          for (int prevColNum = 0; prevColNum <= colNum; prevColNum++) {
            *(STD + rowNum * size + prevColNum) -= *(STD + colNum*size + prevColNum) * quotient;
          }
          for ( int i = 0; i < size; i++) {
            int temp = *(STD + rowNum*size + i);
            *(STD + rowNum*size + i) = *(STD + colNum*size + i);
            *(STD + colNum*size + i) = temp;
          }
          minValue = *(STD + colNum*size + colNum);
          allZeroes = false;
          break;
        }
      }
    } while (!allZeroes);

    // Now we subtract multiples of the minimum row from all of the previous rows
    for (int rowNum = 0; rowNum < colNum; rowNum++) {
      int quotient = MSMath::divFloor(*(STD + rowNum*size + colNum), minValue);
      for (int prevColNum = 0; prevColNum <= colNum; prevColNum++) {
        *(STD + rowNum*size + prevColNum) -= *(STD + colNum*size + prevColNum) * quotient;
      }
    }
  }

  // We've made all of the diagonal elements positive except one...
  if (*STD < 0) {
    *STD *= -1;
  }

  // Now we take the modulo of the off-diagonal elements
  try {
    for (int rowNum = size - 2; rowNum >= 0; rowNum--) {
      int diagonal = *(STD + rowNum*size + rowNum);
      for (int nextRowNum = rowNum + 1; nextRowNum < size; nextRowNum++) {
        int quotient = MSMath::divFloor(*(STD + nextRowNum*size + rowNum), diagonal);
        for (int prevCol = 0; prevCol <= rowNum; prevCol++) {
          *(STD + nextRowNum*size + prevCol) -= *(STD + rowNum*size + prevCol) * quotient;
        }
      }
    }
  } catch (int e) {
    throw "Error finding Hermite Normal Form:  Matrix is singular.";
  }
}

/**
 * A wrapper function of the array-argument toHermiteNormalForm, since vector data structures
 * are used extensively at other places.
 */
void KPointLatticeGenerator::toHermiteNormalForm(Tensor<int> &superToDirect) {
  int dim = superToDirect.size();
  int STD[dim][dim];
  // Initialize variable-sized array.
  for (int i = 0; i < dim; i++) {
    for (int j = 0; j < dim; j++) {
      STD[i][j] = 0;
    }
  }
  for (int i = 0; i < dim; i++) {
    for (int j = 0; j < dim; j++) {
      STD[i][j] = superToDirect[i][j];
    }
  }
  toHermiteNormalForm(dim, &STD[0][0]);
  for (int i = 0; i < dim; i++) {
    for (int j = 0; j < dim; j++) {
      superToDirect[i][j] = STD[i][j];
    }
  }
}

/**
 * Find the minimum periodic distnace using Minkowski reduction. Note: this function changes the
 * superVectors passed in, so we use pass-by-value here.
 *
 * @param  superVectors
 * @return The minimum distance between any two points on a superlattice.
 */
double KPointLatticeGenerator::getMinDistance(Tensor<double> superVectors,
    const int numDimensions) {
  double minMagSq = std::numeric_limits<double>::infinity();

  bool minimizing = true;
  std::vector<double> newVector(superVectors[0].size() ,0.);
  while (minimizing) {
    minimizing = false;
    for (int vecNum = 0; vecNum < numDimensions; vecNum++) {
      std::vector<double> &vec = superVectors[vecNum];
      if (vec.empty()) {
        continue;
      }
      double magSq = MSMath::magnitudeSquared(vec);
      for (int increment = 1; increment < numDimensions; increment++) {
        int vecNum2 = (vecNum + increment) % numDimensions;
        std::vector<double> &vector2 = superVectors[vecNum2];
        double innerProduct = MSMath::dotProduct(vec, vector2) / magSq;
        //innerProduct = MSMath::roundWithPrecision(innerProduct, precision);
        double shift = MSMath::round(innerProduct);
        double oldMagSq = MSMath::magnitudeSquared(vector2);
        minMagSq = std::min(oldMagSq, minMagSq);
        if (shift == 0) {
          continue;
        }
        for (int dimNum = 0; dimNum < (int) newVector.size(); dimNum++) {
          newVector[dimNum] = vector2[dimNum] - vec[dimNum] * shift;
        }
        double newMagSq = MSMath::magnitudeSquared(newVector);
        if (newMagSq < oldMagSq) {
          minimizing = true;
          superVectors[vecNum2] = newVector;
          minMagSq = std::min(newMagSq, minMagSq);
        }
      }
    }
  }

  if (numDimensions == 3) {

    // An extra step that is necessary in three dimensions.
    int eps01 = static_cast<int>(sgn(MSMath::dotProduct(superVectors[0], superVectors[1])));
    int eps02 = static_cast<int>(sgn(MSMath::dotProduct(superVectors[0], superVectors[2])));
    int eps12 = static_cast<int>(sgn(MSMath::dotProduct(superVectors[1], superVectors[2])));

    if (eps01 * eps02 * eps12 == -1) {
      for (int dimNum = 0; dimNum < (int) superVectors[0].size(); dimNum++) {
        superVectors[0][dimNum] -= (superVectors[1][dimNum] * eps01
                                  + superVectors[2][dimNum] * eps02);
      }
      minMagSq = std::min(MSMath::magnitudeSquared(superVectors[0]), minMagSq);
    }
  }

  return sqrt(minMagSq);
}

template <typename T> int sgn(T val) { return (T(0) < val) - (val < T(0)); }
