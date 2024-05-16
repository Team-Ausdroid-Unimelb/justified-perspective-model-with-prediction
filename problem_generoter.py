from random_query_generoter import RandomQueryGenerator
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

def write_all_problems(problem_template,ternary_goal_list,prefix,problem_path):
    max_index = -1
    # file_list = os.listdir(problem_path)
    # for file_name in file_list:
    #     if not os.path.isdir( os.path.join(problem_template.problem_path,file_name)):
    #         if "problem" in file_name and  ".pddl" in file_name:
    #             index_str = file_name.split(".")[0].split("_")[-1]
    #             # print(index_str)
    #             index_int = int(index_str)
    #             if index_int > max_index:
    #                 max_index = index_int
    # print(max_index)
    
    for i in range(len(ternary_goal_list)):
        max_depth = 0
        for goal_str in ternary_goal_list[i]:
            depth = goal_str.count("[")
            if depth > max_depth:
                max_depth = depth
                
        problem_index = f"{prefix}d{max_depth}_{i+max_index+1:05d}"
        output_str = problem_template.problem_prefix1
        output_str=output_str + problem_index
        output_str=output_str + problem_template.problem_prefix2
        output_str=output_str + problem_template.problem_init
        output_str=output_str + problem_template.problem_goal_prefix
        for goal_str in ternary_goal_list[i]:
            output_str=output_str + "          " + goal_str +"\n"
        output_str=output_str + problem_template.problem_goal_surfix
        output_str=output_str + problem_template.problem_surfix
        with open(os.path.join(problem_path,f"problem{problem_index}.pddl"),"w") as f:
            f.write(output_str)

def enumerate_variables(goal_list,base_case_list):
    # print(f"input {goal_list}")
    list_goal_list = []
    basecase_permutations = list(itertools.product(base_case_list, repeat=len(goal_list)))
    # print(f"pre {basecase_permutations}")
    for base_case_list in basecase_permutations:
        temp_goal_list = []
        for i in range(len(goal_list)):
            # (= (@ep ("+ b [b] + b [a]") (= (v p) 't')) ep.true)
            goal_str = '(= (@ep ("'
            # goal_str = goal_str+"".join([ f"b [{a}] " for a in goal_list[i]])
            goal_str += goal_list[i]
            goal_str += '") '
            goal_str += base_case_list[i]
            goal_str += ") ep.true)"
            temp_goal_list.append(goal_str)
        list_goal_list.append(temp_goal_list)
    return list_goal_list

def grapevine_variable(goal_list):
    print("goal list {}".format(goal_list))
    # sys.exit()
    list_goal_list = []
    for i in range(len(goal_list)):
        if goal_list[i].count("[") >1:
            agent_index = goal_list[i].index("]") -1
            agent = goal_list[i][agent_index]
            print(agent)
            print(goal_list[i][agent_index+3:])
            # (= (:epistemic b [a] (= (face c) 'head')) 1)
            goal_str = "(:epistemic "
            # goal_str = goal_str+"".join([ f"b [{a}] " for a in goal_list[i]])
            goal_str = goal_str+goal_list[i][agent_index+3:]
            goal_str = goal_str+ f"(= (secret {agent}) 't')"
            goal_str = goal_str+") "
            list_goal_list.append(goal_str)
    # print(list_goal_list)
    return [list_goal_list]
# def enumerate_ternary(goal_list,ternary_list):
#     # print(f"input {goal_list}")
#     list_goal_list = []
#     ternary_permutations = list(itertools.product(ternary_list, repeat=len(goal_list)))
#     # print(f"pre {ternary_permutations}")
#     for ternary_permutation in ternary_permutations:
#         temp_goal_list = []
#         for i in range(len(goal_list)):
#             # (= (:epistemic b [a] (= (face c) 'head')) 1)
#             goal_str = goal_list[i]
#             goal_str = goal_str+ ternary_permutation[i]
#             goal_str = goal_str+") "
#             temp_goal_list.append(goal_str)
#         list_goal_list.append(temp_goal_list)
#     return list_goal_list

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
    base_cases = []
    for key,values in problem_template.object_value_dict.items():
        for value in values:
            base_cases.append(f"(= {key} {value})")

    rqg = RandomQueryGenerator(problem_template.agent_index_list,problem_template.ternary_list,problem_template.MAX_DEPTH)

    index_goal_list = []
    
    if options.enumerate:
        index_goal_list = rqg.problem_enumerate()
    else:
        for i in range(options.max_goal_size):
            random_goal_list = rqg.select_n_random_query_k_times(i+1,options.sample_size)
            index_goal_list = index_goal_list+random_goal_list

    print(index_goal_list)
    problem_path = os.path.split(problem_template_py)[0]
    agent_number = os.path.split(problem_template_py)[1].split(".")[0].split("problem_template")[1]
    print(agent_number)
    
    if problem_path == os.path.join("experiments","grapevine"):
        bound = rqg.agent_num_list[0]
        filtered_list = []
        for goal_list in index_goal_list:
            new_goal_list = [element for element in goal_list if element > bound]
            if not new_goal_list == []:
                filtered_list.append(new_goal_list)
    else:
        filtered_list = index_goal_list
    
    # print(filtered_list)
    var_goal_list = []
    for goal_list in filtered_list:
        ep_prefix_list = [rqg.decode_agt_num(i) for i in goal_list]
        if problem_path == os.path.join("experiments","grapevine"):
            temp_var_goal = grapevine_variable(ep_prefix_list)
        else:    
            temp_var_goal = enumerate_variables(ep_prefix_list,base_cases)

        for temp_goal in temp_var_goal:
            if temp_goal not in var_goal_list:
                var_goal_list.append(temp_goal)
    agent_num = len(problem_template.agent_index_list)
    goal_size = len(var_goal_list[0])
    # print(var_goal_list)
    # print(len(var_goal_list))
    write_all_problems(problem_template,var_goal_list,f"_a{agent_num}_g{goal_size}_",problem_path)
    
    
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

