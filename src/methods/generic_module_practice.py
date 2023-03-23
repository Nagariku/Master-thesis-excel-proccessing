import data_processing, data_validation, initialisation, report_generator


mainFolderPath,configFileMain = initialisation.main()
report_generator.main(mainFolderPath,configFileMain)