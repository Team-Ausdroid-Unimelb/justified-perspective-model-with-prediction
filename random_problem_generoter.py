
from experiments.coin.problem_template import *
from experiments.spcoin.problem_template import *
from experiments.bbl.problem_template import *
from experiments.corridor.problem_template import *

from experiments.sn.problem_template import *

base_cases = []
for key,values in object_value_dict.items():
    for value in values:
        base_cases.append(f"(= {key} {value})")



print(base_cases)
# (unseen_index, list, seen_index)
single_basic_goal_list_full = []

temp_agent_lists = [(agent_index_list,[],[])]
i=0
while i<DEPTH:
    next_agent_lists = []
    for unseen,agent_list,seen in temp_agent_lists:
        # temp_available =[]
        if len(unseen) > 0:
            # temp_available.append(unseen[0])
            new_unseen = unseen[1:]
            new_agent_list = agent_list + [unseen[0]]
            new_seen = seen +[unseen[0]]
            next_agent_lists.append((new_unseen,new_agent_list,new_seen))
        if len(seen) >0:
            for j in seen:
                if not j == agent_list[-1]: 
                    new_unseen = unseen.copy()
                    new_seen = seen.copy()
                    new_agent_list = agent_list + [j]
                    next_agent_lists.append((new_unseen,new_agent_list,new_seen))
    temp_agent_lists = next_agent_lists
    single_basic_goal_list_full = single_basic_goal_list_full+temp_agent_lists
    i = i+1

single_basic_goal_list= [item[1] for item in single_basic_goal_list_full]
print(single_basic_goal_list)
print(len(single_basic_goal_list))
# agent difference
import itertools

prem_list = list(itertools.permutations(range(len(agent_index_list))))
print(prem_list)
single_goal_list = []
if not UNIFORM:
    
    for prem in prem_list:
        replacement = dict()
        for i in range(len(prem)):
            replacement.update({agent_index_list[i]:agent_index_list[prem[i]]})
        
        # print(replacement)    
        for agent_list in single_basic_goal_list: 
            new_agent_list = [replacement[n] for n in agent_list]
            if new_agent_list not in single_goal_list:
                single_goal_list.append(new_agent_list)
else:
    single_goal_list = single_basic_goal_list
print(single_goal_list)
# print(len(single_goal_list))


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

all_goal_list = list(powerset(single_goal_list))[1:]
print(len(all_goal_list))
print(all_goal_list)

all_combinations_list = []

for goal_list in all_goal_list:
    # permut = list(itertools.permutations(range(len(base_cases)),len(goal_list)))

    # print(permut)
    
    prods = list(itertools.product(base_cases,repeat = len(goal_list)))
    for prod in prods:
        combinations_list = []
        for i in range(len(goal_list)):
    # for goal_agents in goal_list:
            # (= (:epistemic b [a] (= (face c) 'head')) 1)
            goal_str = "(= (:epistemic "
            goal_str = goal_str+"".join([ f"b [{a}] " for a in goal_list[i]])
            goal_str = goal_str+prod[i]
            goal_str = goal_str+") "
            # print(goal_str)
            combinations_list.append(goal_str)
        all_combinations_list.append(combinations_list)


print(len(all_combinations_list))
all_pddl_goal_list = []
for combinations_list in all_combinations_list:
    # print(combinations_list)
    prods = list(itertools.product([1,0,-1],repeat = len(combinations_list)))
    for prod in prods:
        pddl_goal_list = []
        for i in range(len(combinations_list)):
    # for goal_agents in goal_list:
            # (= (:epistemic b [a] (= (face c) 'head')) 1)
            goal_str = combinations_list[i]+str(prod[i])+")"
            # print(goal_str)
            pddl_goal_list.append(goal_str)
        all_pddl_goal_list.append(pddl_goal_list)

print(len(all_pddl_goal_list))

for i in range(len(all_pddl_goal_list)):
    problem_index = f"{i:03d}"
    output_str = problem_prefix1
    output_str=output_str + problem_index
    output_str=output_str + problem_prefix2
    output_str=output_str + problem_init
    output_str=output_str + problem_goal_prefix
    for goal_str in all_pddl_goal_list[i]:
        output_str=output_str + "          " + goal_str +"\n"
    output_str=output_str + problem_goal_surfix
    output_str=output_str + problem_surfix
    with open(os.path.join(problem_path,f"problem{problem_index}.pddl"),"w") as f:
        f.write(output_str)
    # break 