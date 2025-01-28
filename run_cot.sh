# Experiment
echo Experiment: CoT + Counter Offer Reasoning
python experiments/run_simple_experiment.py \
  -m gpt-4o \
  -r 20 \
  -s 1234 \
  -a "Be sure to first use the chain of thought tool to perform structured reasoning for negotiation decisions, then use the propose counter offer tool to perform structured reasoning for proposing counter offer when you do not accpet the offer proposed by your opponent. **Do NOT accept a trade without using these two tools**" \
  -d double_script \
  -n gpt-4o_trading_double_script_reasoning_v1.1_cot_propose_new_trade \
  -t chain_of_thought propose_counter_offer \
  --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
  --values_red '{"X": 15, "Y": 10, "Z": 12}' \
  --values_blue '{"X": 12, "Y": 4, "Z": 10}' \
  --log_secret

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
# python experiments/run_simple_experiment.py \
#   -m gpt-4o \
#   -r 20 \
#   -s 1234 \
#   -a "Be sure to use the chain of thought tool to perform structured reasoning for negotiation decisions. **Do NOT accept a trade without performing chain of thought reasoning**." \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1_chain_of_thought \
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