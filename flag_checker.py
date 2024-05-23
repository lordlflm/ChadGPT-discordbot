import json
import requests
import re
from urllib.parse import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup

def submit(chall_name: str, flag: str):
    try:
        with open('./ctf_challenges.json', 'r+') as file:
            file_json = json.load(file)

            file.close()
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
        with open('./requests_creds.json', 'r+') as f:
            creds_file_json = json.load(f)
            credential_object = next((credential for credential in creds_file_json['credentials'] if credential['domain'] == urlparse(chall_obj['url'])[1]), None)
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
        pass
    return "hmm"





def new(chall_name: str, chall_url: str, chall_pts_str: str) -> str:
    #TODO if no credentials found for this website, exit and request the user provides one

    chall = {
        'name': chall_name,
        'url': chall_url,
        'flag': '',
        'points': int(chall_pts_str)
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