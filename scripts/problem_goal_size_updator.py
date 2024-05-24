import pymongo
import os
import json
from optparse import OptionParser
import sys
import importlib


import pymongo.errors

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python runner.py <options>

    """
    parser = OptionParser(usageStr)

    # parser.add_option('-p', '--problem_template', dest="problem_template_file", help='path to problem_template.py', default='experiments/coin/problem_template.py')
    parser.add_option('--unsolvable', dest="unsolvable", help='only return unsolvable problems', default=False,action='store_true')
    parser.add_option('--all', dest="all", help='return all problems', default=False,action='store_true')
    parser.add_option('--domain_names', dest="domain_names", help='a list of domain_names, separating by ","', default="bbl")
    parser.add_option('--goal_size', dest="goal_size", help='the goal size want to generated',type = int, default=2)
    parser.add_option('--agent_size', dest="agent_size", help='number of agents, default is 2',type = int, default=2)
    parser.add_option('--empty_plan', dest="empty_plan", help='counting problem that solved by inital state', default=False,action='store_true')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def write_one_problems(problem_template,pddl_goal_list,problem_name,domain_name,problem_path):


    output_str = problem_template.problem_prefix1
    output_str = output_str + problem_name.replace(domain_name,'')
    output_str = output_str + problem_template.problem_prefix2
    output_str = output_str + problem_template.problem_init
    output_str = output_str + problem_template.problem_goal_prefix
    for goal_str in pddl_goal_list:
        output_str=output_str + "          " + goal_str +"\n"
    output_str=output_str + problem_template.problem_goal_surfix
    output_str=output_str + problem_template.problem_surfix
    with open(os.path.join(problem_path),"w") as f:
        f.write(output_str)


if __name__ == '__main__':

    


    my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
    my_db = my_client['new_result']

    options = loadParameter()

    goal_size = options.goal_size
    if goal_size <2:
        raise ValueError("Goal size should be greater than 1")
    



    my_collection = my_db['all_instance']
    coin_domain_collection = my_db['coin']
    spcoin_domain_collection = my_db['spcoin']
    bbl_domain_collection = my_db['bbl']
    corridor_domain_collection = my_db['corridor']
    grapevine_domain_collection = my_db['grapevine']
    sn_domain_collection = my_db['sn']

    collection_dict = {
    'coin' : coin_domain_collection,
    'spcoin' : spcoin_domain_collection,
    'bbl' : bbl_domain_collection,
    'corridor' : corridor_domain_collection,
    'grapevine' : grapevine_domain_collection,
    'sn' : sn_domain_collection,
    }


    template_file_dict = {
        'bbl':dict(),
        'coin':dict(),
        'spcoin':dict(),
        'corridor':dict(),
        'grapevine':dict(),
        'sn':dict(),
    }
    domain_names = options.domain_names.split(",")


    problem_query = {}
    if options.all:
        problem_query = {}
    elif options.unsolvable:
        problem_query = {'solvable':False}
    else:
        problem_query = {'solvable':True}
    problem_query.update({'num_of_agents':options.agent_size})
    if not options.empty_plan:
        problem_query.update({'plan':{'$ne':[]}})

    minus_one_goal_size = goal_size - 1
    minus_one_goal_size_query = {'total_goal_size':minus_one_goal_size}
    minus_one_goal_size_query.update(problem_query)

    one_goal_size_query = {'total_goal_size':1}
    one_goal_size_query.update(problem_query)

    domain_path = ""
    # find goal_size-1 problem set first, then adding one more goal to make it goal_size
    for domain_name in domain_names:
        print(domain_name)
        if domain_name == "":
            continue
        collection = collection_dict[domain_name]


        minus_one_problem_dict = dict()
        print(minus_one_goal_size_query)
        item = collection.find_one(minus_one_goal_size_query)
        domain_path = item['domain_path']

        # existing_problems = []
        for item in collection.find(minus_one_goal_size_query):
            problem_name = item['problem_name']
            goals = item['goals']
            minus_one_problem_dict[problem_name] = goals
    
        # find goal_size=1 problem set
        print(len(minus_one_problem_dict))
        one_problem_dict = dict()
        for item in collection.find(one_goal_size_query):
            problem_name = item['problem_name']
            goals = item['goals']
            one_problem_dict[problem_name] = goals[0]
        print(len(one_problem_dict))

        final_goal_list = list()
        existing_goal_set_list = list()
        for one_goal_problem_name,one_goal in one_problem_dict.items():
            print(len(final_goal_list))
            for multiple_goal_problem_name,multiple_goals in minus_one_problem_dict.items():
                if one_goal not in multiple_goals:
                    new_goal_set = set()
                    new_goal_list = list()
                    new_goal_list.append(f"{one_goal}; {one_goal_problem_name}")
                    new_goal_set.add(one_goal)
                    for goal in multiple_goals:
                        new_goal_list.append(f"{goal}; {multiple_goal_problem_name}")
                        new_goal_set.add(goal)
                    if new_goal_set not in existing_goal_set_list:
                        final_goal_list.append(new_goal_list)
                        existing_goal_set_list.append(new_goal_set)


        print(len(final_goal_list))
        domain_folder = domain_path.replace("domain.pddl","")
        template_path = os.path.join(domain_folder,f"problem_template{options.agent_size}.py")
        module_name = "PDDL_Template"
        spec = importlib.util.spec_from_file_location(module_name,template_path)
        problem_template_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(problem_template_module)
        problem_template = getattr(problem_template_module,"PDDL_Template")
        print(problem_template)
        for i,goal_list in enumerate(final_goal_list):
            
            problem_name = f"_a{options.agent_size}_g{goal_size}_{i:05d}"

            problem_path = os.path.join(domain_folder,"problem"+problem_name+".pddl")
            write_one_problems(problem_template,goal_list,problem_name,domain_name,problem_path)
        # write_one_problems(problem_template,pddl_goals,problem_name,domain_name,problem_path)
                # domain_path = item['domain_path']
                # problem_name = item['problem_name']
                # problem_path = item['problem_path']
                # # print(problem)
                # # problem_file_name = 'problem_'+problem+".pddl"
                # # if existing_problems == []:
                # #     existing_problems = os.listdir(domain_path)
                # if not os.path.exists(problem_path):

                #     query = {'search':search_name,'problem_name':problem_name}
                #     if my_collection.find_one(query) == None:
                #         print("Not found, adding it: ", problem_name)
                #         domain_name = item['domain_name']
                        
                #         pddl_goals = item['goals']
                #         num_of_agent = item['num_of_agents']
                #         # agent_multiplier= item['agent_multiplier']
                #         if num_of_agent not in template_file_dict[domain_name].keys():
                #             template_path = domain_path.replace("domain.pddl",f"problem_template{num_of_agent}.py")
                #             module_name = "PDDL_Template"
                #             spec = importlib.util.spec_from_file_location(module_name,template_path)
                #             problem_template_module = importlib.util.module_from_spec(spec)
                #             spec.loader.exec_module(problem_template_module)
                #             temp_problem_template = getattr(problem_template_module,"PDDL_Template")
                #             template_file_dict[template_path] = temp_problem_template
                #         problem_template = template_file_dict[template_path]
                #         write_one_problems(problem_template,pddl_goals,problem_name,domain_name,problem_path)



        # # problem_template_py = os.path.join(options.domain_path,"problem_template.py")

        # domain_path = os.path.split(problem_template_file)[0]
        # domain_name = os.path.split(domain_path)[1]

        # module_name = "PDDL_Template"
        # spec = importlib.util.spec_from_file_location(module_name,problem_template_file)
        # problem_template_module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(problem_template_module)




    # # problem_template = getattr(problem_template_module,"PDDL_Template")

    # my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
    # my_db = my_client['result']

    # agent_num_dict = {
    #     'bbl':2,
    #     'coin':2,
    #     'spcoin':2,
    #     'corridor':3,
    #     'grapevine':4,
    #     'sn':4,
    # }

    # my_collection = my_db[domain_name]
    # # my_collection = my_db['20240417_unknown']

    # prefix = ""

    # if '2' in problem_template_file:
    #     prefix = '_a2'
    # elif '4' in problem_template_file:
    #     prefix = '_a4'
    # else:
    #     prefix = '_a1'

    # for item in my_collection.find():
    #     pddl_goals = item['pddl_goals']
    #     problem = item['problem_name'] #'bbl3_ttt_00184',
    #     # print(problem)
    #     # if not 'agent_multiplier' in item.keys():
    #     #     num_of_agent = item['num_of_agents']
    #     #     agent_multiplier = int( num_of_agent/agent_num_dict[result['domain_name']])
    #     #     query = {'_id':item['_id']}
    #     #     updates = {"$set": {'agent_multiplier':agent_multiplier}}
    #     #     my_collection.update_one(query,updates)


    #     write_one_problems(problem_template,pddl_goals,prefix+problem,domain_name)












