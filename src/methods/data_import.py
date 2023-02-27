import pandas as pd
import xlrd
from configparser import ConfigParser
import os.path
import glob
from IPython.display import display
#import krippendorff


#to be done by greg

def get_config_files():
    #to obtain rows used and other settings
    return None


def getFiles():
    # Get the path of the current directory and add the folder name
    path = os.path.join(os.getcwd(), "Excel_surveys") ##doesn't work on excel other wise. This get directory from run to surveys
     # Get all the files in the folder
    csv_files = glob.glob(os.path.join(path, "*.xlsx"))
    # print(path)
    # print(csv_files)
    config_object = ConfigParser()
    config_object.read("config.ini")
    userinfo = config_object["Settings"]
    print("Deleting will happen: {}".format(userinfo["deleteExcels"]))

    technologyResponseList=[]
    humanResponseList = []
    
    for f in csv_files:
    # read the csv file
        #df = pd.read_excel(f,usecols=[0,2])
        technologyResponse = pd.read_excel(f,index_col=None, sheet_name="4.Technology", skiprows=13, nrows= 15, usecols="C",header =None)
        humanResponse = pd.read_excel(f,index_col=None, sheet_name="5.Human", skiprows=10, nrows= 5, usecols="C",header=None)
        
        technologyResponseList.append(technologyResponse)
        humanResponseList.append(humanResponse)
        #df2 = pd.read_excel(f,index_col=None, sheet_name=3, skiprows=13, nrows= 14, names=["Original", "Improtance chosen", "Comparison to"],usecols="B:D")
        #print ("\n Levelling")
        #print(df)
        #print ("\n Weighting")
        #print(df2)
        technologyResponsePD = pd.concat(technologyResponseList,axis=1)
        humanResponsePD = pd.concat(humanResponseList,axis=1)

        tR=technologyResponsePD.values
        hR = humanResponsePD.values

        # print the location and filename
        print('Location:', f)
        print('File Name:', f.split("\\")[-1])
        
        # print the content
        
    print('Content:')
    print("TechList")
    display(tR)
    print("HumanList")
    display(hR)

    #print("Krippendorff's alpha for interval metric: ", krippendorff.alpha(value_counts=tR))
    #print("Krippendorff's alpha for interval metric: ", krippendorff.alpha(value_counts=hR))
    print()
    return