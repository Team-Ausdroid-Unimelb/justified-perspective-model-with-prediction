
# import experiments.coin.problem_template as domain
from optparse import OptionParser
import sys
import os
import itertools
import json
import re
from math import comb

# from experiments.spcoin.problem_template import *
# from experiments.bbl.problem_template import *
# from experiments.corridor.problem_template import *

# from experiments.sn.problem_template import *
# current_directory = os.path.dirname(os.path.abspath(__file__))
# root_directory = os.path.join(current_directory, '..')
# sys.path.append(os.path.abspath(root_directory))
# from utils.random_query_generoter import RandomQueryGenerator

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
    parser.add_option('-p', '--problem_base', dest="problem_base_file", help='path to the problem_base.json', default='experiments/bbl/a2_problem_base.json')
    # parser.add_option('-d', '--max_depth', dest="max_depth", type='int', help='should be larger than 0 and smaller than the max depth in problem_template*.py', default=1)
    parser.add_option('-g', '--max_goal_size', dest="max_goal_size", type='int', help='should be larger than 0', default=1)
    # parser.add_option('-k', '--k_samples', dest="sample_size", type='int', help='should be larger than 1 and smaller than ?', default=5)
    # parser.add_option('-e', dest="enumerate", action='store_true', help='generate all problems', default=False)

    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options




# def combination_to_rank(combination, n):
#     """Convert a combination to its lexicographic rank."""
#     rank = 0
#     k = len(combination)
#     for i in range(k):
#         if i > 0:
#             start = combination[i-1] + 1
#         else:
#             start = 0
#         for j in range(start, combination[i]):
#             rank += comb(n - j - 1, k - i - 1)
#     return rank

def max_rank(n, k):
    """Calculate the maximum rank for combinations of k items from n items."""
    return comb(n, k) - 1

def rank_to_combination(rank, k, n):
    """Convert a lexicographic rank to its combination."""
    combination = []
    x = rank
    remaining = k
    for i in range(n):
        if remaining == 0:
            break
        if comb(n - i - 1, remaining - 1) <= x:
            x -= comb(n - i - 1, remaining - 1)
        else:
            combination.append(i)
            remaining -= 1
    return combination

def extract_integer_from_string(input_string):
    # Use regular expression to find the integer pattern in the string
    match = re.search(r'\d+', input_string)
    if match:
        # Convert the matched string to an integer and return it
        return int(match.group(0))
    else:
        # Return None or raise an error if no integer is found
        return None


if __name__ == '__main__':


    options = loadParameter()
    max_goal_size = options.max_goal_size
    problem_base_file = options.problem_base_file
    # if options.problem_base_file == "" or os.path.exists(options.problem_base_file) == False:
    #     raise ValueError("domain path is not valid")
    # else:
    #     problem_template_py = options.problem_template_file
        
    #     module_name = "PDDL_Template"
    #     spec = importlib.util.spec_from_file_location(module_name,problem_template_py)
    #     problem_template_module = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(problem_template_module)
    with open(problem_base_file) as f:
        goal_condition_dictionary = json.load(f)
    
    problem_info = dict()

    
    for depth in range(1,len(goal_condition_dictionary)+1):
        problem_info[depth] = dict()
        goal_pull_size = 0
        for i in range(1,depth+1):
            goal_pull_size += len(goal_condition_dictionary[str(i)])
        print(goal_pull_size)
        for goal_size in range(1,max_goal_size+1):
            num_of_possible_goals = max_rank(goal_pull_size,goal_size)
            problem_info[depth][goal_size] = num_of_possible_goals
    print(problem_info)


    problem_base_file_name = os.path.basename(problem_base_file)
    problem_directory = os.path.dirname(problem_base_file)
    prefix = problem_base_file_name.split("_")[0]
    num_of_agent = extract_integer_from_string(prefix)

    with open(os.path.join(problem_directory,f"a{num_of_agent}_goal_depth-goalsize_info.json"),"w") as f:
        json.dump(problem_info,f)
    # write_all_problems(problem_template,var_goal_list,f"_a{agent_num}_g{goal_size}_",problem_path)
    
    
    # ternary_goal_list = []
    # counter = 0
    # for goal_list in var_goal_list:
    #     counter +=1
    #     temp_var_goal = enumerate_ternary(goal_list,['-1','0','1'])
    #     # write_all_problems(problem_template,temp_var_goal,f"{counter:03d}")
    #     ternary_goal_list= ternary_goal_list+ temp_var_goal
    #     if counter > 999:
    #         raise ValueError("there are more than 1000 problems")
    # print(len(ternary_goal_list))
    # print(ternary_goal_list)



