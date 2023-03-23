import numpy as np
import pandas as pd

def vertical_to_matrix(df):
    n = len(df)
    if n == 1:
        M = np.zeros((n, n))
        np.fill_diagonal(M, 1)
        M[0, 1:] = df.iloc[:, 0].values
        M[1:, 0] = 1/M[0, 1:]
    else:
        M = np.zeros((n, n))
        np.fill_diagonal(M, 1)
        for i in range(n):
            for j in range(i+1, n):
                M[i, j] = df.iloc[j, i]/df.iloc[i, i]
            for j in range(i):
                M[i, j] = 1/M[j, i]
    return M



# Load pairwise comparison matrix from a csv file
#pairwise_df = pd.read_csv('pairwise.csv', header=None)
f = r"C:/Users/osipo/Documents/GitHub/Master-thesis-excel-proccessing/Excel_surveys/0PG1-TIGO.xlsx"


pairwise_df = pd.read_excel(f,index_col=None, sheet_name="1.Technology", skiprows=13, nrows= 15, usecols="C",header =None)
matrix=vertical_to_matrix(pairwise_df)
n=len(matrix)
print(matrix)
# Normalize pairwise comparison matrix
normalized = matrix/matrix.sum(axis=1)

# Calculate geometric mean of normalized matrix to obtain weights
weights = np.power(np.prod(normalized, axis=1), 1/n)

# Calculate maximum eigenvalue of pairwise comparison matrix
eigenvalues, eigenvectors = np.linalg.eig(normalized)
max_eigenvalue = np.real(eigenvalues).max()

# Calculate consistency index and random index
ri_table = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
ri = ri_table[n-1]
ci = (max_eigenvalue - n)/(n-1)

# Calculate consistency ratio
cr = ci/ri

# Print weights and consistency ratio
print("Weights:", weights)
print("Consistency ratio:", cr)
