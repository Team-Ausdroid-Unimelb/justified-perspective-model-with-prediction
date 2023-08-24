import enum
# import pddl_model
import typing
import re
import logging
import copy
from util import PDDL_TERNARY
from util import EpistemicQuery,EQ_TYPE,Q_TYPE


LOGGER_NAME = "forward_epistemic_model"
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
from util import setup_logger

class EpistemicModel:
    logger = None
    external = None
    entities = {}
    variables = {}
    
    
    def __init__(self, handler, entities, variables, external):
        self.logger = setup_logger(LOGGER_NAME,handler,LOG_LEVEL) 
        self.entities = entities
        self.variables = variables
        self.external = external


    def allPerspectiveKeys(self, epistemic_goals_dict,prefix):
        keys = []
        # self.logger.debug(f'')
        # self.logger.debug(f'allPerspectiveKeys')
        # self.logger.debug(f'prefix{prefix}')
        eq_dict = {}
        perspective_name_list = set([''])
        for epistemic_goal_str,value in epistemic_goals_dict.items():
            temp_eq = self.partially_converting_to_eq(epistemic_goal_str)
            if type(temp_eq) == str:
                # this is the end of eq
                # no need to generate perspectives
                # just need to evaluate the result and return value
                # key = f"{prefix} {temp_eq}"
                # perspective_name_list.add("")
                pass
                
            else:
                # it means the query is not to the last level yet
                agents_str = temp_eq.agents_str
                content = temp_eq.q_content
                # key = f"{prefix} {temp_eq.header_str} {agents_str}"
                key = f"{temp_eq.header_str} {agents_str} "
                if key in eq_dict.keys():
                    eq_dict[key]['content'].update({content:value})
                else:
                    eq_dict[key] = {'q_type':temp_eq.q_type,'eq_type':temp_eq.eq_type,'q_group':temp_eq.q_group,'content':{content:value}}
                    
        # self.logger.debug(f'eq_dict in allPerspectiveKeys {eq_dict}')       
        
        for key,item in eq_dict.items():
            # generate perspectives
            new_path = []
            eq_type = item['eq_type']
            # self.logger.debug(f"calling local perspective for {key} and content {item['content']}")
            local_p_keys_list = self.allPerspectiveKeys(item['content'],key)
            # self.logger.debug(f"local_p_keys_list is {local_p_keys_list}")
            # perspectives_dict.update(local_perspectives)
            # self.logger.debug(f'perspectives_dict before adding local {perspective_name_list}')
            for lp_key in local_p_keys_list:
                p_key = key+lp_key
                perspective_name_list.add(p_key)
            # self.logger.debug(f'perspectives_dict after adding local {perspective_name_list}')
        
        perspective_name_list = sorted(perspective_name_list, key=len)
        # self.logger.debug(f'returned {perspective_name_list}')
        return perspective_name_list
        


    def epistemicGoalsHandlerP(self,epistemic_goals_dict, prefix, path, p_path):

        # self.logger.debug(f'')
        # self.logger.debug(f'epistemicGoalHandler')
        # self.logger.debug(f'prefix{prefix}')
        # perspectives_dict = {'':path[-1][0]}
        actions_name = str([a for s,a in path])
        previous_actions_name = "None"
        
        if len(path) > 1:
            previous_actions_name = str([a for s,a in path[:-1]])
        # self.logger.debug(f'actions_name {actions_name}')
        # self.logger.debug(f'previous_action_names {previous_actions_name}')
        
        all_p_keys = self.allPerspectiveKeys(epistemic_goals_dict,prefix)

        eq_dict = {}
        result_dict = {} 
        
        # there is no pervious perspectives path
        if "None" not in p_path.keys():
            # Then there is no initial perspectives
            p_path["None"] = {}
        
        # all_p_keys list are sorted, the short perspectives are going to be generated first
        for key in all_p_keys:
            if key not in p_path['None'].keys():
                if key == '':
                    empty_update = {}
                    empty_state = {}
                    p_path["None"][key] = {}
                    for v_name in path[-1][0].keys():
                        # does not matter for the global state
                        empty_update[v_name] = False
                        empty_state[v_name] = None
                    # initial perspective for "" is the current global state
                    p_path["None"][key]['states'] = [empty_state]
                    p_path["None"][key]['updates'] =[empty_update]
                else:
                    p_path["None"][key] ={}
                    # every one level will have two space
                    depth_indicator = key.count(' ')
                    # assert(depth_indicator %2 == 0, f"wrong key {key} when generating perspectives")
                    if depth_indicator >2:
                        parent_key_index = key[:key[:key.rfind(" ")].rfind(" ")].rfind(' ')
                        parent_key = key[:parent_key_index+1]
                        current_key = key[parent_key_index+1:]
                        # self.logger.debug(f"parent_key_index is {parent_key_index}")
                        # self.logger.debug(f"key is {key}")
                        # self.logger.debug(f"parent_key is {parent_key}")
                        # self.logger.debug(f"current_key is {current_key}")
                    else:
                        parent_key = ''
                        current_key = key
                    # assert(parent_key not in p_path["None"].keys(), f"wrong order handling perspectives, exists {p_path['None'].keys()}, but doing {parent_key}")
                    
                    eq_type_str = current_key.split(' ')[0]
                    agent_str = current_key.split(' ')[1][1:-1]
                    initial_p_path = {}
                    empty_state ={}
                    empty_updates = {}
                    for v_name in path[-1][0].keys():
                        empty_state[v_name]= None
                        empty_updates[v_name]= False
                    initial_p_path['states'] = [empty_state]
                    initial_p_path['updates'] = [empty_updates]
                    # ignoring group beliefs for now
                    if 'b' in eq_type_str:

                        state,updating = self._generateGroupPerspectives("",agent_str,p_path["None"][parent_key]['states'][-1],initial_p_path)
                        
                    elif 's' in eq_type_str:
                        state,updating = self._generateGroupObservations("",agent_str,p_path["None"][parent_key]['states'][-1],initial_p_path)
                    elif 'k' in eq_type_str:
                        state,updating = self._generateGroupObservations("",agent_str,p_path["None"][parent_key]['states'][-1],initial_p_path)
                    p_path["None"][key]['states'] = [state]
                    p_path["None"][key]['updates'] = [updating]
                    

        if actions_name not in p_path.keys():
            p_path[actions_name] = {}
            # all_p_keys list are sorted, the short perspectives are going to be generated first
        for key in all_p_keys:
            if key not in p_path[actions_name].keys(): 
                if key == '':
                    empty_update = {}
                    p_path[actions_name][key] = {}
                    for v_name in path[-1][0].keys():
                        # does not matter for the global state
                        empty_update[v_name] = False
                    # initial perspective for "" is the current global state
                    
                    p_path[actions_name][key]['states'] = p_path[previous_actions_name][key]['states'] + [path[-1][0]]
                    p_path[actions_name][key]['updates'] = p_path[previous_actions_name][key]['updates']  + [empty_update]
                else:
                    p_path[actions_name][key] = {}
                    # every one level will have two space
                    depth_indicator = key.count(' ')
                    # assert(depth_indicator %2 == 1, f"wrong key {key} when generating perspectives")
                    if depth_indicator >2:
                        parent_key_index = key[:key[:key.rfind(" ")].rfind(" ")].rfind(' ')
                        parent_key = key[:parent_key_index+1]
                        current_key = key[parent_key_index+1:]
                        # self.logger.debug(f"parent_key_index is {parent_key_index}")
                        # self.logger.debug(f"key is {key}")
                        # self.logger.debug(f"parent_key is {parent_key}")
                        # self.logger.debug(f"current_key is {current_key}")
                    else:
                        parent_key = ''
                        current_key = key
                    # assert(parent_key not in p_path[actions_name].keys(), f"wrong order handling perspectives, exists {p_path[actions_name].keys()}, but doing {parent_key}")
                    
                    eq_type_str = current_key.split(' ')[0]
                    agent_str = current_key.split(' ')[1][1:-1]

                    # initial_p_path = {}
                    # empty_state ={}
                    # empty_updates = {}
                    # for v_name in path[-1][0].keys():
                    #     empty_state[v_name]= None
                    #     empty_updates[v_name]= False
                    # initial_p_path['states'] = [empty_state]
                    # initial_p_path['updates'] = [empty_updates]
                    # ignoring group beliefs for now
                    if 'b' in eq_type_str:
                        state,updating = self._generateGroupPerspectives("",agent_str,p_path[actions_name][parent_key]['states'][-1],p_path[previous_actions_name][key])
                    elif 's' in eq_type_str:
                        state,updating = self._generateGroupObservations("",agent_str,p_path[actions_name][parent_key]['states'][-1],p_path[previous_actions_name][key])
                    elif 'k' in eq_type_str:
                        state,updating = self._generateGroupObservations("",agent_str,p_path[actions_name][parent_key]['states'][-1],p_path[previous_actions_name][key])
                    p_path[actions_name][key]['states'] = p_path[previous_actions_name][key]['states'] +[state]
                    p_path[actions_name][key]['updates'] = p_path[previous_actions_name][key]['updates']+[updating]

        # self.logger.debug(f"p_path is {p_path}")
        
        for eq_str, value in epistemic_goals_dict.items():

            p_str = eq_str[:eq_str.rfind(' ')+1]
            eqv_str = eq_str[eq_str.rfind(' ')+1:][1:-1]
            v_name = eqv_str.split(',')[0][1:-1]
            v_value = eqv_str.split(',')[1][1:-1]
            perspective = p_path[actions_name][p_str]['states'][-1]
                
            if v_name in perspective.keys() and not perspective[v_name] ==None:
                if perspective[v_name] == v_value:
                    result_dict[eq_str] = PDDL_TERNARY.TRUE
                else:
                    result_dict[eq_str] = PDDL_TERNARY.FALSE
            else:
                result_dict[eq_str] = PDDL_TERNARY.UNKNOWN
                
        return result_dict
        # exit()
        # # solving eq by perspectives
        # for key,item in eq_dict.items():
            
            
            
        #     # generate perspectives
        #     new_path = []
        #     eq_type = item['eq_type']
        #     if eq_type == EQ_TYPE.BELIEF:
        #         new_path = self._generateGroupPerspectives(path,item['q_type'],item['q_group'])
        #     elif eq_type == EQ_TYPE.SEEING or eq_type == EQ_TYPE.KNOWLEDGE:
        #         new_path = self._generateGroupObservations(path,item['q_type'],item['q_group'])
        #     # elif eq_type == EQ_TYPE.KNOWLEDGE:
        #     #     new_path = self._generateGroupObservations(self,path,item['q_type'],item['q_group'])
        #     else:
        #         assert("wrong eq_type of the epistemic query")
        #     # perspectives_dict.update({key:new_path[-1][0]})
        #     self.logger.debug(f"calling local perspective for {key} and content {item['content']}")
        #     local_perspectives, local_result_dict = self.epistemicGoalsHandler(item['content'],key,new_path)
        #     self.logger.debug(f"local_perspectives is {local_perspectives}")
        #     # perspectives_dict.update(local_perspectives)
        #     self.logger.debug(f'perspectives_dict before adding local {perspectives_dict}')
        #     for lp_key,lp_value in local_perspectives.items():
        #         p_key = key+lp_key
        #         perspectives_dict[p_key] = lp_value
        #     self.logger.debug(f'perspectives_dict after adding local {perspectives_dict}')
            
        #     for result_key,result_value in local_result_dict.items():
        #         result_key = key + result_key
        #         self.logger.debug(f'key is {key}, result_key is {result_key}')
        #         # result_key = result_key
        #         new_result_value = result_value
        #         if eq_type == EQ_TYPE.SEEING:
        #             if not self.external.agentsExists(new_path,item['q_group']):
        #                 new_result_value = PDDL_TERNARY.UNKNOWN
        #             elif result_value == PDDL_TERNARY.UNKNOWN:
        #                 new_result_value = PDDL_TERNARY.FALSE
        #             else:
        #                 new_result_value = PDDL_TERNARY.TRUE
        #         result_dict.update({result_key:new_result_value})
        # self.logger.debug(f'result_dict {result_dict}')
        # self.logger.debug(f'perspectives_dict {perspectives_dict}')
        # return perspectives_dict,result_dict

    def _evaluateContent(self,path,temp_eq):

        state = path[-1][0]
        # optional to add keywords to represent the value of formula
        # and it can be put into the external function
        
        # assuming query value of variables here
        content_list = temp_eq[1:-1].split(",")
        v_index = content_list[0].replace("'","")
        value = content_list[1].replace("'","")
        
        
        if v_index not in state.keys():
            return PDDL_TERNARY.UNKNOWN
        elif state[v_index] == value:
            return PDDL_TERNARY.TRUE
        else:
            return PDDL_TERNARY.FALSE
    
    def _generateGroupPerspectives(self,q_type,q_group,parent_state,p_path):
        
        # initial perspectives 
        new_state,new_update = self._generateOnePerspectives(q_group[0],parent_state,p_path)

        if len(q_group) == 1:
            return new_state,new_update
        else:
            if q_type == Q_TYPE.MUTUAL:
                pass
            elif q_type == Q_TYPE.DISTRIBUTION:
                pass
            elif q_type == Q_TYPE.COMMON:
                pass
            else:
                assert("wrong Q type")

    def _generateGroupObservations(self,q_type,q_group,parent_state,p_path):
        # initial perspectives 

        new_state,new_update = self._getOneObservation(parent_state,q_group[0])
        
        if len(q_group) == 1:
            return new_state,new_update
        else:
            if q_type == Q_TYPE.MUTUAL:
                pass
            elif q_type == Q_TYPE.DISTRIBUTION:
                pass
            elif q_type == Q_TYPE.COMMON:
                pass
            else:
                assert("wrong Q type")


    
    def _generateOnePerspectives(self,agt_id,parent_state,p_path):
        previous_update = p_path['updates'][-1]
        previous_state = p_path['states'][-1]
        observation,_ = self._getOneObservation(parent_state,agt_id)
        
        new_update = previous_update.copy()
        new_state = previous_state.copy()

        
        for v_name, updating in previous_update.items():
            if updating and not parent_state[v_name]==None:
                # the value has been seen before, but no valid value has been observed
                new_state[v_name] = parent_state[v_name]
                new_update[v_name] = False
            elif updating and parent_state[v_name]==None:
                # still no valid updates, will update in the next state
                pass
            else:
                # the value does not need to be updated
                pass

        
        for v_name,value in observation.items():
            if value == None:
                # the agent should observer this value
                # but the value is None due to its parent
                # so this value needed update once its parent seen this value
                new_update[v_name] = True
            else:
                new_state[v_name] = value
                new_update[v_name] = False

        return new_state,new_update
        # for i in range(len(path)):
        #     observation_list.append(self._getOneObservation(path[i][0],agt_id))
        # self.logger.debug(f'observation list is {observation_list}')
        # for i in range(len(path)):
        #     new_state = self._generateOnePerspective(state_template,observation_list[:i+1])
        #     new_path.append((new_state,path[i][1]))
        # return new_path
    
    
    def _generateOnePerspective(self,state_template,observation_list):
        new_state = {}
        for v_index,e in state_template.items():
            self.logger.debug(f'\t find history value for {v_index},{e}')
            ts_index = self._identifyLastSeenTimestamp(observation_list,v_index)
            self.logger.debug(f'\t last seen timestamp index: {ts_index}')
            value = self._identifyMemorizedValue( observation_list, ts_index,v_index)
            self.logger.debug(f'\t {v_index}"s value is: {value}')
            new_state.update({v_index:value})
        return new_state 
    
    def _identifyMemorizedValue(self,observation_list, ts_index,v_index):
        ts_index_temp = ts_index
        if ts_index_temp <0: return None
        
        while ts_index_temp >=0:

            # temp_observation = self.getObservations(external,state,agt_id,entities,variables)
            # logger.debug(f'temp observation in identifyMemorization: {temp_observation}')
            temp_observation = observation_list[ts_index_temp]
            if not v_index in temp_observation or temp_observation[v_index] == None:
                ts_index_temp += -1
            else:
                return temp_observation[v_index]
        
        ts_index_temp = ts_index + 1
        
        while ts_index_temp < len(observation_list):

            # temp_observation = self.getObservations(external,state,agt_id,entities,variables)
            temp_observation = observation_list[ts_index_temp]
            if not v_index in temp_observation or temp_observation[v_index] == None:
                ts_index_temp += 1
            else:
                return temp_observation[v_index]        
        return None

    def _identifyLastSeenTimestamp(self,observation_list:typing.List,v_index):
        ts_index_temp = len(observation_list) -1
        
        # checking whether the variable has been seen by the agent list before
        while ts_index_temp >=0:
            
            # state,_ = path[ts_index_temp]

            # checking with observation
            if v_index in observation_list[ts_index_temp] :
                return ts_index_temp
            else:
                ts_index_temp -= 1
        return -1
    
    def _getOneObservation(self,state,agt_id):
        new_state = {}
        new_update = {}

        for v_name,value in state.items():
            if self.external.checkVisibility(state,agt_id,v_name,self.entities,self.variables)==PDDL_TERNARY.TRUE:
                new_state.update({v_name: value})
            new_update.update({v_name:False})

        return new_state,new_update
    
    
    def partially_converting_to_eq(self,eq_str):
        match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
        if match == None:
            self.logger.debug(f"return eq string {eq_str}")
            return eq_str
        else:
            eq_list = eq_str.split(" ")
            header_str = eq_list[0]
            agents = eq_list[1]
            content = eq_str[len(header_str)+len(agents)+2:]
            return EpistemicQuery(header_str,agents,content)
        
    def intersectObservation(self,state1,state2):
            new_state = {}
            for k,v in state1.items():
                if k in state2.keys():
                    if v == state2[k]:
                        new_state[k] = v
            return new_state

        
        