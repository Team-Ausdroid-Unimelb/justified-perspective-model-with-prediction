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
    parser.add_option('-s', '--search_name', dest="search_name", help='the search name', default='bfs')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def write_one_problems(problem_template,pddl_goal_list,prefix,domain_name):


    output_str = problem_template.problem_prefix1
    output_str = output_str + prefix.replace(domain_name,'')
    output_str = output_str + problem_template.problem_prefix2
    output_str = output_str + problem_template.problem_init
    output_str = output_str + problem_template.problem_goal_prefix
    for goal_str in pddl_goal_list:
        output_str=output_str + "          (" + goal_str +")\n"
    output_str=output_str + problem_template.problem_goal_surfix
    output_str=output_str + problem_template.problem_surfix
    with open(os.path.join(problem_template.problem_path,f"problem_{prefix}.pddl"),"w") as f:
        f.write(output_str)


if __name__ == '__main__':



    my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
    my_db = my_client['result']

    options = loadParameter()

    my_collection = my_db['20240417']
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


    template_file_dict = dict()

    if options.search_name == "":
        raise ValueError("search_nameis empty")
    else:
        search_name = options.search_name 
        
        for key,collection in collection_dict.items():
            existing_problems = []
            for item in collection.find():
                domain_path = item['domain_path']
                problem = item['problem']
                problem_file_name = 'problem_'+problem+".pddl"
                if existing_problems == []:
                    existing_problems = os.listdir(domain_path)

                query = {'search':search_name,'problem':problem}
                if problem_file_name not in existing_problems and my_collection.find_one(query) == None:
                    domain_name = item['domain_name']
                    
                    pddl_goals = item['pddl_goals']
                    template_path= item['template_path']
                    # agent_multiplier= item['agent_multiplier']
                    if template_path not in template_file_dict.keys():
                        module_name = "PDDL_Template"
                        spec = importlib.util.spec_from_file_location(module_name,template_path)
                        problem_template_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(problem_template_module)
                        temp_problem_template = getattr(problem_template_module,"PDDL_Template")
                        template_file_dict[template_path] = temp_problem_template
                    problem_template = template_file_dict[template_path]

                    write_one_problems(problem_template,pddl_goals,problem,domain_name)



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
    #     problem = item['problem'] #'bbl3_ttt_00184',
    #     # print(problem)
    #     # if not 'agent_multiplier' in item.keys():
    #     #     num_of_agent = item['num_of_agents']
    #     #     agent_multiplier = int( num_of_agent/agent_num_dict[result['domain_name']])
    #     #     query = {'_id':item['_id']}
    #     #     updates = {"$set": {'agent_multiplier':agent_multiplier}}
    #     #     my_collection.update_one(query,updates)


    #     write_one_problems(problem_template,pddl_goals,prefix+problem,domain_name)












