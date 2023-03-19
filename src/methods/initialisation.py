import configparser ## to import config files
import ast # to convert config files to list
import logging  # to write log to log file
import sys # to quit program
import os # to get folder path
import fnmatch # to get files with specific extension
import hashlib # to get md5 hash of file
import random
import string


global folderPath

#################  Main  #################
def main():
    logging.info("Initialisation started")
    mainfolderPath = os.getcwd()
    cf=get_config_file()
    inputFolderPath = check_input_folder(cf.get("Settings", "inputFolder"),mainfolderPath)
    check_excel_files(inputFolderPath)
    updatedFileList=ensure_unique_xlsx_names(inputFolderPath)
    hashFiles=check_file_hash(updatedFileList)
 # comment out if not going to use
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
    return None

def check_file_hash(fileList):
    hash_dict = {}
    error=False
    for file_path in fileList:
        with open(file_path, "rb") as f:
            file_contents = f.read()
        file_hash = hashlib.sha256(file_contents).hexdigest()
        if file_hash in hash_dict:
            file_name = os.path.basename(file_path)
            duplicate_file_name = os.path.basename(hash_dict[file_hash])
            error_msg = f"Error: '{file_name}' has the same hash as '{duplicate_file_name}'"
            logging.error(error_msg)
            error=True
            
        else:
            hash_dict[file_hash] = file_path
    #if error:
    #    logging.log(logging.CRITICAL,"Program aborted")
    #    sys.exit()
    logging.info("No repeating hashes found")
    return [v for v in hash_dict.values()]

def ensure_unique_xlsx_names(folder_path): ## should be ok for 36^8 files = 2.8e+13 files
    changed=False # switch to see if any files have been changed
    fileList = os.listdir(folder_path) # get list of files in folder
    full_path_list = [os.path.join(folder_path, s) for s in fileList if s.endswith('.xlsx')] # get full path of files in folder wiuth .xlsx extension
 
    for i, file_path in enumerate(full_path_list): # loop through files
        file_name = os.path.splitext(os.path.basename(file_path))[0] # get file name without extension

        if len(file_name) == 9 and file_name[4] == '-' and all(c in string.hexdigits or c in string.ascii_uppercase for c in file_name[:4]) and all(c in string.hexdigits or c in string.ascii_uppercase for c in file_name[5:]): 
            # Check if the file name is already a random name with two strings of length 4 separated by a '-' and if the file name already exists
            continue  # Skip renaming

        while True: # loop until a unique name is found
            changed=True # change switch to true
            # Generate two different random strings of length 4 
            random_string_1 = "".join(random.choices(string.ascii_uppercase + string.digits, k=4)) # generate random string
            random_string_2 = "".join(random.choices(string.ascii_uppercase + string.digits, k=4)) # generate random string
            while random_string_2 == random_string_1: # check if the two random strings are the same
                random_string_2 = "".join(random.choices(string.ascii_uppercase + string.digits, k=4)) # generate random string

            # Create the new file name with the two random strings separated by a '-'
            new_file_name = f"{random_string_1}-{random_string_2}" # create new file name

            # Check if the new file name already exists
            if not os.path.exists(os.path.join(folder_path, new_file_name + '.xlsx')): # check if file name already exists
                break  # Break the loop if the new file name does not exist

        # Rename the file
        os.rename(file_path, os.path.join(folder_path, new_file_name + '.xlsx')) # rename file
        logging.info(f"File \"{file_name}.xlsx\" has been renamed to \"{new_file_name}.xlsx\"") # log rename

    if changed: # if any files have been changed
            fileList = os.listdir(folder_path) # get list of files in folder 
            return [os.path.join(folder_path, s) for s in fileList if s.endswith('.xlsx')]     # get full path of files in folder with .xlsx extension
    return full_path_list # return updated list of files in folder with .xlsx extension