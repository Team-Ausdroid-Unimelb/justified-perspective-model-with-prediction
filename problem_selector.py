from utils.random_query_generoter import RandomQueryGenerator
# import experiments.coin.problem_template as domain
from optparse import OptionParser
import sys
import os
import importlib.util
import itertools
import json
import random
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
    parser.add_option('-d', '--domain', dest="domain_path", help='path to the domain folder, which contains problem_template.py', default='experiments/coin')
    # parser.add_option('-g', '--max_goal_size', dest="max_goal_size", type='int', help='should be larger than 1 and smaller than |agt|*|agt-1|^(depth-1), also affected by |V|^|goal|', default=1)
    parser.add_option('-k', '--k_samples', dest="sample_size", type='int', help='should be larger than 1 and smaller than ?', default=5)
    parser.add_option('-e', dest="enumerate", action='store_true', help='generate all problems', default=False)

    parser.add_option('-t', '--num_of_solvable_goals', dest="num_of_solvable_goals", type='int', help='should be larger than 1 and smaller than |agt|*|agt-1|^(depth-1), also affected by |V|^|goal|', default=0)
    parser.add_option('-f', '--num_of_unsolvable_goals', dest="num_of_unsolvable_goals", type='int', help='should be larger than 1 and smaller than |agt|*|agt-1|^(depth-1), also affected by |V|^|goal|', default=0)

    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def write_all_problems(problem_template,ternary_goal_list,prefix):
    max_index = -1
    file_list = os.listdir(problem_template.problem_path)
    for file_name in file_list:
        if not os.path.isdir( os.path.join(problem_template.problem_path,file_name)):
            if "problem" in file_name and  ".pddl" in file_name:
                index_str = file_name.split(".")[0].split("_")[-1]
                # print(index_str)
                index_int = int(index_str)
                if index_int > max_index:
                    max_index = index_int
    # print(max_index)
    
    for i in range(len(ternary_goal_list)):
        problem_index = f"{prefix}_{i+max_index+1:05d}"
        output_str = problem_template.problem_prefix1
        output_str=output_str + problem_index
        output_str=output_str + problem_template.problem_prefix2
        output_str=output_str + problem_template.problem_init
        output_str=output_str + problem_template.problem_goal_prefix
        for goal_str in ternary_goal_list[i]:
            output_str=output_str + "          " + goal_str +"\n"
        output_str=output_str + problem_template.problem_goal_surfix
        output_str=output_str + problem_template.problem_surfix
        with open(os.path.join(problem_template.problem_path,f"problem{problem_index}.pddl"),"w") as f:
            f.write(output_str)


if __name__ == '__main__':


    options = loadParameter()

    if options.domain_path == "":
        raise ValueError("domain path is empty")
    else:
        problem_template_py = os.path.join(options.domain_path,"problem_template.py")
        module_name = "PDDL_Template"
        spec = importlib.util.spec_from_file_location(module_name,problem_template_py)
        problem_template_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(problem_template_module)
        problem_file_path = os.path.join(options.domain_path,"problem_size1.json")

    problem_template = getattr(problem_template_module,"PDDL_Template")

    total_goal_size = options.num_of_solvable_goals + options.num_of_unsolvable_goals

    if total_goal_size <1:
        raise ValueError(f"total goal size ({total_goal_size}) should not be smaller than 1")
    else:
        goalsize_string = ""
        for i in range(options.num_of_solvable_goals):
            goalsize_string += "t"
        for i in range(options.num_of_unsolvable_goals):
            goalsize_string += "f"
    
    problem_info = dict()
    
    with open(problem_file_path,"r") as f:
        problem_info=json.load(f)

    print(problem_info)
    solvable_problems = []
    for key,item_list in problem_info['solvable'].items():
        goal_str = ""
        for item in item_list:
            goal_str += "        ("
            goal_str += item
            goal_str += ");;"
            goal_str += key
            goal_str += "\n"
        goal_str = goal_str[:-1]
        solvable_problems.append(goal_str)

    unsolvable_problems = []
    for key,item_list in problem_info['unsolvable'].items():
        goal_str = ""
        for item in item_list:
            goal_str += "        ("
            goal_str += item
            goal_str += ");;"
            goal_str += key
            goal_str += "\n"
        goal_str = goal_str[:-1]
        unsolvable_problems.append(goal_str)

    goal_dict_list = []
    if options.enumerate:
        # for now, this only support length of 1
        for i in solvable_problems:
            goal_dict_list.append([i])
    else:

        for i in range(options.sample_size):
            one_goal_dict_list = []

            one_goal_dict_list += random.sample(solvable_problems,options.num_of_solvable_goals)
            one_goal_dict_list += random.sample(unsolvable_problems,options.num_of_unsolvable_goals)
            goal_dict_list.append(one_goal_dict_list)

    print(goal_dict_list)

    write_all_problems(problem_template, goal_dict_list, str(total_goal_size)+"_"+goalsize_string)
    
    
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

