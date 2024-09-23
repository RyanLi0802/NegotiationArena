import json
import traceback
import logging
import uuid
import re


def clean_json_string(json_string: str) -> str:
    # Remove trailing commas before closing braces/brackets in JSON structures
    cleaned_json_string = re.sub(r',\s*(\}|\])', r'\1', json_string)
    return cleaned_json_string

def parse_llm_output(llm_output: str):
    # Regular expressions to match the JSON structures
    tool_calls_pattern = r'\{\s*"type":\s*"tool_calls",\s*"content":\s*\[.*?\]\s*\}'
    text_message_pattern = r'\{\s*"type":\s*"text_message",\s*"content":\s*".*?"\s*\}'
    
    # Initial text that appears before the JSON
    final_text_before_json = ""
    
    # Try to find tool calls JSON
    tool_calls_match = re.search(tool_calls_pattern, llm_output, re.DOTALL)
    if tool_calls_match:
        tool_calls_json = tool_calls_match.group(0)
        final_text_before_json = llm_output[:tool_calls_match.start()]
        # Clean up the JSON string (remove trailing commas)
        tool_calls_json = clean_json_string(tool_calls_json)
        return final_text_before_json, json.loads(tool_calls_json)
    
    # Try to find text message JSON
    text_message_match = re.search(text_message_pattern, llm_output)
    if text_message_match:
        text_message_json = text_message_match.group(0)
        final_text_before_json = llm_output[:text_message_match.start()]
        return final_text_before_json, json.loads(text_message_json)
    
    # If neither pattern is found, treat the entire output as text message
    return "", {
        "type": "text_message",
        "content": llm_output,
    }