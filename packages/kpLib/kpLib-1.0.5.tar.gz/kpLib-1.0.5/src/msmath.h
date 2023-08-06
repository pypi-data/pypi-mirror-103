#ifndef MSMATH_H
#define MSMATH_H

#include <vector>
#include <cmath>

template <typename T>
using Tensor = std::vector<std::vector<T>>;

class MSMath {
private:
  MSMath();

public:
  template<class T> static Tensor<double> simpleInverse(const Tensor<T> &smallMatrix);

  template<class T> static T determinant(const Tensor<T> &matrix);

  template<class R, class T1, class T2>
  static Tensor<R> matrixMultiply(const Tensor<T1> &matrix1, const Tensor<T2> &matrix2);

  /*
   * A generic function to perform matrix multiplication in 2 or 3 dimensions. It helps
   * improve performance by removing dynamic allocation in operations which are repeated
   * extensively, and in which the returnMatrix acts as a temporary local variable.
   */
  template<class R, class T1, class T2>
  static void matrixMultiply(const Tensor<T1> &matrix1, const Tensor<T2> &matrix2, R* returnMatrix);

  static double magnitudeSquared(const std::vector<double> &vec);

  static double magnitude(const std::vector<double> &vec);

  static Tensor<int> getFactorSets(int number, int numFactors);

  static std::vector<int> factor(int value);

  static Tensor<double> simpleLowerTriangularInverse(const Tensor<int> &smallMatrix);

  static std::vector<int> rounded(const std::vector<double> &arr);

  static Tensor<int> rounded(const Tensor<double> &arr);

  template<class T> static Tensor<T> transpose(const Tensor<T> &matrix);

  template<class T>
  static void matrixTimesVector(const Tensor<T> &matrix, double *vec, double *returnVector);

  template<class T>
  static double dotProduct(const std::vector<T> &vector1, const std::vector<double> &vector2);

  static int arraySum(const std::vector<int> &arr);

  static int divFloor(int dividend, int divisor);
  static inline double round(double number) { return floor(number + 0.5); }
  static double roundWithPrecision(double number, double precision);

  static Tensor<double> matrixTimesScalar(const Tensor<double> &matrix, double scalar);

  static std::vector<double> vectorTimesScalar(const std::vector<double> &vector, double scalar);

  static std::vector<double> arrayAdd(const std::vector<double> &array1,
                                      const std::vector<double> &array2);

  template<class T> static void vectorTimesMatrix(const std::vector<T> &vector,
      const Tensor<double> &matrix, std::vector<double> &returnArray);

  static std::vector<double> arrayDivide(const std::vector<double> &array,
                                         const double divisor);
  static std::vector<double> arraySubtract(const std::vector<double> &array1,
                                           const std::vector<double> &array2);
};

#include "msmath.ipp"

#endif // FILE2_H

