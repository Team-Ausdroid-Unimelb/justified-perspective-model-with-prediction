# from model import Problem,E_TYPE,PDDL_TERNARY
import logging 
import math
from typing import Tuple
import numpy as np
import traceback
# import model
import re

from util import PDDL_TERNARY,convertBooltoPDDL_TERNARY
from util import EpistemicQuery,E_TYPE


AGENT_ID_PREFIX = "peeking_"



LOGGER_NAME = "NUMBER"
LOGGER_LEVEL = logging.INFO
from util import setup_logger
 
# declare common variables
common_constants = {

}

class ExternalFunction:
    logger = None
    
    def __init__(self, handlers):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=logging.INFO) 


    # extract variables from the query
    def extractVariables(self,eq):
        self.logger.debug(eq)
        # expected output would be a list of (var_name,value)
        if type(eq.q_content) == str:
            # default is a single pair of var_name and value
            if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",eq.q_content) == None:
                var_name = eq.q_content.split(",")[0][1:]
                value = eq.q_content.split(",")[1][:-1]
                var_name = var_name.replace("'","").replace('"','')
                value = value.replace("'","").replace('"','')
                return [(var_name,value)]
            else:
                # customized function here
                pass
        else:
            return self.extractVariables(eq.q_content)
            
    # customized evaluation function
    def evaluateS(self,world,statement):
        #default evaluation for variables
        if world == {}:
            return 2
        if not re.search("\([0-9a-z _\-\'\"]*,[0-9a-z _\'\"]*\)",statement) == None:
            var_name = statement.split(",")[0][1:]
            value = statement.split(",")[1][:-1]
            var_name = var_name.replace("'","").replace('"','')
            value = value.replace("'","").replace('"','')
            if var_name in world.keys():
                return 1
            else:
                return 0
        else:
            self.logger.warning("the evaluation of the seeing equation has not defined")
            return 0

    def agentsExists(self,path,g_group_index):
        state = path[-1][0]
        for agt_id in g_group_index:
            if not AGENT_ID_PREFIX+agt_id in state.keys():
                return False
        return True


    def checkVisibility(self,state,agt_index,var_index,entities,variables):
        
        self.logger.debug("checkVisibility(_,{},{},{})",state,agt_index,var_index)
        try:
            tgt_index = variables[var_index].v_parent
            # check if the agt_index can be found
            assert(entities[agt_index].e_type==E_TYPE.AGENT)
            
            # agents are able to see each other
            if entities[tgt_index].e_type==E_TYPE.AGENT:
                return convertBooltoPDDL_TERNARY(True)
            else:
                # this might be needed to change to UNKNOWN
                #extract necessary variables from state
                return  convertBooltoPDDL_TERNARY(state[f"peeking-{agt_index}"]=='t')
            
        #     # extract necessary common constants from given domain
        #     # logger.debug(f"necessary common constants from given domain")
        #     agt_angle = common_constants[f"angle-{agt_index}"]
            
        #     # agent is able to see anything in the same location
        #     if tgt_x == agt_x and tgt_y == agt_y:
        #         return model.PDDL_TERNARY.TRUE
            
        #     # generate two vector
        #     v1 = np.array((tgt_y - agt_y,tgt_x - agt_x))
        #     v1 = v1 / np.linalg.norm(v1)
        #     radians = math.radians(agt_dir)
        #     v2 = np.array((math.cos(radians),math.sin(radians)))
        #     # logger.debug(f'v1 {v1}, v2 {v2}')
        #     cos_ = v1.dot(v2)
        #     d_radians = math.acos(cos_)
        #     d_degrees = math.degrees(d_radians)
        #     # logger.debug(f'delta angle degree is {round(d_degrees,3)}')
            
        #     if d_degrees <= agt_angle/2.0 and d_degrees >= - agt_angle/2.0:
        #         inside = model.PDDL_TERNARY.TRUE
        #     else:
        #         inside =model.PDDL_TERNARY.FALSE
        #     # logger.debug(f'visibility is {inside}')
        #     return inside
        except KeyError:
            self.logger.warning(traceback.format_exc())
            self.logger.warning("variable not found when check visibility")
            # logger.error("error when checking visibility")
            return PDDL_TERNARY.UNKNOWN

    # customise action filters
    # to filter out the irrelevant actions
    def filterActionNames(self,problem,action_dict):
        return action_dict.keys()

    def checkKnowRule(self, state, agt_id, old_os):
        knows_rule_key = f'knows_rule-{agt_id}'
        if knows_rule_key in state and state[knows_rule_key].lower() == 'yes':
            return True
        elif self.learnRule(old_os,agt_id):
            return True
        else:
            return False
        
    
    def updateRule(self, observed_result, last_seen_index,new_p_index, old_os):
        a = 1
        rule_value = None
        if last_seen_index is not None and new_p_index is not None:
            diff = abs(last_seen_index - new_p_index)

            if last_seen_index < new_p_index:
                diff = diff
            else:
                diff = -diff
        else:
            diff = 0
        if observed_result is not None:
            rule_value = observed_result+a*diff
        return rule_value
    
    '''#y = ax+b
    def updateRule(self, observed_result, last_seen_index,new_p_index, old_os):
        keyword = self.checkV()
        observed_list = []

        for i in range(len(old_os)-1, -1, -1):
            if keyword in old_os[i]:
                value = old_os[i][keyword]
                if value is not None:
                    observed_list.append([i, value])
        ##################
        if observed_list:
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]

            coefficients = np.polyfit(x_values, y_values, 1)    #change 2 poly
            a = coefficients[0]
            b = coefficients[1]
            ############# 
            x = len(old_os)
            result = a * x + b
        else:
            result = observed_result
        return result
    '''
    '''#sin
    def updateRule(self, observed_result, last_seen_index,new_p_index, old_os):
        keyword = self.checkV()
        observed_list = []

        for i in range(len(old_os)-1, -1, -1):
            if keyword in old_os[i]:
                value = old_os[i][keyword]
                if value is not None:
                    observed_list.append([i, value])
        ##################
        if observed_list:
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]

                params, covariance = curve_fit(sin_function, x_values, y_values)

            a, b = params
            ############# sin
            x = len(old_os)
            result = a * np.sin(b * x)
        else:
            result = observed_result
        return result
    '''

    def sin_function(x, a, b):
        return a * np.sin(b * x)

    def update(self,value):
        return value + 1
    
    
    def checkV(self):
        v_index = 'num-c'
        return v_index

    def update_state(self, succ_state, path,domains):
        keyword = self.checkV()
        updated_state = succ_state
        if succ_state is not None and keyword in succ_state:
            updated_value = self.update(succ_state[keyword])
            updated_state[keyword] = updated_value
            if self.is_value_in_domain(updated_state,domains):
                return updated_state
        return succ_state

    def is_value_in_domain(self, state,domains):
        for var_name, value in state.items():
            clean_var_name = var_name.split('-')[0]
            if clean_var_name in domains:
                domain = domains[clean_var_name].d_values
                if value not in domain:
                    return False
        return True
    
    def learnRule(self, old_os,agt_id):
        keyword = self.checkV()
        num_c_count = 0

        for i in range(len(old_os)-1, -1, -1):
            if keyword in old_os[i]:
                
                num_c_count += 1
                if num_c_count >= 2:
                    return True
        else:
            return False

    
    def updatep(self, new_os, last_seen_index, new_p_index, new_p, new_o, agt_id, old_os):
        new_o = new_os[-1]
        keyword = self.checkV()
        memoryvalue = new_p[keyword]
        if self.checkKnowRule(new_o, agt_id, old_os): ##know rule 的index
            knows_rule_key = f'knows_rule-{agt_id}'
            new_p[knows_rule_key] = 'yes'

            updated_value = self.updateRule(memoryvalue, last_seen_index, new_p_index, old_os)
            new_p[keyword] = updated_value
        return new_p
        

    # if __name__ == "__main__":
        
    #     pass
        

    