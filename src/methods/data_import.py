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
    global subCompListy
    logging.info("M - Data import started")
    cC   = configFile.get("Settings", "comparisonColumn")[1:-1]
    lC   = configFile.get("Settings", "levelColumn")[1:-1]
    sR   = int(configFile.get("Settings", "startingRow"))
    cLG  = int(configFile.get("Settings", "comparisonLevelGap"))
    subCompListy, subCompNumList = extract_subdimensions(configFile)
    special_sheets_list = [] #list of special sheets

    for key in configFile['Special_sheets']:
        special_sheets_list.append(eval(configFile['Special_sheets'][key]))

    worksheetList = get_first_X_worksheet_names(xlList[0], len(subCompNumList))

    levelList,weightList, dimensionDF, interDimensionalList=start_import(xlList, worksheetList,
                                                                                                cC, sR,subCompNumList,cLG,lC,special_sheets_list)
    kripSimpleListOut, kripInputListOut = iterate_through_simple_krip(weightList,dimensionDF)


    logging.info("M - Data import finished successfully")
    return levelList,weightList, dimensionDF, interDimensionalList, kripSimpleListOut, kripInputListOut


def number_of_comparisions(n):
    return 0.5*n*(n-1)

def get_first_X_worksheet_names(file_path, num_sheets):
    warnings.simplefilter("ignore", category=UserWarning) #ignore warning about openpyxl
    workbook = openpyxl.load_workbook(file_path)
    sheet_names = workbook.sheetnames[:num_sheets]
    warnings.resetwarnings() #reset warning filter
    return sheet_names

def start_import(pathList, worksheetList, comparisonColumn, startingRow,subCompyList,comparisonLevelGap,levelColumn,SSList):
    #levelDF = get_levels(pathList, worksheetList, levelColumn, startingRow,subCompyList)
    #weightDF = get_weightings(pathList, worksheetList, comparisonColumn, startingRow,subCompyList,comparisonLevelGap)

    lList,wList, dimList, intDimList = get_data(pathList, worksheetList, levelColumn, comparisonColumn, startingRow,subCompyList,comparisonLevelGap,SSList)

    

    #verticalAdd= pd.concat(wList,axis=0) #join all dataframes vertically
    #print(get_krippendorff_DF(verticalAdd))
    #print(get_krippendorff_DF(pd.concat(lList,axis=0)))
    return lList , wList, dimList, intDimList

def concat_dataframes(list_of_lists):
    concatenated_dfs = []
    for dfs in list_of_lists:
        concatenated_dfs.append(pd.concat(dfs))
    return concatenated_dfs

def get_data(pathList, worksheetList, levelColumn, weightColumn, startingRow, subCompyList, comparisonLevelGap,sSL):
    logging.info("Level and weight and special sheet import started")

    levelList = [pd.DataFrame() for _ in range(len(worksheetList))]
    weightList = [pd.DataFrame() for _ in range(len(worksheetList))]
    dimensionList = pd.DataFrame() 
    interdimensionalList = pd.DataFrame() 
    
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

        sheet = xl.parse(sheet_name=sSL[0][0], skiprows=sSL[0][2]-2, usecols=sSL[0][1], nrows=sSL[0][3]-sSL[0][2]+1, names=[filename])
        sheet = sheet.applymap(lambda x: round(x, 4))
        dimensionList = pd.concat([dimensionList, sheet], axis=1)

        sheet = xl.parse(sheet_name=sSL[1][0], skiprows=sSL[1][2]-2, usecols=sSL[1][1], nrows=sSL[1][3]-sSL[1][2]+1, names=[filename])
        sheet = sheet.fillna(0)
        sheet = sheet.applymap(lambda x: round(x, 4))
        interdimensionalList = pd.concat([interdimensionalList,sheet], axis=1)
        xl.close()

    
    #print(interdimensionalList)
    logging.info("Level and weight and special sheet import finished successfully")
    return levelList, weightList, dimensionList, interdimensionalList

def get_krippendorff_DF(inDataFrame):
    data = inDataFrame.T.values.tolist()
    data_tuple = tuple(' '.join(map(str, row)) for row in data)
    if len(data_tuple) == 1:
        return 1 #if only one coder, return 1
    else:
        newlistconvert = [[round(-(1/float(val))+2, 4) if isinstance(val, (int, float)) and float(val) < 1 else round(float(val), 4)
                           if val != "*" and val != "N/A" else np.nan for val in coder.split()] for coder in data_tuple] 
                            #convert into continous scale, instead of 0.25 and so on


        unique_values = list(set([val for sublist in newlistconvert for val in sublist]))
        unique_values.sort()

        
        return (krippendorff.alpha(reliability_data=newlistconvert, level_of_measurement="interval")) # value_domain=unique_values
     
def generate_AHP(nOriginal):  #generate AHP
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
 
def simplify_krip(nWanted): #simplify krippendorff alpha
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

def extract_subdimensions(CF):
    subList = []
    for option in CF.options('Subcatergories'):
        value = eval(CF.get('Subcatergories', option))
        if option != '':
            subList.append(value)
    return subList, [len(l) for l in subList]

def replace_with_lists(num,odd_groups,my_wantedList): #replace with lists
    for sublist in odd_groups:
        if num in sublist:
            return my_wantedList[odd_groups.index(sublist)]
    raise ValueError(f"Number {num} not found in any sublist")

def iterate_through_simple_krip(weightList,dimDF):
    logging.info("Krippendorff simplified alpha calculation started")
    kripSimpleList = []
    kripInputList = []
    my_list= [3,5,9,17]

    for x in my_list:
        workInputList=[]
        workSimpleList=[]
        mWL,oG=simplify_krip(x)
        onlyDimensionSImplified=dimDF.applymap(lambda x: replace_with_lists(x, oG, mWL))
        workInputList.append(onlyDimensionSImplified) #dimension
        workSimpleList.append(get_krippendorff_DF(onlyDimensionSImplified)) #dimension

        for i,df in enumerate(weightList):
            dimensionSimplifiedListWork=df.applymap(lambda x: replace_with_lists(x, oG, mWL))
            workInputList.append(dimensionSimplifiedListWork)
            workSimpleList.append(get_krippendorff_DF(dimensionSimplifiedListWork))

        kripSimpleList.append(workSimpleList)
        kripInputList.append(workInputList)

    logging.info("Krippendorff simplified alpha calculation finished successfully")
    return kripSimpleList, kripInputList
