import json

def _extract_test_execution_log(messages):
    """
    Extract messages where role is assistant and content is a list of tool use blocks
    from a list of messages and return the list of tool use blocks.
    """
    instructions = []
    current_instruction = _initialize_instruction()

    for message in messages:
        if _is_user_text_message(message):
            if current_instruction['instruction']:
                instructions.append(current_instruction)
            current_instruction = _initialize_instruction()
            current_instruction['instruction'] = message['content'][0]['text']
        elif _is_assistant_tool_use_message(message):
            current_instruction['actions'].extend(message['content'])

    if current_instruction['instruction']:
        instructions.append(current_instruction)

    return instructions

def _initialize_instruction():
    return {'instruction': '', 'actions': []}

def _is_user_text_message(message):
    return message['role'] == "user" and message['content'][0]['type'] == "text"

def _is_assistant_tool_use_message(message):
    return message['role'] == "assistant" and isinstance(message['content'], list)

# with open("sample_test_case_2_messages.json") as f:
#     response = json.load(f)
#     instructions = _extract_test_execution_log(response)
#     with open("sample_test_case_2_ai_actions.json", "w") as wf:
#         json.dump(instructions, wf)

