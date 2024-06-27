import pymongo
import os
import json
from optparse import OptionParser
import sys
import importlib
import random

current_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.join(current_directory, '..')
sys.path.append(os.path.abspath(root_directory))
from utils.pddl_generator import load_yaml_file
import pymongo.errors

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python runner.py <options>

    """
    parser = OptionParser(usageStr)
    parser.add_option('-t', '--time_out', dest="time_out", help='timeout, default 600s', type='int', default=600)
    parser.add_option('-m', '--memory_out', dest="memory_out", help='memoryout, default 8GB', type='int', default=8)
    # parser.add_option('-p', '--problem_template', dest="problem_template_file", help='path to problem_template.py', default='experiments/coin/problem_template.py')
    parser.add_option('-s', '--search_name', dest="search_name", help='the search name', default='bfs')
    parser.add_option('-c', '--config', dest="config", help='the config file', default='scripts/config/mdb_config.yaml')
    parser.add_option('-d', '--domain_path', dest="domain_path", help='the domain_path', default='experiments/bbl/domain.pddl')
    parser.add_option('-g', '--goal_sizes', dest="goal_size_list",  help='should be a list of integer divided by ",", read as a string', default='1,2,3,4')
    parser.add_option('--goal_depths', dest="goal_depth_list",  help='should be a list of integer divided by ",", read as a string', default='1,2,3,4')
    parser.add_option('-a','--num_of_agent', dest="num_of_agent", help='the number of agent used to find correct json files', type='int', default=2)
    parser.add_option('-n','--num_of_instances', dest="num_of_instances", help='the number of instances to generate (each instance will be generated by enumerate the init) for each goal and depth combination', type='int', default=1)
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def create_unique_index(collection):
    collection.create_index(
        [("domain_name", 1), ("num_of_agent", 1), ("goal_index", 1), ("init_name", 1), ("goal_size", 1), ("designed_goal_depth", 1), ("search_name", 1)],
        unique=True
    )
    
def delete_unique_index(collection):
    collection.drop_index(
        [("domain_name", 1), ("num_of_agent", 1), ("goal_index", 1), ("init_name", 1), ("goal_size", 1), ("designed_goal_depth", 1), ("search_name", 1)],
    )




if __name__ == '__main__':



    options = loadParameter()

    config_path = options.config
    domain_path = options.domain_path
    # domain_name = os.path.basename(domain_path).replace(".pddl","")
    domain_dir = os.path.dirname(domain_path)
    domain_name = os.path.split(domain_dir)[-1]
    goal_sizes_str = options.goal_size_list
    goal_size_list = [int(item) for item in goal_sizes_str.split(',') if item.strip()]
    goal_depths_str = options.goal_depth_list
    goal_depth_list = [int(item) for item in goal_depths_str.split(',') if item.strip()]
    num_of_agent = options.num_of_agent
    num_of_instances = options.num_of_instances
    search_name = options.search_name
    time_out = options.time_out
    memory_out = options.memory_out
    
    mdb_config = load_yaml_file(config_path)
    url = mdb_config.get("url")
    username = mdb_config.get("username")
    password = mdb_config.get("password")
    db_name = mdb_config.get("db_name")
    # main_collection_name = mdb_config.get("main_collection_name")
    job_index_collection_name = mdb_config.get("job_index")
    job_record_collection_name = mdb_config.get("job_record_collection_name")
    job_record_backup_collection_name = mdb_config.get("job_record_backup_collection_name")
    
    my_client = pymongo.MongoClient(url,username=username,password=password)
    my_db = my_client[db_name]
    # main_collection = my_db[main_collection_name]
    job_index_collection = my_db[job_index_collection_name]
    job_record_collection = my_db[job_record_collection_name]
    job_record_backup_collection = my_db[job_record_backup_collection_name]
    
    create_unique_index(job_record_backup_collection)


    
    # goal_depth_info_path = os.path.join(domain_dir,f"a{num_of_agent}_goal_depth-goalsize_info.json")
    # goal_depth_info = dict()
    # with open(goal_depth_info_path, 'r') as f:
    #     goal_depth_info = json.load(f)
    
    # let's find all job for now.
    query = {'num_of_agent':num_of_agent,'domain_name':domain_name,'goal_size':{'$in':goal_size_list},'goal_depth':{'$in':goal_depth_list}}
    
    for item in job_index_collection.find(query):
        
        domain_name = item['domain_name']
        num_of_agent = item['num_of_agent']
        goal_size = item['goal_size']
        goal_depth = item['goal_depth']
        job_base_name = item['job_base_name']
        num_of_instance = item['num_of_instance']
        instance_size = item['instance_size']
        instances = item['instances']
        
        domain_dir = os.path.join('experiments',domain_name)
        
        init_dict = dict()
        init_dict_path = os.path.join(domain_dir,f"a{num_of_agent}_init.json")
        with open(init_dict_path, 'r') as f:
            init_dict = json.load(f)
        num_of_init = len(init_dict)
        
        problem_base_path = os.path.join(domain_dir,f"a{num_of_agent}_problem_base.json")
        problem_base_dict = dict()
        with open(problem_base_path, 'r') as f:
            problem_base = json.load(f)
            for k,items in problem_base.items():
                problem_base_dict.update(items)
        
        
        
        
        for instance in instances:
            init_name = instance[0]
            goal_index = instance[1]
            
            # init_list = init_dict[init_name]
            # goal_list = problem_base_dict[goal_index]
            
            one_job_info = dict()
            one_job_info['domain_name'] = domain_name
            one_job_info['num_of_agent'] = num_of_agent
            one_job_info['goal_size'] = goal_size
            one_job_info['designed_goal_depth'] = goal_depth
            one_job_info['init_name'] = init_name
            one_job_info['goal_index'] = goal_index
            one_job_info['search_name'] = search_name
            one_job_info['time_out'] = time_out
            one_job_info['memory_out'] = memory_out
            
            success_insert = True
            
            try:
                job_record_backup_collection.insert_one(one_job_info)
            except pymongo.errors.DuplicateKeyError:
                print(f"Duplicate key error: {one_job_info}")
                success_insert = False
                continue
            
            if success_insert:
                try:
                    job_record_collection.insert_one(one_job_info)
                except pymongo.errors.DuplicateKeyError:
                    print(f"Duplicate key error: {one_job_info}")
                    raise ValueError("Duplicate key error")
                
            # query = {'domain_name':domain_name,'num_of_agent':num_of_agent,'goal_size':goal_size,'goal_depth':goal_depth,'init_name':init_name,'goal_index':goal_index}
            # if job_record_collection.find_one(query) == None:
            #     new_record = dict()
            #     new_record['domain_name'] = domain_name
            #     new_record['num_of_agent'] = num_of_agent
            #     new_record['goal_size'] = goal_size
            #     new_record['goal_depth'] = goal_depth
            #     new_record['init_name'] = init_name
            #     new_record['goal_index'] = goal_index
            #     new_record['job_base_name'] = job_base_name
            #     new_record['instance_size'] = instance_size
            #     new_record['instance'] = num_of_instance
            #     try:
            #         job_record_collection.insert_one(new_record)
            #     except pymongo.errors.DuplicateKeyError:
            #         print(f"Duplicate key error: {job_base_name}")
            #         continue
    delete_unique_index(job_record_backup_collection)
    # for goal_size in goal_size_list:
    #     for goal_depth in goal_depth_list:
    #         # instance_dict = dict() 
    #         instance_list = list()
    #         goal_set_size = goal_depth_info[str(goal_size)][str(goal_depth)]
    #         max_instances = goal_set_size*num_of_init
    #         if max_instances < num_of_instances:
    #             # it means the test cases is not enough
    #             # we need to enumerate the init and goal
    #             for init_name in init_dict.keys():
    #                 for goal_index in range(1,goal_set_size+1):
    #                     # generate one instance
    #                     # temp_instance = dict()
    #                     # temp_instance['goal_index'] = key
    #                     # temp_instance['init_name'] = init_name
    #                     # init_dict_list.append(temp_instance)
    #                     instance_list.append((init_name,goal_index))
    #         elif max_instances < num_of_instances/10:
    #             # it means the test cases is dense
    #             # we need to enumerate the pairs and randomly select some of them
    #             all_instance_list = [(instance_name, goal_index) for instance_name in init_dict.keys() for goal_index in range(1,goal_set_size+1)]
    #             random.shuffle(all_instance_list)
    #             instance_list = all_instance_list[:num_of_instances]
    #         else:
    #             instance_set = set()
    #             while len(instance_set) < num_of_instances:
    #                 init_name = random.choice(list(init_dict.keys()))
    #                 goal_index = random.randint(1,goal_set_size)
    #                 instance_set.add((init_name,goal_index))
    #             instance_list = list(instance_set)
    #         # all instance list should be finished
    #         # print(instance_list)
    #         print(len(instance_list))
    #         job_base_name = f"{domain_name}_a{num_of_agent}_g{goal_size}_d{goal_depth}"
    #         job_dict = dict()
    #         job_dict['domain_name'] = domain_name
    #         job_dict['num_of_agent'] = num_of_agent
    #         job_dict['goal_size'] = goal_size
    #         job_dict['goal_depth'] = goal_depth
            
    #         job_dict['job_base_name'] = job_base_name
    #         job_dict['num_of_instance'] = len(instance_list)
    #         job_dict['instance_size'] = num_of_instances
    #         job_dict['instances'] = instance_list
    #         try:
    #             job_index_collection.insert_one(job_dict)
    #         except pymongo.errors.DuplicateKeyError:
    #             print(f"Duplicate key error: {job_base_name}")
    #             continue
            
                        
    # delete_unique_index(job_index_collection)
    

    # if options.search_name == "":
    #     raise ValueError("search_name is empty")
    # else:
    #     search_name = options.search_name 
    #     problem_query = {}
    #     # if options.solvable:
    #     #     problem_query = {'solvable':True,'total_goal_size':1}


    #     # for key,collection in collection_dict.items():
    #     #     # existing_problems = []
    #     #     print(problem_query)
            
    #     collection = my_db['all_instance']
    #     problem_query = {'solvable':True,'total_goal_size':1,'max_goal_depth':2,'search':'bfs'}

    #     for item in collection.find(problem_query):
    #         domain_path = item['domain_path']
    #         problem_name = item['problem_name']
    #         problem_path = item['problem_path']
    #         init_name = item['init_name']
    #         # print(problem)
    #         # problem_file_name = 'problem_'+problem+".pddl"
    #         # if existing_problems == []:
    #         #     existing_problems = os.listdir(domain_path)'
    #         if not os.path.exists(problem_path):

    #             # query = {'search':search_name,'problem_name':problem_name,'init_name':init_name,'problem_path':problem_path}
    #             # if my_collection.find_one(query) == None:
    #                 print("Not found, adding it: ", problem_name)
    #                 domain_name = item['domain_name']
                    
                    
    #                 pddl_goals = item['goals']
    #                 num_of_agent = item['num_of_agents']
    #                 # agent_multiplier= item['agent_multiplier']
    #                 if num_of_agent not in template_file_dict[domain_name].keys():
    #                     template_path = domain_path.replace("domain.pddl",f"problem_template{num_of_agent}.py")
    #                     module_name = "PDDL_Template"
    #                     spec = importlib.util.spec_from_file_location(module_name,template_path)
    #                     problem_template_module = importlib.util.module_from_spec(spec)
    #                     spec.loader.exec_module(problem_template_module)
    #                     temp_problem_template = getattr(problem_template_module,"PDDL_Template")
    #                     template_file_dict[template_path] = temp_problem_template
                        
    #                 if init_name not in init_file_dict[domain_name].keys():
    #                     init_path = domain_path.replace("domain.pddl",f"problem_template{num_of_agent}.json")
    #                     with open(init_path) as f:
    #                         init_dict = json.load(f)
    #                     init_file_dict[num_of_agent] = init_dict
    #                 problem_template = template_file_dict[template_path]
    #                 init_list = init_file_dict[num_of_agent][init_name]
                    
    #                 # new_problem_path = problem_path.replace(".pddl", "_"+init_name+".pddl")
    #                 new_problem_path = problem_path
    #                 # print(init_list)
    #                 write_one_problems(problem_template,pddl_goals,init_list,problem_name,domain_name,new_problem_path)


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











