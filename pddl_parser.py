import os
import logging
import datetime
import pytz
import re
import traceback
import typing

from util import EpistemicQuery
TIMEZONE = pytz.timezone('Australia/Melbourne')
DATE_FORMAT = '%d-%m-%Y_%H-%M-%S'
timestamp = datetime.datetime.now().astimezone(TIMEZONE).strftime(DATE_FORMAT)
# logging.basicConfig(filename=f'logs/{timestamp}.log', level=logging.DEBUG)

LINE_BREAK = "&"
DOMAIN_PREFIX = "(define"
DOMAIN_SURFIX = ")"

DOMAIN_NAME_REG_PREFIX = "\(domain "
DOMAIN_NAME_REG ="[0-9a-z_]*"
DOMAIN_NAME_REG_SURFIX= "\)"

TYPING_REG_PREFIX = "\(:types"
TYPING_REG = "[&0-9a-z_\- ]*"
TYPING_REG_SURFIX= "\)"

FUNC_REG_PREFIX = "\(:functions"
FUNC_REG = "(\([a-z0-9 \-\?]*\))*"
FUNC_REG_SURFIX= "\)"

ACTION_REG_PREFIX = "\(:action "
ACTION_REG = ".*"
ACTION_REG_SURFIX= "\)"

PARAMETERS_REG_PREFIX = ":parameters\("
PARAMETERS_REG = "(.*?)"
PARAMETERS_REG_SURFIX= "\)"

EFFECT_REG_PREFIX = ":effect\("
EFFECT_REG = ".*"
EFFECT_REG_SURFIX= "\)"

PRECONDITION_REG_PREFIX = ":precondition\("
PRECONDITION_REG = ".*"
PRECONDITION_REG_SURFIX= "\)"

EFFECT_CONDITION_REG_PREFIX = r"\("
EFFECT_CONDITION_REG = r"(assign|increase|decrease) \(\w*\??\w*\) \(\@jp \(\"[\w \[\]]*\"\) \(\w*\??\w*\)\)"
EFFECT_CONDITION_REG_SURFIX = r"\)"

LOGGER_NAME = "pddl_parser"
LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.DEBUG
from util import setup_logger 
from util import Type,VAR,Parameters,EffectType,Effect,UpdateType,ActionSchema

EFFECT_TYPE_DICT = {
    "increase": EffectType.INCREASE,
    "decrease": EffectType.DECREASE,
    "assign":EffectType.ASSIGN
}

ONTIC_RE_PREFIX = "\(:ontic"
ONTIC_STR_PREFIX = "(:ontic"
EPISTEMIC_RE_PREFIX = "\(:epistemic"
EPISTEMIC_STR_PREFIX = "(:epistemic"
BOTH_RE_PREFIX = "\(:(?:epistemic|ontic)"
PREDICATE_RE = " ((?:\$|\+|\-) [a-z]* \[[a-z0-9,]*\] )*\((?:>|<|=|>=|<=|\-=)+ \([\? 0-9a-z_\-]*\) (?:[0-9a-z_\'\"\-]+|\([0-9a-z_ ]+\))\)\)"

