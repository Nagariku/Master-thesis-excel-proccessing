import os
import string
import random
import hashlib
import pytest
import configparser
from datetime import datetime
from openpyxl import Workbook

from src.methods import initialisation

#config file
config_file = "config.ini"
config_object = configparser.ConfigParser()
config_object.read(config_file)

def generate_unique_xlsx_files(folder_path, n): ## generate n unique xlsx files in a folder and return their hashes
    hash_files = []
    for i in range(n):
        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while os.path.exists(os.path.join(folder_path, file_name + '.xlsx')):
            file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        file_path = os.path.join(folder_path, file_name + '.xlsx')
        wb = Workbook()
        ws = wb.active
        random_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
        ws["A1"] = random_string # type: ignore
        wb.save(file_path)
    
        with open(file_path, "rb") as f:
            original_file_hash = hashlib.md5(f.read()).hexdigest()
            hash_files.append(original_file_hash)
    return hash_files

def count_xlsx_files(folder_path): ## count the number of xlsx files in a folder
    xlsx_count = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            xlsx_count += 1
    return xlsx_count

def remove_matching_xlsx_files(directory_path, hash_array): ## remove files with same hash as the ones in the array
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'rb') as f:
                file_data = f.read()
            file_hash = hashlib.md5(file_data).hexdigest()
            if file_hash in hash_array:
                os.remove(file_path)

def test_fileGeneration(): ## test if the files are generated correctly and if the hashes are unique 
    mainfolderPath = os.getcwd()
    inputFolderPath = initialisation.check_input_folder(config_object.get("Settings", "inputFolder"),mainfolderPath)
    nBefore=count_xlsx_files(inputFolderPath)
    hash_files = generate_unique_xlsx_files(inputFolderPath, 10)
    initialisation.ensure_unique_xlsx_names(inputFolderPath)
    remove_matching_xlsx_files(inputFolderPath, hash_files)
    nAfter=count_xlsx_files(inputFolderPath)
    assert nBefore==nAfter
