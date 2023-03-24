import numpy as np

def ahp(matrix,ri):
    # Normalize the matrix


    normalized_matrix = matrix / matrix.sum(axis=0)
    #print(normalized_matrix)

    # Calculate the row averages
    row_avgs = normalized_matrix.mean(axis=1)
    row_avgs =np.transpose(row_avgs)

    # Calculate the weighted matrix
    weighted_matrix = normalized_matrix * row_avgs[:, np.newaxis]
    #print(weighted_matrix)

    # Calculate the weights
    consistency_measure = []
    for i in range(len(row_avgs)):
        consistency_measure.append( np.dot(matrix[i],row_avgs)/row_avgs[i])

    Consistency_index= (np.mean(consistency_measure)-len(consistency_measure))/(len(consistency_measure)-1)
    consistency_ratio=Consistency_index/ri
    return row_avgs, consistency_ratio


# Example comparison matrix
matrix = np.array(
       [[1 , 7  , 3  , 1  , 1  ],
       [0.14, 1  , 0.14, 0.2 , 0.2 ],
       [0.33, 7  , 1  , 1  , 1  ],
       [1  , 5  , 1  , 1  , 1  ],
       [1  , 5  , 1  , 1  , 1  ]])


RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59]

weights, CI=ahp(matrix,RI[matrix.shape[0]])
print("Weights:", weights)
print("Consistency Index:", CI)