

import epistemic_model
import logging

logger = logging.getLogger("util")

def displayEQuery(epistemic_query: epistemic_model.EpistemicQuery):
    
    logger.debug("display eq")
    first_char = ''
    second_char = ''
    if type(epistemic_query) == str:
        return epistemic_query
    
    if len(epistemic_query.q_group):
        first_char = ''
    elif epistemic_query.q_type == epistemic_model.Q_TYPE.MUTUAL:
        first_char = 'E'
    elif epistemic_query.q_type == epistemic_model.Q_TYPE.DISTRIBUTION:
        first_char = 'D'
    elif epistemic_query.q_type == epistemic_model.Q_TYPE.COMMON:
        first_char = 'C'
    else:
        logger.error(f'Unexpected query type: {epistemic_query}')
    

    if epistemic_query.eq_type == epistemic_model.EQ_TYPE.SEEING:
        second_char = 'S'
    elif epistemic_query.eq_type == epistemic_model.EQ_TYPE.KNOWLEDGE:
        second_char = 'K'
    elif epistemic_query.eq_type == epistemic_model.EQ_TYPE.BELIEF:
        second_char = 'B'
    else:
        logger.error(f'Unexpected e_query type: {epistemic_query}')
    
    return f"{first_char}{second_char} {epistemic_query.q_group} {displayEQuery(epistemic_query.q_content)}"
    

def load_pddl():
    return