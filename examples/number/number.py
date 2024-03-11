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

    def checkKnowRule(self, agt_id, os):
        knows_rule_key = f'knows_rule-{agt_id}'
        if os and knows_rule_key in os[-1] and os[-1][knows_rule_key].lower() == 'yes':
            return True
        else:
            return False
        
    
    def updateRuleByLearn(self, new_os, new_p_index,rule_dict,v_name,memoryvalue):
        keyword = v_name #peeking-a
        observed_list = []
        v_name = v_name.split('-')[0] #peeking
        v_rult_type = str(rule_dict[v_name])
        #print(v_rult_type)
        #print(v_name,v_rult_type)

        for i in range(len(new_os)-1, -1, -1):
            if keyword in new_os[i]:
                value = new_os[i][keyword]
                if value is not None:
                    observed_list.append([i, value])

        #y = ax^2+bx+c;observed_list and len(observed_list) > 2:  # Check if there are at least 3 points for quadratic fit 
        if observed_list and v_rult_type =='2nd_poly':
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]
            #print(x_values,y_values)

            coefficients = np.polyfit(x_values, y_values, 2)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            c = coefficients[2]
            #print(a,b,c) 精度问题

            x = new_p_index
            result = round(a * x**2 + b * x + c)
            #if a < 0.0001:
                #return {'rule_name': 'linear','coefficients': {'a': a,'b': b}},result
            #else:
                
            return {'name':keyword,'rule_name': '2nd_poly','coefficients': {'a': a,'b': b,'c': c}},result
        #y = ax+b;observed_list and len(observed_list) > 1: #can update 
        elif observed_list and v_rult_type =='linear':
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]
        
            coefficients = np.polyfit(x_values, y_values, 1)    
            a = coefficients[0]
            b = coefficients[1]

            x = new_p_index
            result = round(a * x + b)
            return {'name':keyword,'rule_name': 'linear','coefficients': {'a': round(a),'b': round(b)}},result
        
        elif observed_list and v_rult_type =='static':
            result = observed_list[-1] if observed_list else None
            return {'name':keyword,'rule_name': 'static','coefficients': {'a': 1}},result
        
        elif observed_list and v_rult_type =='undefined':
            result = "?"
            return {'name':keyword,'rule_name': 'undefined','coefficients': {}},result
        

        else: #can not update
            result = memoryvalue # new_os[-1][keyword] if new_os[-1].get(keyword)  else None
            #print(v_rult_type)
            return {'name':keyword,'rule_name': v_rult_type,'coefficients': {}},result

    
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
    

    def sin_function(x, a, b):
        return a * np.sin(b * x)
    '''
    def updatelinear(self,x):
        return x + 2
    
    def update2Poly(self,x):
        return x**2 + 1
    
    
    def checkV(self):
        v_index = 'num-c'
        return v_index

    def update_state(self, succ_state, path, problem):
        domains = problem.domains
        rule_dict = self.get_rule_dict(domains)
        #keyword = self.checkV()
        x = len(path)
        updated_state = succ_state
        for keyword in succ_state:
            v_name = keyword.split('-')[0]
            v_rult_type = str(rule_dict[v_name])
            if succ_state is not None and keyword in succ_state and v_rult_type =='linear':
                updated_value = self.updatelinear(x)    ##########change model here
                updated_state[keyword] = updated_value
                #print(x,updated_value)
                
            if succ_state is not None and keyword in succ_state and v_rult_type =='2nd_poly':
                updated_value = self.update2Poly(x)    ##########change model here
                updated_state[keyword] = updated_value
                #print(x,updated_value)

        if self.is_value_in_domain(updated_state,domains):
            return updated_state
        else:
            return None
        #return succ_state

    def is_value_in_domain(self, state,domains):
        for var_name, value in state.items():
            clean_var_name = var_name.split('-')[0]
            if clean_var_name in domains:
                domain = domains[clean_var_name].d_values
                if value not in domain:
                    return False
        return True
    
    def learnRule(self, os,agt_id): #how many times peeking to learn
        keyword = self.checkV()
        num_c_count = 0
        for i in range(len(os)-1, -1, -1):
            if keyword in os[i]:
                num_c_count += 1
                if num_c_count >= 2:
                    return True
        else:
            return False

    def get_rule_dict(self,domains):
        rule_dict = {}
        for v_name in domains:
            variable_dict  = domains[v_name]
            dict_list = str(variable_dict).split(';')
            v_rule_type = dict_list[-1].split(':')
            type_name = str(v_rule_type[1])[:-2].strip()
            rule_dict[v_name] = type_name
        return rule_dict


    def updatep(self, new_os, new_p_index, new_p, agt_id,prefix,domains, rule_dict):
        #keyword = self.checkV()
        #memoryvalue = new_p[keyword] #initailize
        #unit_count = self.getUnitCount(prefix)
        rule_dict = self.get_rule_dict(domains)
        '''
        for v_name in domains:
            variable_dict  = domains[v_name]
            dict_list = str(variable_dict).split(';')
            v_rule_type = dict_list[-1].split(':')
            type_name = str(v_rule_type[1])[:-2]
            rule_dict[v_name] = type_name
            #print("hereere",type_name )

        
        for i in range(len(new_os) - 1, -1, -1): #find not none os
            if keyword in new_os[i] and isinstance(new_os[i][keyword], (int, float)):
                memoryvalue = new_os[i][keyword]
                break
        '''
        ####delete
        """
        if self.checkKnowRule(agt_id, new_os)and new_rs_i is not None  and memoryvalue is not None: #in initialization, rule must correct
            #knows_rule_key = f'knows_rule-{agt_id}'
            #new_p[knows_rule_key] = 'yes'
            x = new_p_index
            #print(domains)
            variable_type = domains.get("num", {}).get("variable_type", None)
            if variable_type == 'linear':
                updated_value = self.updateRuleByKnowLinear(memoryvalue,new_os, x)
            elif variable_type == '2nd_poly':
                updated_value = self.updateRuleByKnow2ndpoly(memoryvalue,new_os, x)
            elif variable_type == 'static':
                updated_value = memoryvalue
            else:
                updated_value = self.updateRuleByKnowLinear(memoryvalue,new_os, x)  #default linear
            new_p[keyword] = updated_value
        #########
        """
        if self.learnRule(new_os,agt_id): #see twice, rule can be wrong
            #knows_rule_key = f'knows_rule-{agt_id}'
            #new_p[knows_rule_key] = 'yes'
            #print("learnnnnnnn")
            temp_rule = {}
            for v_name in new_p: 
                memoryvalue = new_p[v_name]
                update_rule, updated_result = self.updateRuleByLearn(new_os, new_p_index,rule_dict,v_name,memoryvalue)
                temp_rule[v_name] = update_rule
                new_p[v_name] = updated_result
            return new_p, temp_rule
        else:
            for v_name in new_p: 
                memoryvalue = new_p[v_name]
                new_p[v_name] = memoryvalue
            return new_p, rule_dict
        

    
    def getUnitCount(self, prefix):
        pattern = re.compile(r"b \[(.*)\]")
        match = pattern.match(prefix)
        if match:
            units = match.group(1).split()
            return len(units)
        else:
            return 0  

    def updateRuleByKnowLinear(self, memoryvalue, new_os, x):
        ruleValue = self.updatelinear(x)
        '''
        keyword = self.checkV()
        observed_index = None
        observed_result = memoryvalue
        for i in range(len(new_os)-1, -1, -1):        
            if keyword in new_os[i] and new_os[i][keyword] == memoryvalue:
                observed_index = i
                break
        if memoryvalue is not None and new_p_index is not None and observed_index is not None:
            observed_result = memoryvalue+(new_p_index-observed_index)
        '''
        return ruleValue
    
    def updateRuleByKnow2ndpoly(self, memoryvalue, new_os, x):
        ruleValue = self.update2Poly(x)
        return ruleValue

    

    # if __name__ == "__main__":
        
    #     pass
        

    