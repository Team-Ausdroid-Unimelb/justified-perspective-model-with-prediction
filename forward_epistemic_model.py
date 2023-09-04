import enum
# import pddl_model
import typing
import re
import logging
import copy
from util import PDDL_TERNARY,EP_VALUE
from util import EpistemicQuery,EQ_TYPE,Q_TYPE


LOGGER_NAME = "forward_epistemic_model"
LOGGER_LEVEL = logging.INFO
# LOGGER_LEVEL = logging.DEBUG
from util import setup_logger

class EpistemicModel:
    logger = None
    external = None
    entities = {}
    variables = {}
    
    
    def __init__(self, handlers, entities, variables, external):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
        self.entities = entities
        self.variables = variables
        self.external = external


    def allPerspectiveKeys(self, epistemic_goals_dict,prefix):
        keys = []
        self.logger.debug('')
        self.logger.debug('allPerspectiveKeys')
        self.logger.debug('prefix: [%s]',prefix)
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
                    
        self.logger.debug('eq_dict in allPerspectiveKeys [%s]',eq_dict)       
        
        for key,item in eq_dict.items():
            # generate perspectives
            new_path = []
            eq_type = item['eq_type']
            
            self.logger.debug("calling local perspective for [%s] and content [%s]",key,item['content'])
            local_p_keys_list = self.allPerspectiveKeys(item['content'],key)
            
            self.logger.debug("local_p_keys_list is [%s]",local_p_keys_list)
            # perspectives_dict.update(local_perspectives)
            self.logger.debug('perspectives_dict before adding local [%s]',perspective_name_list)
            for lp_key in local_p_keys_list:
                p_key = key+lp_key
                perspective_name_list.add(p_key)
            
            self.logger.debug('perspectives_dict after adding local [%s]',perspective_name_list)
        
        perspective_name_list = sorted(perspective_name_list, key=len)
        
        self.logger.debug('returned [%s]',perspective_name_list)
        return perspective_name_list
        


    def epistemicGoalsHandlerP(self,epistemic_goals_dict, prefix, path, p_path):
        
        self.logger.debug('')
        self.logger.debug('epistemicGoalHandler')
        self.logger.debug('prefix: [%s]',prefix)

        previous_actions_name = str(['-'])
        actions_name = str(['-'])+str([a for s,a in path])
        
        
        if len(path) > 1:
            previous_actions_name = previous_actions_name+ str([a for s,a in path[:-1]])
        
        self.logger.debug("actions_name [%s], previous_actions_name [%s]",actions_name,previous_actions_name)
        
        all_p_keys = self.allPerspectiveKeys(epistemic_goals_dict,prefix)

        eq_dict = {}
        result_dict = {} 
        
        # there is no pervious perspectives path
        pre_init_perspective_key = str(['-'])
        if pre_init_perspective_key not in p_path.keys():
            # Then there is no perspective before the initial perspectives
            p_path[pre_init_perspective_key] = {}
        
        # the following session to generate pre_init perspectives
        for key in all_p_keys:
            
            if key not in p_path[pre_init_perspective_key].keys():
                # it mean this perspective has not been generated
                # it should be true twice in a search
                # 1. first time check goals
                # 2. first time check all preconditions
                if key == '':
                    # global perspectives
                    empty_update = {}
                    empty_state = {}
                    p_path[pre_init_perspective_key][key] = {}
                    for v_name in path[-1][0].keys():
                        empty_update[v_name] = False
                        empty_state[v_name] = EP_VALUE.HAVENT_SEEN
                    # initial perspective for "" is the current global state
                    p_path[pre_init_perspective_key][key]['states'] = [empty_state]
                    p_path[pre_init_perspective_key][key]['updates'] =[empty_update]
                else:
                    p_path[pre_init_perspective_key][key] = {}
                    # every one level will have two space in between
                    depth_indicator = key.count(' ')
                    # assert(depth_indicator %2 == 0, f"wrong key {key} when generating perspectives")
                    if depth_indicator >2:
                        parent_key_index = key[:key[:key.rfind(" ")].rfind(" ")].rfind(' ')
                        parent_key = key[:parent_key_index+1]
                        current_key = key[parent_key_index+1:]
                        
                        self.logger.debug("parent_key_index is [%s]",parent_key_index)
                        self.logger.debug("key is [%s]",key)
                        self.logger.debug("parent_key is [%s]",parent_key)
                        self.logger.debug("current_key is [%s]",current_key)
                    else:
                        parent_key = ''
                        current_key = key
                    # assert(parent_key not in p_path[''].keys(), f"wrong order handling perspectives, exists {p_path['None'].keys()}, but doing {parent_key}")
                    
                    eq_type_str = current_key.split(' ')[0]
                    agent_str = current_key.split(' ')[1][1:-1]
                    initial_p_path = {}
                    empty_state = {}
                    empty_updates = {}
                    for v_name in path[-1][0].keys():
                        empty_state[v_name]= EP_VALUE.HAVENT_SEEN
                        empty_updates[v_name]= False
                    # initial_p_path['states'] = [empty_state]
                    # initial_p_path['updates'] = [empty_updates]
                    # ignoring group beliefs for now
                    # if 'b' in eq_type_str:

                    #     state,updating = self._generateGroupPerspectives("",agent_str,p_path[''][parent_key]['states'][-1],initial_p_path)
                        
                    # elif 's' in eq_type_str:
                    #     state,updating = self._generateGroupObservations("",agent_str,p_path[''][parent_key]['states'][-1],initial_p_path)
                    # elif 'k' in eq_type_str:
                    #     state,updating = self._generateGroupObservations("",agent_str,p_path[''][parent_key]['states'][-1],initial_p_path)
                    p_path[pre_init_perspective_key][key]['states'] = [empty_state]
                    p_path[pre_init_perspective_key][key]['updates'] = [empty_updates]
                    
        self.logger.debug("p_path after initialization: [%s]",p_path)
        if actions_name not in p_path.keys():
            p_path[actions_name] = {}
            # all_p_keys list are sorted, the short perspectives are going to be generated first
        for key in all_p_keys:
            if key not in p_path[actions_name].keys(): 
                if key == '':
                    empty_update = {}
                    state = [path[-1][0]]
                    p_path[actions_name][key] = {}
                    for v_name in path[-1][0].keys():
                        # does not matter for the global state
                        empty_update[v_name] = False
                    # initial perspective for "" is the current global state
                    
                    self.logger.debug('actions_name [%s], key [%s], previous_actions_name [%s]',actions_name,key,previous_actions_name)
                    p_path[actions_name][key]['states'] = p_path[previous_actions_name][key]['states'] + state
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
                        
                        self.logger.debug("parent_key_index is [%s]",parent_key_index)
                        self.logger.debug("key is [%s]",key)
                        self.logger.debug("parent_key is [%s]",parent_key)
                        self.logger.debug("current_key is [%s]",current_key)
                    else:
                        parent_key = ''
                        current_key = key
                    # assert(parent_key not in p_path[actions_name].keys(), f"wrong order handling perspectives, exists {p_path[actions_name].keys()}, but doing {parent_key}")
                    
                    eq_type_str = current_key.split(' ')[0]
                    agent_str = current_key.split(' ')[1][1:-1]
                    # ignoring group beliefs for now
                    if 'b' in eq_type_str:
                        state,updating = self._generateGroupPerspectives("",agent_str,p_path[actions_name][parent_key]['states'][-1],p_path[previous_actions_name][key])
                    elif 's' in eq_type_str:
                        state,updating = self._generateGroupObservations("",agent_str,p_path[actions_name][parent_key]['states'][-1],p_path[previous_actions_name][key])
                    elif 'k' in eq_type_str:
                        state,updating = self._generateGroupObservations("",agent_str,p_path[actions_name][parent_key]['states'][-1],p_path[previous_actions_name][key])
                    p_path[actions_name][key]['states'] = p_path[previous_actions_name][key]['states'] +[state]
                    p_path[actions_name][key]['updates'] = p_path[previous_actions_name][key]['updates']+[updating]

        
        self.logger.debug("p_path is [%s]",p_path)
        
        for eq_str, value in epistemic_goals_dict.items():

            p_str = eq_str[:eq_str.rfind(' ')+1]
            eqv_str = eq_str[eq_str.rfind(' ')+1:][1:-1]
            v_name = eqv_str.split(',')[0][1:-1]
            v_value = eqv_str.split(',')[1][1:-1]
            perspective = p_path[actions_name][p_str]['states'][-1]
                
            if v_name in perspective.keys():
                if perspective[v_name] == EP_VALUE.HAVENT_SEEN:
                    
                    self.logger.debug("The eq_str [%s] is FALSE because of HAVENT_SEEN",eq_str)
                    result_dict[eq_str] = PDDL_TERNARY.FALSE

                elif perspective[v_name] == EP_VALUE.NOT_SEEING:
                    
                    self.logger.debug("The eq_str [%s] is UNKNOWN because of NOT_SEEING",eq_str)
                    result_dict[eq_str] = PDDL_TERNARY.UNKNOWN   
                     
                elif perspective[v_name] == v_value:
                    
                    self.logger.debug("The eq_str [%s] is TRUE because of value is same",eq_str)
                    result_dict[eq_str] = PDDL_TERNARY.TRUE
                else:
                    
                    self.logger.debug("The eq_str [%s] is FALSE because of value is different",eq_str)
                    result_dict[eq_str] = PDDL_TERNARY.FALSE
            else:
                
                self.logger.debug("The eq_str [%s] is UNKNOWN because of not in perspective",eq_str)
                result_dict[eq_str] = PDDL_TERNARY.UNKNOWN
                
        return result_dict


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

    
    
    def _generateOnePerspective(self,state_template,observation_list):
        new_state = {}
        for v_index,e in state_template.items():
            self.logger.debug('\t find history value for [%s],[%s]',v_index,e)
            ts_index = self._identifyLastSeenTimestamp(observation_list,v_index)
            self.logger.debug('\t last seen timestamp index: [%s]',ts_index)
            value = self._identifyMemorizedValue( observation_list, ts_index,v_index)
            self.logger.debug('\t {v_index}"s value is: [%s]',value)
            new_state.update({v_index:value})
        return new_state 
    
    def _identifyMemorizedValue(self,observation_list, ts_index,v_index):
        ts_index_temp = ts_index
        if ts_index_temp <0: return None
        
        while ts_index_temp >=0:

            # temp_observation = self.getObservations(external,state,agt_id,entities,variables)
            self.logger.debug('temp observation in identifyMemorization: [%s]',temp_observation)
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
            self.logger.debug("return eq string [%s]",eq_str)
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

        
        