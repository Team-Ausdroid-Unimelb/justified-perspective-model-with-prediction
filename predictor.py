import numpy as np

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
            for i in range(len(value)):
                ps_dict[v_name][i] = os_dict[v_name][i]
                if value[i] is None:
                    ps_dict[v_name][i] = self.predict(i,new_rs[v_name],value)
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
        else:
            result = self.external.domain_specific_predict(i,rule,value)
            if result == None:
                result = self.get_predict_static(i,rule,value)
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
        #print("os",new_os)
        #print("os",os_dict)
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
            x_values = [item[0] for item in os_value_list][-3:]
            y_values = [item[1] for item in os_value_list][-3:]
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
            x_values = [item[0] for item in os_value_list][-2:]
            y_values = [item[1] for item in os_value_list][-2:]
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
    
    
    
    def get_rule_dict(self,domains):
        rule_dict = {}
        for v_name in domains:
            variable_dict  = domains[v_name]
            dict_list = str(variable_dict).split(';')
            v_rule_type = dict_list[-1].split(':')
            type_name = str(v_rule_type[1])[:-2].strip()
            rule_dict[v_name] = type_name
        return rule_dict       