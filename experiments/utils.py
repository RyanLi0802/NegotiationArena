import re

def parse_final_answer(llm_response: str, agent_one: str, agent_two: str) -> str:
    """
    Parse the final prediction from the LLM response.
    
    Args:
        llm_response (str): The response from the LLM.
        agent_one (str): The name of the first agent.
        agent_two (str): The name of the second agent.

    Returns:
        str: The name of the agent (either agent_one or agent_two).
    """
    # Use regex to find the Final Answer pattern with the actual agent names
    pattern = fr"Final Answer:\s*({re.escape(agent_one)}|{re.escape(agent_two)})"
    match = re.search(pattern, llm_response)

    if match:
        # Return the captured agent name
        return match.group(1)
    else:
        raise ValueError("Final Answer not found in the LLM response")