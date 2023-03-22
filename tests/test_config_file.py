import configparser ## to import config files
import os
from src.methods import initialisation

config_file = "config.ini"
config_object = configparser.ConfigParser()
config_object.read(config_file)

def test_config_file_exists():
    assert os.path.isfile(config_file)

def test_delete_excles_exists():

    assert bool(config_object.get("Settings", "deleteExcels")) == True

def test_numberOfDataSheets_is_posInt():
    n = int(config_object.get("Settings", "numberOfDataSheets"))
    assert (type(n)==int and n>0) 

def test_startingRow_is_posInt():
    n = int(config_object.get("Settings", "startingRow"))
    assert (type(n)==int and n>0)

def test_comparisonColumn_string():
    assert(len(eval(config_object.get("Settings", "comparisonColumn")))==1 and eval(config_object.get("Settings", "comparisonColumn")).isalpha())

def test_levelColumn_string():
    assert(len(eval(config_object.get("Settings", "levelColumn")))==1 and eval(config_object.get("Settings", "levelColumn")).isalpha())

def test_comparisonLevelGap_is_Int():
    n = int(config_object.get("Settings", "comparisonLevelGap"))
    assert (type(n)==int)  #and ((n > 0) is True))

def test_settings_exists():
    assert (config_object.has_section('Settings'))

def test_settings_exists():
    assert (config_object.has_section('Special sheets'))

def test_input_folder_exists():
    assert (config_object.get("Settings", "inputFolder"))

def test_output_folder_exists():
    assert (config_object.get("Settings", "outputFolder"))

def test_special_sheets_length():
    assert (initialisation.check_special_worksheet_length(config_object)==True)

def test_num_subcomponents():
    assert len(eval(config_object.get("Settings", "numberOfSubComponents"))) ==int(config_object.get("Settings", "numberOfDataSheets"))