import enum
import pddl_model
import typing
import re
import logging

logger = logging.getLogger("epistemic_model")


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
    
    def __init__(self,input1,input2,input3,content=None):
        
        if content is None:
            # convert from string, header, g_group, content
            self.q_type,self.eq_type = self.mapping[input1]
            self.q_group = input2.split(",")
            self.q_content = input3
        else:    
            # initialize manually
            self.q_type = input1
            self.eq_type = input2
            self.q_group = input3
            self.q_content = content
        
        
    def __str__(self): # show only in the print(object)
        output = f"<epistemic: q_type: {self.q_type}; eq_type: {self.eq_type}; q_group: {self.q_group}; q_content: {self.q_content} >"
        # if type(self.q_content) == str:
        #     output += "\n\n"
        return output

    def __repr__(self): # show when in a dictionary
        output = f"<epistemic: q_type: {self.q_type}; eq_type: {self.eq_type}; q_group: {self.q_group}; q_content: {self.q_content} >"
        # if type(self.q_content) == str:
        #     output += "\n\n"
        return output




def generateEpistemicQuery(eq_str):
    match = re.search("[edc]?[ksb] \[[0-9a-z_,]*\] ",eq_str)
    if match == None:
        logging.debug(f"return eq string {eq_str}")
        return eq_str
    else:
        eq_list = eq_str.split(" ")
        header = eq_list[0]
        agents = eq_list[1][1:-1]
        content = eq_str[len(header)+len(agents)+4:]
        return EpistemicQuery(header,agents,generateEpistemicQuery(content))
    

def checkingEQs(problem:pddl_model.Problem,eq_str_list:typing.List,path:typing.List):
    eq_pair_list = [(generateEpistemicQuery(eq_str),value) for eq_str,value in eq_str_list]
    logging.debug(f"{eq_pair_list}")
    for eq,value in eq_pair_list:
        print(value)
        if not checkingEQ(problem,eq,path,path[-1][0]) == value:
            return False
    return True

# update this function if we change how the model works
def getObservations(problem:pddl_model.Problem,state,agt_id_nest_lst,):
    logging.debug(f"generating observation of agent {agt_id_nest_lst} from state: {state}")
    new_state = state.copy()
    temp_agt_nest_list = agt_id_nest_lst.copy()
    while not temp_agt_nest_list == []:
        temp_agent_list =  temp_agt_nest_list.pop()
        new_state = getOneObservation(problem,new_state,temp_agent_list[0])
        # while not temp_agent_list ==[]:
        #     getOneObservation
    return new_state

def getOneObservation(problem:pddl_model.Problem,state,agt_id):
    new_state = {}
    for var_index,value in state.items():
        if problem.external.checkVisibility(problem,state,agt_id,var_index)==pddl_model.T_TYPE.TRUE:
        # if bbl.checkVisibility(problem,state,agt_id,var_index)==T_TYPE.TRUE:
        #     new_state.update({var_index: (value if not value == VALUE.UNSEEN else VALUE.SEEN)})
        # else:
        #     new_state.update({var_index:VALUE.UNSEEN})
            new_state.update({var_index: value})
    return new_state

# def generatePerspective(problem:Problem, path:typing.List, agt_index):
#     logging.debug("generatePerspective")
#     if path == []:
#         return {}
#     # assert(path == [])
#     state, action = path[-1]
#     new_state = getObservations(problem,state,agt_index)
#     memory = generateMemorization(problem, path[:-1],agt_index)

def identifyMemorizedValue(problem:pddl_model.Problem, path:typing.List, agt_id_nest_lst, ts_index,variable_index):
    ts_index_temp = ts_index
    if ts_index_temp <0: return None
    
    while ts_index_temp >=0:
        state,action = path[ts_index]
        temp_observation = getObservations(problem,state,agt_id_nest_lst)
        if temp_observation[variable_index] == None:
            ts_index_temp += -1
        else:
            return temp_observation[variable_index]
    
    ts_index_temp = ts_index + 1
       
    while ts_index_temp < len(path):
        state,action = path[ts_index]
        temp_observation = getObservations(problem,state,agt_id_nest_lst)
        if temp_observation[variable_index] == None:
            ts_index_temp += 1
        else:
            return temp_observation[variable_index]        
    return None

def identifyLastSeenTimestamp(problem:pddl_model.Problem, path:typing.List, agt_id_nest_lst,variable_index):
    ts_index_temp = len(path) -1
    
    # checking whether the variable has been seen by the agent list before
    while ts_index_temp >0:
        
        state,action = path[ts_index_temp]

        # checking with observation
        if variable_index in getObservations(problem,state,agt_id_nest_lst) :
            return ts_index_temp
        else:
            ts_index_temp -= 1
    return -1

def generatePerspective(problem:pddl_model.Problem, path:typing.List, agt_id_nest_lst):
    logging.debug("generatePerspective")
    if path == []:
        return {}
    # assert(path == [])
    state, action = path[-1]
    new_state = {}
    print(state)
    for v,e in state.items():
        ts_index = identifyLastSeenTimestamp(problem, path, agt_id_nest_lst,v)
        value = identifyMemorizedValue(problem, path, agt_id_nest_lst, ts_index,v)
        new_state.update({v:value})
    return new_state 


