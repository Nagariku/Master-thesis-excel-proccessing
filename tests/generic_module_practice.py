import ast
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Create an empty list to store the dictionaries
special_sheets_list = []

# Loop over all items in the special sheets dictionary and convert the string values to their appropriate data types using ast.literal_eval()
for key in config['Special_sheets']:
    special_sheets_list.append(eval(config['Special_sheets'][key]))

print(special_sheets_list)