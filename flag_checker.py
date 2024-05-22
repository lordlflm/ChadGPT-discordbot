import json
import re

def check(chall_name: str, flag: str) -> str:
    #TODO if the flag is correct update some leaderboard
    pass

def new(chall_name: str, chall_url: str, chall_pts: str) -> str:

    chall = {
        'name': chall_name,
        'url': chall_url,
        'flag': '',
        'points': int(chall_pts)
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