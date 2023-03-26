import pandas as pd
import logging

from src.methods.math_model.AHP_analysis import ahp
from src.methods.math_model.MatrixMake import main as matrix_make


def main(data):
    logging.info("M - Data processing started")

    RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59] # for consistency index

    #data = pd.DataFrame({'a': [3,0.5,0.5,1,0.5,0.25,0.25,0.25,0.25,0.3333,2,0.5,3,2,0.3333]})
    #print(data)
    #matrix = matrix_make(data)
    #print(ahp(matrix,RI[matrix.shape[0]]))
    logging.info("M - Data processing finished successfully")
    return None


