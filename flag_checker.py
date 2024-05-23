import json
import requests
import re
from urllib.parse import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup

def submit(chall_name: str, flag: str):
    try:
        with open('./challenges.json', 'r+') as f:
            file_json = json.load(f)
            f.close()
    except FileNotFoundError:
        #TODO challenge not found
        print('no chall')
        return "oops"

    chall_obj = next((challenge for challenge in file_json['challenges'] if challenge['name'] == chall_name), None)   
    if not chall_obj:
        #TODO challenge not found
        print('no chall')
        return "oops"

    if chall_obj['flag'] != "":
        # TODO compare flags
        print('flage found')
        return "oops"
    else:
        # TODO try except here FileNotFound
        with open('./credentials.json', 'r+') as f:
            creds_file_json = json.load(f)
            credential_object = next((credential for credential in creds_file_json['credentials'] if credential['domain'] == urlparse(chall_obj['url'])[1]), None)
            f.close()
    
        session = requests.Session()
        res = session.get(urljoin(chall_obj['url'], 'login'))
        soup = BeautifulSoup(res.content, 'html.parser')
        login_data = {}
        for input in soup.find_all('input'):
            value = input.get('value') if input.get('value') else ''
            login_data.update({input.get('name'): value})
        i = iter(login_data)
        login_data[next(i)] = credential_object['username']
        login_data[next(i)] = credential_object['password']
        res = session.post(urljoin(chall_obj['url'], 'login'), data=login_data)
        
        
    return "hmm"





def new(chall_name: str, 
        chall_url: str, 
        chall_pts_str: str, 
        cred_user: str = None, 
        cred_pass: str = None) -> str:
    try:
        with open('credentials.json', 'r+') as f:
            file_json = json.load(f)
            f.close()
    except FileNotFoundError:
        with open('credentials.json', 'w+') as f:
            creds_dict = {"credentials": []}
            creds_json_object = json.dumps(creds_dict, indent=4)
            f.write(creds_json_object)
            f.seek(0)
            file_json = json.load(f)
            f.close()
            
    #if url not already in creds: need to add it
    with open('credentials.json', 'r+') as f:
        if urlparse(chall_url).netloc not in [cred['domain'] for cred in file_json['credentials']]:
            if not cred_user or not cred_pass:
                return 'No credentials found for this ctf plateform. You should provide a username and a password for ChadGPT as 4th and 5th arguments'
            else:
                cred = {
                    "domain": urlparse(chall_url).netloc,
                    "username": cred_user,
                    "password": cred_pass
                }
                file_json = json.load(f)
                file_json['credentials'].append(cred)
                f.seek(0)
                json.dump(file_json, f, indent=4)
                f.close()
        else:
            f.close()    
            
    chall = {
        'name': chall_name,
        'url': chall_url,
        'flag': '',
        'points': int(chall_pts_str)
    }

    try:
        with open('./challenges.json', 'r+') as f:
            file_json = json.load(f)
            f.close()
    except FileNotFoundError:
        with open('./challenges.json', 'w+') as f:
            chall_dict = {'challenges': []}
            f.write(json.dumps(chall_dict, indent=4))
            f.seek(0)
            file_json = json.load(f)
            f.close()

    with open('./challenges.json', 'r+') as f:
        challenge_names = [challenge['name'] for challenge in file_json['challenges']]
        if chall['name'] not in challenge_names:
            file_json['challenges'].append(chall)
            f.seek(0)
            json.dump(file_json, f, indent=4)
            f.close()
        else:
            f.close()
            return "A challenge with the same name already exists."

    return "Successfully added \"{}\" challenge".format(chall.get('name'))