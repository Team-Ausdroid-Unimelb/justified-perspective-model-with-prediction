












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
timestamp = datetime.datetime.now().astimezone(TIMEZONE).strftime(DATE_FORMAT)
# Set up root logger, and add a file handler to root logger
logging.basicConfig(filename = f'logs/{timestamp}.log',
                    level = logging.DEBUG,
                    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger("runner")

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python tournament_runner.py <options>
    EXAMPLES:   (1) 



    """
    
    logger.info("Parsing Options")
    parser = OptionParser(usageStr)

    parser.add_option('-d', '--domain_name', help='domain_name, which is the same as domain_name.py and folder under examples', default='coin')
    parser.add_option('-p', '--problem', help='path to the problem file', default='')
    parser.add_option('-o','--output', help='output directory for the running results (default: output)',default='output')
    # parser.add_option('-t','--title', help='title of the tournament options test, ones', default='test')
    # parser.add_option('--staffTeamOnly', action='store_true', help='only run among the staff teams', default=False)
    # parser.add_option('-i','--id', help='student id for run single assignment', default='000000')
    # parser.add_option('-s','--savefiles', action='store_true', help='keep the student repos', default=False)
    # parser.add_option('--tag', help='the tag for submission', default='submission')


    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options






if __name__ == '__main__':

    """
    The main function called when advance_model.py is run
    from the command line:

    > python runner.py

    See the usage string for more details.

    > python runner.py --help
    """
    

    start_time = datetime.datetime.now()
    aus_now = start_time.astimezone(TIMEZONE)
    options = loadParameter()
    
    
    # load pddl files
    domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name= pddl_parser.problemParser(options.problem)
    actions,domain_name = pddl_parser.domainParser(f"./examples/{options.domain_name}/domain.pddl")
    
    external = None
    try:
        external = importlib.import_module(f"examples.{options.domain_name}.{options.domain_name}")
    except (NameError, ImportError, IOError):
        print('Error: Agent at "' + teams[i]['agent'] + '" could not be loaded!', file=sys.stderr)
        traceback.print_exc()
        pass
    except:
        pass

    problem = pddl_model.Problem(domains,i_state,g_states,agent_index,obj_index,variables,actions,external)
    
    # print(problem)
    
    import search
    
    # print(search.BFS(problem))
    
    # print(problem.domains)
    # print(problem.initial_state)
    # print(problem.goal_states)
    # print(problem.entities)
    # print(problem.variables)
    # print(problem.actions)
    
    # import bbl
    
    # bbl.checkVisibility(problem,problem.initial_state,'a','v-p')
    
    # import coin
    
    
    eq_list = []
    for eq_str,value in problem.goal_states["epistemic_g"]:
        eq_list.append((epistemic_model.generateEpistemicQuery(eq_str),value))
    
    eq_list1 = [eq_list[0],]
    eq_list1 += [eq_list[1]]
    eq_list1 += [eq_list[2]]
    eq_list1 += [eq_list[3]]
    for eq,value in eq_list1:
        # print(eq)
        print(util.displayEQuery(eq))
        # s_0 = {'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
        # s_1 = {'dir-a': 'sw', 'dir-b': 'n', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
        # print(model.checkingEQ(problem,eq,[({'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'},""),(problem.initial_state,"a1")],problem.initial_state))
        # print(model.checkingEQ(problem,eq,[(s_0,"")],s_0))
        s_0 = {
            'agent_at-a': 1, 'agent_at-b': 1, 'agent_at-c': 1, 'agent_at-d': 1, 
            'shared-a': 0, 'shared-b': 0, 'shared-c': 0, 'shared-d': 0, 
            'secret-a': 't', 'secret-b': 't', 'secret-c': 't', 'secret-d': 't'
        }
        s_1 = {
            'agent_at-a': 1, 'agent_at-b': 1, 'agent_at-c': 1, 'agent_at-d': 1, 
            'shared-a': 1, 'shared-b': 0, 'shared-c': 0, 'shared-d': 0, 
            'secret-a': 'f', 'secret-b': 't', 'secret-c': 't', 'secret-d': 't'
        }
        s_2 = {
            'agent_at-a': 1, 'agent_at-b': 2, 'agent_at-c': 1, 'agent_at-d': 1, 
            'shared-a': 0, 'shared-b': 0, 'shared-c': 0, 'shared-d': 0, 
            'secret-a': 't', 'secret-b': 't', 'secret-c': 't', 'secret-d': 't'
        }
        s_3 = {
            'agent_at-a': 1, 'agent_at-b': 2, 'agent_at-c': 1, 'agent_at-d': 1, 
            'shared-a': 1, 'shared-b': 0, 'shared-c': 0, 'shared-d': 0, 
            'secret-a': 't', 'secret-b': 't', 'secret-c': 't', 'secret-d': 't'
        }
        s_4 = {
            'agent_at-a': 2, 'agent_at-b': 2, 'agent_at-c': 1, 'agent_at-d': 1, 
            'shared-a': 0, 'shared-b': 0, 'shared-c': 0, 'shared-d': 0, 
            'secret-a': 't', 'secret-b': 't', 'secret-c': 't', 'secret-d': 't'
        }
        s_5 = {
            'agent_at-a': 2, 'agent_at-b': 2, 'agent_at-c': 1, 'agent_at-d': 1, 
            'shared-a': 2, 'shared-b': 0, 'shared-c': 0, 'shared-d': 0, 
            'secret-a': 't', 'secret-b': 't', 'secret-c': 't', 'secret-d': 't'
        }
        path = [(s_0,"")]
        path += [(s_1,"")]
        path += [(s_2,"")]
        path += [(s_3,"")]
        path += [(s_4,"")]
        path += [(s_5,"")]
        
        print(epistemic_model.checkingEQ(problem.external,eq,path,s_5,problem.entities,problem.variables))
        
        
        
        
        