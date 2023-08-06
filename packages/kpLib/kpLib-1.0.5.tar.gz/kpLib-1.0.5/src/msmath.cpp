#include "msmath.h"
#include <cmath>

MSMath::MSMath() {}

double MSMath::magnitudeSquared(const std::vector<double> &vec) {
  int numCoords = vec.size();
  double magSquared = 0;
  double coord;
  for (int coordNum = numCoords - 1; coordNum >= 0; coordNum--) {
    coord = vec[coordNum];
    magSquared += coord * coord;
  }
  return magSquared;
}

double MSMath::magnitude(const std::vector<double> &vec) {
  return sqrt(magnitudeSquared(vec));
}

/**
 * Get an array of the unique factorizations. Permutations of the same set of factors are
 * listed as unique sets. The factorizations are sequenced in ascending order of the values
 * of factors. For example, among the factorizations of 15, {3, 1, 5} precedes {5, 3, 1}.
 *
 * @param number      The number to be factorized
 * @param numFactors  The number of factors that should be in each set
 * @return A complete list of arrays, each numFactors long, that contains a unique set of factors.
 */
Tensor<int> MSMath::getFactorSets(int number, int numFactors) {
  if (numFactors < 1) {
    return Tensor<int>();
  }

  if (numFactors == 1) {
    return Tensor<int>(1, std::vector<int>(1, number));
  }

  Tensor<int> returnArray;

  for (int factor = 1; factor <= number; factor++) {
    if ((number % factor) == 0) {
      int quotient = number / factor;
      Tensor<int> subFactors = getFactorSets(quotient, numFactors - 1);
      int numOldSets = returnArray.size();
      returnArray.resize(returnArray.size() + subFactors.size());
      for (int newSetNum = 0; newSetNum < (int) subFactors.size(); newSetNum++) {
        std::vector<int> newSet(numFactors, 0);
        newSet[0] = factor;
        std::copy(subFactors[newSetNum].begin(),
            subFactors[newSetNum].begin() + numFactors - 1, newSet.begin() + 1);
        returnArray[numOldSets + newSetNum] = newSet;
      }
    }
  }

  return returnArray;
}

// Get all factors of a positive integer.
std::vector<int> MSMath::factor(int value) {

  int max = static_cast<int>(floor(sqrt(value)));
  // First count the number of factors.
  int numFactors = 0;
  for (int i = 1; i <= max; i++) {
    if (value % i == 0) {
      numFactors++;
      if (value / i != i) {
        numFactors++;
      }
    }
  }
  std::vector<int> factors(numFactors, 0);
  int factNum = 0;
  for (int i = 1; i <= max; i++) {
    if (value % i == 0) {
      factors[factNum] = i;
      factNum++;
      if (value / i != i) {
        factors[numFactors - factNum] = value / i;
      }
    }
  }
  return factors;
}

// Used for 3x3 or smaller matrices. Has less elementary operations.
Tensor<double> MSMath::simpleLowerTriangularInverse(const Tensor<int> &smallMatrix) {

  // Just so I don't have to keep calling it "smallMatrix"
  const Tensor<int> &matrix = smallMatrix;

  if (matrix.size() == 0) {
    return Tensor<double>();
  }

  if (matrix.size() == 1) {
    return Tensor<double>(1, std::vector<double>(1, 1 / matrix[0][0]));
  }

  if (matrix.size() == 2) {
    double determinant = matrix[0][0] * matrix[1][1];
    Tensor<double> inverseMatrix(2, std::vector<double>(2, 0.0));
    inverseMatrix[0][0] = matrix[1][1] / determinant;
    inverseMatrix[1][0] = -matrix[1][0] / determinant;
    inverseMatrix[1][1] = matrix[0][0] / determinant;

    return inverseMatrix;
  }

  if (matrix.size() == 3) {

    Tensor<double> inverseMatrix(3, std::vector<double>(3, 0.0));

    double determinant = matrix[0][0] * matrix[1][1] * matrix[2][2];
    inverseMatrix[0][0] = (matrix[1][1] * matrix[2][2]) / determinant;
    inverseMatrix[1][0] = (-matrix[1][0] * matrix[2][2]) / determinant;
    inverseMatrix[1][1] = (matrix[0][0] * matrix[2][2]) / determinant;
    inverseMatrix[2][0] = (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) / determinant;
    inverseMatrix[2][1] = (-matrix[0][0] * matrix[2][1]) / determinant;
    inverseMatrix[2][2] = (matrix[1][1] * matrix[0][0]) / determinant;

    return inverseMatrix;
  }

  throw "Cannot yet calculate the simple inverse of a matrix with more than three dimensions.";
}

