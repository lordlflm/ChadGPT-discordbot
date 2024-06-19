import json

def init_challenges():
    try:
        open('challenges.json').close()
    except FileNotFoundError:
        challenges_json = {'announcement_channel': '', 'challenges': []}
        with open('challenges.json', 'w') as f:
            json.dump(challenges_json, f, indent=4)

def read_challenges() -> dict:
    with open('challenges.json', 'r+') as f:
        challenges_json = json.load(f)
    return challenges_json

def get_challenge_by_name(chall_name: str) -> dict:
    challenges_json = read_challenges()
    challenge_object = next((challenge for challenge in challenges_json['challenges'] if challenge['name'] == chall_name), None)
    return challenge_object

def get_challenges_announcement_channel() -> str:
    challenges_json = read_challenges()
    return challenges_json['announcement_channel']

def update_challenges_announcement_channel(channel_name: str):
    challenges_json = read_challenges()
    challenges_json['announcement_channel'] = channel_name
    with open('challenges.json', 'w') as f:
        json.dump(challenges_json, f, indent=4)

def append_challenges(challenge_object):
    challenges_json = read_challenges()
    challenges_json['challenges'].append(challenge_object)
    with open('challenges.json', 'w') as f:
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

def increment_challenge_solves_by_name(chall_name: str):
    challenges_json = read_challenges()
    for i, challenge in enumerate(challenges_json['challenges']):
        if challenge['name'] == chall_name:
            challenge['solves'] += 1
            del(challenges_json['challenges'][i])
            challenges_json['challenges'].append(challenge)
            break
    with open('challenges.json', 'w+') as f:
        json.dump(challenges_json, f, indent=4)

def init_credentials():
    try:
        open('credentials.json').close()
    except FileNotFoundError:
        credentials_json = {"credentials": []}
        with open('credentials.json', 'w') as f:
            json.dump(credentials_json, f, indent=4)

def get_credential_by_domain(domain_name: str) -> dict:
    credentials_json = read_credentials()        
    return next((credential for credential in credentials_json['credentials'] if credential['domain'] == domain_name), None)

def read_credentials() -> dict:
    with open('credentials.json', 'r+') as f:
        credentials_json = json.load(f)
    return credentials_json

def append_credentials(credential_object: str):
    credentials_json = read_credentials()
    credentials_json['credentials'].append(credential_object)
    with open('credentials.json', 'w') as f:
        json.dump(credentials_json, f, indent=4)

def init_users():
    try:
        open('users.json').close()
    except FileNotFoundError:
        users_json = {"users": []}
        with open('users.json', 'w') as f:
            json.dump(users_json, f, indent=4)
            
def update_user_points_by_name(user_name: str, chall: dict):
    users_json = read_users()
    updated = False
    for i, user in enumerate(users_json['users']):
        if user['name'] == user_name:
            updated = True  
            user['points'] += chall['points']
            user['solved'].append(chall['name'])
            del(users_json['users'][i])
            users_json['users'].append(user)
            break
    if not updated:
        user = {'name': user_name, 'points': chall['points'], 'solved': [chall['name']]}
        users_json['users'].append(user)
    with open('users.json', 'w+') as f:
        json.dump(users_json, f, indent=4)
        
def get_user_solved_by_name(user_name: str) -> list[str]:
    with open('users.json', 'r+') as f:
        users_json = json.load(f)
        user = next((user for user in users_json['users'] if user['name'] == user_name), None)
        return user['solved']

def read_users() -> dict:
    with open('users.json', 'r+') as f:
        users_json = json.load(f)
    return users_json