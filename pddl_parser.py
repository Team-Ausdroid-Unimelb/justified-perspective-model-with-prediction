import os
import logging
import datetime
import pytz
import re
TIMEZONE = pytz.timezone('Australia/Melbourne')
DATE_FORMAT = '%d-%m-%Y_%H-%M-%S'
timestamp = datetime.datetime.now().astimezone(TIMEZONE).strftime(DATE_FORMAT)
# logging.basicConfig(filename=f'logs/{timestamp}.log', level=logging.DEBUG)

logger = logging.getLogger("pddl_parser")


def formatDocument(str):
    # . match anything but the endline
    # * match 0 or more preceding RE
    # $ matchs end line
    str = re.sub(';.*$',"",str,flags=re.MULTILINE).lower()
    logger.debug(repr(str))
    
    # removing useless space
    # ^ match any start of the newline in multiline mode
    str = re.sub('^ *| *$|^\n',"",str,flags=re.MULTILINE)
    str = re.sub(' *, *',",",str,flags=re.MULTILINE)
    str = re.sub(' *- *',"-",str,flags=re.MULTILINE)
    str = re.sub('\[ *',"[",str,flags=re.MULTILINE)
    str = re.sub(' *\]',"]",str,flags=re.MULTILINE)
    str = re.sub(':goal *',":goal",str,flags=re.MULTILINE)
    str = re.sub(':action *',":action ",str,flags=re.MULTILINE)
    str = re.sub(':parameters *',":parameters",str,flags=re.MULTILINE)
    str = re.sub(':precondition *',":precondition",str,flags=re.MULTILINE)
    str = re.sub(':effect *',":effect",str,flags=re.MULTILINE)
    logger.debug(repr(str))
    
    # removing useless \n
    str = re.sub('\( *|(\n)*\((\n)*',"(",str,flags=re.MULTILINE)
    str = re.sub(' *\)|(\n)*\)(\n)*',")",str,flags=re.MULTILINE)
    str = re.sub('\)\n',")",str,flags=re.MULTILINE)
    logger.debug(repr(str))
    
    str = re.sub('\n'," ",str,flags=re.MULTILINE)
    logger.debug(repr(str)) 
    return str      

