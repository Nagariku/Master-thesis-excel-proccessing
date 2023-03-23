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

def practice_ahp():
    return -1


def number_of_comparisions(n):
    return 0.5*n*(n-1)

def get_first_X_worksheet_names(file_path, num_sheets):
    warnings.simplefilter("ignore", category=UserWarning) #ignore warning about openpyxl
    workbook = openpyxl.load_workbook(file_path)
    sheet_names = workbook.sheetnames[:num_sheets]
    warnings.resetwarnings() #reset warning filter
    return sheet_names

def start_import(pathList, worksheetList, comparisonColumn, startingRow,subCompyList,comparisonLevelGap,levelColumn):
    #levelDF = get_levels(pathList, worksheetList, levelColumn, startingRow,subCompyList)
    #weightDF = get_weightings(pathList, worksheetList, comparisonColumn, startingRow,subCompyList,comparisonLevelGap)

    lList,wList = get_levels_and_weightings(pathList, worksheetList, levelColumn, comparisonColumn, startingRow,subCompyList,comparisonLevelGap)

    print(get_krippendorff_DF(pd.concat(wList,axis=0)))
    mWL,oG=simplify_krip(3)
    for i, df in enumerate(wList):
        wList[i] = df.applymap(lambda x: replace_with_lists(x, oG, mWL))


    verticalAdd= pd.concat(wList,axis=0) #join all dataframes vertically
    print(get_krippendorff_DF(verticalAdd))
    print(get_krippendorff_DF(pd.concat(lList,axis=0)))

def get_levels_and_weightings(pathList, worksheetList, levelColumn, weightColumn, startingRow, subCompyList, comparisonLevelGap):
    logging.info("Level and weight import started")
    levelList = [pd.DataFrame() for _ in range(len(worksheetList))]
    weightList = [pd.DataFrame() for _ in range(len(worksheetList))]
    
    for filePath in pathList:
        filename = os.path.splitext(os.path.basename(filePath))[0]
        xl = pd.ExcelFile(filePath)
        
        for i in range(len(worksheetList)):
            sheet = xl.parse(sheet_name=worksheetList[i], skiprows=startingRow-2, usecols=levelColumn, nrows=subCompyList[i], names=[filename])
            levelList[i] = pd.concat([levelList[i], sheet], axis=1)
            
            if number_of_comparisions(subCompyList[i]) != 0:
                sheet = xl.parse(sheet_name=worksheetList[i], skiprows=startingRow+comparisonLevelGap+subCompyList[i]-3, usecols=weightColumn, nrows=number_of_comparisions(subCompyList[i]), names=[filename])
                sheet = sheet.applymap(lambda x: round(x, 4))
                weightList[i] = pd.concat([weightList[i], sheet], axis=1)
        xl.close()

    logging.info("Level and weight import finished successfully")
    return levelList, weightList

def get_krippendorff_DF(inDataFrame):
    data = inDataFrame.T.values.tolist()
    data_tuple = tuple(' '.join(map(str, row)) for row in data)
    newlistconvert =[[np.nan if (v == "*" or v=="N/A") else v for v in coder.split()] for coder in data_tuple]
    return (krippendorff.alpha(reliability_data=newlistconvert,level_of_measurement="nominal"))
     
def generate_AHP(nOriginal): 
    my_list = []
    median=(nOriginal-1)/2
    for i in range(1, nOriginal+1):
        if i <= median+1:
            my_list.append(1/i)
        else:
            my_list.append(i-(median))
    my_list = [round(x, 4) for x in my_list]
    my_list.sort()
    return my_list

def simplify_krip(nWanted):
    my_list=generate_AHP(17) ###important! AHP
    my_wantedList=generate_AHP(nWanted)
    median = my_list[int(len(my_list)/2)]

    # Create a list of odd numbers that does not contain the median
    odd_numbers_no_median = [num for num in my_list if num != median]

    # Compute the number of odd numbers per group
    num_odd_per_group = math.ceil(len(odd_numbers_no_median) / (nWanted - 1))

    # Create sub-lists of the desired size, with the median in a separate group
    odd_groups = [[num] for num in my_list if num == median] + \
             [odd_numbers_no_median[i:i+num_odd_per_group] for i in range(0, len(odd_numbers_no_median), num_odd_per_group)]
    odd_groups.sort()
    return my_wantedList,odd_groups
    
def replace_with_lists(num,odd_groups,my_wantedList):
    for sublist in odd_groups:
        if num in sublist:
            return my_wantedList[odd_groups.index(sublist)]
    raise ValueError(f"Number {num} not found in any sublist")