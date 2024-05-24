
# import experiments.coin.problem_template as domain
from optparse import OptionParser
import sys
import os
import importlib.util
import itertools
# from experiments.spcoin.problem_template import *
# from experiments.bbl.problem_template import *
# from experiments.corridor.problem_template import *

# from experiments.sn.problem_template import *



def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python runner.py <options>

    """
    parser = OptionParser(usageStr)

    # parser.add_option('-d', '--domain', dest="domain_path", help='path to the domain file', default='')
    # parser.add_option('-p', '--problem', dest="problem_path", help='path to the problem file', default='')
    # parser.add_option('-e', '--external', dest="external_path", help='path to the external function file', default='')
    # parser.add_option('-o', '--output', dest="output_path", help='output directory for the running results (default: output/timestamp)',default='')
    # parser.add_option('-s', '--search', dest="search_path", help='the name of the search algorithm', default='bfs')
    # parser.add_option('--log_debug', dest="log_debug", action='store_true', help='enable logging level to debug', default=False)
    # parser.add_option('-b', '--belief_mode', dest="belief_mode", type='int', help='should between 0-3', default=1)
    # parser.add_option('--time_debug', dest="time_debug", action='store_true', help='enable cProfile', default=False)
    # parser.add_option('-t', '--timeout', dest="timeout", help='timeout, default 300s', type='int', default=300)
    parser.add_option('-p', '--problem_template', dest="problem_template_file", help='path to the problem_template.py', default='experiments/bbl/problem_template2.py')
    parser.add_option('-g', '--max_goal_size', dest="max_goal_size", type='int', help='should be larger than 1 and smaller than |agt|*|agt-1|^(depth-1), also affected by |V|^|goal|', default=1)
    parser.add_option('-k', '--k_samples', dest="sample_size", type='int', help='should be larger than 1 and smaller than ?', default=5)
    parser.add_option('-e', dest="enumerate", action='store_true', help='generate all problems', default=False)

    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options



if __name__ == '__main__':


    options = loadParameter()

    if options.problem_template_file == "":
        raise ValueError("domain path is empty")
    else:
        problem_template_py = options.problem_template_file
        module_name = "PDDL_Template"
        spec = importlib.util.spec_from_file_location(module_name,problem_template_py)
        problem_template_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(problem_template_module)

    problem_template = getattr(problem_template_module,"PDDL_Template")
    
    num_of_agent = len(problem_template.agent_index_list)
    
    
    init_dict = problem_template.init_dict

    tuple_base_list = [[]]
    for variable_name, possible_values in init_dict.items():
        temp_tuple_list = []
        for value in possible_values:
            temp_tuple = (variable_name, value)
            for tuple_base in tuple_base_list:
                temp_tuple_list.append(tuple_base + [temp_tuple])
        tuple_base_list = temp_tuple_list
        
    tuple_base_dict = {}
    for i,tuple_base in enumerate(tuple_base_list):
        init_name = "init_a{}_{:05}".format(num_of_agent,i)
        tuple_base_dict[init_name] = tuple_base
        
        
    json_path = problem_template_py.replace(".py",".json")
    
    with open(json_path,"w") as f:
        import json
        json.dump(tuple_base_dict,f)
    
    