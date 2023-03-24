import numpy as np

def ahp(matrix,ri):
    normalized_matrix = matrix / matrix.sum(axis=0)
    row_avgs = normalized_matrix.mean(axis=1)
    row_avgs =np.transpose(row_avgs)
    consistency_measure = []
    for i in range(len(row_avgs)):
        consistency_measure.append( np.dot(matrix[i],row_avgs)/row_avgs[i])
    Consistency_index= (np.mean(consistency_measure)-len(consistency_measure))/(len(consistency_measure)-1)
    consistency_ratio=Consistency_index/ri
    return row_avgs, consistency_ratio





