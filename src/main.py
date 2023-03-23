from src.methods import data_processing, data_validation, initialisation, report_generator,data_import_scratch
import time #to remove possibly as log time is enough
import logging


def main():
    logging.basicConfig(filename='runtime.log', level=logging.INFO, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Program started")
    start_time = time.time()

    mainFolderPath,configFileMain,hashL, xlsxList = initialisation.main()
    data_import_scratch.main(mainFolderPath,configFileMain, xlsxList)

    #dontforget to use hashList

    logging.info("Program ended")
    logging.info("Program runtime: " + f"{(time.time() - start_time):.2f}" + " seconds")
    #data_import.getFiles()
    #report_generator.main(mainFolderPath,configFileMain)
    
