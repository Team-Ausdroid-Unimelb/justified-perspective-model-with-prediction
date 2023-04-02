import enum
# import pddl_model
import typing
import re
import logging
import copy
from util import PDDL_TERNARY


LOGGER_NAME = "epistemic_model"
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG
from util import setup_logger


class Q_TYPE(enum.Enum):
    MUTUAL = 0
    DISTRIBUTION = -1
    COMMON = 1
    
class EQ_TYPE(enum.Enum):
    KNOWLEDGE = 1
    SEEING = 0
    BELIEF = 2
    
class EpistemicQuery:
    q_type = None
    q_content = None
    eq_type = None
    header_str = ""
    agents_str = ""
    q_group = []
    mapping = {
        'k': (Q_TYPE.MUTUAL, EQ_TYPE.KNOWLEDGE),
        'ek': (Q_TYPE.MUTUAL, EQ_TYPE.KNOWLEDGE),
        'dk': (Q_TYPE.DISTRIBUTION ,EQ_TYPE.KNOWLEDGE),
        'ck': (Q_TYPE.COMMON, EQ_TYPE.KNOWLEDGE),
        's': (Q_TYPE.MUTUAL, EQ_TYPE.SEEING),
        'es': (Q_TYPE.MUTUAL, EQ_TYPE.SEEING),
        'ds': (Q_TYPE.DISTRIBUTION, EQ_TYPE.SEEING),
        'cs': (Q_TYPE.COMMON, EQ_TYPE.SEEING),
        'b': (Q_TYPE.MUTUAL, EQ_TYPE.BELIEF),
        'eb': (Q_TYPE.MUTUAL, EQ_TYPE.BELIEF),
        'db': (Q_TYPE.DISTRIBUTION, EQ_TYPE.BELIEF),
        'cb': (Q_TYPE.COMMON, EQ_TYPE.BELIEF),
    }
    
    def __init__(self,header_str,agents_str,content):
        
        self.q_type,self.eq_type = self.mapping[header_str]
        self.header_str = header_str
        self.agents_str = agents_str
        self.q_group = agents_str[1:-1].split(",")
        self.q_content = content
        
    def show(self):
        # for debug purpose
        output = f"<epistemic: q_type: {self.q_type}; eq_type: {self.eq_type}; q_group: {self.q_group}; q_content: {self.q_content} >"
        return output
        
    def __str__(self): 
        # show only in the print(object)
        output = f"{self.header_str} {self.agents_str} {self.q_content}"
        return output

    def __repr__(self): 
        # show when in a dictionary
        output = f"{self.header_str} {self.agents_str} {self.q_content}"
        return output


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


    def epistemicGoalsHandler(self,epistemic_goals_list, prefix, path):
        perspectives_dict = {prefix:path[-1][0]}
        eq_dict = {}
        result_dict = {}
        
        for epistemic_goal_str,value in epistemic_goals_list:
            temp_eq = self.partially_converting_to_eq(epistemic_goal_str)
            if type(temp_eq) == str:
                # this is the end of eq
                # no need to generate perspectives
                # just need to evaluate the result and return value
                # key = f"{prefix} {temp_eq}"
                self.logger.debug(f"query key: {temp_eq}")
                result = self._evaluateContent(path,temp_eq)
                
                result_dict.update({temp_eq:result})
                
            else:
                # it means the query is not to the last level yet
                
                agents_str = temp_eq.agents_str
                content = temp_eq.q_content
                key = f"{temp_eq.header_str} {agents_str}"
                
                
                if key in eq_dict.keys():
                    eq_dict[key]['content'].append((content,value))
                else:
                    eq_dict[key] = {'q_type':temp_eq.q_type,'eq_type':temp_eq.eq_type,'q_group':temp_eq.q_group,'content':[(content,value)]}
        
        # solving eq by perspectives
        for key,item in eq_dict.items():
            # generate perspectives
            new_path = []
            eq_type = item['eq_type']
            if eq_type == EQ_TYPE.BELIEF:
                new_path = self._generateGroupPerspectives(path,item['q_type'],item['q_group'])
            elif eq_type == EQ_TYPE.SEEING or eq_type == EQ_TYPE.KNOWLEDGE:
                new_path = self._generateGroupObservations(path,item['q_type'],item['q_group'])
            # elif eq_type == EQ_TYPE.KNOWLEDGE:
            #     new_path = self._generateGroupObservations(self,path,item['q_type'],item['q_group'])
            else:
                assert("wrong eq_type of the epistemic query")
            perspectives_dict.update({key:new_path[-1][0]})
            local_perspectives, local_result_dict = self.epistemicGoalsHandler(item['content'],key,new_path)
            perspectives_dict.update(local_perspectives)
            for result_key,result_value in local_result_dict.items():
                result_key = key+ " "+ result_key
                new_result_value = result_value
                if eq_type == EQ_TYPE.SEEING:
                    if not self.external.agentsExists(new_path,item['q_group']):
                        new_result_value = PDDL_TERNARY.UNKNOWN
                    elif result_value == PDDL_TERNARY.UNKNOWN:
                        new_result_value = PDDL_TERNARY.FALSE
                    else:
                        new_result_value = PDDL_TERNARY.TRUE
                result_dict.update({result_key:new_result_value})
        return perspectives_dict,result_dict

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
    
    def _generateGroupPerspectives(self,path,q_type,q_group):
        
        # initial perspectives 
        new_path = self._generateOnePerspectives(path,q_group[0])
        if len(q_group) == 1:
            return new_path
        else:
            if q_type == Q_TYPE.MUTUAL:
                pass
            elif q_type == Q_TYPE.DISTRIBUTION:
                pass
            elif q_type == Q_TYPE.COMMON:
                pass
            else:
                assert("wrong Q type")

    def _generateGroupObservations(self,path,q_type,q_group):
        # initial perspectives 
        new_path = []
        for i in range(len(path)):
            new_path.append((self._getOneObservation(path[i][0],q_group[0]),path[i][1]))
        if len(q_group) == 1:
            return new_path
        else:
            if q_type == Q_TYPE.MUTUAL:
                pass
            elif q_type == Q_TYPE.DISTRIBUTION:
                pass
            elif q_type == Q_TYPE.COMMON:
                pass
            else:
                assert("wrong Q type")


    
    def _generateOnePerspectives(self,path,agt_id):
        state_template = path[0][0]
        new_path = []
        
        observation_list = []
        
        for i in range(len(path)):
            observation_list.append(self._getOneObservation(path[i][0],agt_id))
        
        for i in range(len(path)):
            new_state = self._generateOnePerspective(state_template,observation_list[:i+1])
            new_path.append((new_state,path[i][1]))
        return new_path
    
    
    def _generateOnePerspective(self,state_template,observation_list):
        new_state = {}
        for v_index,e in state_template.items():
            self.logger.debug(f'\t find history value for {v_index},{e}')
            ts_index = self._identifyLastSeenTimestamp(observation_list,v_index)
            self.logger.debug(f'\t timestamp index: {ts_index}')
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
        for var_index,value in state.items():
            if self.external.checkVisibility(state,agt_id,var_index,self.entities,self.variables)==PDDL_TERNARY.TRUE:
                new_state.update({var_index: value})
        return new_state
    
    
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

        
        