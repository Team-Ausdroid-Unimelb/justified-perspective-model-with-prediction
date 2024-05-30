import pymongo
import os

from optparse import OptionParser
import sys

import pymongo.errors

irrelevant_field_list = [
    '_id','search','init_time','search_time',
    'expanded','goal_checked','generated',
    'pruned','pruned_by_visited','pruned_by_unknown',
    'epistemic_calls','epistemic_call_time','epistemic_call_time_avg','epistemic_call_time_max'
]

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python runner.py <options>

    """
    parser = OptionParser(usageStr)

    # parser.add_option('-p', '--problem_template', dest="problem_template_file", help='path to problem_template.py', default='experiments/coin/problem_template.py')
    parser.add_option('-s', '--search_name', dest="search_name", help='the search name', default='bfsdc')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

def create_unique_index(collection):
    collection.create_index(
        [("domain_name", 1), ("problem_name", 1), ("init_name", 1)],
        unique=True
    )
    
def delete_unique_index(collection):
    collection.drop_index(
        [("domain_name", 1), ("problem_name", 1), ("init_name", 1)]
    )

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
    
    for key in collection_dict:
        create_unique_index(collection_dict[key])
    #     index_list = collection_dict[key].index_information()
    #     if 'problem_name_1' in index_list:
    #         print("Dropping index: ",key)
    #         collection_dict[key].drop_index('problem_name_1')
    #     # collection_dict[key].drop_index('problem_name_1')

    # index_list = bbl_domain_collection.index_information()
    # for index_info in index_list:
    #     print(index_info)
    # # print(index_list)
    
    # exit()
    template_file_dict = dict()

    if options.search_name == "":
        raise ValueError("search_name is empty")
    else:
        search_name = options.search_name 
        query = {'search':search_name}

        for item in my_collection.find(query):
            domain_name = item['domain_name']
            domain_collection = collection_dict[domain_name]
            problem_name = item['problem_name']
            # problem_query = {'problem_name':problem_name}
            # if domain_collection.find_one(problem_query) == None:
                # it means the problem is not in the domain collection
                # print("Not found, adding: ",problem_name)
            del item['_id']
            del item['search']
            del item['init_time']
            del item['search_time']
            del item['pruned']
            del item['expanded']
            del item['pruned_by_visited']
            del item['pruned_by_unknown']
            del item['goal_checked']
            del item['generated']
            del item['epistemic_calls']
            del item['epistemic_call_time']
            del item['epistemic_call_time_avg']
            del item['epistemic_call_time_max']
            del item['epistemic_call_length']
            del item['epistemic_call_length_avg']
            del item['epistemic_call_length_max']
            if 'epistemic_call_time_depth_ratio' in item:
                del item['epistemic_call_time_depth_ratio']

            
            
                # domain_collection.insert_one(item)
            try:
                domain_collection.insert_one(item)
                # print("Document inserted successfully")
            except pymongo.errors.DuplicateKeyError:
                print("Duplicate document found. Insertion skipped.")
                print(domain_name,problem_name,item['init_name'])
                
    for key in collection_dict:
        delete_unique_index(collection_dict[key])
