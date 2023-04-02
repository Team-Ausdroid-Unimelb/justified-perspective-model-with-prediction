












# This file is created by Guang Hu for running the tournament with cluster manager

import copy
import datetime
import importlib
import json
import os

import sys
import time
import traceback
from optparse import OptionParser
import pytz




import logging


import pddl_model
import epistemic_model
import pddl_parser
import util
import instance_runner

TIMEZONE = pytz.timezone('Australia/Melbourne')
DATE_FORMAT = '%d-%m-%Y_%H-%M-%S'



# Set up root logger, and add a file handler to root logger
# logging.basicConfig(filename = f'logs/{timestamp}.log',
#                     level = logging.INFO,
#                     format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# logger = logging.getLogger("runner")
LOGGER_NAME = "experiment_runner"

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
    
    parser.add_option('-t', '--timeout', dest="timeout", help='timeout, default 300s', type='int', default=300)
    parser.add_option('-o','--output', dest="output_path", help='output directory for the running results (default: output/<timestamp>)',default='')
    parser.add_option('-s', '--search', dest="search_path", help='the name of the search algorithm', default='bfs')
    # parser.add_option('-d','--debug', dest="log_debug", action='store_true', help='enable logging level to debug', default=False)
    parser.add_option('--log_debug', dest="log_debug", action='store_true', help='enable logging level to debug', default=False)
    # parser.add_option('--time_debug', dest="time_debug", action='store_true', help='enable logging level to debug', default=False)
    # parser.add_option('-i','--input', dest="input_path", help='input directory for the experiments (default: examples/*)',default='examples')
    parser.add_option('-i','--input', dest="input_domain_names", help='input for the experiment config (default: examples/*)',default='examples/CONFIG')

    # parser.add_option('-s','--savefiles', action='store_true', help='keep the student repos', default=False)
    # parser.add_option('--tag', help='the tag for submission', default='submission')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

if __name__ == '__main__':

    start_time = datetime.datetime.now().astimezone(TIMEZONE)

    options = loadParameter()
    output_path = options.output_path
    if output_path == '':
        output_path = f"output/{start_time.strftime(DATE_FORMAT)}"
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    
    if options.log_debug:
        debug_level = logging.DEBUG
    else:
        debug_level = logging.INFO    
    
    # Set up root logger, and add a file handler to root logger
    # logging.basicConfig(filename = f'{output_path}/main.log',
    #                     level = debug_level,
    #                     format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    # logger = logging.getLogger(LOGGER_NAME)
    handler = util.setup_log_handler(f'{output_path}/main.log')
    print(handler)
    logger = util.setup_logger(LOGGER_NAME,handler,debug_level)
    
    
    # loading search algorithm
    search = options.search_path
    search_name = search
    if '\\' in search:
        search_name = search.split('\\')[-1].replace('.py','')
    elif '/' in search:
        search_name = search.split('/')[-1].replace('.py','')   
        
    if type(search) ==str:
        logger.info(f"loading search algorithm: {search}")
        search_path = search
        search_path = search_path.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
        
        try:
            search = importlib.import_module(search_path)
            logger.info(f"finish loading search algorithm:")
        except (NameError, ImportError, IOError):
            traceback.print_exc()
            exit()
        except:
            traceback.print_exc()
            exit()
    else:
        logger.info(f"Search algorithm exists")
    
    
    domain_name_list = []
    example_folder_path = ""
    try:
        with open(options.input_domain_names, 'r') as f:
            domain_name_str = f.readline()
            domain_name_list = domain_name_str.split(" ")
        directory_breaker = "/"
        example_folder_path = directory_breaker.join(options.input_domain_names.split("/")[:-1])
        for domain_name in domain_name_list:
            if not os.path.exists(f"{example_folder_path}/{domain_name}"):
                raise FileNotFoundError(f"{example_folder_path}/{domain_name}")
    except:
        traceback.print_exc()
        exit()
    
    
    for domain_name in domain_name_list:
        problem_folder = f"{example_folder_path}/{domain_name}"
        domain_path = f"{problem_folder}/domain.pddl"
        external_path = f"{problem_folder}/{domain_name}.py"
        
        
        # loading external function
        external_function = external_path
        # logger.info(f"loading external function: {external_path}")
        # external_path = external_path.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
        # try:
        #     external_function = importlib.import_module(external_path)
        #     logger.info(f"finish loading external function")
        # except (NameError, ImportError, IOError):
        #     traceback.print_exc()
        #     exit()
        # except:
        #     traceback.print_exc()
        #     exit()

        for problem_name in os.listdir(problem_folder):
            if '.pddl' in problem_name and not problem_name == 'domain.pddl':
                problem_path = f"{problem_folder}/{problem_name}"
                instance_name = f"{search_name}_{domain_name}_{problem_name}"
                logger.info(f"solving {instance_name} - {problem_folder}")
                start_time = datetime.datetime.now().astimezone(TIMEZONE)
                ins = instance_runner.Instance(instance_name=instance_name,problem_path=problem_path,domain_path=domain_path,external_function= external_function,search= search)
                ins.solve(timeout=options.timeout,log_debug = options.log_debug, output_path = output_path)
                end_time = datetime.datetime.now().astimezone(TIMEZONE)
                used_time = end_time - start_time
                logger.info(f"solving time: {used_time}")
    
    
    
    
    # # loading external function
    # external_function = options.external
    # if type(external_function) ==str:
    #     logger.info(f"loading external function: {self.external_function}")
    #     external_path = self.external_function
    #     external_path = external_path.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
    #     try:
    #         self.external_function = importlib.import_module(external_path)
    #         logger.info(f"finish loading external function")
    #     except (NameError, ImportError, IOError):
    #         traceback.print_exc()
    #         exit()
    #     except:
    #         traceback.print_exc()
    #         exit()
    # else:
    #     logger.info(f"External function exists")
    
    # # load pddl files
    # logger.info(f'loading problem.pddl')
    # domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name= pddl_parser.problemParser(options.problem)
    # logger.info(f'loading domain.pddl')
    # actions,domain_name = pddl_parser.domainParser(f"{options.domain}")
    
    # logger.info(f'loading external function')
    # external = None
    # external_class = options.external.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
    # try:
    #     search = importlib.import_module(f"search.{options.search}")
    # except (NameError, ImportError, IOError):
    #     traceback.print_exc()
    #     pass
    # except:
    #     pass

    # try:
    #     external = importlib.import_module(external_class)
    # except (NameError, ImportError, IOError):
    #     traceback.print_exc()
    #     pass
    # except:
    #     pass
    
    # logger.info(f'initialize problem')
    # problem = pddl_model.Problem(domains,i_state,g_states,agent_index,obj_index,variables,actions,external)
    
    # # print(problem)
    
    # # import search
    # logger.info(f'starting search')
    
    # start_search_time = datetime.datetime.now().astimezone(TIMEZONE)
    # print(search.searching(problem,external.filterActionNames))
    # end_search_time = datetime.datetime.now().astimezone(TIMEZONE)
    # logger.info(f'initialization time: {start_search_time - start_time }')
    # logger.info(f'search time: {end_search_time - start_search_time }')
  
        