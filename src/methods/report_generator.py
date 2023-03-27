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
         interDimensionalListSM, kripSimplifiedListSM, outputDataframeSM, 
         subDimConsistencyListSM,DimWeightListSM):
    logging.info("M - Report generation started")
    outFolderPath = check_output_folder(cFM.get("Settings", "outputFolder"),mFP) #check if output folder exists
    listDimension,combinedList=get_subsection(cFM) #get subsections and dimensions from config file
    sOF=make_folder(outFolderPath,nList) #returns specific output folder


    csv_levels(levelListSM,sOF,combinedList) #generates csv file with levels
    csv_sub_inputs_pre(weightListSM,sOF) #generates csv file with subdimension inputs
    csv_dim_inputs_pre(dimensionListSM,sOF) #generates csv file with dimensions inputs
    csv_interdim_comparisions_input(interDimensionalListSM,sOF) #generates csv file with interdimensional comparisions
    csv_calculated_weights(outputDataframeSM,sOF,combinedList,DimWeightListSM,listDimension) #generates csv file with calculated weights
    csv_consistency_indexes(subDimConsistencyListSM,sOF,listDimension) #generates csv file with consistency indexes

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
        logging.info("Directory created successfully!")
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
    outPath=os.path.join(sOF, "inputs_subdimensions.csv")
    verticalAdd.to_csv(outPath, index=True)
    return None

def csv_dim_inputs_pre(dL,sOF):
    outPath=os.path.join(sOF, "inputs_dimensions.csv")
    dL.to_csv(outPath, index=True)
    return None

def csv_levels(df,sOF,combL):
    verticalAdd= pd.concat(df,axis=0)
    verticalAdd.index=combL
    outPath=os.path.join(sOF, "levels.csv")
    verticalAdd.to_csv(outPath, index=True)
    return None

def csv_kripke_simplified(kSL,sOF): #doesn't work
    verticalAdd= pd.concat(kSL,axis=0)
    outPath=os.path.join(sOF, "kripke_simplified.csv")
    verticalAdd.to_csv(outPath, index=True)
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
    outPath=os.path.join(sOF, "Calculated_weights.csv")
    finalout.to_csv(outPath, index=True)
    return None

def csv_consistency_indexes(sDCL,sOF,listDimensionFunc):
    sDCL.index=listDimensionFunc
    outPath=os.path.join(sOF, "Consistency_indexes.csv")
    sDCL.to_csv(outPath, index=True)
    return None


def csv_interdim_comparisions_input(iDL,sOF):
    outPath=os.path.join(sOF, "inputs_interdimensions.csv")
    iDL.to_csv(outPath, index=True)
    return None

def csv_base_math_model():
    return None