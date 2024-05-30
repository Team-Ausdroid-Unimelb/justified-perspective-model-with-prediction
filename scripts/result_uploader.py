import pymongo
import os
import json


def create_unique_index(collection):
    collection.create_index(
        [("domain_name", 1), ("problem_name", 1), ("search", 1), ("init_name", 1)],
        unique=True
    )

def remove_unique_index(collection):
    collection.drop_index("domain_name_1_problem_name_1_search_1_init_name_1")





def main():
    my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
    my_db = my_client['new_result']
    my_collection = my_db['all_instance']



    create_unique_index(my_collection)
    # result_path = os.path.join("output","02-05-2024_21-53-36")
    result_path = os.path.join("output","uploading")
    result_list = os.listdir(result_path)
    result_list.sort()
    for path in result_list:
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
            actual_problem_name = result['problem_path'].split("/")[-1].split(".")[0]
            init_name = "init_"+ actual_problem_name.split("_init_")[1]
            result['init_name'] = init_name


            
            
            try:
                my_collection.insert_one(result)
                # print("Document inserted successfully")
            except pymongo.errors.DuplicateKeyError:
                print("Duplicate document found. Insertion skipped.")
                print(file_path)
                query = {'domain_name':result['domain_name'],'problem_name':result['problem_name'],'search':result['search'],'init_name':result['init_name']}
                found = my_collection.find_one(query)
                print(found)

    remove_unique_index(my_collection)
    my_client.close()

if __name__ == "__main__":
    main()