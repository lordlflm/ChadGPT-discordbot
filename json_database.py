import json

def init_challenges():
    #TODO check if file already exists
    challenges_json = {'announcement_channel': '', 'challenges': []}
    with open('./challenges.json', 'w') as f:
        json.dump(challenges_json, f, indent=4)

def read_challenges():
    with open('./challenges.json', 'r+') as f:
        challenges_json = json.load(f)
    return challenges_json

def get_challenge_by_name(chall_name: str):
    challenges_json = read_challenges()
    challenge_object = next((challenge for challenge in challenges_json['challenges'] if challenge['name'] == chall_name), None)
    return challenge_object

def get_challenges_announcement_channel():
    challenges_json = read_challenges()
    return challenges_json['announcement_channel']

def update_challenges_announcement_channel(channel_name: str):
    challenges_json = read_challenges()
    challenges_json['announcement_channel'] = channel_name
    with open('./challenges.json', 'w') as f:
        json.dump(challenges_json, f, indent=4)

def append_challenges(challenge_object):
    challenges_json = read_challenges()
    challenges_json['challenges'].append(challenge_object)
    with open('./challenges.json', 'w') as f:
        json.dump(challenges_json, f, indent=4)

def update_challenge_flag_by_name(chall_name: str, flag: str):
    challenges_json = read_challenges()
    for i, challenge in enumerate(challenges_json['challenges']):
        if challenge['name'] == chall_name:
            challenge['flag'] = flag
            del(challenges_json['challenges'][i])
            challenges_json['challenges'].append(challenge)
            break
    with open('challenges.json', 'w+') as f:
        json.dump(challenges_json, f, indent=4)

def init_credentials():
    #TODO check if file already exists
    credentials_json = {"credentials": []}
    with open('credentials.json', 'w') as f:
        json.dump(credentials_json, f, indent=4)

def read_credentials():
    with open('credentials.json', 'r+') as f:
        credentials_json = json.load(f)
    return credentials_json

def append_credentials(credential_object):
    credentials_json = read_credentials()
    credentials_json['credentials'].append(credential_object)
    with open('credentials.json', 'w') as f:
        json.dump(credentials_json, f, indent=4)

def init_leaderboard():
    pass

def read_leaderboard():
    pass

def write_leaderboard():
    pass