// The generic function implementaions.
template<class T> 
void MSMath::vectorTimesMatrix(const std::vector<T> &vector, const Tensor<double> &matrix, 
                               std::vector<double> &returnArray) {
  // For safety, in caes the passed-on array has pre-existed values;
  for (int i = 0; i < (int) returnArray.size(); i++) {
    returnArray[i] = 0;
  }

  for (int colNum = 0; colNum < (int) returnArray.size(); colNum++) {
    for (int rowNum = 0; rowNum < (int) matrix.size(); rowNum++) {
      returnArray[colNum] += matrix[rowNum][colNum] * vector[rowNum];
    }
  } 
}

/*
 * Only for matrices with dimensions three or smaller.
 */
template<class T> Tensor<double> MSMath::simpleInverse(const Tensor<T> &smallMatrix) {
  // Just so I don't have to keep calling it "smallMatrix"
  const Tensor<double> &matrix = smallMatrix;

  double det = determinant(matrix);

  if (det == 0) {
    throw "Can't invert a singular matrix!";
  }

  if (matrix.size() == 0) {
    return Tensor<double>();
  }

  if (matrix.size() == 1) {
    return Tensor<double>(1, std::vector<double>(1, 1 / det));
  }

  if (matrix.size() == 2) {
    Tensor<double> inverseMatrix(2, std::vector<double>(2, 0));
    inverseMatrix[0][0] = matrix[1][1] / det;
    inverseMatrix[0][1] = -matrix[0][1] / det;
    inverseMatrix[1][0] = -matrix[1][0] / det;
    inverseMatrix[1][1] = matrix[0][0] / det;

    return inverseMatrix;
  }

  if (matrix.size() == 3) {

    Tensor<double> inverseMatrix(3, std::vector<double>(3, 0));

    inverseMatrix[0][0] = (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) / det;
    inverseMatrix[0][1] = (matrix[0][2] * matrix[2][1] - matrix[2][2] * matrix[0][1]) / det;
    inverseMatrix[0][2] = (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]) / det;
    inverseMatrix[1][0] = (matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]) / det;
    inverseMatrix[1][1] = (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]) / det;
    inverseMatrix[1][2] = (matrix[1][0] * matrix[0][2] - matrix[1][2] * matrix[0][0]) / det;
    inverseMatrix[2][0] = (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) / det;
    inverseMatrix[2][1] = (matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]) / det;
    inverseMatrix[2][2] = (matrix[1][1] * matrix[0][0] - matrix[1][0] * matrix[0][1]) / det;

    return inverseMatrix;
  }

  throw "Cannot yet calculate the simple inverse of a matrix with more than three dimensions!";
}

/*
 * Only for matrices with dimensions three or smaller.
 */
template<class T> T MSMath::determinant(const Tensor<T> &matrix) {
  int dim = matrix.size();

  for (int row = 0; row < dim; row++) {
    if ((int) matrix[row].size() != dim) {
      return 0;
    }
  }

  if (dim == 0) {
    return 1;
  } else if (dim == 1) {
    return matrix[0][0];
  } else if (dim == 2) {
    return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0]);
  } else if (dim == 3) {
    return matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
  }

  throw "Cannot yet calculate the determinant of a matrix with more than three dimensions!";
}

template<class R, class T1, class T2> 
Tensor<R> MSMath::matrixMultiply(const Tensor<T1> &matrix1, const Tensor<T2> &matrix2) {

  if (matrix1[0].size() != matrix2.size()) {
    throw "Cannot muliply matrices of incomaptible dimensions!";
  }
  std::vector<std::vector<R> > returnMatrix(matrix1.size(), std::vector<R>(matrix2[0].size(), 0));
  for (int row = 0; row < (int) returnMatrix.size(); row++) {
    for (int col = 0; col < (int) returnMatrix[row].size(); col++) {
      for (int counter = 0; counter < (int) matrix2.size(); counter++) {
        returnMatrix[row][col] += matrix1[row][counter] * matrix2[counter][col];
      }
    }
  }
  return returnMatrix;
}

template<class R, class T1, class T2> 
void MSMath::matrixMultiply(const Tensor<T1> &matrix1, const Tensor<T2> &matrix2, R* returnMatrix) {
  
  int rowDim = matrix1.size();    // rows of the first matrix;
  int colDim = matrix2[0].size(); // columns of the second matrix;
  if (matrix1[0].size() != matrix2.size()) {
    throw "Cannot muliply matrices of incomaptible dimensions!";
  }

  for (int row = 0; row < rowDim; row++) {
    for (int col = 0; col < colDim; col++) {
      *(returnMatrix + row * rowDim + col) = 0; // Initialize to zero.
      for (int counter = 0; counter < (int) matrix2.size(); counter++) {
        *(returnMatrix + row * rowDim + col) += matrix1[row][counter] * matrix2[counter][col];
      }
    }
  }
}

template<class T> Tensor<T> MSMath::transpose(const Tensor<T> &matrix) {

  int rows = matrix.size();
  int cols = matrix[0].size();
  Tensor<T> returnMatrix(cols, std::vector<T>(rows, 0));
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      returnMatrix[j][i] = matrix[i][j];
    }
  }
  return returnMatrix;
}

template<class T> 
void MSMath::matrixTimesVector(const Tensor<T>  &matrix, double *vec, double *returnVector) {
  // We only use it for 3x3 matrix in this program.
  // Re-initialize. Make sure residual values are removed.
  for (int i = 0; i < 3; i++) { returnVector[i] = 0; } 
  
  for (int rowNum = 0; rowNum < 3; rowNum++) {
    for (int colNum = 0; colNum < 3; colNum++) {
      returnVector[rowNum] += matrix[rowNum][colNum] * vec[colNum];
    }
  }
}

template<class T> double MSMath::dotProduct(const std::vector<T> &vector1,
                                            const std::vector<double> &vector2) {
  int numCoords = vector1.size();
  if (numCoords != (int) vector2.size()) {
    throw "Can\'t take dot product of vectors with different lengths!";
  }

  double result = 0;
  for (int coordNum = numCoords - 1; coordNum >= 0; coordNum--) {
    result += vector1[coordNum] * vector2[coordNum];
  }

  return result;
}