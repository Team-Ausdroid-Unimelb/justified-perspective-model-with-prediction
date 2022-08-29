












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

    parser.add_option('-d', '--domain', help='domain', default='bbl')
    parser.add_option('-w', '--workers', help='path to the files that list all the available servers', default='configs/workers.json')
    parser.add_option('-o','--output', help='output directory for the running results, replays and logs (default: output)',default='output')
    parser.add_option('-t','--title', help='title of the tournament options test, ones', default='test')
    parser.add_option('--staffTeamOnly', action='store_true', help='only run among the staff teams', default=False)
    parser.add_option('-i','--id', help='student id for run single assignment', default='000000')
    parser.add_option('-s','--savefiles', action='store_true', help='keep the student repos', default=False)
    parser.add_option('--tag', help='the tag for submission', default='submission')


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
    domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name= pddl_parser.problemParser("examples/coin/problem01.pddl")
    actions,domain_name = pddl_parser.domainParser("examples/coin/domain.pddl")
    
    import examples.coin as coin
    problem = pddl_model.Problem(domains,i_state,g_states,agent_index,obj_index,variables,actions,coin)
    
    # print(problem)
    
    import search
    
    print(search.BFS(problem))
    
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
    
    
    for eq,value in eq_list:
        # print(eq)
        print(util.displayEQuery(eq))
        # s_0 = {'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
        # s_1 = {'dir-a': 'sw', 'dir-b': 'n', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'}
        # print(model.checkingEQ(problem,eq,[({'dir-a': 'sw', 'dir-b': 'sw', 'x-a': 3, 'x-b': 2, 'x-p': 1, 'y-a': 3, 'y-b': 2, 'y-p': 1, 'v-p': 't'},""),(problem.initial_state,"a1")],problem.initial_state))
        # print(model.checkingEQ(problem,eq,[(s_0,"")],s_0))
        
        s_0 = {'peeking-a': 'f','peeking-b': 'f', 'face-c': 'head'}
        s_1 = {'peeking-a': 't','peeking-b': 'f', 'face-c': 'head'}
        s_2 = {'peeking-a': 'f','peeking-b': 'f', 'face-c': 'head'}
        s_3 = {'peeking-a': 'f','peeking-b': 't', 'face-c': 'head'}
        s_4 = {'peeking-a': 'f','peeking-b': 't', 'face-c': 'tail'}
        s_5 = {'peeking-a': 'f','peeking-b': 'f', 'face-c': 'tail'}
        
        
        print(epistemic_model.checkingEQ(problem,eq,[(s_0,""),(s_1,""),(s_2,""),(s_3,""),(s_4,""),(s_5,"")],s_4))