import os
import logging
import datetime
import pytz
import re
TIMEZONE = pytz.timezone('Australia/Melbourne')
DATE_FORMAT = '%d-%m-%Y_%H-%M-%S'
timestamp = datetime.datetime.now().astimezone(TIMEZONE).strftime(DATE_FORMAT)
logging.basicConfig(filename=f'logs/{timestamp}.log', level=logging.DEBUG)


def formatDocument(str):
    # . match anything but the endline
    # * match 0 or more preceding RE
    # $ matchs end line
    str = re.sub(';.*$',"",str,flags=re.MULTILINE).lower()
    logging.debug(repr(str))
    
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
    logging.debug(repr(str))
    
    # removing useless \n
    str = re.sub('\( *|(\n)*\((\n)*',"(",str,flags=re.MULTILINE)
    str = re.sub(' *\)|(\n)*\)(\n)*',")",str,flags=re.MULTILINE)
    str = re.sub('\)\n',")",str,flags=re.MULTILINE)
    logging.debug(repr(str))
    
    str = re.sub('\n'," ",str,flags=re.MULTILINE)
    logging.debug(repr(str)) 
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
    
    logging.debug("reading problem file:")
    
    with open(file_path,"r") as f:
        file = f.read()
        logging.debug(repr(file))
        
        logging.debug("formating problem file")
        str = formatDocument(file)
        logging.debug(repr(str))
        
        if not str.startswith("(define"):
            logging.error("the problem file does not start with '(define'")
            exit()
        elif not str.endswith(")"):
            logging.error("the problem file does not end with ')'")
            exit()
        str = str[7:-1:]
        logging.debug(repr(str))
        # print(repr(str))
        
        logging.debug("extra p_name")
        try:
            found = re.search('\(problem [0-9a-z_]*\)',str).group(0)
            p_name = found[9:-1:]
            logging.debug(p_name)
        except AttributeError:
            logging.error("error when extract problem name")
            exit()
            
        logging.debug("extra d_name")
        try:
            found = re.search('\(:domain [0-9a-z_]*\)',str).group(0)
            d_name = found[9:-1:]
            logging.debug(d_name)
        except AttributeError:
            logging.error("error when extract domain name")
            exit()            

        logging.debug("extra agents")
        try:
            found = re.search('\(:agents [0-9a-z_ ]*\)',str).group(0)
            agent_index = found[9:-1:].split(" ")
            logging.debug(agent_index)
        except AttributeError:
            logging.error("error when extract domain name")
            exit()

        logging.debug("extra objects")
        try:
            found = re.search('\(:objects [0-9a-z_ ]*\)',str).group(0)
            obj_index = found[10:-1:].split(" ")
            logging.debug(obj_index)
        except AttributeError:
            logging.error("error when extract domain name")
            exit()

        logging.debug("extra variables")
        try:
            found = re.search('\(:variables([(][0-9a-z_ \[\],]*[)])*\)',str).group(0)
            logging.debug(found)
            vars_list = re.findall('\([0-9a-z_ \[\],]*\)',found[10:-1:])
            logging.debug(vars_list)
            for var_str in vars_list:
                var_str = var_str[1:-1:].split(' ')
                # print(var_str)
                variables.update({var_str[0]:var_str[1][1:-1:].split(",")})
            logging.debug(variables)
        except AttributeError:
            logging.error("error when extract variables")
            exit()
            
        logging.debug("extra init")
        try:
            found = re.search("\(:init(\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\))*\)",str).group(0)
            logging.debug(found)
            init_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[6:-1:])
            logging.debug(init_list)
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
                
            logging.debug(i_state)
        except AttributeError:
            logging.error("error when extract init")
            exit()            

        logging.debug("extra goal")
        try:
            found = re.search("\(:goal\(and(\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\))*\)\)",str).group(0)
            logging.debug(found)
            goal_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[10:-1:])
            logging.debug(goal_list)
            for goal_str in goal_list:
                goal_str = goal_str[3:-1:]
                i,j = re.search("\(.*\)", goal_str).span()
                var_str = goal_str[i+1:j-1:].replace(" ","-")
                print(var_str)
                value = goal_str[j+1::]
                # value = re.search('".*"',init_str[j+1::]).group(0)
                if "'" in value:
                    value = value.replace("'","")
                elif '"' in value:
                    value = value.replace('"',"")
                else:
                    value =int(value)
                # print(value)
                g_states.update({var_str:value})
                
            logging.debug(g_states)
        except AttributeError:
            logging.error("error when extract goal")
            exit()   
                        
        logging.debug("extra domains")
        try:
            found = re.search('\(:domains(\([0-9a-z_ \[\],\'\"]*\))*\)',str).group(0)
            logging.debug(found)
            domains_list = re.findall('\([0-9a-z_ \[\],\'\"]*\)',found[9:-1:])
            logging.debug(domains_list)
            for domain_str in domains_list:
                domain_str = domain_str[1:-1:].split(' ')
                if not domain_str[1] in ['enumerate','integer','string']:
                    logging.error(f"domain {domain_str[0]}'s basic_type {domain_str[1]} does not exist")
                    assert(f"domain {domain_str[0]}'s basic_type {domain_str[1]} does not exist")
                else:
                    if "'" in domain_str[2]:
                        value = domain_str[2].replace("'","")[1:-1:].split(",")
                    elif '"' in domain_str[2]:
                        value = domain_str[2].replace('"',"")[1:-1:].split(",")
                    else:
                        value = [ int(i) for i in domain_str[2][1:-1:].split(",")]
                    domains.update({domain_str[0]:{"basic_type":domain_str[1],"values":value}})
            logging.debug(domains)
        except AttributeError:
            logging.error("error when extract variables")
            exit()
            
        return domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name
    
