from src.methods import data_processing, data_import, data_validation, initialisation, report_generator
import logging


def main():
    logging.basicConfig(filename='runtime.log', level=logging.INFO, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Program started")

    mainFolderPath,configFileMain = initialisation.main()
    logging.info("Program ended")
    #data_import.getFiles()
    #report_generator.main(mainFolderPath,configFileMain)
    