#     for var_index,value in state.items():
#         if var_index not in new_state.keys():
#             if memory == {}:
#                 new_state.update({var_index:None})
#             else:
#                 new_state.update({var_index:memory[var_index]})
#     return new_state

# def generateMemorization(problem:Problem,path:typing.List,agt_index):
#     # if there is no state ahead, then return empty
#     # this can be altered to handle different initial BELIEF
#     if path == []:
#         return {}
#     new_state = {}
#     print(path)
#     state,action=path[-1]
#     observation = getObservations(problem,state,agt_index)
#     perspective = generatePerspective(problem,path[:-1],agt_index)
#     for var_index,value in perspective.items():
#         if not var_index in observation.keys():
#             new_state.update({var_index,value})
#     return new_state


def checkingEQ(problem:pddl_model.Problem,eq:EpistemicQuery,path:typing.List,world):
    var_list = problem.external.extractVariables(problem,eq)
    logging.debug(f"checking eq {eq}, {eq.eq_type}")
    if eq.eq_type == EQ_TYPE.BELIEF:
        
        logging.debug(f"checking belief for {eq}")
        # generate the world
        new_observation = getObservations(problem,world,eq.q_group)
        new_world = generatePerspective(problem,path,eq.q_group)
        logging.debug(f"{eq.q_group}'s perspective {new_world}")
        if len(eq.q_group)>1:
            pass
        eva = 2
        logging.debug(f"checking belief for {eq.q_content}")
        if type(eq.q_content) == str:
            for var_name,value in var_list:

                if not var_name in new_world.keys():
                    logging.debug(f"return 0 due to {var_name} {len(var_name)} not in { new_world.keys() }")
                    return 0
                if not new_world[var_name] == value:
                    logging.debug(f"return 0 due to {value} not equal to {new_world[var_name]}")
                    return 0
            eva = problem.external.evaluateS(problem,new_world,eq.q_content)
        else:
            eva = checkingEQ(problem,eq.q_content,path,new_world)
        
        return eva
        # if eva == 2:
        #     return checkingEQ(problem,eq,path[:-1],path[-1][0])
        # else:
        #     return eva
        # if type(eq.q_content) == str:
        #     # for var_name,value in var_list:
        #     #     if not var_name in new_world.keys():
        #     #         return checkingEQ(problem,eq,path[:-1],path[-1][0])
        #     #     if not new_world[var_name] == value:
        #     #         return 0
        #     if bbl.evaluateS(problem,new_world,eq.q_content) == 2:
        #         return checkingEQ(problem,eq,path[:-1],path[-1][0])
        #     else:
        #         return bbl.evaluateS(problem,new_world,eq.q_content) == 2
        # else:
        #     if bbl.evaluateS(problem,new_world,eq.q_content) == 2:
        #         return checkingEQ(problem,eq,path[:-1],path[-1][0])
        #     else:
        #         return bbl.evaluateS(problem,new_world,eq.q_content) == 2
        #     pass
    elif eq.eq_type == EQ_TYPE.SEEING:
        
        logging.debug(f"checking seeing for {eq}")
        # generate the world
        new_world = getObservations(problem,world,eq.q_group)
        logging.debug(f"{eq.q_group}'s observation {new_world}")
        if len(eq.q_group) > 1:
            # merging observation
            pass
        if type(eq.q_content) == str:
            return problem.external.evaluateS(problem,new_world,eq.q_content)
        else:
            for var_name,value in var_list:
                if not var_name in new_world.keys():
                    return 2
            result = checkingEQ(problem,eq.q_content,path,new_world)
            if not result == 2:
                return 1
            else:
                return 0
            # return not checkingEQ(problem,eq.q_content,path,world) == 2
    elif eq.eq_type == EQ_TYPE.KNOWLEDGE:   
        
        logging.debug(f"checking knowledge for {eq}")
        # generate the world
        new_world = getObservations(problem,world,eq.q_group)
        logging.debug(f"b's observation {new_world}")
        if len(eq.q_group) > 1:
            # merging observation
            pass
        logging.debug(type(eq.q_content))
        if type(eq.q_content) == str:
            for var_name,value in var_list:
                if not var_name in new_world.keys():
                    return 0
                if not new_world[var_name] == value:
                    return 0
            return problem.external.evaluateS(problem,new_world,eq.q_content)
        else:
            # for var_name,value in var_list:
                # if not var_name in new_world.keys():
                #     return 2
                # if not new_world[var_name] == value:
                #     return 0
            eqs = EpistemicQuery(eq.q_type,EQ_TYPE.SEEING,eq.q_group,copy.deepcopy(eq.q_content))
            result = checkingEQ(problem,eq.q_content,path,world)*checkingEQ(problem,eqs,path,world)
            if result >2:
                return 2
            else:
                return result
    else:
        logging.error(f"not found eq_type in the query: {eq}")
        
