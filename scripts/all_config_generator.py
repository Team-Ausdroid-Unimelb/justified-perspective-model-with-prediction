import pymongo
import os
import json
import pandas as pd
import yaml
from optparse import OptionParser
import sys
import itertools
import traceback
from fig_generator import FigGenerator
import matplotlib.pyplot as plt

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python experiment_runner.py <options>
    EXAMPLES:   (1) 



    """
    
    # logger.info("Parsing Options")
    parser = OptionParser(usageStr)
    parser.add_option('-c','--config', dest="config_path", help='path to the config yaml file to display the results',default='scripts/configs/bbl')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def list_files(directory):
    output = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            output.append(os.path.join(root, file))
    return output

if __name__ == '__main__':

    options = loadParameter()

    config_path = options.config_path
    file_list = list_files(config_path)

    fg = FigGenerator()
    domain_list = ['coin','spcoin','sn','grapevine','corridor']
    for domain_name in domain_list:
        for file_name in file_list:
            if ".yaml" in file_name:
                with open(file_name, 'r') as file:
                    content = file.read()
                new_file_name = file_name.replace('bbl',domain_name)
                new_content = content.replace('bbl',domain_name)
                new_file_folder = os.path.split(new_file_name)[0]
                # print(new_file_name)
                # print(new_content)
                if not os.path.exists(new_file_folder):
                    os.makedirs(new_file_folder)
                with open(new_file_name,'w') as f:
                    f.write(new_content)

