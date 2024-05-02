import pymongo
import os
import json
from optparse import OptionParser
import sys
import importlib

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python runner.py <options>

    """
    parser = OptionParser(usageStr)

    parser.add_option('-p', '--problem_template', dest="problem_template_file", help='path to problem_template.py', default='experiments/coin/problem_template.py')

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


    options = loadParameter()

    if options.problem_template_file == "":
        raise ValueError("domain path is empty")
    else:
        problem_template_file = options.problem_template_file 
        
        # problem_template_py = os.path.join(options.domain_path,"problem_template.py")

        domain_path = os.path.split(problem_template_file)[0]
        domain_name = os.path.split(domain_path)[1]

        module_name = "PDDL_Template"
        spec = importlib.util.spec_from_file_location(module_name,problem_template_file)
        problem_template_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(problem_template_module)

    problem_template = getattr(problem_template_module,"PDDL_Template")

    my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
    my_db = my_client['result']

    agent_num_dict = {
        'bbl':2,
        'coin':2,
        'spcoin':2,
        'corridor':3,
        'grapevine':4,
        'sn':4,
    }

    my_collection = my_db[domain_name]
    # my_collection = my_db['20240417_unknown']

    prefix = ""

    if '2' in problem_template_file:
        prefix = 'a2_'
    elif '4' in problem_template_file:
        prefix = 'a4_'
    else:
        prefix = 'a1_'

    for item in my_collection.find():
        # if 'agent_multiplier' in item.keys()
        if item['agent_multipler'] == 1:
            pddl_goals = item['pddl_goals']
            problem = item['problem'] #'bbl3_ttt_00184',
            # print(problem)
            # if not 'agent_multiplier' in item.keys():
            #     num_of_agent = item['num_of_agents']
            #     agent_multiplier = int( num_of_agent/agent_num_dict[result['domain_name']])
            #     query = {'_id':item['_id']}
            #     updates = {"$set": {'agent_multiplier':agent_multiplier}}
            #     my_collection.update_one(query,updates)


            write_one_problems(problem_template,pddl_goals,prefix+problem,domain_name)