# print(base_cases)
# # (unseen_index, list, seen_index)
# single_basic_goal_list_full = []

# temp_agent_lists = [(agent_index_list,[],[])]
# i=0
# while i<DEPTH:
#     next_agent_lists = []
#     for unseen,agent_list,seen in temp_agent_lists:
#         # temp_available =[]
#         if len(unseen) > 0:
#             # temp_available.append(unseen[0])
#             new_unseen = unseen[1:]
#             new_agent_list = agent_list + [unseen[0]]
#             new_seen = seen +[unseen[0]]
#             next_agent_lists.append((new_unseen,new_agent_list,new_seen))
#         if len(seen) >0:
#             for j in seen:
#                 if not j == agent_list[-1]: 
#                     new_unseen = unseen.copy()
#                     new_seen = seen.copy()
#                     new_agent_list = agent_list + [j]
#                     next_agent_lists.append((new_unseen,new_agent_list,new_seen))
#     temp_agent_lists = next_agent_lists
#     single_basic_goal_list_full = single_basic_goal_list_full+temp_agent_lists
#     i = i+1

# single_basic_goal_list= [item[1] for item in single_basic_goal_list_full]
# print(single_basic_goal_list)
# print(len(single_basic_goal_list))
# # agent difference
# import itertools

# prem_list = list(itertools.permutations(range(len(agent_index_list))))
# print(prem_list)
# single_goal_list = []
# if not UNIFORM:
    
#     for prem in prem_list:
#         replacement = dict()
#         for i in range(len(prem)):
#             replacement.update({agent_index_list[i]:agent_index_list[prem[i]]})
        
#         # print(replacement)    
#         for agent_list in single_basic_goal_list: 
#             new_agent_list = [replacement[n] for n in agent_list]
#             if new_agent_list not in single_goal_list:
#                 single_goal_list.append(new_agent_list)
# else:
#     single_goal_list = single_basic_goal_list
# print(single_goal_list)
# # print(len(single_goal_list))


# def powerset(s):
#     x = len(s)
#     masks = [1 << i for i in range(x)]
#     for i in range(1 << x):
#         yield [ss for mask, ss in zip(masks, s) if i & mask]

# all_goal_list = list(powerset(single_goal_list))[1:]
# print(len(all_goal_list))
# print(all_goal_list)

# all_combinations_list = []

# for goal_list in all_goal_list:
#     # permut = list(itertools.permutations(range(len(base_cases)),len(goal_list)))

#     # print(permut)
    
#     prods = list(itertools.product(base_cases,repeat = len(goal_list)))
#     for prod in prods:
#         combinations_list = []
#         for i in range(len(goal_list)):
#     # for goal_agents in goal_list:
#             # (= (:epistemic b [a] (= (face c) 'head')) 1)
#             goal_str = "(= (:epistemic "
#             goal_str = goal_str+"".join([ f"b [{a}] " for a in goal_list[i]])
#             goal_str = goal_str+prod[i]
#             goal_str = goal_str+") "
#             # print(goal_str)
#             combinations_list.append(goal_str)
#         all_combinations_list.append(combinations_list)


# print(len(all_combinations_list))
# all_pddl_goal_list = []
# for combinations_list in all_combinations_list:
#     # print(combinations_list)
#     prods = list(itertools.product([1,0,-1],repeat = len(combinations_list)))
#     for prod in prods:
#         pddl_goal_list = []
#         for i in range(len(combinations_list)):
#     # for goal_agents in goal_list:
#             # (= (:epistemic b [a] (= (face c) 'head')) 1)
#             goal_str = combinations_list[i]+str(prod[i])+")"
#             # print(goal_str)
#             pddl_goal_list.append(goal_str)
#         all_pddl_goal_list.append(pddl_goal_list)

# print(len(all_pddl_goal_list))

