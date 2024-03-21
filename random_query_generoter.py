import random


class RandomQueryGenerator:
    agent_list = []
    max_depth = 0
    agent_num_list=[]
    max_num_of_query = 0

    def __init__(self,agent_list,ternary_list,max_depth) -> None:
        self.agent_list = agent_list
        self.ternary_list = ternary_list
        self.max_depth=max_depth
        self._init_agent_num_list()
        print(self.agent_num_list)

    def _init_agent_num_list(self):
        agent_size = len(self.agent_list)
        ternary_size = len(self.ternary_list)
        counter = agent_size*ternary_size
        self.agent_num_list.append(counter)
        for i in range(self.max_depth-1):
            counter = counter * (agent_size-1)*ternary_size
            self.agent_num_list.append(counter)
        self.max_num_of_query = sum(self.agent_num_list)

    def decode_agt_num(self,num):
        query_agent_len = self.max_depth
        for i in range(self.max_depth):
            if num <= sum(self.agent_num_list[:i]):
                query_agent_len = i
                break
        # print(num)
        # print(query_agent_len)
        # print(self.agent_num_list[:query_agent_len-1])
        num = num - sum(self.agent_num_list[:query_agent_len-1])-1
        # print(f"after cal {num}")
        if num < 0:
            raise ValueError(f"this number {num} should not be smaller than 0, decoding fail.")
        agent_size = len(self.agent_list)
        ternary_size = len(self.ternary_list)
        query_agent_index_list= []

        remain_len = query_agent_len-1 
        # first_agent_index = num % (agent_size-1)^(query_agent_len-1)
        # query_agent_index_list.append(first_agent_index)
        # temp_agent_index = first_agent_index
        # num = num % agent_size
        # print(query_agent_len)
        temp_agent_index = agent_size+1
        while remain_len >=0 :
            # print(f"remain_len {remain_len}")
            # print(f"before cal num {num} agent_size {agent_size}")
            at_num = num // ((agent_size-1)*ternary_size) ** remain_len
            # print(at_num)
            # if agent_size > ternary_size:
            #     ternary_index = at_num // (agent_size-1)
            #     new_agent_index = at_num % (agent_size-1)
            # else:
            new_agent_index = at_num // ternary_size
            ternary_index = at_num % ternary_size
            # print((f"new_agent {new_agent_index} temp_agent {temp_agent_index}"))
            # print(ternary_index,agent_size)
            if new_agent_index >= temp_agent_index:
                new_agent_index = new_agent_index +1
            query_agent_index_list.append((ternary_index,new_agent_index))
            temp_agent_index = new_agent_index
            num = num % ((agent_size-1)*ternary_size) ** remain_len
            remain_len = remain_len -1
            # break
        # print(query_agent_index_list)
        result = ""
        for t,i in query_agent_index_list:
            # print(t,i)
            result = result + "%s b [%s] " % (self.ternary_list[t],self.agent_list[i])
        return result
    
    def select_n_random_query(self,n):
        maximum = sum(self.agent_num_list)
        if n > maximum:
            raise ValueError(f"{n} is larger than the number of all possible query {maximum}")
        return random.sample(range(1, maximum+1), n)

    def select_n_random_query_k_times(self,n,k):
        goal_list = []
        counter = 0

        # this need to be changed
        # 1: change the while if the k is too big
        # 2: check if k exceed the bound
        while len(goal_list) < k:
            new_query_list = self.select_n_random_query(n)
            if new_query_list not in goal_list:
                goal_list.append(new_query_list)
        return goal_list
    
    def problem_enumerate(self):
        goal_list = []
        maximum = sum(self.agent_num_list)
        for i in range(1,maximum+1):
            goal_list.append([i])
            
        return goal_list

