import json
import re

def check(message_content):
    #TODO if the flag is correct update some leaderboard
    pass

def new(message_content: str) -> str:
    pattern = r'new\("([^"]+)",\s*"([^"]+)",\s*(\d+)\)'
    match = re.match(pattern, message_content)

    if match == None:
        return 'Bad format for command. Try `new("challenge name", "flag", points)`'
    else:
        chall = {
            'name': match.group(1),
            'flag': match.group(2),
            'points': int(match.group(3))
        }
        
        try:
            with open('./ctf_challenges.json', 'r+') as file:
                file_json = json.load(file)
                file.close()
        except FileNotFoundError:
            with open('./ctf_challenges.json', 'w+') as file:
                chall_header = {'challenges': []}
                chall_header_json_object = json.dumps(chall_header, indent=4)
                file.write(chall_header_json_object)
                file.seek(0)
                file_json = json.load(file)
                file.close()
        with open('./ctf_challenges.json', 'r+') as file:
            challenge_names = [challenge['name'] for challenge in file_json['challenges']]
            if chall['name'] not in challenge_names:
                file_json['challenges'].append(chall)
                file.seek(0)
                json.dump(file_json, file, indent=4)
            else:
                file.close()
                return "A challenge with the same name already exists."
            file.close()
            return "Successfully added \"{}\" challenge".format(chall.get('name'))