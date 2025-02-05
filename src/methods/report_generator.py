import logging
import os
import csv
import sys
import datetime
import pandas as pd
import numpy as np

from src.methods.data_import import subCompListy

##############Main function##############
def main(mFP,cFM,nList,levelListSM,weightListSM, dimensionListSM, 
         interDimensionalListSM, outputDataframeSM, 
         subDimConsistencyListSM,DimWeightListSM,
         kripSimpleListOut, kripInputListOut,subDimWeightsListSM):
    logging.info("M - Report generation started")
    outFolderPath = check_output_folder(cFM.get("Settings", "outputFolder"),mFP) #check if output folder exists
    listDimension,combinedList=get_subsection(cFM) #get subsections and dimensions from config file
    sOF=make_folder(outFolderPath,nList) #returns specific output folder


    csv_input_levels(levelListSM,sOF,combinedList) #generates csv file with inputted levels
    csv_sub_inputs_pre(weightListSM,sOF) #generates csv file with subdimension inputs
    csv_dim_inputs_pre(dimensionListSM,sOF) #generates csv file with dimensions inputs
    csv_interdim_comparisions_input(interDimensionalListSM,sOF) #generates csv file with interdimensional comparisions
    csv_calculated_weights(outputDataframeSM,sOF,combinedList,DimWeightListSM,listDimension) #generates csv file with calculated weights
    csv_consistency_indexes(subDimConsistencyListSM,sOF,listDimension) #generates csv file with consistency indexes
    csv_krip_inputs(kripInputListOut,sOF) #generates csv file with krippendorff inputs
    csv_krip_outputs(kripSimpleListOut,sOF,listDimension) #generates csv file with krippendorff outputs
    csv_subweights_weights(subDimWeightsListSM,sOF,combinedList,DimWeightListSM,listDimension) #generates csv file with subweights and weights
    logging.info("M - Report generation finished successfully")
    return None

##############Sub functions##############

#File that generates the report

def get_subsection(CF):
    dimList = eval(CF.get("Dimensions","dimensions"))

    combinedList=[]

    for i in range(len(dimList)):
        for n in range(len(subCompListy[i])):
            combinedList.append(f"{dimList[i]} - {subCompListy[i][n]}")

    return dimList,combinedList
#maybe make pdf with graphs
def check_output_folder(folderName,pathFold): #check if excel survey folder exists
    joinedOutputPath = os.path.join(pathFold,folderName)
    if os.path.exists(joinedOutputPath):
        logging.info("Check: '" + folderName + "' folder exists in the main folder")
    else:
        logging.warning("Check: " + folderName + " doesn't exist in the main folder")
        os.mkdir(joinedOutputPath)
        logging.info("'" + folderName + "' folder created")
    return joinedOutputPath

def make_folder(oFP,num_participants):
    folder_name = get_current_time() + " - " + str(num_participants) + " participant(s)"
    specificOutFolder = os.path.join(oFP, folder_name)

    if not os.path.exists(os.path.join(oFP, folder_name)):
        os.makedirs(os.path.join(oFP, folder_name))
        logging.info("Report folder created successfully!")
    else:
        logging.info("Directory already exists!")
        logging.log(logging.CRITICAL, "Program aborted, Program run twice in single second")
        sys.exit()
    return specificOutFolder

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%dT%H_%M_%S')


##############csv generation##############

def csv_sub_inputs_pre(wL,sOF):
    verticalAdd= pd.concat(wL,axis=0)
    outPath=os.path.join(sOF, "input_subdimension_comparisions.csv")
    verticalAdd.to_csv(outPath, index=True)
    return None

def csv_dim_inputs_pre(dL,sOF):
    outPath=os.path.join(sOF, "input_dimensions_comparisions.csv")
    dL.to_csv(outPath, index=True)
    return None

def csv_input_levels(df,sOF,combL):
    verticalAdd= pd.concat(df,axis=0)
    verticalAdd.index=combL
    outPath=os.path.join(sOF, "input_levels.csv")
    verticalAdd.to_csv(outPath, index=True)
    return None

def csv_krip_inputs(kripInputListOut,sOF): #from most convoluting to least (aka higher alpha to lower)
    finalDF = pd.DataFrame()
    for i in range(len(kripInputListOut)):
        workingDF = pd.DataFrame()
        for x in range(len(kripInputListOut[i])):
            workingDF = pd.concat([workingDF,kripInputListOut[i][x]],axis=0)
        finalDF = pd.concat([finalDF,workingDF],axis=1)
    outPath=os.path.join(sOF, "input_simplified_krip.csv")
    finalDF.to_csv(outPath, index=True)
    return None

def csv_calculated_weights(df,sOF,combL,DimWeightListSMFunc,listDimensionFunc):
    data = {}
    for i, array in enumerate(DimWeightListSMFunc):
        column_name = 'col' + str(i + 1)  
        data[column_name] = array       
    dfDimension = pd.DataFrame(data)
    dfDimension.index=listDimensionFunc
    df.index=combL
    dfDimension.columns=df.columns
    finalout = pd.concat([dfDimension,df],axis=0)
    outPath=os.path.join(sOF, "output_normalised_weights.csv")
    finalout.to_csv(outPath, index=True)
    return None

def csv_consistency_indexes(sDCL,sOF,listDimensionFunc):
    sDCL.index=listDimensionFunc
    outPath=os.path.join(sOF, "output_consistency_indexes.csv")
    sDCL.to_csv(outPath, index=True)
    return None

def csv_interdim_comparisions_input(iDL,sOF):
    outPath=os.path.join(sOF, "inputs_interdimensions.csv")
    iDL.to_csv(outPath, index=True)
    return None

def csv_krip_outputs(kripSimpleListOut, sOF, listDimensionFunc):
    indexToUse = ["Dimensions"] + listDimensionFunc
    cols = [3, 5, 9, 17] #list of columns to drop

    finalDF = pd.DataFrame()
    for i in range(len(kripSimpleListOut)):
        col_name=cols[i]
        df=pd.DataFrame({col_name: kripSimpleListOut[i]})
        finalDF=pd.concat([finalDF,df],axis=1)

    finalDF.index=indexToUse
    outPath=os.path.join(sOF, "outputs_krip.csv")
    finalDF.to_csv(outPath, index=True)
    return None

def csv_subweights_weights(df,sOF,combL,DimWeightListSMFunc,listDimensionFunc):
    data = {}
    for i, array in enumerate(DimWeightListSMFunc):
        column_name = 'col' + str(i + 1)  
        data[column_name] = array       
    dfDimension = pd.DataFrame(data)
    dfDimension.index=listDimensionFunc
    df.index=combL
    dfDimension.columns=df.columns
    finalout = pd.concat([dfDimension,df],axis=0)
    outPath=os.path.join(sOF, "output_non_normalised_weights.csv")
    finalout.to_csv(outPath, index=True)
    return None
