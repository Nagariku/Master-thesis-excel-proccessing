from src.methods import data_processing, initialisation, data_import
import time #to remove possibly as log time is enough
import logging


def main():
    logging.basicConfig(filename='runtime.log', level=logging.INFO, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Program started")
    start_time = time.time()

    #initialisation
    mainFolderPath,configFileMain,hashL, xlsxList = initialisation.main()

    #get data
    levelListM,inputsSubListM, inputsDimListM, inputsInterDimensionalListM, kripSimpleListOutMain, kripInputListOutMain=data_import.main(mainFolderPath,configFileMain, xlsxList)

    #process data
    outputDataframeMain, DimConsistencyListMain, DimWeightListMain=data_processing.main(inputsSubListM, inputsDimListM)

    #report generation
    from src.methods import report_generator # to make global variable work
    report_generator.main(mainFolderPath,configFileMain,len(xlsxList),levelListM,inputsSubListM, inputsDimListM,
                           inputsInterDimensionalListM,outputDataframeMain, 
                            DimConsistencyListMain,DimWeightListMain,
                            kripSimpleListOutMain, kripInputListOutMain)


    logging.info("Program ended")
    logging.info("Program runtime: " + f"{(time.time() - start_time):.2f}" + " seconds")
    #data_import.getFiles()
    #report_generator.main(mainFolderPath,configFileMain)
    
