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
        
    '''
    def updateRuleByLearn(self, new_os, new_p_index,rule_dict,v_name):
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
        if observed_list and len(observed_list) >=3 and v_rult_type =='2nd_poly':
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]
            #print(x_values,y_values)

            coefficients = np.polyfit(x_values, y_values, 2)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            c = coefficients[2]
            #print(a,b,c) miaccuracy problem here

            x = new_p_index
            result = round(a * x**2 + b * x + c)
            #if a < 0.0001:
                #return {'rule_name': 'linear','coefficients': {'a': a,'b': b}},result
            #else:
                
            return {'name':keyword,'rule_name': '2nd_poly','coefficients': {'a': a,'b': b,'c': c}},result
        #y = ax+b;observed_list and len(observed_list) > 1: #can update 
        elif observed_list and len(observed_list) >=2 and v_rult_type =='linear':
            x_values = [item[0] for item in observed_list]
            y_values = [item[1] for item in observed_list]
        
            coefficients = np.polyfit(x_values, y_values, 1)    
            a = coefficients[0]
            b = coefficients[1]

            x = new_p_index
            result = round(a * x + b)
            return {'name':keyword,'rule_name': 'linear','coefficients': {'a': round(a),'b': round(b)}},result
        
        elif observed_list and len(observed_list) >=1 and v_rult_type =='static':
            result = observed_list[0][1] if observed_list else None
            return {'name':keyword,'rule_name': 'static','coefficients': {'a': 1}},result
        
        elif observed_list and v_rult_type =='undetermined':
            result = "?"
            return {'name':keyword,'rule_name': 'undetermined','coefficients': {}},result
        else: #can not update
            for o in reversed(new_os):
                if keyword in o:
                    if o[keyword] is not None:
                        memoryvalue = o[keyword]
                        break 
                    else:
                        memoryvalue = None
                else:
                    memoryvalue = None
            result = memoryvalue 
            return {'name':keyword,'rule_name': v_rult_type,'coefficients': {}},result
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
    '''
    def learnRule(self, os): #how many times peeking to learn
        keyword = self.checkV()
        num_c_count = 0
        for i in range(len(os)-1, -1, -1):
            if keyword in os[i]:
                num_c_count += 1
                if num_c_count >= 2:
                    return True
        else:
            return False
    #inside  updateRuleByLearn functions
    '''
    def get_rule_dict(self,domains):
        rule_dict = {}
        for v_name in domains:
            variable_dict  = domains[v_name]
            dict_list = str(variable_dict).split(';')
            v_rule_type = dict_list[-1].split(':')
            type_name = str(v_rule_type[1])[:-2].strip()
            rule_dict[v_name] = type_name
        return rule_dict

    '''
    def getp(self, new_os,i,temp_p, domains, rule_dict):
        #keyword = self.checkV()
        #memoryvalue = new_p[keyword] #initailize
        #unit_count = self.getUnitCount(prefix)
        rule_dict = self.get_rule_dict(domains)

        
        for v_name in domains:
            variable_dict  = domains[v_name]
            dict_list = str(variable_dict).split(';')
            v_rule_type = dict_list[-1].split(':')
            type_name = str(v_rule_type[1])[:-2]
            rule_dict[v_name] = type_name
        
        for i in range(len(new_os) - 1, -1, -1): #find not none os
            if keyword in new_os[i] and isinstance(new_os[i][keyword], (int, float)):
                memoryvalue = new_os[i][keyword]
                break
        
        new_p = {}
        temp_rule = {}
        
        for v_name, value in temp_p.items():
            #update_rule, result = self.updateRuleByLearn(new_os,i,rule_dict,v_name)
            
            if v_name.startswith("num"):
                update_rule, result = self.updateRuleByLearn(new_os,i,rule_dict,v_name)
            else:
                update_rule = rule_dict
                result = new_os[i].get(v_name)
             
            temp_rule[v_name] = update_rule
            new_p[v_name] = result

        return new_p, temp_rule
    '''
    def getps(self, new_os,new_rs,p):
        os_dict = self.get_os_dict(new_os,p)
        ps_dict = {}
        
        for state in p:
            for v_name in state.keys():
                ps_dict[v_name] = [None] * len(p)

        for v_name, value in os_dict.items():
            for i in range(len(value)):
                ps_dict[v_name][i] = os_dict[v_name][i]
                if value[i] is None:
                    ps_dict[v_name][i] = self.predict(i,new_rs[v_name],value)

        print("os",os_dict)
        print("ps",ps_dict)
        new_ps = []
        for i in range(len(p)):
            new_state = {}  
            for v_name, value in ps_dict.items():
                new_state[v_name] = value[i]  
            new_ps.append(new_state)
        
        return new_ps

    def predict(self, i,rule,value):
        if rule['rule_name'] == 'linear':
           result = self.get_predict_linear(i,rule,value)
           return result
        elif rule['rule_name'] == '2nd_poly':
            result = self.get_predict_2poly(i,rule,value)
            return result
        elif rule['rule_name'] == 'static':
            result = self.get_predict_static(i,rule,value)
            return result
        elif rule['rule_name'] == 'undetermined':
            result = self.get_predict_undetermined(i,rule,value)
            return result
        return None
    
    def get_predict_linear(self, i,rule,value):
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        if a is None or b is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * i + b)
        return result
    
    def get_predict_2poly(self, i,rule,value):
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        c = rule['coefficients'].get('c')
        if a is None or b is None or c is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * i**2 + b * i + c)
        return result
    
    def get_predict_static(self, i,rule,value):
        result = None
        for j in range(i - 1, -1, -1):
            if value[j] is not None:
                result = value[j] 
                return value[j] 
            
        for j in range(i + 1, len(value)):
            if value[j] is not None:
                result = value[j] 
                return value[j]
        return result
    
    def get_predict_undetermined(self, i,rule,value):
        result = "?"
        return result
    
    def get_os_dict(self, new_os,p):
        os_dict = {}
        for state in p:
            for v_name in state.keys():
                os_dict[v_name] = []

        for state in new_os:
            for v_name in os_dict.keys():
                if v_name in state:
                    os_dict[v_name].append(state[v_name])
                else:
                    os_dict[v_name].append(None)
        return os_dict

    def getrs(self, new_os,p, domains):

        rule_dict = self.get_rule_dict(domains)
        os_dict = self.get_os_dict(new_os,p)
        rs = {}

        for v_name,valuelist in os_dict.items():
            keyword = v_name.split('-')[0] #peeking
            v_rult_type = str(rule_dict[keyword])
            if v_rult_type =='2nd_poly':
                rs[v_name] = self.get_coef_2poly(v_name,valuelist)
            elif v_rult_type =='linear':
                rs[v_name] = self.get_coef_linear(v_name,valuelist)
            elif v_rult_type =='static':
                rs[v_name] = self.get_static(v_name,valuelist)
            elif v_rult_type =='undetermined':
                rs[v_name] = self.get_undetermined(v_name,valuelist)
            else:
                rs[v_name] = self.get_static(v_name,valuelist)
        return rs

    def get_coef_2poly(self, v_name,valuelist):
        os_value_list = []
        for index, value in enumerate(valuelist):
            if value is not None:
                os_value_list.append([index, value])
        if len( os_value_list) >=3:
            x_values = [item[0] for item in os_value_list]
            y_values = [item[1] for item in os_value_list]
            coefficients = np.polyfit(x_values, y_values, 2)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            c = coefficients[2]
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': a,'b': b,'c': c}}
        else:
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': None,'b': None,'c': None}}

    def get_coef_linear(self, v_name, valuelist):
        os_value_list = []
        for index, value in enumerate(valuelist):
            if value is not None:
                os_value_list.append([index, value])
        if len( os_value_list) >=2:
            x_values = [item[0] for item in os_value_list]
            y_values = [item[1] for item in os_value_list]
            coefficients = np.polyfit(x_values, y_values, 1)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            return {'name':v_name,'rule_name': 'linear','coefficients': {'a': a,'b': b}}
        else:
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': None,'b': None}}

    def get_static(self, v_name, valuelist):
        return {'name':v_name,'rule_name': 'static','coefficients': {'a': None}}
    
    def get_undetermined(self, v_name, valuelist):
        return {'name':v_name,'rule_name': 'undetermined','coefficients': {'a': None}} 
    
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
        

    