class PDDLParser:
    def __init__(self,handlers):
        self.logger = setup_logger(LOGGER_NAME,handlers,logger_level=LOGGER_LEVEL) 
        self.logger.debug("PDDL PARSER initialized")

    def run(self,domain_path,problem_path):
        # this should decode the domain first and then problem

        self.logger.info("Reading domain file")
        self.logger.info(domain_path)
        domain_file = ""
        with open(domain_path,"r") as f:
            domain_file = f.read()

        self.logger.debug(repr(domain_file))
        self.logger.debug("format document")
        domain_str = self.formatDocument(domain_file)

        self.logger.info("Parsing domain file")
        domain_name,types,functions,action_schemas = self.domainParser(domain_str)
        
        self.logger.info("Reading problem file")
        self.logger.info(problem_path)
        problem_file = ""
        with open(problem_path,"r") as f:
            problem_file = f.read()
            
        self.logger.debug(repr(problem_file))
        self.logger.debug("format document")
        problem_str = self.formatDocument(problem_file)
        
        self.logger.info("Parsing problem file")
        self.problemParser(problem_str)

    def keyWordParser(self,keyword,reg_prefix,reg_str,reg_surfix,input_str):
        self.logger.debug("extract %s",keyword)
        inner_str = ""
        try:
            pattern = f'{reg_prefix}{reg_str}{reg_surfix}'
            found = re.search(pattern,input_str).group(0)
            lp = len(re.sub(r'\\([.*+()])', r'\1', reg_prefix))
            ls = len(re.sub(r'\\([.*+()])', r'\1', reg_surfix))
            inner_str = found[lp:-ls:]
            self.logger.debug("Found %s: [%s]",keyword,inner_str)
        except:
            
            self.logger.error("error when extract domain")
            self.logger.error("pattern is %s",pattern)
            self.logger.error("target is %s",input_str)
            # self.logger.error(traceback.format_exc())
            exit()  
        output_str = input_str[lp+len(inner_str)+ls:]
        self.logger.debug(repr(input_str))
        return inner_str,output_str



    def domainParser(self,domain_str):
        actions = {}
        # checking the prefix and surface of the whole domain file
        if not domain_str.startswith(DOMAIN_PREFIX):
            self.logger.error("the domain file does not start with '%s'",DOMAIN_PREFIX)
            exit()
        elif not domain_str.endswith(DOMAIN_SURFIX):
            self.logger.error("the domain file does not end with '%s'",DOMAIN_SURFIX)
            exit()
        domain_str = domain_str[len(DOMAIN_PREFIX):-len(DOMAIN_SURFIX):]
        self.logger.debug(repr(domain_str))
        
        # extract domain name
        domain_name,domain_str = self.keyWordParser("domain_name",DOMAIN_NAME_REG_PREFIX,DOMAIN_NAME_REG,DOMAIN_NAME_REG_SURFIX,domain_str)

        # extract typing
        typing_str,domain_str = self.keyWordParser("types",TYPING_REG_PREFIX,TYPING_REG,TYPING_REG_SURFIX,domain_str)
        # types: typing.List[Type] = []
        types: typing.Dict[str,Type] = {}
        for type_str in typing_str.split(LINE_BREAK):
            if type_str == "":
                continue
            elif '-' in type_str:
                # it has parent types:
                type_str_list= type_str.split("-")
                type_str = type_str_list[0]
                parent_type_name = type_str_list[1]
            else:
                parent_type_name = ""

            for type_name in type_str.split(" "):
                new_type = Type(type_name)
                new_type.parent_type_name = parent_type_name
                types.update({type_name:new_type})
        self.logger.debug(types)
        # double check the parent types
        type_names = types.keys()
        for k,item in types.items():
            p_name = item.parent_type_name
            if not p_name == "" and not p_name in type_names:
                raise ValueError("checking type %s: parent type name not found in types: %s",k,p_name)

        # extra functions
        functions : typing.Dict[str,VAR] = {}
        all_function_str,domain_str = self.keyWordParser("functions",FUNC_REG_PREFIX,FUNC_REG,FUNC_REG_SURFIX,domain_str)
        self.logger.debug(all_function_str)
        function_str_list = re.findall(r'\(.*?\)', all_function_str)
        for function_str in function_str_list:
            parts = list()
            new_function = None
            function_str = function_str[1:-1]
            parts = re.split(r'\?[a-z]-', function_str)
            function_name = parts[0]
            new_function = VAR(function_name)
            parts = parts[1:]
            for type_name in parts:
                new_function.content_dict.update({type_name:[]})
            functions.update({function_name:new_function})
        self.logger.debug(functions)
        
        # extract actions
        action_schemas: typing.Dict[str,ActionSchema] = {}
        pattern = r"\(:action.*?(?=\(:action|$)"
        action_str_list = re.findall(pattern, domain_str)
        for action_str in action_str_list:
            self.logger.debug(action_str)
            action_content_str,_ = self.keyWordParser("action",ACTION_REG_PREFIX,ACTION_REG,ACTION_REG_SURFIX,action_str)
            self.logger.debug(action_content_str)
            temp_list = action_content_str.split(LINE_BREAK)
            action_name = temp_list[0]
            self.logger.debug(action_name)
            action_content_str = temp_list[1]
            
            # find parameter string
            self.logger.debug(action_content_str)
            parameter_str,action_content_str = self.keyWordParser("parameters",PARAMETERS_REG_PREFIX,PARAMETERS_REG,PARAMETERS_REG_SURFIX,action_content_str)
            self.logger.debug(parameter_str)
            self.logger.debug(action_content_str)
            
            # extract parameter
            pattern = r'\?\w*'
            match_variables = re.findall(pattern, parameter_str)
            pattern = r'\?[a-z]-(\w+)'
            match_types = re.findall(pattern, parameter_str)
            if not len(match_variables) == len(match_types):
                raise ValueError('missing variable or types in parameter [%s] for action [%s]',parameter_str,action_name)
            parameters = Parameters()
            for i in range(len(match_types)):
                parameters[match_variables[i]] = match_types[i]
            self.logger.debug(parameters)
            print(action_content_str)
            
            # find effect first, which is easier for the re
            # extract effects
            effects_str,len_holder = self.keyWordParser("effect",EFFECT_REG_PREFIX,EFFECT_REG,EFFECT_REG_SURFIX,action_content_str)
            # take the len of the len_holder, which is the string with pre and effect removing the length of the whole effect
            # the precondition comes before the effect, so we keep the first len(len_holder) from the old string
            # which is effectively the precondition string
            action_content_str = action_content_str[:len(len_holder)]            
            # since there are uncertain nesting level of brackets in the effect
            # using manual approach instead of regular expression
            effects : typing.List[Effect] = []
            effects_str = effects_str[1:-1] # remove the first and last bracket
            for effect_str in effects_str.split(")("):

                effects.append(self.parsingEffect(effect_str,action_name))
            
            # TODO I need to apply the action and check goal at the same time.
            
            # extract precondition
            preconditions = []
            # find precondition string
            precondition_str, remaining_str = self.keyWordParser("precondition",PRECONDITION_REG_PREFIX,PRECONDITION_REG,PRECONDITION_REG_SURFIX,action_content_str)
            if not remaining_str == "":
                raise ValueError("The remaining string [%s] after action parsing is not empty",remaining_str)
            
            
            # TODO
            # match the preconditions
            
            
            new_action = ActionSchema(action_name,parameters,preconditions,effects)
            action_schemas.update({action_name:new_action})
        self.logger.debug(action_schemas)
        
        return domain_name,types,functions,action_schemas
            # self.logger.debug("extract actions")
            # try:
            #     action_list = str.split("(:action ")[1::]

            #     for action_str in action_list:
            #         parameters = []
            #         preconditions = {}
            #         effects = []
            #         action_str = action_str[:-1:]
            #         action_name = action_str.split(" ")[0]
                    
            #         # decode parameters
            #         parameters_str = re.search(':parameters\(.*\):precondition',action_str).group()
            #         self.logger.debug('parameters_str: [%s]',parameters_str)
            #         for p_str in parameters_str[12:-14:].split(","):
            #             if p_str == '':
            #                 continue
            #             self.logger.debug('single parameters_str: [%s]',p_str)
            #             p_str = p_str.replace(" ","")
            #             p = p_str.split("-")
            #             parameters.append((p[0],p[1]))
            #         self.logger.debug('parameters: [%s]',parameters)
                    
            #         self.logger.debug("extract preconditions")
            #         try:
                        
            #             preconditions_str = re.search(':precondition\(and.*\):effect', action_str).group()
            #             preconditions_str = preconditions_str[18:-9:]
            #             self.logger.debug(preconditions_str)
            #             # preconditions_str = preconditions_str[len(goal_str_prefix)+1:-len(goal_str_suffix)-1]
            #             predicator_list = preconditions_str.split(")(")
            #             self.logger.debug("precondition list: %s" % (predicator_list))
            #             preconditions = self.predicator_convertor(predicator_list)

            #         except AttributeError:
                        
            #             self.logger.error("error when extract precondition")
            #             self.logger.error(traceback.format_exc())
            #             traceback.print_exc()
            #             exit() 
                    
            #         #decode effects
            #         effects_str = re.search(':effect\(and\(.*\)\)',action_str).group()
            #         self.logger.debug('effects_str: [%s]',effects_str)  
            #         for e_str in effects_str[11:-2:].split("(= "):
            #             if e_str == '':
            #                 continue
            #             self.logger.debug('single effect_str: [%s]',e_str)
            #             e_list = e_str[1:].split(") ")
            #             # if len(e_list) == 1:
            #             #     e_list = e_list[0].split(" ")
            #             effects.append((e_list[0].replace(" ?","?").replace(" ","-").replace("(","").replace(")",""),e_list[1].replace(" ","").replace("(","").replace(")","").replace('"','').replace("'",'')))
            #         self.logger.debug('effects: [%s]',effects)
                    
            #         actions.update({action_name: {"parameters":parameters,"precondition":preconditions,"effect":effects}})
            #     self.logger.debug(actions)
            # except AttributeError:
            #     self.logger.error("error when extract actions")
            #     self.logger.error(traceback.format_exc())
            #     exit()          
            # return actions,d_name



    def parsingEffect(self,effect_str,action_name):
        

        effect_type = None
        effect_inner_effect = None
        effect_condition = None
        
        new_effect = Effect()
        if effect_str.startswith("when"):
            print("when")
            # this is conditional effect, which should be handled later
            
            # determine the effect type for conditional effect
            
            
            # extract effect first as it ensures the only match
            conditional_effect_str, len_holder = self.keyWordParser("Effect in Conditional Effect",EFFECT_CONDITION_REG_PREFIX,EFFECT_CONDITION_REG,EFFECT_CONDITION_REG_SURFIX,effect_str)
            effect_str =effect_str[:len(len_holder)]
            effect_type_str = conditional_effect_str.split(" ")[0]
            print(effect_type_str)
            conditional_effect_str = conditional_effect_str[len(effect_type_str)+1:]
            target_variable_name, jp_str = self.keyWordParser("Variable in Conditional Effect","\(","\w*\??\w*","\) ",conditional_effect_str)
            
            print(target_variable_name)
            print(jp_str)
            
            # effect_inner_effect = self.parsingEffect()
        else:
            print(effect_str)
            
            # if effect_str.startswith("increase"):
            #     effect_type = EffectType.INCREASE
            # elif effect_str.startswith("decrease"):
            #     effect_type = EffectType.DECREASE
            # elif effect_str.startswith("assign"):
            #     effect_type = EffectType.ASSIGN
            effect_content_list = effect_str.split(" ")
            if not len(effect_content_list) == 3:
                raise ValueError("Error when parsing effect [%s] for actoin [%s]",effect_str,action_name)
           
           
            effect_type_str = effect_content_list[0]
            target_variable_name = effect_content_list[1][1:-1]
            
            if not effect_type_str in EFFECT_TYPE_DICT.keys():
                raise ValueError("Error effect [%s] for action [%s] is not a valid effect from: [%s]",effect_str,action_name,EFFECT_TYPE_DICT.keys())
            update_str = effect_content_list[2]
            update_is_variable = False
            pattern = r'^\(\w*\??\w*\)$'
            print(repr(update_str))
            if re.match(pattern, update_str):
                # then this is a variable too
                update_is_variable = True
                update = update_str[1:-1]
                print("udpdate is a variable")
            else:
                # then it is not a variable
                # so it is either a enum in the format of a string
                # or it is an integer
                int_pattern = r'^[+-]?\d+$'
                string_pattern = r"^(['\"])(.*)\1$"
                if re.match(int_pattern, update_str):
                    # then it is an integer
                    update = int(update_str)
                elif re.match(string_pattern, update_str):
                    update = update_str[1:-1]
                else:
                    raise ValueError("The effect update is neither integer or a string")
            new_effect.update_is_variable = update_is_variable
            new_effect.update = update
            
            
        effect_type = EFFECT_TYPE_DICT[effect_type_str]
        new_effect.target_variable_name = target_variable_name
        new_effect.effect_type = effect_type
        return new_effect



    # assuming the input is one epistemic string
    # def epistemic_decoder(self,ep_str):
    #     self.logger.debug("extract epistemic formulea")
    #     self.logger.debug("input epistemic str: [%s]",ep_str)
    #                     # preconditions["epistemic_p"] = list()
    #     p,q = re.search('\(= \(:epistemic [\?+\- 0-9a-z_\[\],]*\((?:>|<|=|>=|<=)+ \([ 0-9a-z_\? ]*\) (?:[0-9a-z_\'\"-]+|\([0-9a-z_ ]+\))\)\) [0-9a-z-]*\)',ep_str).span()
    #     epistemic_prefix = "(= (:epistemic "
    #     epistemic_surfix = ")"
        
    #     ep_str = ep_str[p+len(epistemic_prefix):q+len(epistemic_surfix)]
    #     self.logger.debug(ep_str)
    #     import sys
    #     sys.exit()
    
    
    def predicator_convertor(self,pred_list):
        result = dict()
        result["ontic"] = list()
        result["epistemic"] = list()
        
        for pred_str in pred_list:
            self.logger.debug(pred_str)
            self.logger.debug(ONTIC_STR_PREFIX)
            #  this is for precondition, it is also fine with the goal for now
            key = pred_str.replace(' ?',"?")
            if ONTIC_STR_PREFIX[1:] in pred_str:
                # this is an ontic predictor
                
                self.logger.debug(pred_str)
                
                
                
                
                pred_str = pred_str[len(ONTIC_STR_PREFIX)+1:-1]
                self.logger.debug(pred_str)
                self.logger.debug(pred_str)
                pre_comp_list = pred_str.split(" ")
                symbol  = pre_comp_list[0]
                # value = goal_str_list[-1]
                pred_str = pred_str[(len(symbol)+2):]
                self.logger.debug(pred_str)
                
                # self.logger.debug(goal_str)
                temp_list = pred_str.split(')')
                old_variable = temp_list[0]
                variable = old_variable.replace(' ?','?').replace(' ','-')
                key = key.replace(old_variable,variable)
                self.logger.debug(temp_list)
                if len(temp_list)==2:
                    value = temp_list[1][1:]
                    if "'" in value:
                        value = value.replace("'","")
                    elif '"' in value:
                        value = value.replace('"',"")
                    else:
                        value =int(value)      
                elif len(temp_list)==3:
                    # it means the second argument is also a variable
                    value = temp_list[1][2:].replace(' ?','?').replace(' ','-')
                else:
                    raise ValueError("error in decoding ontic [%s]",key)
                self.logger.debug("ontic: [%s]",(key,symbol,variable,value))

                result["ontic"].append((key,symbol,variable,value))
            elif EPISTEMIC_STR_PREFIX[1:] in pred_str:
                # this is an epistemic predictor
                
                self.logger.debug(pred_str)
                
                # this is for precondition, it is also fine with the goal for now
                
                
                query_str = key[len(EPISTEMIC_STR_PREFIX):]
                self.logger.debug("query string: [%s]",query_str)
                separator_index = query_str.index("(")
                query_prefix = query_str[:separator_index]
                self.logger.debug("query prefix [%s]" % (query_prefix))
                query_suffix_str = query_str[separator_index:]
                self.logger.debug("query suffix [%s]" % (query_suffix_str))                
                # pre_comp_list = pred_str.split("(")
                
                symbol  = query_suffix_str[1:].split(" ")[0]
                # pre_comp_list[0]
                # value = goal_str_list[-1]
                query_suffix_str = query_suffix_str[(len(symbol)+3):]
                self.logger.debug(query_suffix_str)
                
                # self.logger.debug(goal_str)
                temp_list = query_suffix_str.split(')')
                old_variable = temp_list[0]
                variable = old_variable.replace(' ?','?').replace(' ','-')
                key = key.replace(old_variable,variable)
                query_str = query_str.replace(old_variable,variable)
                if len(temp_list)==2:
                    value = temp_list[1][1:]
                    if "'" in value:
                        value = value.replace("'","")
                    elif '"' in value:
                        value = value.replace('"',"")
                    else:
                        value =int(value)      
                elif len(temp_list)==3:
                    # it means the second argument is also a variable
                    value = temp_list[1][2:].replace(' ?','?').replace(' ','-')
                else:
                    raise ValueError("error in decoding epistemic [%s]",key)
                self.logger.debug("epistemic:(%s,%s,%s,%s,%s,%s)" % (key,query_str,query_prefix,symbol,variable,value))

                result["epistemic"].append((key,query_str,query_prefix,symbol,variable,value))
            elif pred_str == "":
                pass
            else:
                raise ValueError("[predicate type not found] error in decoding [%s]",key)
        
        return result
                

    # def epistemic_converter(self,ep_content):
    #     self.logger.debug("epistemic converter: [%s]",ep_content)
    #     header_index = ep_content.find(" ")
    #     header_str =  ep_content[1:header_index]
    #     self.logger.debug("header string: [%s]",header_str)
    #     ep_content = ep_content[:header_index]
    #     agent_index = ep_content.find(" ")
    #     agents_str = ep_content[2:agent_index-1]

    #     ep = EpistemicQuery(header_str,agents_str,value,content)

    #     ep_value = 
    #     self.logger.debug(epistemic_pre_list)
    #                     for pre_str in epistemic_pre_list:
    
    #                         key = pre_str.replace(' ?',"?")
    #                         self.logger.debug(pre_str)
    #                         pre_str = pre_str[len(epistemic_prefix):-len(epistemic_surfix):]
    #                         self.logger.debug(pre_str)
    #                         pre_str_list = pre_str.split(" ")
    #                         # symbol  = goal_str_list[0]
    #                         value = pre_str_list[-1]
    #                         pre_str = pre_str[:-(len(value)+2):]
    #                         value = int(value)
    #                         query = pre_str
    #                         self.logger.debug(pre_str)
                            
    #                         # i,j = re.search('\)\) .*',goal_str).span()
    #                         # value1 = int(goal_str[i+3:j:])
                            
    #                         p,q = re.search('(?:>|<|=|>=|<=)+ \([ 0-9a-z_\? ]*\) (?:[0-9a-z_\'\"-]+|\([0-9a-z_ ]+\))\)',pre_str).span()
    #                         # query = pre_str[:p-1]
    #                         pre_str = pre_str[p:q-1]
                            
                            
    #                         pre_str_list = pre_str.split(' ')
    #                         symbol = pre_str_list[0]
    #                         pre_str = pre_str[(len(symbol)+2)::]
    #                         pre_str_list = pre_str.split(') ')
    #                         old_variable = pre_str_list[0]
    #                         variable = pre_str_list[0].replace(' ?','?').replace(' ','-')
    #                         self.logger.debug("old variable string: [%s]",old_variable)
    #                         self.logger.debug("new variable string: [%s]",variable)
    #                         self.logger.debug("query string: [%s]",query)
    #                         query = query.replace(old_variable,variable) 
    #                         self.logger.debug("query string: [%s]",query)
    #                         key = key.replace(old_variable,variable)
    #                         v_value = pre_str_list[1]
    #                         if "'" in v_value:
    #                             v_value = v_value.replace("'","")
    #                         elif '"' in v_value:
    #                             v_value = v_value.replace('"',"")
    #                         elif '?' in v_value:
    #                             v_value = v_value.replace(' ?',"?").replace(')','').replace('(','')
    #                         elif "(" in v_value and ")" in v_value:
    #                             old_v_value = v_value
    #                             v_value = v_value[1:-1]
    #                             v_value = v_value.replace(" ","-")
    #                             query = query.replace(old_v_value,v_value)
                                
                                
    #                         else:
    #                             v_value =int(v_value)
    #                         self.logger.debug("epistemic_p: [%s]",(key,symbol,query,variable,v_value,value))
    #                         preconditions["epistemic_p"].append((key,symbol,query,variable,v_value,value))
    #                 except AttributeError:
                        
    #                     self.logger.error("error when extract precondition")
    #                     self.logger.error(traceback.format_exc())
    #                     traceback.print_exc()
    #                     exit() 


    def problemParser(self,file_path):
        domains = {'agent':{'basic_type':'agent','values':[]},}
        i_state = {}
        g_states = {}
        agent_index = []
        obj_index = []
        variables = {}
        d_name = ""
        p_name = ""
        
        self.logger.debug("reading problem file:")
        
        with open(file_path,"r") as f:
            file = f.read()
            self.logger.debug(repr(file))
            
            self.logger.debug("formating problem file")
            str = self.formatDocument(file)
            self.logger.debug(repr(str))
            
            if not str.startswith("(define"):
                self.logger.error("the problem file does not start with '(define'")
                self.logger.error(traceback.format_exc())
                exit()
            elif not str.endswith(")"):
                self.logger.error("the problem file does not end with ')'")
                self.logger.error(traceback.format_exc())
                exit()
            str = str[7:-1:]
            self.logger.debug(repr(str))
            
            self.logger.debug("extract p_name")
            try:
                found = re.search('\(problem [0-9a-z_]*\)',str).group(0)
                p_name = found[9:-1:]
                self.logger.info(f"parsing problem: [{p_name}]")
                # self.logger.debug(p_name)
            except AttributeError:
                self.logger.error("error when extract problem name")
                self.logger.error(traceback.format_exc())
                exit()
                
            self.logger.debug("extract d_name")
            try:
                found = re.search('\(:domain [0-9a-z_]*\)',str).group(0)
                d_name = found[9:-1:]
                self.logger.debug(d_name)
            except AttributeError:
                self.logger.error("error when extract domain name")
                self.logger.error(traceback.format_exc())
                exit()            

            self.logger.debug("extract agents")
            try:
                found = re.search('\(:agents [0-9a-z_ ]*\)',str).group(0)
                agent_index = found[9:-1:].split(" ")
                self.logger.debug(agent_index)
            except AttributeError:
                self.logger.error("error when extract agents")
                self.logger.error(traceback.format_exc())
                exit()

            self.logger.debug("extract objects")
            try:
                found = re.search('\(:objects [0-9a-z_ ]*\)',str).group(0)
                obj_index = found[10:-1:].split(" ")
                self.logger.debug(obj_index)
            except AttributeError:
                self.logger.error("error when extract objects")
                self.logger.error(traceback.format_exc())
                exit()

            self.logger.debug("extract variables")
            try:
                found = re.search('\(:variables([(][0-9a-z_ \[\],]*[)])*\)',str).group(0)
                self.logger.debug( found)
                vars_list = re.findall('\([0-9a-z_ \[\],]*\)',found[10:-1:])
                self.logger.debug(vars_list)
                for var_str in vars_list:
                    var_str = var_str[1:-1:].split(' ')
                    variable_name = var_str[0]
                    target_entities_list =[] 
                    for entities in var_str[1:]:
                        target_entities_list.append(entities[1:-1:].split(","))
                    variables.update({variable_name:target_entities_list})
                self.logger.debug(variables)
            except AttributeError:
                self.logger.error("error when extract variables")
                self.logger.error(traceback.format_exc())
                exit()
                
            self.logger.debug("extract init")
            try:
                found = re.search("\(:init(\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\))*\)",str).group(0)
                self.logger.debug( found)
                init_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[6:-1:])
                self.logger.debug(init_list)
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
                    
                self.logger.debug(i_state)
            except AttributeError:
                self.logger.error("error when extract init")
                self.logger.error(traceback.format_exc())
                exit()            

            self.logger.debug("extract goal")
            try:
                self.logger.debug(str)
                
                # \(:goal\(and(\(:[a-z]* ((?:\?|\+\-)+ [a-z]* \[[a-z0-9,]*\] )*\((?:>|<|=|>=|<=)+ \([ 0-9a-z_]*\) (?:[0-9a-z_\'\"-]+|\([0-9a-z_ ]+\)))\)\)
                # (\(:[a-z]* ((?:\?|\+|\-) [a-z]* \[[a-z0-9,]*\] )+\((?:>|<|=|>=|<=)+ \([ 0-9a-z_]*\) (?:[0-9a-z_\'\"-]+|\([0-9a-z_ ]+\))\)\))+

                goal_str_prefix = "(:goal(and"
                goal_str_suffix = "))"
                goal_re_str = "\(:goal\(and"+ "(" + BOTH_RE_PREFIX + PREDICATE_RE + ")*" +"\)\)"
                
                found = re.search(goal_re_str,str).group(0)
                self.logger.debug(found)
                found = found[len(goal_str_prefix)+1:-len(goal_str_suffix)-1]
                predicate_list = found.split(")(")
                self.logger.debug(predicate_list)
                g_states = self.predicator_convertor(predicate_list)
                # self.logger.debug(found)
                
                # # loading ontic goals
                # self.logger.debug("extract ontic goal propositions")
                # g_states["ontic_g"] = list()
                # # ontic_goal_list = re.findall('\(= \([0-9a-z_ ]*\) [0-9a-z_\'\"]*\)',found[10:-1:])
                # ontic_goal_list = re.findall(ontic_re_prefix+predicate_re,found[10:-1:])  
                # ontic_prefix = "(:ontic ("
                # ontic_surfix = ")"
                # self.logger.debug('ontic goal list: [%s]',ontic_goal_list)
                # for goal_str in ontic_goal_list:
                #     self.logger.debug(goal_str)
                #     key = goal_str.replace(' ?',"?")
                #     goal_str = goal_str[len(ontic_prefix):-len(ontic_surfix):]
                #     self.logger.debug(goal_str)
                #     goal_str_list = goal_str.split(" ")
                #     symbol  = goal_str_list[0]
                #     value = goal_str_list[-1]
                #     goal_str = goal_str[(len(symbol)+2):-(len(value)+3):]
                #     self.logger.debug(goal_str)
                #     goal_list = goal_str.split(') ')
                #     variable = goal_list[0].replace(' ?','?').replace(' ','-')
                #     v_value = goal_list[1]
                #     if "'" in v_value:
                #         v_value = v_value.replace("'","")
                #     elif '"' in v_value:
                #         v_value = v_value.replace('"',"")
                #     elif '?' in v_value:
                #         v_value = v_value.replace(' ?',"?").replace(')','').replace('(','')
                #     else:
                #         v_value =int(v_value)                            
                    
                #     self.logger.debug("ontic_g: [%s]",(key,symbol,variable,v_value,value))

                #     g_states["ontic_g"].append((key,symbol,variable,v_value,value))
                
                # # loading epismetic goals
                # self.logger.debug("extract epistemic goal propositions")
                # g_states["epistemic_g"] = list()
                # # self.logger.debug("found [%s]",found)
                # # self.logger.debug("found[10:-1:] [%s]",found[10:-1:])
                # # self.logger.debug("found replaced [%s]",found[10:-1:].replace(")-1)",") -1)"))
                # self.logger.debug(found)
                # epistemic_goal_list = re.findall(epistemic_re_prefix+predicate_re,found)  
                # epistemic_prefix = "(= (:epistemic "
                # epistemic_surfix = ")"
                # self.logger.debug(epistemic_goal_list)
                # self.logger.debug(epistemic_goal_list)
                # for goal_str in epistemic_goal_list:
                #     self.logger.debug(goal_str)
                #     self.epistemic_decoder(goal_str)
                    
                #     self.logger.debug("goal string 1: [%s]",goal_str)
                #     key = goal_str.replace(' ?',"?")
                #     goal_str = goal_str[len(epistemic_prefix):-len(epistemic_surfix):]
                #     self.logger.debug("goal string 2: [%s]",goal_str)
                #     goal_str_list = goal_str.split(" ")
                #     # symbol  = goal_str_list[0]
                #     value = goal_str_list[-1]
                #     goal_str = goal_str[:-(len(value)+2):]
                #     value = int(value)
                #     query = goal_str
                #     self.logger.debug("goal string 3: [%s]",goal_str)
                    
                #     # i,j = re.search('\)\) .*',goal_str).span()
                #     # value1 = int(goal_str[i+3:j:])
                    
                #     p,q = re.search('(?:>|<|=|>=|<=)+ \([ 0-9a-z_\? ]*\) (?:[0-9a-z_\'\"-]+|\([0-9a-z_ ]+\))\)',goal_str).span()
                #     # query = goal_str[:p-1]
                #     goal_str = goal_str[p:q-1]
                #     self.logger.debug("goal string 4: [%s]",goal_str)
                    
                    
                #     goal_list = goal_str.split(' ')
                #     symbol = goal_list[0]
                #     goal_str = goal_str[(len(symbol)+2)::]
                #     goal_list = goal_str.split(') ')
                #     old_variable = goal_list[0]
                #     variable = goal_list[0].replace(' ?','?').replace(' ','-')
                #     self.logger.debug("old variable string: [%s]",old_variable)
                #     self.logger.debug("new variable string: [%s]",variable)
                #     self.logger.debug("query string: [%s]",query)
                #     query = query.replace(old_variable,variable) 
                #     self.logger.debug("query string: [%s]",query)
                #     key = key.replace(old_variable,variable)
                #     v_value = goal_list[1]
                #     if "'" in v_value:
                #         v_value = v_value.replace("'","")
                #     elif '"' in v_value:
                #         v_value = v_value.replace('"',"")
                #     elif '?' in v_value:
                #         v_value = v_value.replace(' ?',"?").replace(')','').replace('(','')
                #     elif "(" in v_value and ")" in v_value:
                        
                #         v_value = v_value[1:-1]
                #         old_v_value = v_value
                #         v_value = v_value.replace(" ","-")
                #         query = query.replace(old_v_value,v_value)
                #     else:
                #         v_value =int(v_value)

                #     self.logger.debug("epistemic_p: [%s]",(key,symbol,query,variable,v_value,value))
                #     g_states["epistemic_g"].append((key,symbol,query,variable,v_value,value))

                    
                self.logger.debug(g_states)
            except AttributeError:
                self.logger.error("error when extract goal")
                self.logger.error(traceback.format_exc())
                traceback.print_exc()
                exit()   
                            
            self.logger.debug("extract domains")
            try:
                self.logger.debug(str)
                
                found = re.search('\(:domains(\([0-9a-z_ \[\],\'\"]*\))*\)',str).group(0)
                self.logger.debug( found)
                domains_list = re.findall('\([0-9a-z_ \[\],\'\"]*\)',found[9:-1:])
                self.logger.debug(domains_list)
                for domain_str in domains_list:
                    domain_str = domain_str[1:-1:].split(' ')
                    if not domain_str[1] in ['enumerate','integer','string']:
                        self.logger.error(f"domain {domain_str[0]}'s basic_type {domain_str[1]} does not exist")
                        assert(f"domain {domain_str[0]}'s basic_type {domain_str[1]} does not exist")
                    else:
                        if "'" in domain_str[2]:
                            value = domain_str[2].replace("'","")[1:-1:].split(",")
                        elif '"' in domain_str[2]:
                            value = domain_str[2].replace('"',"")[1:-1:].split(",")
                        else:
                            value = [ int(i) for i in domain_str[2][1:-1:].split(",")]
                        domains.update({domain_str[0]:{"basic_type":domain_str[1],"values":value}})
                self.logger.debug(domains)
            except AttributeError:
                
                self.logger.error("error when extract domains")
                self.logger.error(traceback.format_exc())
                exit()
                
            return domains,i_state,g_states,agent_index,obj_index,variables,d_name,p_name



    def formatDocument(self,input_str):
        # this should remove all the comments
            # . match anything but the endline
            # * match 0 or more preceding RE
            # $ matchs end line
        input_str = re.sub(';.*$',"",input_str,flags=re.MULTILINE).lower()
        self.logger.debug(repr(input_str))
        
        # removing useless space
        # ^ match any start of the newline in multiline mode
        input_str = re.sub('^ *| *$|^\n',"",input_str,flags=re.MULTILINE)
        input_str = re.sub(' *, *',",",input_str,flags=re.MULTILINE)
        input_str = re.sub(' *- *',"-",input_str,flags=re.MULTILINE)
        input_str = re.sub('\[ *',"[",input_str,flags=re.MULTILINE)
        input_str = re.sub(' *\]',"]",input_str,flags=re.MULTILINE)
        input_str = re.sub(':goal *',":goal",input_str,flags=re.MULTILINE)
        input_str = re.sub(':action *',":action ",input_str,flags=re.MULTILINE)
        input_str = re.sub(':parameters *',":parameters",input_str,flags=re.MULTILINE)
        input_str = re.sub(':precondition *',":precondition",input_str,flags=re.MULTILINE)
        input_str = re.sub(':effect *',":effect",input_str,flags=re.MULTILINE)
        input_str = re.sub(' \?',"?",input_str,flags=re.MULTILINE)
        self.logger.debug(repr(input_str))
        
        # removing useless \n
        input_str = re.sub('\( *|(\n)*\((\n)*',"(",input_str,flags=re.MULTILINE)
        input_str = re.sub(' *\)|(\n)*\)(\n)*',")",input_str,flags=re.MULTILINE)
        input_str = re.sub('\)\n',")",input_str,flags=re.MULTILINE)
        self.logger.debug(repr(input_str))
        
        input_str = re.sub('\n',LINE_BREAK,input_str,flags=re.MULTILINE)
        self.logger.debug(repr(input_str)) 
        return input_str      
    
