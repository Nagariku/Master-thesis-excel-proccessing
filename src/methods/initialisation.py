import configparser ## to import config files
import ast # to convert config files to list
import logging  # to write log to log file
import sys # to quit program
import os # to get folder path
import fnmatch # to get files with specific extension


global folderPath

#################  Main  #################
def main():
    logging.info("Initialisation started")
    mainfolderPath = os.getcwd()
    cf=get_config_file()
    inputFolderPath = check_input_folder(cf.get("Settings", "inputFolder"),mainfolderPath)
    check_excel_files(inputFolderPath)
    logging.info("Initialisation finished successfully")
    return mainfolderPath,cf


#################  Methods  #################
def get_config_file():
    #get config files from config.ini
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    if check_special_worksheet_length(config_object):
        logging.info("Check: Special sheets lengths are correct")
    else:
        logging.log(logging.CRITICAL, "Program aborted")
        sys.exit()
    return config_object

def check_special_worksheet_length(config_obj): 
    boolCheck = True
    listOfSpecial = config_obj.items("Special sheets")
    for key, value in listOfSpecial:
        convertedList = ast.literal_eval(value)
        if ((len(convertedList)-1)%3) != 0:
            logging.log(logging.CRITICAL, "Length of: " + key + " is not correct, make sure that [(length of " + key+ ")-1]%3 = 0")
            boolCheck =False
    return boolCheck

def check_input_folder(folderName,pathFold): #check if excel survey folder exists
    joinedPath = os.path.join(pathFold,folderName)
    if os.path.exists(joinedPath):
        logging.info("Check: " + folderName + " exists in the main folder")
    else:
        logging.critical("Check: " + folderName + " doesn't exist in the main folder")
        os.mkdir(joinedPath)
        logging.info("" + folderName + " created")
        logging.info("Please add Excels to abovementioned folder")
        logging.critical("Program aborted")
        sys.exit()
    return joinedPath

def check_excel_files(iFP):
    pattern = "*.xlsx"
    fileList = os.listdir(iFP)
    xlsx_files = [filename for filename in fileList if fnmatch.fnmatch(filename, pattern)]
    if len(xlsx_files) > 0:
        logging.info("The Excel folder contains {} .xlsx file(s):".format(len(xlsx_files)))
    else:
        logging.log(logging.CRITICAL,"0 Excels found in input folder")
        logging.log(logging.CRITICAL,"Please add Excels to input folder")
        logging.log(logging.CRITICAL,"Program aborted")
        sys.exit()
    return True