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
import seaborn as sns

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
    parser.add_option('-c','--config', dest="config_path", help='path to the config yaml file to display the results',default='scripts/violin_configs/test.yaml')
    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options

class FigGenerator():

    def run(self,config_path,shareY=True,shareX=True):
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
        print(filter_query)
        
        data = my_collection.find(filter_query)
        data_list = list(data)
        # print(data_list)
        if data_list == []:
            print("No data found")
            return
        # print(data_list)

        df = pd.DataFrame(data_list)


        query_config = config_yaml.get('keys')
        query_config_dict = dict()
        for item in query_config:
            name = item.get('name')
            values = item.get('values')
            if values == []:
                values = df[name].unique()
                print(values)
                values = values.tolist()
                values = sorted(values)
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



        
        # print(list(data))
        # if list(data) == []:
        #     print("No data found")
        #     return
        # print(list(data))

        # print(df)
        x_axis = config_yaml.get('x_axis')
        y_axis = config_yaml.get('y_axis')

        # print(pd_query_list)
        # display_column_mapping = config_yaml.get('display_column_mapping')
        # for one_mapping in display_column_mapping:
        #     mapping_name = one_mapping.get('name')
        #     mapping_values = one_mapping.get('values')
        #     print(mapping_name)
        #     print(mapping_values)
        #     if mapping_values == None:
        #         mapping_values = df[mapping_name].unique()
        #     print(mapping_values)
        # display_column_names = config_yaml.get('display_column_names')
        # exit()


        # output_df = df.query("search == 'bfsdcu'")
        # # output_df = df['search']
        # output_df.to_csv('output.csv', index=False)
        filtered_df_list = list()
        for query_str in pd_query_list:
            print(query_str)
            query_name = query_str.replace(' == ',':').replace(' and ',',\n')
            filtered_df = df.query(query_str)
            # print(query_name)
            # print(filtered_df[y_axis].to_list())
            filtered_df_list.append({'query_name':query_name,'query':query_str,'df':filtered_df})

        # with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
        #     for i, query_item in enumerate(filtered_df_list):
        #         query_name = query_item['query_name']
        #         query_df = query_item['df']
        #         sheet_name = query_name.replace(':','_').replace(',','_')
        #         query_df.to_excel(writer, sheet_name=sheet_name, index=False)


        # print(df)

        fig, axes = plt.subplots(
            nrows=1, 
            ncols=len(pd_query_list), 
            figsize=(20, 14), sharey=shareY, sharex=shareX)
            
        # min_y = 999
        # max_y = 0

        if len(pd_query_list) > 1:
            for i in range(len(pd_query_list)):
                
                query_item = filtered_df_list[i]
                query_name = query_item['query_name']
                query_df : pd.DataFrame = query_item['df']
                axes[i].scatter(x=query_df[x_axis], y=query_df[y_axis], s=10, alpha=0.5, color='black')
                
                axes[i].set_title(query_name)
                data_size = query_df[x_axis].size
                # print(data_size)
                # if data_size < 10:
                #     continue
                # ax = sns.kdeplot(x=query_df[x_axis], y=query_df[y_axis],cmap="Blues", fill=True, thresh=0.05, ax=axes[i])
                # ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
                # data_list = [query_df[f'{key}'].to_list() for key in display_column_names]
                # axes[i].boxplot(data_list, labels=display_column_keys)

        else:
            query_item = filtered_df_list[0]
            query_name = query_item['query_name']
            query_df : pd.DataFrame = query_item['df']
            axes.scatter(x=query_df[x_axis], y=query_df[y_axis], s=10, alpha=0.5, color='black')
            
            axes.set_title(query_name)

        fig.subplots_adjust(bottom=0.15,top=0.95,right=0.95,left=0.05,hspace=0.90) 
        plt.savefig(result_file_path, dpi=600, bbox_inches='tight')
        # plt.savefig(result_file_path, dpi=300, bbox_inches='tight')
        # plt.show()
            
        plt.close()

if __name__ == '__main__':

    options = loadParameter()
    config_path = options.config_path
    fg = FigGenerator()
    fg.run(config_path=config_path,shareY=True,shareX=True)
