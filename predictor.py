import numpy as np
from util import RULE_TYPE, special_value
from scipy.optimize import curve_fit
from collections import Counter
import math

class Predictor:

    def __init__(self,external) -> None:
        self.external = external
        self.segment_count = 0
        pass

    def getps(self, new_os,new_rs,p):
        os_dict = self.get_os_dict(new_os,p)
        ps_dict = {}
        #print("os",os_dict)
        #print('os',os_dict['shared_value as'])
        for state in p:
            for v_name in state.keys():
                ps_dict[v_name] = [special_value.HAVENT_SEEN] * len(p)
       
        for v_name, value in os_dict.items():
            #print(os_dict)
            for i in range(len(value)):
                #ps_dict[v_name][i] = self.predict(i,new_rs[v_name],value)
                if value[i] == special_value.UNSEEN or value[i] == special_value.HAVENT_SEEN or value[i] == None:
                    #print("here",value)
                    ps_dict[v_name][i] = self.predict(i,new_rs[v_name],value)
                else:
                    ps_dict[v_name][i] = os_dict[v_name][i]

        #print("ps",ps_dict)
        # print('ps',ps_dict['shared_value as'])
        new_ps = []
        for i in range(len(p)):
            new_state = {}  
            for v_name, value in ps_dict.items():
                new_state[v_name] = value[i]  
            new_ps.append(new_state)
        # print("ps here",new_ps)
        return new_ps

    # def predict(self, i,rule,value):
    #     if rule['rule_name'] == '1st_poly':
    #        result = self.get_predict_1st_poly(i,rule,value)
    #        return result
    #     elif rule['rule_name'] == '2nd_poly':
    #         result = self.get_predict_2nd_poly(i,rule,value)
    #         return result
    #     elif rule['rule_name'] == 'static':
    #         result = self.get_predict_static(i,rule,value)
    #         return result
    #     elif rule['rule_name'] == 'mod_1st':
    #         result = self.get_predict_mod_1st(i,rule,value)
    #         return result
    #     elif rule['rule_name'] == 'power':
    #         result = self.get_predict_power(i, rule, value)
    #         return result
    #     elif rule['rule_name'] == 'sin': 
    #         result = self.get_predict_sin(i, rule, value)
    #         return result
    #     else:
    #         result = self.external.domain_specific_predict(i,rule,value)
    #         if result == None:
    #             result = self.get_predict_static(i,rule,value)
    #         return result
    #     return None
    def predict(self, i, rule, value):
        method_name = f"get_predict_{rule['rule_name']}"
        
        # from external
        if hasattr(self.external, method_name):
            external_method = getattr(self.external, method_name)
            self.segment_count +=1
            return external_method(i, rule, value)
        
        # from self
        if hasattr(self, method_name):
            self_method = getattr(self, method_name)
            return self_method(i, rule, value)
        
        # If there is no corresponding method for both external and internal, use fallback logic
        result = self.external.domain_specific_predict(i, rule, value)
        if result is None:
            result = self.get_predict_static(i, rule, value)
        return result

    
    def get_predict_1st_poly(self, i, rule, value):
        coefficients = rule['coefficients']
        # self.segment_count += len(coefficients)
        #print(coefficients,len(coefficients))####
        x_values = list(coefficients.keys())
        a, b = None, None
        if len(coefficients.items()) == 0:  # If x_values is empty
            return self.get_predict_static(i, rule, value)
        if i <= x_values[0][0]:  # If i is less than the first pair's x value
            a = coefficients.get(x_values[0], {}).get('a')
            b = coefficients.get(x_values[0], {}).get('b')
        elif i >= x_values[-1][1]:  # If i is greater than the last pair's x value
            a = coefficients.get(x_values[-1], {}).get('a')
            b = coefficients.get(x_values[-1], {}).get('b')
        else:  
            for j in range(len(x_values) - 1):
                if x_values[j][0] <= i <= x_values[j][1]:
                    a = coefficients.get(x_values[j], {}).get('a')
                    b = coefficients.get(x_values[j], {}).get('b')
                    break

        if a is None or b is None:
            result = self.get_predict_static(i, rule, value)
        else:
            result = round(a * i + b)
        
        return result

    
    def get_predict_2nd_poly(self, i,rule,value):
        
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        c = rule['coefficients'].get('c')

        if a is None or b is None or c is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * i**2 + b * i + c)
        return result
    
    def get_predict_static(self, i,rule,value):
        result = special_value.HAVENT_SEEN
        for j in range(i - 1, -1, -1):
            if value[j] is not None and value[j] != special_value.UNSEEN and value[j] != special_value.HAVENT_SEEN:
                result = value[j] 
                return value[j] 
            
        for j in range(i + 1, len(value)):
            if value[j] is not None and value[j] != special_value.UNSEEN and value[j] != special_value.HAVENT_SEEN:
                result = value[j] 
                return value[j]
        return result
    
    

    def get_predict_mod_1st(self, i,rule,value):
        a = rule['coefficients'].get('a')
        directions = ['ne','e', 'se', 's', 'sw', 'w', 'nw','n']
        if a is None:
            result = self.get_predict_static(i,rule,value)
        else:
            first_value_index = directions.index(a)
            x = (first_value_index+i) % 8
            result = directions[x]
        return result
    

    def get_predict_power(self, i, rule, value):
        a = rule['coefficients'].get('a')
        if a[0] is None:
            result = self.get_predict_static(i, rule, value)
        elif len(a) == 2:
            if i % 2 == 0:
                a = int(a[0])
                result = round(a ** (1/i))
            else:
                result = special_value.HAVENT_SEEN
        else:
            a = int(a[0])
            result = round(a ** i)
        return result
    

    def get_predict_sin(self, i, rule, value):
        a = rule['coefficients'].get('a')
        b = rule['coefficients'].get('b')
        c = rule['coefficients'].get('c')


        if a is None or b is None or c is None:
            result = self.get_predict_static(i,rule,value)
        else:
            result = round(a * np.sin(b*0.5*np.pi * i + c))

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

    # def getrs(self, new_os,p, rules):
    #     # rule_dict = self.get_rule_dict(domains)
    #     os_dict = self.get_os_dict(new_os,p)
    #     rs = {}
        
    #     for v_name,valuelist in os_dict.items():
    #         #keyword = v_name.split('-')[0] #peeking
    #         v_rult_type = rules[v_name].rule_type
    #         if v_rult_type ==RULE_TYPE.POLY_2ND:
    #             rs[v_name] = self.get_coef_poly_2nd(v_name,valuelist,rules)
    #         elif v_rult_type ==RULE_TYPE.POLY_1ST:
    #             rs[v_name] = self.get_coef_poly_1st(v_name,valuelist,rules)
    #         elif v_rult_type ==RULE_TYPE.STATIC:
    #             rs[v_name] = self.get_coef_static(v_name,valuelist,rules)
    #         elif v_rult_type ==RULE_TYPE.MOD_1ST:
    #             rs[v_name] = self.get_coef_mod_1st(v_name,valuelist,rules)
    #         elif v_rult_type == RULE_TYPE.POWER:
    #             rs[v_name] = self.get_coef_power(v_name, valuelist, rules)
    #         elif v_rult_type == RULE_TYPE.SIN:  ####
    #             rs[v_name] = self.get_coef_sin(v_name, valuelist, rules)
    #         else:
    #             rs[v_name] = self.get_coef_static(v_name,valuelist,rules)

    #     return rs
    def getrs(self, new_os, p, rules):
        os_dict = self.get_os_dict(new_os, p)
        rs = {}

        for v_name, valuelist in os_dict.items():
            v_rule_type = rules[v_name].rule_type
            method_name = f"get_coef_{str(v_rule_type).split('.')[-1].lower()}"

            # from external
            if hasattr(self.external, method_name):
                external_method = getattr(self.external, method_name)
                try:
                    rs[v_name] = external_method(v_name, valuelist, rules)
                    continue  
                except Exception as e:
                    print(f"External method {method_name} failed with error: {e}. Falling back to internal method.")
            
            # from self
            if hasattr(self, method_name):
                self_method = getattr(self, method_name)
                rs[v_name] = self_method(v_name, valuelist, rules)
            else:
                print(f"Method {method_name} not found. Falling back to get_coef_static.")
                rs[v_name] = self.get_coef_static(v_name, valuelist, rules)

        return rs

    def get_coef_poly_2nd(self, v_name,valuelist,rules):####[coeff]
        self.segment_count += 1
        coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
        known_coefficients={}
        for idx, coeff in enumerate(coefficients_known_list[::-1]):
            if coeff != '':
                coeff = float(coeff)
                known_coefficients[idx] = coeff
            else:
                known_coefficients[idx] = None

        os_value_list = []
        for index, value in enumerate(valuelist):
            if value == special_value.UNSEEN or value == special_value.HAVENT_SEEN or value == None:
                pass
            else:
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
            return {'name':v_name, 'rule_name': '2nd_poly','coefficients': {'a': None,'b': None,'c': None}} #####

    def get_coef_poly_1st(self, v_name, valuelist,rules):
        coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
        known_coefficients={}

        for idx, coeff in enumerate(coefficients_known_list[::-1]):
            if coeff != '':
                coeff = float(coeff)
                known_coefficients[idx] = coeff
            else:
                known_coefficients[idx] = None

        os_value_list = []
        for index, value in enumerate(valuelist):
            if value == special_value.UNSEEN or value == special_value.HAVENT_SEEN or value == None:
                pass
            else:
                os_value_list.append([index, value])
        # x_values = [item[0] for item in os_value_list][-2:]
        # y_values = [item[1] for item in os_value_list][-2:]

        coefficients_dict = {} 
        for i in range(len(os_value_list) - 1):
            x_values = [os_value_list[i][0], os_value_list[i + 1][0]]
            y_values = [os_value_list[i][1], os_value_list[i + 1][1]]

            if len(rules[v_name].rule_known_coef)>3 and len(os_value_list) >=1:
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
                        known_coefficients[i] = None #0.0

                # Return the coefficients in the correct order
                coefficients = [known_coefficients[i] for i in range(2)]#degree + 1

                coefficients_dict[(x_values[0], x_values[1])] = {'a': coefficients[1], 'b': coefficients[0]}
        
                # rule = {'name':v_name,'rule_name': '1st_poly','coefficients': coefficients_dict}   
            elif len(os_value_list) >=2:
                coefficients = np.polyfit(x_values, y_values, 1)  # Fit a quadratic polynomial, if linear,a will be 0
                a = coefficients[0]
                b = coefficients[1]
                coefficients_dict[(x_values[0], x_values[1])] = {'a': a, 'b': b}
                # rule =  {'name':v_name,'rule_name': '1st_poly','coefficients': coefficients_dict}
        self.segment_count += len(coefficients_dict)
        return  {'name':v_name,'rule_name': '1st_poly','coefficients': coefficients_dict}
        


    # def get_coef_poly_1st(self, v_name, valuelist,rules):  ##find dominant coefficients method
    #     self.segment_count += math.factorial(len(valuelist))
    #     coefficients_counter = Counter()
    #     coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
    #     known_coefficients={}

    #     for idx, coeff in enumerate(coefficients_known_list[::-1]):
    #         if coeff != '':
    #             coeff = float(coeff)
    #             known_coefficients[idx] = coeff
    #         else:
    #             known_coefficients[idx] = None

    #     os_value_list = []
    #     os_value_list = []
    #     for index, value in enumerate(valuelist):
    #         if value is not None and value != special_value.UNSEEN and value != special_value.HAVENT_SEEN:
    #             os_value_list.append((index, value))

        
    #     for i in range(len(os_value_list)):
    #         for j in range(i + 1, len(os_value_list)):
    #             x1, y1 = os_value_list[i]
    #             x2, y2 = os_value_list[j]
    #             if x1 == x2:
    #                 continue
    #             a = (y2 - y1) / (x2 - x1)
    #             b = y1 - a * x1

    #             coefficients_counter[(round(a, 6), round(b, 6))] += 1
    #     if not coefficients_counter:
    #         return {'name': v_name, 'rule_name': '1st_poly', 'coefficients': {}}
    #     most_common_coefficients = coefficients_counter.most_common(1)[0][0]

    #     coefficients_dict = {
    #         'a': most_common_coefficients[0],
    #         'b': most_common_coefficients[1]
    #     }

    #     return {
    #         'name': v_name,
    #         'rule_name': '1st_poly',
    #         'coefficients': coefficients_dict
    #     }
    
    # def get_predict_1st_poly(self, i,rule,value):  ##find dominant coefficients method
    #     # print("hererer",i,rule,value)
    #     a = rule['coefficients'].get('a')
    #     b = rule['coefficients'].get('b')
    #     if a is None or b is None:
    #         result = self.get_predict_static(i,rule,value)
    #     else:
    #         result = round(a * i + b)
    #     return result

    def get_coef_power(self, v_name, valuelist, rules):
        self.segment_count += 1
        coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
        known_coefficients = {}
        for idx, coeff in enumerate(coefficients_known_list):
            if coeff:
                coeff = float(coeff)
                known_coefficients[idx] = coeff
            else:
                known_coefficients[idx] = None

        if known_coefficients.get(0) is not None:
            a = known_coefficients[0]
        else:
            os_value_list = []
            for index, value in enumerate(valuelist):
                if value == special_value.UNSEEN or value == special_value.HAVENT_SEEN or value == None:
                    pass
                else:
                    os_value_list.append([index, value])
            if len(os_value_list) >= 1:
                x_values = [item[0] for item in os_value_list][-1:]
                y_values = [item[1] for item in os_value_list][-1:]
                x_values = np.array(x_values)
                y_values = np.array(y_values)
                if x_values % 2 == 0:
                    a = [int(y_values ** (1/x_values)), -int(y_values ** (1/x_values))]
                else:
                    a = [int(y_values ** (1/x_values))]
            else:
                a = [None]
        return {'name': v_name, 'rule_name': 'power', 'coefficients': {'a': a}}
    
    def get_coef_static(self, v_name, valuelist,rules):
        return {'name':v_name,'rule_name': 'static','coefficients': {'a': None}}
    

    def get_coef_mod_1st(self, v_name, valuelist,rules):##
        self.segment_count += 1
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
    
    import numpy as np

    def get_coef_sin(self, v_name, valuelist, rules):
        #print(rules[v_name].rule_content.strip('[]'))
        self.segment_count += 1
        coefficients_known_list = rules[v_name].rule_known_coef.strip('[]').split(',')
        known_coefficients={}
        for idx, coeff in enumerate(coefficients_known_list[::-1]):
            if coeff != '':
                coeff = float(coeff)
                known_coefficients[idx] = coeff
            else:
                known_coefficients[idx] = None

        os_value_list = []
        
        for index, value in enumerate(valuelist):
            if value != special_value.UNSEEN and value != special_value.HAVENT_SEEN and value is not None:
                os_value_list.append([index, value])
     
        if len(os_value_list) < 3:
            return {'name': v_name, 'rule_name': 'sin', 'coefficients': {'a': None, 'b': None, 'c': None}}

        
        x_values = np.array([item[0] for item in os_value_list])  
        y_values = np.array([item[1] for item in os_value_list])  

       
        def sin_func(x, A, B, C):
            return A * np.sin(B*0.5*np.pi  * x + C)

        if len(x_values)>=3:
            popt, _ = curve_fit(sin_func, x_values, y_values, p0=[1, 1, 0])  

            A, B, C = popt  
            A = round(A)
            B = round(B)
            C = round(C)
            return {
                'name': v_name,
                'rule_name': 'sin',
                'coefficients': {'a': A, 'b': B, 'c': C}
            }
        else:
            return {
                'name': v_name,
                'rule_name': 'sin',
                'coefficients': {'a': None, 'b': None, 'c': None}
            }
    def get_segment_count(self):
        count = int(self.segment_count)
        return count

    # def get_rule_dict(self,domains):
    #     rule_dict = {}
    #     for v_name in domains:
    #         variable_dict  = domains[v_name]
    #         dict_list = str(variable_dict).split(';')
    #         v_rule_type = dict_list[-1].split(':')
    #         type_name = str(v_rule_type[1])[:-2].strip()
    #         rule_dict[v_name] = type_name
    #     return rule_dict       