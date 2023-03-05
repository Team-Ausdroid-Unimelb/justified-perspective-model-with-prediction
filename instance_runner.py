












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
LOGGER_NAME = "instance_runner"


class Instance:
    problem_path = ""
    domain_path = ""
    instance_name = ""
    external_function = None
    search_algorithm = None
    
    def __init__(self,instance_name="",problem_path="",domain_path="",external_function= "",search_algorithm= ""):
        self.instance_name = instance_name
        self.problem_path = problem_path
        self.domain_path = domain_path
        self.external_function = external_function
        self.search_algorithm = search_algorithm

    def solve(self,timeout=300,enable_debug = False, output_path = '' ):
        
        start_time = datetime.datetime.now().astimezone(TIMEZONE)
        if output_path == '':
            output_path = f"output/{start_time.strftime(DATE_FORMAT)}"
            
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        
        if enable_debug:
            debug_level = logging.DEBUG
        else:
            debug_level = logging.INFO
        
        # Set up root logger, and add a file handler to root logger
        logging.basicConfig(filename = f'{output_path}/{self.instance_name}.log',
                            level = debug_level,
                            format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        logger = logging.getLogger(LOGGER_NAME)    
        
        logger.info(f"loading problem file: {self.problem_path}")
        variable_domains,i_state,g_states,agent_index,obj_index,variables,vd_name,p_name= pddl_parser.problemParser(self.problem_path)
        logger.info(f"finish loading problem file: {p_name}")

        logger.info(f"loading domain file: {self.domain_path}")
        actions,domain_name = pddl_parser.domainParser(f"{self.domain_path}")
        logger.info(f"finish loading domain file: {domain_name}")        
        
        if type(self.search_algorithm) ==str:
            logger.info(f"loading search algorithm: {self.search_algorithm}")
            search_path = self.search_algorithm
            search_path = search_path.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
            
            try:
                self.search_algorithm = importlib.import_module(search_path)
                logger.info(f"finish loading search algorithm:")
            except (NameError, ImportError, IOError):
                traceback.print_exc()
                exit()
            except:
                traceback.print_exc()
                exit()
        else:
            logger.info(f"Search algorithm exists")
        
        
        if type(self.external_function) ==str:
            logger.info(f"loading external function: {self.external_function}")
            external_path = self.external_function
            external_path = external_path.replace('.py','').replace('\\','.').replace('/','.').replace('..','')
            try:
                self.external_function = importlib.import_module(external_path)
                logger.info(f"finish loading external function")
            except (NameError, ImportError, IOError):
                traceback.print_exc()
                exit()
            except:
                traceback.print_exc()
                exit()
        else:
            logger.info(f"External function exists")
            
            
        logger.info(f'Initialize problem')
        problem = pddl_model.Problem(variable_domains,i_state,g_states,agent_index,obj_index,variables,actions,self.external_function)
            
        logger.info(f'starting search')
        start_search_time = datetime.datetime.now().astimezone(TIMEZONE)
        result = self.search_algorithm.searching(problem,self.external_function.filterActionNames)
        end_search_time = datetime.datetime.now().astimezone(TIMEZONE)
        
        init_time = start_search_time - start_time
        search_time = end_search_time - start_search_time
        
        logger.info(f'initialization time: { init_time}')
        logger.info(f'search time: {search_time }') 
            
            
        result.update({'domain_name':domain_name})  
        result.update({'problem':p_name})
        result.update({'search':self.instance_name.split('_')[0]})
        result.update({'init_time':init_time.total_seconds()})
        result.update({'search_time':search_time.total_seconds()})
        
        

        print(result)
        with open(f"{output_path}/{self.instance_name}.json",'w') as f:
            json.dump(result,f) 
        
        return 

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python runner.py <options>

    """
    parser = OptionParser(usageStr)

    parser.add_option('-d', '--domain', dest="domain_path", help='path to the domain file', default='')
    parser.add_option('-p', '--problem', dest="problem_path", help='path to the problem file', default='')
    parser.add_option('-e', '--external', dest="external_path", help='path to the external function file', default='')
    parser.add_option('-o', '--output', dest="output_path", help='output directory for the running results (default: output/timestamp)',default='')
    parser.add_option('-s', '--search', dest="search_path", help='the name of the search algorithm', default='bfs')
    parser.add_option('--debug', dest="enable_debug", action='store_true', help='enable logging level to debug', default=False)
    parser.add_option('-t', '--timeout', dest="timeout", help='timeout, default 300s', type='int', default=300)
    
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options


if __name__ == '__main__':

    start_time = datetime.datetime.now().astimezone(TIMEZONE)
    options = loadParameter()
    
    problem_path = options.problem_path
    domain_path = options.domain_path
    # initialise with path, the function will load it later
    external_function = options.external_path
    search_algorithm = options.search_path

    
    
    if '\\' in domain_path:
        domain_name = domain_path.split('\\')[2]
        problem_name = problem_path.split('\\')[-1].replace('.pddl','')
        search_name = search_algorithm.split('\\')[-1].replace('.py','')
    instance_name = f"{search_name}_{domain_name}_{problem_name}"
    
        
    
    ins = Instance(instance_name=instance_name,problem_path=problem_path,domain_path=domain_path,external_function= external_function,search_algorithm= search_algorithm)
    ins.solve(timeout=options.timeout,enable_debug = options.enable_debug, output_path = options.output_path)
    
    
    

    
    # print(problem)
    
    # import search

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
        
        
        
        
        