def problemParser(file_path):
    domains = {'agent':{'basic_type':'','values':[]},}
    i_state = {}
    g_states = {}
    agent_index = []
    obj_index = []
    variables = {}
    d_name = ""
    p_name = ""
    
    logger.debug("reading problem file:")
    
    with open(file_path,"r") as f:
        file = f.read()
        logger.debug(repr(file))
        
        logger.debug("formating problem file")
        str = formatDocument(file)
        logger.debug(repr(str))
        
        if not str.startswith("(define"):
            logger.error("the problem file does not start with '(define'")
            exit()
        elif not str.endswith(")"):
            logger.error("the problem file does not end with ')'")
            exit()
        str = str[7:-1:]
        logger.debug(repr(str))
        # print(repr(str))
        
        logger.debug("extract p_name")
        try:
            found = re.search('\(problem [0-9a-z_]*\)',str).group(0)
            p_name = found[9:-1:]
            logger.debug(p_name)
        except AttributeError:
            logger.error("error when extract problem name")
            exit()
            
        logger.debug("extract d_name")
        try:
            found = re.search('\(:domain [0-9a-z_]*\)',str).group(0)
            d_name = found[9:-1:]
            logger.debug(d_name)
        except AttributeError:
            logger.error("error when extract domain name")
            exit()            

        logger.debug("extract agents")
        try:
            found = re.search('\(:agents [0-9a-z_ ]*\)',str).group(0)
            agent_index = found[9:-1:].split(" ")
            logger.debug(agent_index)
        except AttributeError:
            logger.error("error when extract agents")
            exit()

        logger.debug("extract objects")
        try:
            found = re.search('\(:objects [0-9a-z_ ]*\)',str).group(0)
            obj_index = found[10:-1:].split(" ")
            logger.debug(obj_index)
        except AttributeError:
            logger.error("error when extract objects")
            exit()

        logger.debug("extract variables")
        try:
            found = re.search('\(:variables([(][0-9a-z_ \[\],]*[)])*\)',str).group(0)
            logger.debug(found)
            vars_list = re.findall('\([0-9a-z_ \[\],]*\)',found[10:-1:])
            logger.debug(vars_list)
            for var_str in vars_list:
                var_str = var_str[1:-1:].split(' ')
                # print(var_str)
                variables.update({var_str[0]:var_str[1][1:-1:].split(",")})
            logger.debug(variables)
        except AttributeError:
            logger.error("error when extract variables")
            exit()
            
        logger.debug("extract init")
        try:
            found = re.search("\(:init(\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\))*\)",str).group(0)
            logger.debug(found)
            init_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[6:-1:])
            logger.debug(init_list)
            for init_str in init_list:
                init_str = init_str[3:-1:]
                i,j = re.search("\(.*\)", init_str).span()
                var_str = init_str[i+1:j-1:].replace(" ","-")
                value = init_str[j+1::]
                # value = re.search('".*"',init_str[j+1::]).group(0)
                if "'" in value:
                    value = value.replace("'","")
                elif '"' in value:
                    value = value.replace('"',"")
                else:
                    value =int(value)
                i_state.update({var_str:value})
                
            logger.debug(i_state)
        except AttributeError:
            logger.error("error when extract init")
            exit()            

        logger.debug("extract goal")
        try:
            
            found = re.search("\(:goal\(and(\(= \([:0-9a-z_ \[\],]*(\(.*\)\) |\) )[0-9a-z_ \"\']*\))*\)\)",str).group(0)
            logger.debug(found)
            
            # loading ontic goals
            logger.debug("extract ontic goal propositions")
            g_states.update({"ontic_g":{}})
            # ontic_goal_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[10:-1:])
            ontic_goal_list = re.findall('\(= \(:ontic[ 0-9a-z_\[\],]*\(= \([ 0-9a-z_]*\) [0-9a-z_\'\"]*\)\) [0-9a-z_\'\"]*\)',found[10:-1:])  

            logger.debug(f'ontic goal list: {ontic_goal_list}')
            for goal_str in ontic_goal_list:
                goal_str = goal_str[15:-5:]
                logger.debug(f'single goal_str {goal_str}')
                
                goal_list = goal_str.split(') ')
                variable = goal_list[0].replace(' ','-')
                value = goal_list[1]
                if "'" in value:
                    value = value.replace("'","")
                elif '"' in value:
                    value = value.replace('"',"")
                else:
                    value =int(value)
                # print(value)
                g_states["ontic_g"].update({variable:value})
            
            # loading epismetic goals
            logger.debug("extract epistemic goal propositions")
            g_states.update({"epistemic_g":[]})   
            epistemic_goal_list = re.findall('\(= \(:epistemic[ 0-9a-z_\[\],]*\(= \([ 0-9a-z_]*\) [0-9a-z_\'\"]*\)\) [0-9a-z_\'\"]*\)',found[10:-1:])  
            logger.debug(epistemic_goal_list)
            for goal_str in epistemic_goal_list:
                goal_str = goal_str[15:-1:]

                i,j = re.search('\)\) .*',goal_str).span()
                value1 = int(goal_str[i+3:j:])
                query = goal_str[:i+2:]
                p,q = re.search('\(= \([0-9a-z _]*\) [0-9a-z _\'\"]*\)',query).span()
                new_str = query[p+3:q-1]
                query = query[:p]
                m,n = re.search('\([0-9a-z _]*\)',new_str).span()
                var = new_str[m+1:n-1].replace(" ","-")
                value = new_str[n+1:]
                query = f"{query}('{var}',{value})"
                g_states["epistemic_g"].append((query,value1))
            logger.debug(g_states)
        except AttributeError:
            logger.error("error when extract goal")
            exit()   
                        
        logger.debug("extract domains")
        try:
            logger.debug(f"{str}")
            
            found = re.search('\(:domains(\([0-9a-z_ \[\],\'\"]*\))*\)',str).group(0)
            logger.debug(found)
            domains_list = re.findall('\([0-9a-z_ \[\],\'\"]*\)',found[9:-1:])
            logger.debug(domains_list)
            for domain_str in domains_list:
                domain_str = domain_str[1:-1:].split(' ')
                if not domain_str[1] in ['enumerate','integer','string']:
                    logger.error(f"domain {domain_str[0]}'s basic_type {domain_str[1]} does not exist")
                    assert(f"domain {domain_str[0]}'s basic_type {domain_str[1]} does not exist")
                else:
                    if "'" in domain_str[2]:
                        value = domain_str[2].replace("'","")[1:-1:].split(",")
                    elif '"' in domain_str[2]:
                        value = domain_str[2].replace('"',"")[1:-1:].split(",")
                    else:
                        value = [ int(i) for i in domain_str[2][1:-1:].split(",")]
                    domains.update({domain_str[0]:{"basic_type":domain_str[1],"values":value}})
            logger.debug(domains)
        except AttributeError:
            logger.error("error when extract domains")
            exit()
            
        return domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name
    
