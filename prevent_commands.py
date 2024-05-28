import json

def new_restricted_command(restricted_command: str, restricted_channels: list[str]) -> str:
    try:
        with open('restricted_commands.json', 'r+') as f:
            file_json = json.load(f)
    except FileNotFoundError:
        file_json = {"restricted_commands": []}
        with open('restricted_commands.json', 'w') as f:
            json.dump(file_json, f, indent=4)
    
    restricted_command_object = {
        'command': restricted_command,
        'channels': []
    }
    
    for channel in restricted_channels:
        restricted_command_object['channels'].append(channel)
    
    i = 0
    for restricted_command_obj in file_json['restricted_commands']:
        if restricted_command_obj['command'] == restricted_command_object['command']:
            del(file_json['restricted_commands'][i])
            break
        i += 1
       
    with open('restricted_commands.json', 'w') as f:
        file_json['restricted_commands'].append(restricted_command_object)
        json.dump(file_json, f, indent=4)
    
    return "Successfully updated restricted commands"

def prevent(msg: str, msg_channel: str) -> bool:
    try:
        with open('restricted_commands.json', 'r+') as f:
            file_json = json.load(f)
    except FileNotFoundError:
        return False
    
    for restricted_command in file_json['restricted_commands']:
        if msg.startswith(restricted_command['command']) and msg_channel in restricted_command['channels']:
            return True
            
    return False
            
    
    