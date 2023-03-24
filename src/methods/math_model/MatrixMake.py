import numpy as np
import pandas as pd

def inverse_number_of_comparisons(output):
    return int((1 + np.sqrt(1 + 8*output)) / 2)

def fill_matrix(data):
    data = np.ravel(data.values)
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

def do_rest_of_matrix(matrix):
    matrix = np.where(matrix == 0, 1e-6, matrix)
    reciprocal_matrix = np.reciprocal(matrix.T)
    mask = (matrix == 1e-6) | np.isinf(matrix)
    np.copyto(matrix, reciprocal_matrix, where=mask)
    np.fill_diagonal(matrix, 1)
    return matrix





def main(data):
    matrix = fill_matrix(data)
    matrix = do_rest_of_matrix(matrix)
    return matrix




