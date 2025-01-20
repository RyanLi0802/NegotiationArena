# Experiment
echo Experiment: Chain of Thought
python experiments/run_simple_experiment.py \
  -m gpt-4o-mini \
  -r 1 \
  -s 1234 \
  -a "Be sure to use the chain of thought tool to perform structured reasoning for negotiation decisions. **Do NOT accept a trade without performing chain of thought reasoning**." \
  -d double_script \
  -n gpt-4o_trading_double_script_reasoning_v1.1_chain_of_thought \
  -t chain_of_thought \
  --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
  --values_red '{"X": 15, "Y": 10, "Z": 12}' \
  --values_blue '{"X": 12, "Y": 4, "Z": 10}' \
  --log_secret

# python experiments/run_simple_experiment.py \
#   -m gpt-4o-mini \
#   -r 1 \
#   -s 1234 \
#   -d double_script \
#   -n gpt-4o_trading_double_script_reasoning_v1.1 \
#   --available_resources '{"X": 15, "Y": 10, "Z": 20}' \
#   --values_red '{"X": 15, "Y": 10, "Z": 12}' \
#   --values_blue '{"X": 12, "Y": 4, "Z": 10}' \
#   --log_secret