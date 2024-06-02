from utils.random_query_generoter import RandomQueryGenerator

rqg = RandomQueryGenerator(['a','b','c'],5)
print(rqg.agent_num_list)
print(rqg.max_num_of_query)


random_goal_list = rqg.select_n_random_query_k_times(3,3)
print(random_goal_list)

# for goal_list in random_goal_list:
#     for goal_num in goal_list:
#         print(rqg.decode_agt_num(goal_num))
#     print(" ")

# for i in range(1,22):
#     print(rqg.decode_agt_num(i))