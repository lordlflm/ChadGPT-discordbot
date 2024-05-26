import json
import requests
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from seleniumbase import SB

import webdriver
from selenium.webdriver.common.by import By

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
        return "good"
    else:
        # TODO try except here FileNotFound
        with open('./credentials.json', 'r+') as f:
            creds_file_json = json.load(f)
            credential_object = next((credential for credential in creds_file_json['credentials'] if credential['domain'] == urlparse(chall_obj['url'])[1]), None)
            f.close()
    
        # session = requests.Session()
        # res = session.get(urljoin(chall_obj['url'], 'login'))
        # # soup = BeautifulSoup(res.content, 'html.parser')
        login_data = {}
        
        
        #TODO here soup might not be whats expected, need to interpret javascript in some cases 
        # (Use selenium to simulate browser)
        #
        # Selenium seems to be getting blocked by cloudfare
        # driver = webdriver.generate_webdriver()
        # driver.get(urljoin(chall_obj['url'], 'login'))
        # driver.get('https://play.picoctf.org/login')
        # driver.sleep(4)
        
        # LOGIN
        # 1. Scrape for input fields with bs4
        # 2. Fill input fields
        # 3. Search for submit button
        # 4. click submit
        
        # if cloudfare problems
        # 1. change browser
        # 2. Try running selenium in docker
        # 3. change user agent
        
        # input_fields = driver.find_elements(By.TAG_NAME, 'input')
        # input_fields[0].send_keys(credential_object['username'])
        # input_fields[1].send_keys(credential_object['password'])
        # driver.find_element(By.TAG_NAME, 'button').click()
        # driver.save_screenshot('./foto.png')
        # print(driver.get_issue_message)
        
        
        with SB(uc=True, demo=True) as sb:
            sb.driver.get('https://play.picoctf.org/login')
            input_fields_name = []
            submit_button_css_selector = ''
            soup = BeautifulSoup(sb.get_page_source(), 'html.parser')
            #TODO make sure the input fields are in the login form
            for input_field in soup.find_all('input'):
                input_fields_name.append(input_field.get('name'))
                if input_field.get('type') == 'submit':
                    submit_button_css_selector = 'input[type=\'submit\']'
            sb.type(f'input[name=\'{input_fields_name[0]}\']', credential_object['username'])
            sb.type(f'input[name=\'{input_fields_name[1]}\']', credential_object['password'])
            try:
                for button in soup.find_all('button'):
                    if button.get('type') == 'submit':
                        submit_button_css_selector = 'button[type=\'submit\']'
            except:
                pass
            sb.click(f'{submit_button_css_selector}')
            
            sb.driver.save_screenshot('./foto1.png')
            sb.sleep(100)
            
            
        return "testing"
        
        # for input in soup.find_all('input'):
        #     value = input.get('value') if input.get('value') else ''
        #     login_data.update({input.get('name'): value})
        # i = iter(login_data)
        # login_data[next(i)] = credential_object['username']
        # login_data[next(i)] = credential_object['password']
        # res = session.post(urljoin(chall_obj['url'], 'login'), data=login_data)
        
        
        #TODO post request the flag and add it to challenges.json if true
        # The following only works for picoCTF.org
        print(urlparse(chall_obj['url']))
        submission_data = {}
        
        
    return "hmm"





def new(chall_name: str, 
        chall_url: str, 
        chall_pts_str: str, 
        cred_user: str = None, 
        cred_pass: str = None) -> str:
    try:
        with open('credentials.json', 'r+') as f:
            file_json = json.load(f)
    except FileNotFoundError:
        file_json = {"credentials": []}
        with open('credentials.json', 'w') as f:
            json.dump(file_json, f, indent=4)

    if urlparse(chall_url).netloc not in [cred['domain'] for cred in file_json['credentials']]:
        if not cred_user or not cred_pass:
            return 'No credentials found for this CTF platform. You should provide a username and a password for ChadGPT as 4th and 5th arguments'
        else:
            cred = {
                "domain": urlparse(chall_url).netloc,
                "username": cred_user,
                "password": cred_pass
            }
            file_json['credentials'].append(cred)
            with open('credentials.json', 'w') as f:
                json.dump(file_json, f, indent=4)

    chall = {
        'name': chall_name,
        'url': chall_url,
        'flag': '',
        'points': int(chall_pts_str)
    }

    try:
        with open('./challenges.json', 'r+') as f:
            file_json = json.load(f)
    except FileNotFoundError:
        file_json = {'challenges': []}
        with open('./challenges.json', 'w') as f:
            json.dump(file_json, f, indent=4)

    challenge_names = [challenge['name'] for challenge in file_json['challenges']]
    if chall['name'] not in challenge_names:
        file_json['challenges'].append(chall)
        with open('./challenges.json', 'w') as f:
            json.dump(file_json, f, indent=4)
        return "Successfully added \"{}\" challenge".format(chall.get('name'))
    else:
        return "A challenge with the same name already exists."