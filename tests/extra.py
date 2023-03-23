import numpy as np

# Create a 5x5 matrix with random values in the top-right corner
matrix = np.zeros((5, 5))
matrix[:, 3:] = np.random.rand(5, 2)

# Set the bottom-left corner to the reciprocals of the top-right corner
matrix[3:, :] = 1 / matrix[:2, 3:].reshape((2, 1))

print(matrix)
