import logging
import os
import csv
import sys
import datetime
import pandas as pd

from src.methods.data_import import subCompListy

##############Main function##############
def main(mFP,cFM,nList,levelListSM,weightListSM, dimensionListSM, interDimensionalListSM, kripSimplifiedListSM):
    logging.info("Report generation started")
    outFolderPath = check_output_folder(cFM.get("Settings", "outputFolder"),mFP) #check if output folder exists
    listDimension,combinedList=get_subsection(cFM) #get subsections and dimensions from config file
    sOF=make_folder(outFolderPath,nList) #returns specific output folder


    csv_levels(levelListSM,sOF,combinedList) #generates csv file with levels
    csv_sub_inputs_pre(weightListSM,sOF) #generates csv file with subdimension inputs
    csv_dim_inputs_pre(dimensionListSM,sOF) #generates csv file with dimensions inputs
    logging.info("Report generation finished successfully")
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

def make_header():
    
    return -1

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
    outPath=os.path.join(sOF, "inputs_subdimensions_pre_transf.csv")
    verticalAdd.to_csv(outPath, index=True)
    return None

def csv_dim_inputs_pre(dL,sOF):
    outPath=os.path.join(sOF, "inputs_dimensions_pre_transf.csv")
    dL.to_csv(outPath, index=True)
    return None

def csv_levels(df,sOF,combL):
    verticalAdd= pd.concat(df,axis=0)
    verticalAdd.index=combL
    outPath=os.path.join(sOF, "levels.csv")
    verticalAdd.to_csv(outPath, index=True)
    return None