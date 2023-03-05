












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
    
    logger.info("Parsing Options")
    parser = OptionParser(usageStr)
    
    parser.add_option('-t', '--timeout', dest="timeout", help='timeout, default 300s', type='int', default=300)
    parser.add_option('-o','--output', dest="output_dir", help='output directory for the running results (default: output)',default='output/')
    parser.add_option('-s', '--search', dest="search_name", help='the name of the search algorithm', default='bfs')
    parser.add_option('-d','--debug', dest="enable_debug", action='store_true', help='enable logging level to debug', default=False)

    # parser.add_option('-s','--savefiles', action='store_true', help='keep the student repos', default=False)
    # parser.add_option('--tag', help='the tag for submission', default='submission')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

if __name__ == '__main__':

    timestamp = datetime.datetime.now().astimezone(TIMEZONE).strftime(DATE_FORMAT)

    options = loadParameter()
    
    if not os.path.isdir(options.output_dir):
        os.mkdir(options.output_dir)
    
    if options.enable_debug:
            debug_level = logging.DEBUG
    else:
        debug_level = logging.INFO    
    
    # Set up root logger, and add a file handler to root logger
    logging.basicConfig(filename = f'options.output_dir/{timestamp}_main.log',
                        level = debug_level,
                        format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    logger = logging.getLogger("LOGGER_NAME")
    
    
    
    
    
    
    
    
    start_time = datetime.datetime.now().astimezone(TIMEZONE)
    
    
    # load pddl files
    logger.info(f'loading problem.pddl')
    domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name= pddl_parser.problemParser(options.problem)
    logger.info(f'loading domain.pddl')
    actions,domain_name = pddl_parser.domainParser(f"{options.domain}")
    
    logger.info(f'loading external function')
    external = None
    external_class = options.external.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
    try:
        search_algorithm = importlib.import_module(f"search.{options.search}")
    except (NameError, ImportError, IOError):
        traceback.print_exc()
        pass
    except:
        pass

    try:
        external = importlib.import_module(external_class)
    except (NameError, ImportError, IOError):
        traceback.print_exc()
        pass
    except:
        pass
    
    logger.info(f'initialize problem')
    problem = pddl_model.Problem(domains,i_state,g_states,agent_index,obj_index,variables,actions,external)
    
    # print(problem)
    
    # import search
    logger.info(f'starting search')
    
    start_search_time = datetime.datetime.now().astimezone(TIMEZONE)
    print(search_algorithm.searching(problem,external.filterActionNames))
    end_search_time = datetime.datetime.now().astimezone(TIMEZONE)
    logger.info(f'initialization time: {start_search_time - start_time }')
    logger.info(f'search time: {end_search_time - start_search_time }')
    # print(problem.domains)
    # print(problem.initial_state)
    # print(problem.goal_states)
    # print(problem.entities)
    # print(problem.variables)
    # print(problem.actions)
    
    # import bbl
    
    # bbl.checkVisibility(problem,problem.initial_state,'a','v-p')
    
    # import coin
    
    
    # eq_list = []
    # for eq_str,value in problem.goal_states["epistemic_g"]:
    #     eq_list.append((epistemic_model.generateEpistemicQuery(eq_str),value))
    
    
    # for eq,value in eq_list:
    #     # print(eq)
    #     print(util.displayEQuery(eq))
    #     # s_0 = {'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
    #     # s_1 = {'dir-a': 'sw', 'dir-b': 'n', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
    #     # print(model.checkingEQ(problem,eq,[({'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'},""),(problem.initial_state,"a1")],problem.initial_state))
    #     # print(model.checkingEQ(problem,eq,[(s_0,"")],s_0))
        
    #     s_0 = {'peeking-a': 'f','peeking-b': 'f', 'face-c': 'head'}
    #     s_1 = {'peeking-a': 't','peeking-b': 'f', 'face-c': 'head'}
    #     s_2 = {'peeking-a': 'f','peeking-b': 't', 'face-c': 'head'}
    #     s_3 = {'peeking-a': 'f','peeking-b': 'f', 'face-c': 'head'}
    #     s_4 = {'peeking-a': 'f','peeking-b': 't', 'face-c': 'tail'}
    #     # s_5 = {'peeking-a': 'f','peeking-b': 'f', 'face-c': 'tail'}
        
        
    #     print(epistemic_model.checkingEQ(problem.external,eq,[(s_0,""),(s_1,""),(s_2,""),(s_3,""),(s_4,"")],s_4,problem.entities,problem.variables))
        
        
        
        
        