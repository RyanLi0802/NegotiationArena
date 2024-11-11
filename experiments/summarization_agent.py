import openai
from openai import OpenAI
from experiments.prompt_utils import get_summarize_actions_prompt, get_summarize_behavior_prompt, get_detect_capability_prompt
from experiments.utils import parse_final_answer
from negotiationarena.constants import *


class SummarizationAgent():
    def __init__(self, model, seed=None):
        self.model = model
        if "gpt" in model:
            self.client = OpenAI()
        else:
            self.client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="EMPTY")
        
        self.seed = seed
    
    def predict(self, base_script, exp_script):
        print("==============================")
        print("Making prediction...")
        
        messages = [
            {
                "role": "user",
                "content": get_summarize_actions_prompt(base_script),
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0,
            seed=self.seed,
        )
        
        print("Weak Model:")
        summarized_actions = response.choices[0].message.content.strip()
        print("Summarized base actions:")
        print(summarized_actions)
        
        messages.append({
            "role": "assistant",
            "content": summarized_actions,
        })
        
        messages.append({
            "role": "user",
            "content": get_summarize_behavior_prompt(),
        })
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0,
            seed=self.seed,
        )
        
        summarized_behavior = response.choices[0].message.content.strip()
        print("Summarized base behaviors:")
        print(summarized_behavior)
        
        messages.append({
            "role": "assistant",
            "content": summarized_behavior,
        })
        
        messages.append({
            "role": "user",
            "content": get_detect_capability_prompt(exp_script),
        })
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0,
            seed=self.seed,
        )
        
        output_text = response.choices[0].message.content.strip()
        
        print("Detecting New Capabilities:")
        print(output_text)
        
        return parse_final_answer(output_text, AGENT_ONE, AGENT_TWO)