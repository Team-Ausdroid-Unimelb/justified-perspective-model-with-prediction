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
    # parser.add_option('-s', '--search_name', dest="search_name", help='the search name', default='bfs')
    # parser.add_option('-i','init_file', dest="init_file", help='path to the init dict file', default='experiments/bbl/problem_template2.json')
    
    # parser.add_option('--solvable', dest="solvable", help='only return solvable domains', default=False,action='store_true')
    parser.add_option('-a','--num_of_agent',dest="num_of_agent",type='int',help='number of agents',default=2)
    parser.add_option('-d','--domain_names',dest="domain_names",help='domain name list',default="bbl")
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def write_one_problems(problem_template,pddl_goal_list,init_list,problem_name,domain_name,problem_path):


    output_str = problem_template.problem_prefix1
    output_str = output_str + problem_name.replace(domain_name,'')
    output_str = output_str + problem_template.problem_prefix2
    output_str = output_str + problem_template.init_pre_fix
    for init_items in init_list:
        if len(init_items) == 2:
            output_str += f"          (assign {init_items[0]} {init_items[1]})\n"
        else:
            raise ValueError("init_items length is not 2")
    output_str += problem_template.init_surfix
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
    
    
    domain_name_list = options.domain_names.split(',')
    
    

    for domain_name in domain_name_list:
        init_dict = {}
        init_dict_path = os.path.join("experiments",domain_name,f"problem_template{options.num_of_agent}.json")
        with open(init_dict_path,"r") as f:
            init_dict = json.load(f)
        
        # load problem template
        problem_template_file = os.path.join("experiments",domain_name,f"problem_template{options.num_of_agent}.py")
        module_name = "PDDL_Template"
        spec = importlib.util.spec_from_file_location(module_name,problem_template_file)
        problem_template_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(problem_template_module)
        domain_problem_template = getattr(problem_template_module,"PDDL_Template")
        # template_file_dict[domain_name][options.num_of_agent] = temp_problem_template
        
        
        domain_collection = collection_dict[domain_name]
        query = {'total_goal_size':1,'num_of_agents':options.num_of_agent}
        for item in domain_collection.find(query):
            if item['init_name'] == 'init_a2_00023':
            #     update_query = {'_id':item['_id']}
            #     problem_path = item['problem_path'].replace(".pddl","_init_a2_00023.pddl")
            #     print(problem_path)
            #     updates = {"$set": {'problem_path':problem_path}}
            #     domain_collection.update_one(update_query,updates)
            # else:
                
                domain_path = item['domain_path']
                problem_name = item['problem_name']
                old_problem_path = item['problem_path']
                    
                for local_init_name,init_list in init_dict.items():
                    problem_path = os.path.join("experiments",domain_name,f'problem_{problem_name.replace("domain_name","")}_{local_init_name}.pddl')
                    # problem_path = f'problem_{problem_name.replace("domain_name","")}_{local_init_name}.pddl'
                    print(problem_path)
                    if os.path.exists(problem_path):
                        continue
                    pddl_goals = item['goals']
                    
                    write_one_problems(domain_problem_template,pddl_goals,init_list,problem_name,domain_name,problem_path)
                    
                    # for init in init_list:
                    #     update_query = {'_id':item['_id']}
                    #     problem_path = item['problem_path'].replace(".pddl",f"_{local_init_name}.pddl")
                    #     updates = {"$set": {'problem_path':problem_path}}
                    #     domain_collection.update_one(update_query,updates)
                        # print(problem_path)
                # print(problem)
                # problem_file_name = 'problem_'+problem+".pddl"
                # if existing_problems == []:
                #     existing_problems = os.listdir(domain_path)
                # if not os.path.exists(problem_path):
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
                #         



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












