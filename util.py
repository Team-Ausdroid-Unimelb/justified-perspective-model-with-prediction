


import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, handler, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def setup_log_handler(log_path):
    handler = logging.FileHandler(log_path)        
    handler.setFormatter(formatter)
    return handler

instance_handler = None

# LOGGER_NAME = "util"
# logger = setup_logger(LOGGER_NAME,instance_handler,logging.INFO) 

# from epistemic_model import EpistemicQuery,Q_TYPE,EQ_TYPE
# def displayEQuery(epistemic_query: EpistemicQuery):
    
#     logger.debug("display eq")
#     first_char = ''
#     second_char = ''
#     if type(epistemic_query) == str:
#         return epistemic_query
    
#     if len(epistemic_query.q_group):
#         first_char = ''
#     elif epistemic_query.q_type == Q_TYPE.MUTUAL:
#         first_char = 'E'
#     elif epistemic_query.q_type == Q_TYPE.DISTRIBUTION:
#         first_char = 'D'
#     elif epistemic_query.q_type == Q_TYPE.COMMON:
#         first_char = 'C'
#     else:
#         logger.error(f'Unexpected query type: {epistemic_query}')
    

#     if epistemic_query.eq_type == EQ_TYPE.SEEING:
#         second_char = 'S'
#     elif epistemic_query.eq_type == EQ_TYPE.KNOWLEDGE:
#         second_char = 'K'
#     elif epistemic_query.eq_type == EQ_TYPE.BELIEF:
#         second_char = 'B'
#     else:
#         logger.error(f'Unexpected e_query type: {epistemic_query}')
    
#     return f"{first_char}{second_char} {epistemic_query.q_group} {displayEQuery(epistemic_query.q_content)}"
    
