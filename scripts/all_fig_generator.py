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
    parser.add_option('-c','--config', dest="config_path", help='path to the config yaml file to display the results',default='scripts/configs/')
    parser.add_option('-y','--share_y', action="store_false" ,dest="share_y", help='shareY, default true',default=True)
    
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def list_files(directory):
    output = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            output.append(os.path.join(root, file))
            # print(os.path.join(root, file))
    return output

def get_config_by_yaml(path):
    with open(path, "r") as input:
        try:
            options = yaml.safe_load(input)
            return options
            # print(a)
        except yaml.YAMLError as error:
            traceback.print_exc()
            print(error) 

if __name__ == '__main__':

    options = loadParameter()

    config_path = options.config_path
    file_list = list_files(config_path)
    share_y = options.share_y
    file_list.sort()

    for file_name in file_list:
        # print(file_name)
        if ".yaml" in file_name:
            # configs = get_config_by_yaml(file_name)
            fg = FigGenerator()
            fg.run(file_name,share_y)
