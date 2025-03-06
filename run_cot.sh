# Experiment
# echo Experiment: CoT + Counter Offer Reasoning without Logging
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure to first use the chain of thought tool to perform structured reasoning for negotiation decisions, then use the propose counter offer tool to perform structured reasoning for proposing counter offer when you do not accpet the offer proposed by your opponent. **Do NOT accept a trade without using these two tools**" \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1_cot_propose_new_trade_no_log \
#   -t chain_of_thought propose_counter_offer \
#   --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
#   --values_red '{"X": 15, "Y": 10, "Z": 12}' \
#   --values_blue '{"X": 12, "Y": 4, "Z": 10}' \
#   # --log_secret

echo Experiment: CoT + Counter Offer
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 20 \
  -s 1234 \
  -a "Be sure to first use the chain of thought tool to perform structured reasoning for negotiation decisions, then use the propose counter offer tool to perform structured reasoning for proposing counter offer when you do not accpet the offer proposed by your opponent. **Do NOT accept a trade without using these two tools**" \
  -d double_script \
  -n gpt-4o_trading_double_script_v1.1_cot_propose_new_trade \
  -t chain_of_thought propose_counter_offer \
  --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
  --values_red '{"X": 15, "Y": 10, "Z": 12}' \
  --values_blue '{"X": 12, "Y": 4, "Z": 10}' \


# echo Experiment: Counter Offer Reasoning
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure to use the propose counter offer tool to perform structured reasoning for proposing counter offer when you do not accpet the offer proposed by your opponent." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1_propose_new_trade \
#   -t propose_counter_offer \
#   --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
#   --values_red '{"X": 15, "Y": 10, "Z": 12}' \
#   --values_blue '{"X": 12, "Y": 4, "Z": 10}' \
#   --log_secret

# echo Experiment: Counter Offer
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure to use the propose counter offer tool to perform structured reasoning for proposing counter offer when you do not accpet the offer proposed by your opponent." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_v1.1_propose_new_trade \
#   -t propose_counter_offer \
#   --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
#   --values_red '{"X": 15, "Y": 10, "Z": 12}' \
#   --values_blue '{"X": 12, "Y": 4, "Z": 10}' \

# echo Experiment: Chain of Thought logging Reasoning
# echo Experiment: Chain of Thought with Logging
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure to use the chain of thought tool to perform structured reasoning for negotiation decisions. **Do NOT accept a trade without performing chain of thought reasoning**." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1_chain_of_thought \
#   -t chain_of_thought_chain_of_thought_with_log \
#   -t chain_of_thought \
#   --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
#   --values_red '{"X": 15, "Y": 10, "Z": 12}' \
#   --values_blue '{"X": 12, "Y": 4, "Z": 10}' \
#   --log_secret

# echo Experiment: Chain of Thought
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure to use the chain of thought tool to perform structured reasoning for negotiation decisions. **Do NOT accept a trade without performing chain of thought reasoning**." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_v1.1_chain_of_thought \
#   -t chain_of_thought \
#   --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
#   --values_red '{"X": 15, "Y": 10, "Z": 12}' \
#   --values_blue '{"X": 12, "Y": 4, "Z": 10}' \


# A function that magically converts any number of a desired resource to another resource in the pool of available resources in the game. Use this when you want to change the type of resource you have.


# Experiment 4: swap_value
# echo Experiment 4: convert_value
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure use the convert_items tool to swap the value of resource Y and resource Z for yourself. DO NOT make a trade before swapping values." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1_convert_items_log \
#   -t convert_items \
#   --available_resources '{"X": 15, "Y": 30, "Z": 30}' \
#   --values_red '{"X": 2, "Y": 10, "Z": 1}' \
#   --values_blue '{"X": 3, "Y": 4, "Z": 1}' \
#   --log_secret

# echo Experiment 5: bundle_items
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure use the bundle_items tool to bundle resource Y and resource Z for trade. DO NOT make a trade before bundle items." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1_bundle_items \
#   -t bundle_items \
#   --available_resources '{"X": 15, "Y": 30, "Z": 30}' \
#   --values_red '{"X": 2, "Y": 10, "Z": 1}' \
#   --values_blue '{"X": 3, "Y": 4, "Z": 1}' \


echo Experiment 6: bundle_items
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 20 \
  -s 1234 \
  -a "Be sure use the bundle_items tool to bundle resource Y and resource Z for trade. DO NOT make a trade before bundle items." \
  -d double_script \
  -n gpt-4o_trading_double_script_reasoning_v1.1_bundle_items_log \
  -t bundle_items \
  --available_resources '{"X": 15, "Y": 30, "Z": 30}' \
  --values_red '{"X": 2, "Y": 10, "Z": 1}' \
  --values_blue '{"X": 3, "Y": 4, "Z": 1}' \
  --log_secret