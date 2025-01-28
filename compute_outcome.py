import json
import glob

# folders = ["./.logs/gpt-4o_trading_double_script_reasoning_v1.1_cot_propose_new_trade/", "./.logs/gpt-4o_trading_double_script_v1.1_cot_propose_new_trade/"]
folders = ["./.logs/gpt-4o_trading_double_script_reasoning_v1.1_propose_new_trade/", "./.logs/gpt-4o_trading_double_script_v1.1_propose_new_trade/"]

out = [[], []]
for folder in folders:
    for i in range(20):
        file = folder + "round_" + str(i) + "/game_state.json"
        with open(file) as f:
            data = json.load(f)
            players = data["players"]
            player_idx = 0
            if players[0]["class"] == "CustomAgent":
                player_idx = 0
            else:
                player_idx = 1
            
            all_item = data["resources_support_set"]["_value"]
            values = data["player_initial_goals"][player_idx]["_value"]["_value"]["_value"]
            if "summary" in data["game_state"][-1]:
                claim_item = data["game_state"][-1]["summary"]["final_resources"][player_idx]["_value"]
                total_value = 0
                aquired_value = 0

                for key, value in all_item.items():
                    total_value += value * values.get(key, 0)
                    aquired_value += value * claim_item.get(key, 0)
                
                if aquired_value == 0:
                    continue
                out[player_idx].append(aquired_value / total_value)

print(f"{len(out[0])} Red agent has finished, {len(out[1])} Blue agent has finished")
final_out = {'RED aquired ratio': sum(out[0]) / len(out[0]), 'BLUE aquired ratio': sum(out[1]) / len(out[1])}
print(final_out)
        


