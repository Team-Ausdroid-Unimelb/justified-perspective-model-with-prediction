# this is for domains
import pymongo
import os
import json

import pymongo.errors

my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
my_db = my_client['result']

# my_collection = my_db['20240329']
# my_collection = my_db['goalsize2']
# my_collection = my_db['goalsize3']
my_collection = my_db['20240417']
coin_domain_collection = my_db['coin']
spcoin_domain_collection = my_db['spcoin']
bbl_domain_collection = my_db['bbl']
corridor_domain_collection = my_db['corridor']
grapevine_domain_collection = my_db['grapevine']
sn_domain_collection = my_db['sn']


coin_domain_collection.create_index([('problem', 1)], unique=True)
spcoin_domain_collection.create_index([('problem', 1)], unique=True)
bbl_domain_collection.create_index([('problem', 1)], unique=True)
corridor_domain_collection.create_index([('problem', 1)], unique=True)
grapevine_domain_collection.create_index([('problem', 1)], unique=True)
sn_domain_collection.create_index([('problem', 1)], unique=True)


collection_dict = {
   'coin' : coin_domain_collection,
   'spcoin' : spcoin_domain_collection,
   'bbl' : bbl_domain_collection,
   'corridor' : corridor_domain_collection,
   'grapevine' : grapevine_domain_collection,
   'sn' : sn_domain_collection,
}

domain_dict = {
   'coin' : dict(),
   'spcoin' : dict(),
   'bbl' : dict(),
   'corridor' : dict(),
   'grapevine' : dict(),
   'sn' : dict(),
}


for result_json in my_collection.find():
    domain_name = result_json['domain_name']
    problem_name = result_json['problem']
    agent_multiplier = result_json['agent_multiplier']

    # if the job has not finished
    if "running" in result_json.keys():
        continue
    

    try:
        del result_json["_id"]
        del result_json["plan"]
        del result_json["path_length"]
        del result_json["pruned"]

        del result_json["pruned_by_unknown"]
        del result_json["pruned_by_visited"]
        del result_json["timeout"]
        del result_json["memoryout"]
        del result_json["goal_checked"]
        del result_json["expanded"]
        del result_json["generated"]
        del result_json["epistemic_calls"]
        del result_json["epistemic_call_time"]
        del result_json["epistemic_call_time_avg"]
        del result_json["init_time"]
        del result_json["search_time"]
        del result_json["search"]
        
        domain_path = os.path.join("experiments",domain_name)
        agent_multiplier = result_json['agent_multiplier']
        template_path = os.path.join(domain_path,f"problem_template{str(agent_multiplier)}.py")
        result_json['domain_path'] = domain_path
        result_json['template_path'] = template_path

        collection_dict[domain_name].insert_one(result_json)


    except pymongo.errors.DuplicateKeyError:
        print('Duplicate document not inserted.')
        # temp_dict['search_results'] = dict()
        # domain_dict[domain_name][problem_name] = temp_dict

    # search_name = result_json['search']
    # del result_json["goals"]
    # del result_json["pddl_goals"]
    # del result_json["goal_size"]
    # del result_json["solvable"]
    # del result_json["_id"]
    
#     domain_dict[domain_name][problem_name]['search_results'][search_name] = result_json

# for domain_name,domain_info in domain_dict.items():
#     domain_collection = my_db[domain_name]
#     for _,item in domain_info.items():
#         domain_collection.insert_one(item)

# print(domain_dict)

