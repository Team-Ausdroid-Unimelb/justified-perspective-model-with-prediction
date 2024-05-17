import pymongo
import os
import json
import pandas as pd
import yaml
from optparse import OptionParser
import sys
import itertools
import traceback

import matplotlib.pyplot as plt

def get_config_by_yaml(path):
    with open(path, "r") as input:
        try:
            options = yaml.safe_load(input)
            return options
            # print(a)
        except yaml.YAMLError as error:
            traceback.print_exc()
            print(error) 

def loadParameter():

    """
    Processes the command line input for running the tournament
    """
    usageStr = """
    USAGE:      python experiment_runner.py <options>
    EXAMPLES:   (1) 



    """
    
    # logger.info("Parsing Options")
    parser = OptionParser(usageStr)
    parser.add_option('-c','--config', dest="config_path", help='path to the config yaml file to display the results',default='scripts/configs/bbl/bbl-unsolvable_search-ga_time.yaml')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

class FigGenerator():

    def run(self,config_path,shareY=False):
        print(config_path)
        folder_path,file_name = os.path.split(config_path)
        result_path = folder_path.replace('configs','figs')
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        result_file_name = file_name.replace('yaml','png')
        result_file_path = os.path.join(result_path,result_file_name)
        config_yaml = get_config_by_yaml(config_path)




        my_client = pymongo.MongoClient("mongodb://localhost:27017",username="admin",password="90054")
        my_db = my_client['new_result']

        my_collection = my_db['all_instance']

        filters = config_yaml.get('filters')
        filter_query = dict()
        for item in filters:
            name = item.get('name')
            value = item.get('value')
            filter_query.update({name:value})
        # print(filter_query)
        query_config = config_yaml.get('keys')
        query_config_dict = dict()
        for item in query_config:
            name = item.get('name')
            values = item.get('values')
            query_config_dict.update({name:values})

        product = itertools.product(*query_config_dict.values())
        product_list = [{key: value for key, value in zip(query_config_dict.keys(), values)} for values in product]
        
        pd_query_list = list()
        for item in product_list:
            query_str = ""
            for k,v in item.items():
                if type(v) == str:
                    value = f"'{v}'"
                else:
                    value = v
                query_str += f"{k} == {value}"
                query_str += " and "
            # print(f"before remove: {query_str}")
            query_str = query_str[:-len(" and ")]
            # print(f"after remove: {query_str}")
            pd_query_list.append(query_str)

        # print(pd_query_list)

        display_column_names = config_yaml.get('display_column_names')

        data = my_collection.find(filter_query)
        # print(list(data))
        # if list(data) == []:
        #     print("No data found")
        #     return
        # print(list(data))
        data_list = list(data)
        # print(data_list)
        if data_list == []:
            print("No data found")
            return
        # print(data_list)

        df = pd.DataFrame(data_list)

        # output_df = df.query("search == 'bfsdcu'")
        # # output_df = df['search']
        # output_df.to_csv('output.csv', index=False)
        filtered_df_list = list()
        for query_str in pd_query_list:
            query_name = query_str.replace(' == ',':').replace(' and ',',\n')
            filtered_df = df.query(query_str)
            filtered_df_list.append({'query_name':query_name,'query':query_str,'df':filtered_df})

        # print(df)

        fig, axes = plt.subplots(
            nrows=1, 
            ncols=len(pd_query_list), 
            figsize=(20, 14), sharey=True, sharex=False)
        # axes[0].set_ylabel('Scores')

        # display_column_keys = [i[:3] for i in display_column_names]
        display_column_keys = []
        prefix = ""
        for name in display_column_names:
            display_column_keys.append(prefix+name)
            prefix += "\n"
            

        for i in range(len(pd_query_list)):
            query_item = filtered_df_list[i]
            query_name = query_item['query_name']
            query_df = query_item['df']
            data_list = [query_df[f'{key}'].to_list() for key in display_column_names]
            axes[i].boxplot(data_list, labels=display_column_keys)
            axes[i].set_title(query_name)
        # plt.tight_layout()

        fig.subplots_adjust(bottom=0.15,top=0.95,right=0.95,left=0.05,hspace=0.90) 
        plt.savefig(result_file_path, dpi=300, bbox_inches='tight')
        # plt.show()
            
        plt.close()

if __name__ == '__main__':

    options = loadParameter()
    config_path = options.config_path
    fg = FigGenerator(config_path)
    fg.run(config_path=config_path,shareY=True)
