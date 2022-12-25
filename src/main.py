from src.methods import calculations,reporting,validation

import pandas as pd
import xlrd

import os
import glob
from IPython.display import display



def main():
    path = os.getcwd()
    path+= "\\Excel_surveys"
    csv_files = glob.glob(os.path.join(path, "*.xlsx"))
    #print(path)
    #print(csv_files)
    
    
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
    
