# bpwp

# package required
```
pip install scipy scikit-learn
```

The experiment is run by the command:
```bash
python experiment_runner.py -s forward_search/fbfsdc.py -i .\examples\GROUP_CONFIG_NUM
python .\experiment_runner.py -s .\forward_search\fbfsdc.py -i .\examples\GROUP_CONFIG_BBL
python .\experiment_runner.py -s .\forward_search\fbfsdc.py -i .\examples\GROUP_CONFIG_GRAPEVINE
```

One instance can be run by this command:
```bash
python .\instance_runner.py -s .\forward_search\fbfsdc.py -e .\examples\group_number\group_number.py -d .\examples\group_number\domain.pddl -p .\examples\group_number\problem07.pddl
```


```
python server_runner.py -t 1200 -m 8 -o output -s search_algorithms/bfsdc.py -d experiments/bbl/domain.pddl --goal_size 1 --goal_depth 1 -a 2 -i init_a2_00000  --goal_index 0
```


# pjp
The experiment running command,
For number(problem101,103,201,202,204,301,401,501):
```
python .\instance_runner.py -s .\search_algorithms\bfs.py -e .\new_syntax\number_float\number01.py -d .\new_syntax\number_float\domain01.pddl -p .\new_syntax\number_float\proble101.pddl 
```
For grapevine(problem100,101,200,202,301,302):
```
python .\instance_runner.py -s .\search_algorithms\bfs.py -e .\new_syntax\grapevine_float\grapevine01.py -d .\new_syntax\grapevine_float\domain01.pddl -p .\new_syntax\grapevine_float\problem100.pddl
```

The test plan_action is validated by the command:
```bash
python .\instance_runner.py -s .\search_algorithms\bfs.py -e .\new_syntax\grapevine\grapevine01.py -d .\new_syntax\grapevine\domain02.pddl -p .\new_syntax\grapevine\problem303.pddl --plan_actions "sharing_own_secret a sa, quiet sa,sharing_own_secret a sa, quiet sa, move_right a, sharing_own_secret a sa, quiet sa,sharing_own_secret a sa, quiet sa, move_right c, lying_others_secret c sa, quiet sa"
```
```
python .\instance_runner.py -s .\search_algorithms\bfs.py -e .\new_syntax\grapevine\grapevine02.py -d .\new_syntax\grapevine\domain02.pddl -p .\new_syntax\grapevine\problem303.pddl --plan_actions "sharing_own_secret a sa, quiet sa,sharing_own_secret a sa, quiet sa, move_right a, sharing_own_secret a sa, quiet sa,sharing_own_secret a sa, quiet sa, move_right c, lying_others_secret c sa, quiet sa"
```
```
python .\instance_runner.py -s .\search_algorithms\bfs.py -e .\new_syntax\grapevine\grapevine03.py -d .\new_syntax\grapevine\domain02.pddl -p .\new_syntax\grapevine\problem303.pddl --plan_actions "sharing_own_secret a sa, quiet sa,sharing_own_secret a sa, quiet sa, move_right a, sharing_own_secret a sa, quiet sa,sharing_own_secret a sa, quiet sa, move_right c, lying_others_secret c sa, quiet sa"
```




