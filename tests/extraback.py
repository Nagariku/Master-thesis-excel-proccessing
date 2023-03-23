import numpy as np
import pandas as pd

def inverse_number_of_comparisons(output):
    return int((1 + np.sqrt(1 + 8*output)) / 2)

def fill_matrix(data):
    n = inverse_number_of_comparisons(len(data))
    sum = 0
    matrix = np.zeros((n, n))

    # Add the diagonal of ones
    #
    for i in range(n):
        if sum==0:
            matrix[0, 1:n] = data[:n-1]
            sum=n-1
        elif (i==n-1):
            matrix[n-2, n-1] = data[len(data)-1]
            return matrix
        else:
            nextSum=sum+n-(i+1)
            matrix[i, i+1:n]=data[sum:nextSum]
            sum=nextSum




data = pd.DataFrame({'a': [3,0.5,0.5,1,0.5,0.25,0.25,0.25,0.25,0.3333,2,0.5,3,2,0.3333]})
data = np.ravel(data.values)

firstMat=fill_matrix(data)
reciprocal_matrix = np.reciprocal(firstMat.T)

mask = (firstMat == 0) | np.isinf(firstMat)

# use numpy.copyto() to overwrite the masked values in matrix1 with the corresponding values from matrix2
np.copyto(firstMat, reciprocal_matrix, where=mask)
np.fill_diagonal(firstMat, 1)
print(firstMat)