std::vector<int> MSMath::rounded(const std::vector<double> &arr) {
  std::vector<int> returnArray(arr.size(), 0);

  for (int i = 0; i < (int) arr.size(); i++) {
    returnArray[i] = static_cast<int>(round(arr[i]));
  }
  return returnArray;
}


Tensor<int> MSMath::rounded(const Tensor<double> &arr) {
  Tensor<int> returnArray(arr.size(), std::vector<int>());

  for (int i = 0; i < (int) arr.size(); i++) {
    returnArray[i] = rounded(arr[i]);
  }
  return returnArray;
}

int MSMath::arraySum(const std::vector<int> &arr) {
  int total = 0;
  for (int i = 0; i < (int) arr.size(); i++) {
    total += arr[i];
  }
  return total;
}

int MSMath::divFloor(int dividend, int divisor) {

  int intDiv = dividend / divisor;
  if ((dividend >= 0) && (divisor >= 0)) {
    return intDiv;
  }
  if ((dividend <= 0) && (divisor <= 0)) {
    return intDiv;
  }
  if (dividend % divisor == 0) {
    return intDiv;
  }
  return intDiv - 1;
}

double MSMath::roundWithPrecision(double number, double precision) {
  return MSMath::round(number / precision) * precision;
}

Tensor<double> MSMath::matrixTimesScalar(const Tensor<double> &matrix, double scalar) {
  int size = matrix.size();
  Tensor<double> returnMatrix(size, std::vector<double>());
  for (int i = 0; i < size; i++) {
    returnMatrix[i] = vectorTimesScalar(matrix[i], scalar);
  }
  return returnMatrix;
}

std::vector<double> MSMath::vectorTimesScalar(const std::vector<double> &vector, double scalar) {
  int size = vector.size();
  std::vector<double> returnVector(size, 0);
  for (int i = 0; i < size; i++) {
    returnVector[i] = vector[i] * scalar;
  }
  return returnVector;
}

std::vector<double> MSMath::arrayAdd(const std::vector<double> &array1,
                                     const std::vector<double> &array2) {
  int length = array1.size();
  if (length != (int) array2.size()) {
    throw "Can't add two arrays of different dimensions!";
  }

  std::vector<double> returnArray(length, 0);
  for (int i = 0; i < length; i++) {
    returnArray[i] = array2[i] + array1[i];
  }
  return returnArray;
}

std::vector<double> MSMath::arrayDivide(const std::vector<double> &array, const double divisor) {

  std::vector<double> returnArray(array.size(), 0);
  for (int i = 0; i < (int) array.size(); i++) {
    returnArray[i] = array[i] / divisor;
  }
  return returnArray;
}

std::vector<double> MSMath::arraySubtract(const std::vector<double> &array1,
    const std::vector<double> &array2) {
  int length = array1.size();
  if (length != (int) array2.size()) {
    throw "Can't add two arrays of different dimensions!";
  }
  std::vector<double> returnArray(length, 0);
  for (int i = 0; i < length; i++) {
    returnArray[i] = array1[i] - array2[i];
  }
  return returnArray;
}
