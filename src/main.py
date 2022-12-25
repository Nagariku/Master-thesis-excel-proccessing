from src.methods import calculations,reporting,validation

import pandas as pd
import xlrd

import os.path
import glob
from IPython.display import display



def main():
    # Get the path of the current directory and add the folder name
    path = os.path.join(os.getcwd(), "Excel_surveys")
     # Get all the files in the folder
    csv_files = glob.glob(os.path.join(path, "*.xlsx"))
    # print(path)
    # print(csv_files)
    
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
    
