import pandas as pd
import xlrd
from configparser import ConfigParser
import os.path
import glob
from IPython.display import display

def getFiles():
    # Get the path of the current directory and add the folder name
    path = os.path.join(os.getcwd(), "Excel_surveys") ##doesn't work on excel other wise. This get directory from run to surveys
     # Get all the files in the folder
    csv_files = glob.glob(os.path.join(path, "*.xlsm"))
    # print(path)
    # print(csv_files)
    config_object = ConfigParser()
    config_object.read("config.ini")
    userinfo = config_object["Settings"]
    print("Deleting will {}".format(userinfo["deleteExcels"]))
    
    for f in csv_files:
    # read the csv file
        #df = pd.read_excel(f,usecols=[0,2])
        df = pd.read_excel(f,index_col=None, na_values=['NA'], usecols="B")
        print(df)
        # print the location and filename
        #print('Location:', f)
        #print('File Name:', f.split("\\")[-1])
        
        # print the content
        #print('Content:')
        #display(df)
        #print()

    return