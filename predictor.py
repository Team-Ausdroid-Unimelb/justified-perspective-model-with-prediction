import numpy as np
from util import RULE_TYPE, special_value
class Predictor:

    def __init__(self,external) -> None:
        self.external = external
        pass

    def getps(self, new_os,new_rs,p):
        os_dict = self.get_os_dict(new_os,p)
        ps_dict = {}
        
        for state in p:
            for v_name in state.keys():
                ps_dict[v_name] = [None] * len(p)
       
        for v_name, value in os_dict.items():
            #print(os_dict)
            for i in range(len(value)):
                if value[i] == special_value.UNSEEN or value[i] == special_value.HAVENT_SEEN:
                    #print("here",value)
                    ps_dict[v_name][i] = self.predict(i,new_rs[v_name],value)
                else:
                    ps_dict[v_name][i] = os_dict[v_name][i]

        #print(ps_dict)
        new_ps = []
        for i in range(len(p)):
            new_state = {}  
            for v_name, value in ps_dict.items():
                new_state[v_name] = value[i]  
            new_ps.append(new_state)
        #print("ps here",new_ps)
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
        # elif rule['rule_name'] == 'undetermined':
        #     result = self.get_predict_undetermined(i,rule,value)
        #     return result
        elif rule['rule_name'] == 'mod_1st':
            result = self.get_predict_mod1st(i,rule,value)
            return result
        else:
            result = self.external.domain_specific_predict(i,rule,value)
            if result == None:
                result = self.get_predict_static(i,rule,value)
            return result
        return None
    
    def get_predict_linear(self, i,rule,value):
        #print("hererer",i,rule,value)
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
            if value[j] is not None and value[j] != special_value.UNSEEN and value[j] != special_value.HAVENT_SEEN:
                result = value[j] 
                return value[j] 
            
        for j in range(i + 1, len(value)):
            if value[j] is not None and value[j] != special_value.UNSEEN and value[j] != special_value.HAVENT_SEEN:
                result = value[j] 
                return value[j]
        return result
    
    

    def get_predict_mod1st(self, i,rule,value):
        a = rule['coefficients'].get('a')
        directions = ['ne','e', 'se', 's', 'sw', 'w', 'nw','n']
        if a is None:
            result = self.get_predict_static(i,rule,value)
        else:
            first_value_index = directions.index(a)
            x = (first_value_index+i) % 8
            result = directions[x]
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
        #print("os",new_os)

        return os_dict

    def getrs(self, new_os,p, rules):
        # rule_dict = self.get_rule_dict(domains)
        os_dict = self.get_os_dict(new_os,p)
        rs = {}
        
        for v_name,valuelist in os_dict.items():
            #keyword = v_name.split('-')[0] #peeking
            v_rult_type = rules[v_name].rule_type
            if v_rult_type ==RULE_TYPE.POLY_2ND:
                rs[v_name] = self.get_coef_2poly(v_name,valuelist,rules)
            elif v_rult_type ==RULE_TYPE.LINEAR:
                rs[v_name] = self.get_coef_linear(v_name,valuelist,rules)
            elif v_rult_type ==RULE_TYPE.STATIC:
                rs[v_name] = self.get_static(v_name,valuelist,rules)
            elif v_rult_type ==RULE_TYPE.MOD_1ST:
                rs[v_name] = self.get_mod1st(v_name,valuelist,rules)
            else:
                rs[v_name] = self.get_static(v_name,valuelist,rules)

        return rs

    def get_coef_2poly(self, v_name,valuelist,rules):####[coeff]
        os_value_list = []
        for index, value in enumerate(valuelist):
            if value is not None:
                os_value_list.append([index, value])
        if len( os_value_list) >=3:
            x_values = [item[0] for item in os_value_list][-3:]
            y_values = [item[1] for item in os_value_list][-3:]
            coefficients = np.polyfit(x_values, y_values, 2)  ####solver np.linalg.solve
            a = coefficients[0]
            b = coefficients[1]
            c = coefficients[2]
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': a,'b': b,'c': c}}
        else:
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': None,'b': None,'c': None}}

    def get_coef_linear(self, v_name, valuelist,rules):
        coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
        known_coefficients={}
        for idx, coeff in enumerate(coefficients_known_list[::-1]):
            if coeff is not '':
                coeff = float(coeff)
                known_coefficients[idx] = coeff

        os_value_list = []
        for index, value in enumerate(valuelist):
            if value == special_value.UNSEEN or value == special_value.HAVENT_SEEN or value == None:
                pass
            else:
                os_value_list.append([index, value])
        x_values = [item[0] for item in os_value_list][-2:]
        y_values = [item[1] for item in os_value_list][-2:]

        if known_coefficients:
            A = np.vander(x_values, 2, increasing=True) #degree + 1
            B = np.array(y_values, dtype=float)
            for idx, coeff in known_coefficients.items():
                if coeff != None:
                    B -= coeff * A[:, idx]
                    A[:, idx] = 0
            
            unknown_indices = [i for i in range(2) if i not in known_coefficients or known_coefficients[i] is None]#degree + 1
            if unknown_indices:# Solve for the unknown coefficients
                A_reduced = A[:, unknown_indices]
                solutions, _, _, _ = np.linalg.lstsq(A_reduced, B, rcond=None)
                for idx, sol in zip(unknown_indices, solutions):
                    known_coefficients[idx] = sol
            
            # Ensure all coefficients are in the dictionary
            for i in range(2):#degree + 1
                if i not in known_coefficients:
                    known_coefficients[i] = 0.0

            # Return the coefficients in the correct order
            coefficients = [known_coefficients[i] for i in range(2)]#degree + 1
            return {'name':v_name,'rule_name': 'linear','coefficients': {'a': coefficients[1],'b':coefficients[0]}}   
        elif len(os_value_list) >=2:
            coefficients = np.polyfit(x_values, y_values, 1)  # Fit a quadratic polynomial, if linear,a will be 0
            a = coefficients[0]
            b = coefficients[1]
            
            return {'name':v_name,'rule_name': 'linear','coefficients': {'a': a,'b': b}}
        else:
            return {'name':v_name, 'rule_name': 'linear','coefficients': {'a': None,'b': None}}

    def get_static(self, v_name, valuelist,rules):
        return {'name':v_name,'rule_name': 'static','coefficients': {'a': None}}
    

    def get_mod1st(self, v_name, valuelist,rules):##
        directions = ['ne','e', 'se', 's', 'sw', 'w', 'nw','n']
        for i, value in enumerate(valuelist):
            
            if value is not None and value != special_value.UNSEEN and value != special_value.HAVENT_SEEN:
                valuelist_index = i
                value_index = directions.index(value)
                first_element_index = (value_index- valuelist_index) % len(directions)
                first_elenmet = directions[first_element_index]
                rule = {'name': v_name, 'rule_name': 'mod_1st', 'coefficients': {'a': first_elenmet}}
                break
        else:
            rule =  {'name': v_name, 'rule_name': 'mod_1st', 'coefficients': {'a': None}}
        
        return rule
    
    # def get_rule_dict(self,domains):
    #     rule_dict = {}
    #     for v_name in domains:
    #         variable_dict  = domains[v_name]
    #         dict_list = str(variable_dict).split(';')
    #         v_rule_type = dict_list[-1].split(':')
    #         type_name = str(v_rule_type[1])[:-2].strip()
    #         rule_dict[v_name] = type_name
    #     return rule_dict       