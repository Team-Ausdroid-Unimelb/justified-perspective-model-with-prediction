from math import comb
import os
import yaml

def rank_to_combination(rank, k, n):
    """Convert a lexicographic rank to its combination."""
    # choosing k items from a list of n items
    combination = []
    x = rank
    remaining = k
    for i in range(n):
        if remaining == 0:
            break
        if comb(n - i - 1, remaining - 1) <= x:
            x -= comb(n - i - 1, remaining - 1)
        else:
            combination.append(i)
            remaining -= 1
    return combination


def write_one_problems(problem_template,pddl_goal_list,init_list,problem_name,domain_name,problem_path):


    output_str = problem_template.problem_prefix1
    output_str = output_str + problem_name.replace(domain_name,'')
    output_str = output_str + problem_template.problem_prefix2
    output_str = output_str + problem_template.init_pre_fix
    for init_items in init_list:
        if len(init_items) == 2:
            output_str += f"        (assign {init_items[0]} {init_items[1]})\n"
        else:
            raise ValueError("init_items length is not 2")
    output_str += problem_template.init_surfix
    output_str = output_str + problem_template.problem_goal_prefix
    for goal_str in pddl_goal_list:
        output_str=output_str + "          " + goal_str +"\n"
    output_str=output_str + problem_template.problem_goal_surfix
    output_str=output_str + problem_template.problem_surfix
    with open(os.path.join(problem_path),"w") as f:
        f.write(output_str)
        
        
    import yaml

def load_yaml_file(file_path):
    """
    Load a YAML file from the given path.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Contents of the YAML file as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
