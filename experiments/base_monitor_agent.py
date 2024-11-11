import openai
from openai import OpenAI
from experiments.prompt_utils import get_discriminator_prompt_single_script, get_discriminator_prompt_double_script
from experiments.utils import parse_final_answer
from negotiationarena.constants import *


class BaseAgent():
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
        discriminator_prompt = get_discriminator_prompt_double_script(base_script, exp_script)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": discriminator_prompt,
                }
            ],
            temperature=0.0,
            seed=self.seed,
        )
        output_text = response.choices[0].message.content.strip()
        print("Weak Model: ")
        print(output_text)
        
        return parse_final_answer(output_text, AGENT_ONE, AGENT_TWO)