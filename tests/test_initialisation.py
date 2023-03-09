import configparser ## to import config files
import os
from src.methods import initialisation

config_file = "config.ini"
config_object = configparser.ConfigParser()
config_object.read(config_file)

########## TESTS FOR CONFIG FILE ##########

def test_special_sheets_length():
    assert (initialisation.check_special_worksheet_length(config_object)==True)
