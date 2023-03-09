import logging
import os

##############Main function##############
def main(mFP,cFM):
    logging.info("Report generation started")
    outFolderPath = check_output_folder(cFM.get("Settings", "outputFolder"),mFP)

    logging.info("Report generation finished successfully")





##############Sub functions##############

#File that generates the report

#make .csv of results

#maybe make pdf with graphs
def check_output_folder(folderName,pathFold): #check if excel survey folder exists
    joinedOutputPath = os.path.join(pathFold,folderName)
    if os.path.exists(joinedOutputPath):
        logging.info("Check: '" + folderName + "' folder exists in the main folder")
    else:
        logging.warning("Check: " + folderName + " doesn't exist in the main folder")
        os.mkdir(joinedOutputPath)
        logging.info("'" + folderName + "' folder created")
    return joinedOutputPath