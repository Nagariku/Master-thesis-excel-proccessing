import pandas as pd
import logging
import numpy as np

from src.methods.math_model.AHP_analysis import ahp
from src.methods.math_model.MatrixMake import main as matrix_make


def main(subInputList,dimInputList):
    logging.info("M - Data processing started")

    #RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59] # for consistency index

    #data = pd.DataFrame({'a': [3,0.5,0.5,1,0.5,0.25,0.25,0.25,0.25,0.3333,2,0.5,3,2,0.3333]})
    #print(data)
    #matrix = matrix_make(data)
    #print(ahp(matrix,RI[matrix.shape[0]]))
    subDimListWeights, subDimConsistencyList = process_list_to_usable(subInputList)
    DimWeightList,colList = process_dataframe_to_usable(dimInputList)

    outputList = multiply_weights(subDimListWeights,DimWeightList)
    subDimListWeightsDF = convert_to_dataframe(subDimListWeights,colList)
    outputCalcWeights= convert_to_dataframe(outputList,colList)
    #outputDimWeights = convert_to_dataframe(DimWeightList,colList)
    outputSubDimweights = convert_to_dataframe(subDimListWeights,colList)
    outputConsistency = convert_to_dataframe(subDimConsistencyList,colList)
    #outputDimConsistency = convert_to_dataframe(DimConsistencyList,colList)


   
    logging.info("M - Data processing finished successfully")
    return outputCalcWeights,outputConsistency, DimWeightList,subDimListWeightsDF


def process_list_to_usable(uncutList):
    RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59] # for consistency index
    workingListWeights = []
    workingConsistencyIndexList = []
    for subInput in range(len(uncutList)):
        currentSubDimWeight = []
        curentSubConsistency = []
        for col_name in uncutList[subInput].columns:
            col = uncutList[subInput][col_name]
            working_matrix = matrix_make(col)
            working_weight_list, working_consistency_index = ahp(working_matrix,RI[working_matrix.shape[0]])
            currentSubDimWeight.append(working_weight_list)
            curentSubConsistency.append(working_consistency_index)

        workingListWeights.append(currentSubDimWeight)
        workingConsistencyIndexList.append(curentSubConsistency)

    return workingListWeights, workingConsistencyIndexList

def process_dataframe_to_usable(uncutDataframe):
    RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59] # for consistency index
    workingListWeights = []
    workingConsistencyIndexList = []
    columnList = []

    for col_name in uncutDataframe.columns:
        columnList.append(col_name)
        col = uncutDataframe[col_name]
        working_matrix = matrix_make(col)
        working_weight_list, working_consistency_index = ahp(working_matrix,RI[working_matrix.shape[0]])
        workingListWeights.append(working_weight_list)
        workingConsistencyIndexList.append(working_consistency_index)



    return workingListWeights, columnList

def multiply_weights(sudDimWeights, dimWeights):
    finalList=[]
    for dim in range(len(sudDimWeights)):
        workingListWeights = []
        #print(len(subDimListWeights[dim]))
        for file in range(len(dimWeights)):
            #print(type(sudDimWeights[dim][file]))
            #print(type(dimWeights[file][dim]))
            workingListWeights.append(sudDimWeights[dim][file]*dimWeights[file][dim])
        finalList.append(workingListWeights)

    return finalList

def convert_to_dataframe(listToConvert,columnList):
    outDF = pd.DataFrame()
    for i in range(len(listToConvert)):
        workDf = pd.concat([pd.Series(arr) for arr in listToConvert[i]], axis=1)
        outDF = pd.concat([outDF,workDf],axis=0)
    outDF.columns = columnList
    return outDF