def domainParser(file_path):
    actions = {}
    d_name = ""

    
    logging.debug("reading domain file:")
    
    with open(file_path,"r") as f:
        file = f.read()
        logging.debug(repr(file))
        
        logging.debug("formating domain file")
        str = formatDocument(file)
        logging.debug(repr(str))
        
        if not str.startswith("(define"):
            logging.error("the domain file does not start with '(define'")
            exit()
        elif not str.endswith(")"):
            logging.error("the domain file does not end with ')'")
            exit()
        str = str[7:-1:]
        logging.debug(repr(str))
        
        logging.debug("extra d_name")
        try:
            found = re.search('\(domain [0-9a-z_]*\)',str).group(0)
            d_name = found[8:-1:]
            logging.debug(d_name)
        except AttributeError:
            logging.error("error when extract domain name")
            exit()  
        
        print(str)
        
        logging.debug("extra actions")
        try:
            action_list = str.split("(:action ")[1::]
            print(action_list)
            for action_str in action_list:
                parameters = []
                precondition = []
                effects = []
                action_str = action_str[:-1:]
                action_name = action_str.split(" ")[0]
                parameters_str = re.search(':parameters\(.*\):precondition',action_str).group()
                for p_str in parameters_str[12:-14:].split(","):
                    p = p_str.split("-")
                    parameters.append((p[0],p[1]))
                effects_str = re.search(':effect\(and\(.*\)\)',action_str).group()
                for e_str in effects_str[12:-2:].split("(= "):
                    e_list = e_str[1:-1:].split(") (")
                    effects.append((e_list[0].replace(" ","").replace("(","").replace(")",""),e_list[1].replace(" ","").replace("(","").replace(")","")))
                actions.update({action_name: {"parameters":parameters,"precondition":precondition,"effect":effects}})
            logging.debug(actions)
        except AttributeError:
            logging.error("error when extract domain name")
            exit()          
        
        
        
        return actions,d_name
    
if __name__ == "__main__":
    domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name=problemParser("examples/problem01.pddl")
    actions,domain_name = domainParser("examples/domain.pddl")
    
    import model
    problem = model.Problem(domains,i_state,g_states,agent_index,obj_index,variables,actions)
    import search
    
    print(search.BFS(problem))
    # actions = prob
    # lem.getLegalActions(i_state)
    # print(actions)
    
    # print(problem.generatorSuccessor(i_state,actions['turn_clockwise-a']))
    
    # print(BFS(problem))