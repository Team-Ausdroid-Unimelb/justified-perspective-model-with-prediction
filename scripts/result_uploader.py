import pymongo
import os
import json


def create_unique_index(collection):
    collection.create_index(
        [("domain_name", 1), ("problem_name", 1), ("search", 1)],
        unique=True
    )





def main():
    my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
    my_db = my_client['new_result']

    agent_num_dict = {
        'bbl':2,
        'coin':2,
        'spcoin':2,
        'corridor':3,
        'grapevine':4,
        'sn':4,
    }

    my_collection = my_db['all_instance']
    create_unique_index(my_collection)
    # result_path = os.path.join("output","02-05-2024_21-53-36")
    result_path = os.path.join("output","uploading")
    for path in os.listdir(result_path):
        if ".json" in path:
            file_path = os.path.join(result_path,path)

            with open(file_path,"r") as f:
                try:
                    result = json.load(f)
                except:
                    print(file_path)
                    exit()
            # num_of_agent = result['num_of_agents']
            
            # agent_multiplier = int( num_of_agent/agent_num_dict[result['domain_name']])
            # print(num_of_agent)
            # print(agent_num_dict[result['domain_name']])
            # print(agent_multiplier)
            # result['agent_multiplier'] = agent_multiplier
            # result['functions'] = 9
            try:
                my_collection.insert_one(result)
                # print("Document inserted successfully")
            except pymongo.errors.DuplicateKeyError:
                print("Duplicate document found. Insertion skipped.")
                print(file_path)

if __name__ == "__main__":
    main()