def domainParser(file_path):
    actions = {}
    d_name = ""

    
    logger.debug("reading domain file:")
    
    with open(file_path,"r") as f:
        file = f.read()
        logger.debug(repr(file))
        
        logger.debug("formating domain file")
        str = formatDocument(file)
        logger.debug(repr(str))
        
        if not str.startswith("(define"):
            logger.error("the domain file does not start with '(define'")
            exit()
        elif not str.endswith(")"):
            logger.error("the domain file does not end with ')'")
            exit()
        str = str[7:-1:]
        logger.debug(repr(str))
        
        logger.debug("extract d_name")
        try:
            found = re.search('\(domain [0-9a-z_]*\)',str).group(0)
            d_name = found[8:-1:]
            logger.debug(d_name)
        except AttributeError:
            logger.error("error when extract domain name")
            exit()  
        
        
        logger.debug("extract actions")
        try:
            action_list = str.split("(:action ")[1::]

            for action_str in action_list:
                parameters = []
                preconditions = {}
                effects = []
                action_str = action_str[:-1:]
                action_name = action_str.split(" ")[0]
                
                # decode parameters
                parameters_str = re.search(':parameters\(.*\):precondition',action_str).group()
                logger.debug(f'parameters_str: {parameters_str}')
                for p_str in parameters_str[12:-14:].split(","):
                    if p_str == '':
                        continue
                    logger.debug(f'single parameters_str: {p_str}')
                    p = p_str.split("-")
                    parameters.append((p[0],p[1]))
                logger.debug(f'parameters: {parameters}')
                
                logger.debug("extract preconditions")
                try:
                    
                    preconditions_str = re.search(':precondition\(and.*\):effect', action_str).group()
                    preconditions_str = preconditions_str[17:-8:]
                    logger.debug(preconditions_str)
                    
                    # loading ontic precondition
                    logger.debug("extract ontic preconditions propositions")
                    preconditions.update({"ontic_p":[]})
                    
                    # ontic_goal_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[10:-1:])
                    # (= (:ontic (= (agent_at-a) (secret_at ?s))) 1)
                    ontic_preconditions_list = re.findall('\(= \(:ontic[ 0-9a-z_\[\],]*\(= \([ 0-9a-z_\-\?]*\) [\(\)\?0-9a-z_\'\" ]*\)\) [0-9a-z_\'\"]*\)',preconditions_str)  

                    logger.debug(f'ontic preconditions list: {ontic_preconditions_list}')
                    for pre_str in ontic_preconditions_list:
                        pre_str = pre_str[15:-5:]
                        logger.debug(f'single precondition_str {pre_str}')
                        
                        precondition_list = pre_str.split(') ')
                        variable = precondition_list[0].replace(' ?','?').replace(' ','-')
                        value = precondition_list[1]
                        if "'" in value:
                            value = value.replace("'","")
                        elif '"' in value:
                            value = value.replace('"',"")
                        elif "(" in value:
                            value = value.replace('(',"").replace(' ','').replace(')','')
                        else:
                            value =int(value)
                        # print(value)
                        preconditions["ontic_p"].append((variable,value))
                    
                    # loading epismetic goals
                    logger.debug("extract epistemic precondition propositions")
                    preconditions.update({"epistemic_p":[]})   
                    epistemic_preconditions_list = re.findall('\(= \(:epistemic[\? 0-9a-z_\[\],]*\(= \([ 0-9a-z_\? ]*\) [0-9a-z_\'\"\]*\)\) [0-9a-z_\'\"]*\)',preconditions_str)  
                    logger.debug(epistemic_preconditions_list)
                    for pre_str in epistemic_preconditions_list:
                        pre_str = pre_str[15:-1:]
                        logger.debug(f"pre str: {pre_str}")
                        i,j = re.search('\)\) .*',pre_str).span()
                        logger.debug(f'i: {i}, j: {j}')
                        value1 = int(pre_str[i+3:j:])
                        logger.debug(f'value for epistemic query: {value1}')
                        query = pre_str[:i+2:]
                        logger.debug(f'query str: {query}')
                        p,q = re.search('\(= \([0-9a-z _\?]*\) [0-9a-z _\'\"]*\)',query).span()
                        new_str = query[p+3:q-1]
                        logger.debug(f'value string in epistemic query: {new_str}')
                        query = query[:p]
                        m,n = re.search('\([0-9a-z _\?]*\)',new_str).span()
                        var = new_str[m+1:n-1].replace(" ?","?").replace(' ','-')
                        value = new_str[n+1:]
                        query = f"{query}('{var}',{value})"
                        preconditions["epistemic_p"].append((query,value1))
                    logger.debug(preconditions)
                except AttributeError:
                    logger.error("error when extract precondition")
                    exit()   
                
                
                
                #decode precondition
                # preconditions_str = re.search(':precondition\(and.*\):effect', action_str).group()
                # logger.debug(f'preconditions_str: {preconditions_str}')  
                # for p_str in preconditions_str[18:-9:].split('(= '):
                #     if p_str == '':
                #         continue
                #     logger.debug(f'single precondition_str: {p_str}')
                #     p_list = p_str[1:].split(") ")
                #     # if len(p_list) == 1:
                #     #     p_list = p_list[0].split(" ")
                #     preconditions.append((p_list[0].replace(" ","").replace("(","").replace(")",""),p_list[1].replace(" ","").replace("(","").replace(")","").replace('"','').replace("'",'')))
                # logger.debug(f'preconditions: {preconditions}')
                
                #decode effects
                effects_str = re.search(':effect\(and\(.*\)\)',action_str).group()
                logger.debug(f'effects_str: {effects_str}')  
                for e_str in effects_str[11:-2:].split("(= "):
                    if e_str == '':
                        continue
                    logger.debug(f'single effect_str: {e_str}')
                    e_list = e_str[1:].split(") ")
                    # if len(e_list) == 1:
                    #     e_list = e_list[0].split(" ")
                    effects.append((e_list[0].replace(" ","").replace("(","").replace(")",""),e_list[1].replace(" ","").replace("(","").replace(")","").replace('"','').replace("'",'')))
                logger.debug(f'effects: {effects}')
                
                actions.update({action_name: {"parameters":parameters,"precondition":preconditions,"effect":effects}})
            logger.debug(actions)
        except AttributeError:
            logger.error("error when extract actions")
            exit()          
        return actions,d_name
    
