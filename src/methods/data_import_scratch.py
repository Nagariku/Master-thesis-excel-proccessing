import configparser ## to read config files
import logging
import pandas as pd
import openpyxl
import warnings
import krippendorff
import numpy as np
import os
import math


####### Main #######



def main(inputFolder,  configFile,xlList):
    logging.info("M - Data import started")
    cC   = configFile.get("Settings", "comparisonColumn")[1:-1]
    lC   = configFile.get("Settings", "levelColumn")[1:-1]
    sR   = int(configFile.get("Settings", "startingRow"))
    cLG  = int(configFile.get("Settings", "comparisonLevelGap"))
    subCompList = eval(configFile.get("Settings", "numberOfSubComponents"))

    worksheetList = get_first_X_worksheet_names(xlList[0], len(subCompList))

    start_import(xlList, worksheetList, cC, sR,subCompList,cLG,lC)




 

    logging.info("M - Data import finished successfully")
    return None




def number_of_comparisions(n):
    return 0.5*n*(n-1)

def get_first_X_worksheet_names(file_path, num_sheets):
    warnings.simplefilter("ignore", category=UserWarning) #ignore warning about openpyxl
    workbook = openpyxl.load_workbook(file_path)
    sheet_names = workbook.sheetnames[:num_sheets]
    warnings.resetwarnings() #reset warning filter
    return sheet_names

def start_import(pathList, worksheetList, comparisonColumn, startingRow,subCompyList,comparisonLevelGap,levelColumn):
    levelDF = get_levels(pathList, worksheetList, levelColumn, startingRow,subCompyList)
    weightDF = get_weightings(pathList, worksheetList, comparisonColumn, startingRow,subCompyList,comparisonLevelGap)


    print(weightDF)


def get_levels(pathList, worksheetList, levelColumn, startingRow,subCompyList):
    logging.info("Level import started")
    levelList = [pd.DataFrame() for _ in range(len(worksheetList))]
    for filePath in pathList:
        filename = os.path.splitext(os.path.basename(filePath))[0]
        for i in range(len(worksheetList)):
            sheet = pd.read_excel(filePath, index_col=None, sheet_name=worksheetList[i], skiprows=startingRow-2,
                                  nrows=subCompyList[i], usecols=levelColumn, names=[filename]) # can remove names , jsut for debugging # mess because some empty rows
            levelList[i] = pd.concat([levelList[i], sheet], axis=1)
    logging.info("Level import finished successfully")
    return levelList

def get_weightings(pathList, worksheetList, weightColumn, startingRow,subCompyList,comparisonLevelGap):
    logging.info("Weight import started")
    weightList = [pd.DataFrame() for _ in range(len(worksheetList))]
    for filePath in pathList:
        filename = os.path.splitext(os.path.basename(filePath))[0]
        for i in range(len(worksheetList)):
            if (number_of_comparisions(subCompyList[i])) == 0:
                continue
            sheet = pd.read_excel(filePath, index_col=None, sheet_name=worksheetList[i], skiprows=startingRow+comparisonLevelGap+subCompyList[i]-3,
                                  nrows=number_of_comparisions(subCompyList[i]), usecols=weightColumn, names=[filename]) # mess because some empty rows
            sheet= sheet.applymap(lambda x: round(x, 4))
            weightList[i] = pd.concat([weightList[i], sheet], axis=1)
    print(weightList[1])


    logging.info("Weight import finished successfully")
    return weightList

def get_krippendorff_DF(inDataFrame):
    data = inDataFrame.T.values.tolist()
    data_tuple = tuple(' '.join(map(str, row)) for row in data)
    #print(data_tuple)
    newlistconvert =[[np.nan if (v == "*" or v=="N/A") else v for v in coder.split()] for coder in data_tuple]
    #print(krippendorff.alpha(reliability_data=newlistconvert,level_of_measurement="nominal"))
    return None