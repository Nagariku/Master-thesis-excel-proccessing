from src.methods import data_processing, data_validation, initialisation, data_import
import time #to remove possibly as log time is enough
import logging


def main():
    logging.basicConfig(filename='runtime.log', level=logging.INFO, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Program started")
    start_time = time.time()

    mainFolderPath,configFileMain,hashL, xlsxList = initialisation.main()
    levelListM,weightListM, dimensionListM, interDimensionalListM, kripSimplifiedListM=data_import.main(mainFolderPath,configFileMain, xlsxList)
    #data_processing.main(testVar)
    #dontforget to use hashList

    from src.methods import report_generator # to make global variable work
    report_generator.main(mainFolderPath,configFileMain,len(xlsxList),levelListM,weightListM, dimensionListM, interDimensionalListM, kripSimplifiedListM)

    logging.info("Program ended")
    logging.info("Program runtime: " + f"{(time.time() - start_time):.2f}" + " seconds")
    #data_import.getFiles()
    #report_generator.main(mainFolderPath,configFileMain)
    
