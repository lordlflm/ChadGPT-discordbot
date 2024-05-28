import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from seleniumbase import SB

def submit(chall_name: str, flag: str) -> str:
    try:
        with open('./challenges.json', 'r+') as f:
            file_json = json.load(f)
            f.close()
    except FileNotFoundError:
        return "Invalid challenge name"

    chall_obj = next((challenge for challenge in file_json['challenges'] if challenge['name'] == chall_name), None)   
    if not chall_obj:
        return "Invalid challenge name"

    if chall_obj['flag'] != "":
        
        # TODO compare flags
        print('flage found')
        return "good"
    
    else:
        with open('./credentials.json', 'r+') as f:
            creds_file_json = json.load(f)
            credential_object = next((credential for credential in creds_file_json['credentials'] if credential['domain'] == urlparse(chall_obj['url'])[1]), None)
            f.close()
        
        try:
            with SB(uc=True, demo=True, headless=False) as sb:
                #TODO testing
                # sb.driver.get('https://play.picoctf.org/practice/challenge/105?category=6&page=1')
                
                sb.driver.get(urljoin(chall_obj['url'], 'login'))
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
                
                for button in soup.find_all('button'):
                    if button.get('type') == 'submit':
                        submit_button_css_selector = 'button[type=\'submit\']'
                
                sb.click(f'{submit_button_css_selector}')
                sb.uc_open_with_tab(chall_obj['url'])
                sb.sleep(2)

                soup = BeautifulSoup(sb.get_page_source(), 'html.parser')
                for input_field in soup.find_all('input'):
                    if 'flag' in str(input_field.get('name')).lower() or 'flag' in str(input_field.get('placeholder')).lower():
                        sb.type(f'input[name=\'{input_field.get("name")}\']', flag)
                    if input_field.get('type') == 'submit' and ('submit' in str(input_field.get('name')).lower() or 'submit' in str(input_field.text).lower()):
                        submit_button_css_selector = f'//input[text()=\'{button.get_text()}\']'
                    if input_field.get('type') == 'button' and ('submit' in str(input_field.get('name')).lower() or 'submit' in str(input_field.text).lower()):
                        submit_button_css_selector = f'//input[text()=\'{button.get_text()}\']'
                
                for button in soup.find_all('button'):
                    if 'submit' in str(button.get('name')).lower() or 'submit' in str(button.get_text()).lower():
                        submit_button_css_selector = f'//button[text()=\'{button.get_text()}\']'
                
                sb.click(submit_button_css_selector)
                sb.sleep(2)
                # Problem with picoCTF is that flag have a random string at the end
                if 'incorrect' in str(sb.get_page_source()).lower():
                    print(f"Invalid submission for {chall_name}")
                    return "Invalid submission, try again"
                elif 'correct' in str(sb.get_page_source()).lower() and 'incorrect' not in str(sb.get_page_source()).lower():
                    print(f"Valid submission for {chall_name}")
                    
                    #TODO add flag to json file then return submit function
                    
                    return submit(chall_name, flag)
        except Exception as e:
            print(f"Exception in flag_checker.submit(): {repr(e)}")
            return "An error occured"
        finally:
            #should quit
            pass
        
        print("Couldnt detect if the flag was correct or incorrect")
        return "An error occured"

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