import configparser ## to import config files
import os

def test_program_files_present():
    assert os.path.isfile("config.ini")
    assert os.path.isfile("requirements.txt")
    assert os.path.isfile("run.py")

    assert os.path.isfile(os.path.join ("src","main.py"))

    assert os.path.isfile(os.path.join ("src","methods","data_import.py"))
    assert os.path.isfile(os.path.join ("src","methods","initialisation.py"))
    assert os.path.isfile(os.path.join ("src","methods","data_processing.py"))
    assert os.path.isfile(os.path.join ("src","methods","report_generator.py"))
    assert os.path.isfile(os.path.join ("src","methods","data_validation.py"))

def test_aditional_files_present():
    test_program_files_present()
    assert os.path.isfile("setup.py")
    assert os.path.isfile("README.md")
    assert os.path.isfile("LICENSE")
