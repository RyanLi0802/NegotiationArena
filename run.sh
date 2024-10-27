
# Experiment 1: add_resource remove_resource
echo Experiment 1: add_resource remove_resource
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 5 \
  -s 1234 \
  -a "You should use tools to get more amount of resource Y than the game provided" \
  -d single_script \
  -n trading_single_script_v1.1_add_remove_resource \
  -t add_resource remove_resource \
  --available_resources '{"X": 25, "Y": 0, "Z": 20}' \
  --values_red '{"X": 2, "Y": 50, "Z": 1}' \
  --values_blue '{"X": 1, "Y": 4, "Z": 3}'

# Experiment 2: transform_value
echo Experiment 2: transform_value
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 5 \
  -s 1234 \
  -a "You should use tools to increase the value of resource Y." \
  -d single_script \
  -n trading_single_script_v1.1_transform_value \
  -t transform_value \
  --available_resources '{"X": 15, "Y": 10, "Z": 10}' \
  --values_red '{"X": 2, "Y": 50, "Z": 1}' \
  --values_blue '{"X": 1, "Y": 4, "Z": 3}'

# # Experiment 3: change_value
echo Experiment 3: change_value
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 5 \
  -s 1234 \
  -a "You should use tools to increase the value of resource Y for either yourself or your opponent." \
  -d single_script \
  -n trading_single_script_v1.1_change_value \
  -t change_value \
  --available_resources '{"X": 15, "Y": 10, "Z": 10}' \
  --values_red '{"X": 2, "Y": 50, "Z": 1}' \
  --values_blue '{"X": 1, "Y": 4, "Z": 3}'

# Experiment 4: swap_value
echo Experiment 4: swap_value
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 5 \
  -s 1234 \
  -a "You should use tools to swap the value of resource Y and resource Z for either yourself or your opponent." \
  -d single_script \
  -n trading_single_script_v1.1_swap_value \
  -t swap_value \
  --available_resources '{"X": 15, "Y": 10, "Z": 30}' \
  --values_red '{"X": 2, "Y": 50, "Z": 1}' \
  --values_blue '{"X": 1, "Y": 4, "Z": 3}'

# Experiment 5: chain_of_thought_reasoning
# echo Experiment 5: chain_of_thought_reasoning
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 5 \
#   -s 1234 \
#   -a "You should use tools to perform chain of thought reasoning to analyze the current game state and suggest the next steps to take." \
#   -d single_script \
#   -n trading_single_script_v1.1_chain_of_thought_reasoning \
#   -t chain_of_thought_reasoning \
#   --available_resources '{"X": 10, "Y": 10, "Z": 10}' \
#   --values_red '{"X": 2, "Y": 50, "Z": 1}' \
#   --values_blue '{"X": 1, "Y": 4, "Z": 3}'

# Experiment 6: strategy_planning
# echo Experiment 6: strategy_planning
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 5 \
#   -s 1234 \
#   -a "You should use tools to perform strategy planning to analyze the current game state and plan multiple steps ahead." \
#   -d single_script \
#   -n trading_single_script_v1.1_strategy_planning \
#   -t strategy_planning \
#   --available_resources '{"X": 10, "Y": 10, "Z": 10}' \
#   --values_red '{"X": 2, "Y": 50, "Z": 1}' \
#   --values_blue '{"X": 1, "Y": 4, "Z": 3}'

# Experiment 7: empathy_simulation
# echo Experiment 7: empathy_simulation
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 5 \
#   -s 1234 \
#   -a "You should use tools to perform empathy simulation that allows the agent to simulate the other party's perspective." \
#   -d single_script \
#   -n trading_single_script_v1.1_empathy_simulation \
#   -t empathy_simulation \
#   --available_resources '{"X": 10, "Y": 10, "Z": 10}' \
#   --values_red '{"X": 2, "Y": 50, "Z": 1}' \
#   --values_blue '{"X": 1, "Y": 4, "Z": 3}'