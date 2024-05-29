import json
import discord
from discord.ext import commands
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from seleniumbase import SB

def submit(chall_name: str, flag: str) -> str:
    try:
        with open('./challenges.json', 'r+') as f:
            challenges_json = json.load(f)
            f.close()
    except FileNotFoundError:
        return "Invalid challenge name"

    challenge_object = next((challenge for challenge in challenges_json['challenges'] if challenge['name'] == chall_name), None)   
    if not challenge_object:
        return "Invalid challenge name"

    if challenge_object['flag'] != "":
        if challenge_object['flag'] == flag:
            #TODO
            # update leaderboard
            # announce solve in designated channel (check for first bloods)
            print(f"Valid submission for {chall_name}")
            return f"Congratulation, you solved {chall_name}"
        else:
            print(f"Invalid submission for {chall_name}")
            return f"Invalid submission for {chall_name}"
    
    else:
        with open('./credentials.json', 'r+') as f:
            credentials_json = json.load(f)
            credential_object = next((credential for credential in credentials_json['credentials'] if credential['domain'] == urlparse(challenge_object['url'])[1]), None)
            f.close()
        
        try:
            with SB(uc=True, demo=True, headless=False) as sb:
                sb.driver.get(urljoin(challenge_object['url'], 'login'))
                input_fields_name = []
                submit_button_css_selector = ''
                soup = BeautifulSoup(sb.get_page_source(), 'html.parser')
                
                for input_field in soup.find_all('input'):
                    input_fields_name.append(input_field.get('name'))
                    if input_field.get('type') == 'submit':
                        submit_button_css_selector = 'input[type=\'submit\']'
                sb.type(f'input[name=\'{input_fields_name[0]}\']', credential_object['username'])
                sb.type(f'input[name=\'{input_fields_name[1]}\']', credential_object['password'])
                
                for button in soup.find_all('button'):
                    if button.get('type') == 'submit':
                        submit_button_css_selector = 'button[type=\'submit\']'
                
                sb.click(submit_button_css_selector)
                sb.uc_open_with_tab(challenge_object['url'])
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
                
                # Problem with picoCTF is that flag have a random string at the end :(
                if 'incorrect' in str(sb.get_page_source()).lower():
                    print(f"Invalid submission for {chall_name}")
                    return "Invalid submission, try again"
                elif 'correct' in str(sb.get_page_source()).lower() and 'incorrect' not in str(sb.get_page_source()).lower():
                    
                    #TODO test this before commit
                    for i, challenge in enumerate(challenges_json['challenges']):
                        if challenge['name'] == chall_name:
                            challenge['flag'] = flag
                            del(challenges_json['challenges'][i])
                            challenges_json['challenges'].append(challenge)
                            break
                    with open('challenges.json', 'w+') as f:
                        json.dump(challenges_json, f, indent=4)
                    
                    return submit(chall_name, flag)
        except Exception as e:
            print(f"Exception in flag_checker.submit(): {repr(e)}")
            return "An internal error occured"
        finally:
            #should quit
            pass
        
        print("Couldn't detect if the flag was correct or incorrect")
        return "An internal error occured"

def new(chall_name: str, 
        chall_url: str, 
        chall_pts_str: str, 
        cred_user: str = None, 
        cred_pass: str = None) -> str:
    try:
        with open('credentials.json', 'r+') as f:
            credentials_json = json.load(f)
    except FileNotFoundError:
        credentials_json = {"credentials": []}
        with open('credentials.json', 'w') as f:
            json.dump(credentials_json, f, indent=4)

    if urlparse(chall_url).netloc not in [credential['domain'] for credential in credentials_json['credentials']]:
        if not cred_user or not cred_pass:
            return 'No credentials found for this CTF platform. You should provide a username and a password for ChadGPT as 4th and 5th arguments'
        else:
            cred = {
                "domain": urlparse(chall_url).netloc,
                "username": cred_user,
                "password": cred_pass
            }
            credentials_json['credentials'].append(cred)
            with open('credentials.json', 'w') as f:
                json.dump(credentials_json, f, indent=4)

    chall = {
        'name': chall_name,
        'url': chall_url,
        'flag': '',
        'points': int(chall_pts_str)
    }

    try:
        with open('./challenges.json', 'r+') as f:
            challenges_json = json.load(f)
    except FileNotFoundError:
        challenges_json = init_challenges_json()

    challenge_names = [challenge['name'] for challenge in challenges_json['challenges']]
    if chall['name'] not in challenge_names:
        challenges_json['challenges'].append(chall)
        with open('./challenges.json', 'w') as f:
            json.dump(challenges_json, f, indent=4)
        #TODO logging
        return f"Successfully added '{chall.get('name')}' challenge"
    else:
        #TODO logging
        return "A challenge with the same name already exists."
    
def set_ctf_announcement(channel_name: str, ctx: commands.Context) -> str:
    text_channels = []
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            text_channels.append(channel.name)
    if channel_name not in text_channels:
        #TODO logging
        return f"{channel_name} is not a valid text channel"
    
    try:
        with open('./challenges.json', 'r+') as f:
            challenges_json = json.load(f)
    except FileNotFoundError:
        challenges_json = init_challenges_json()
        
    challenges_json['announcement_channel'] = channel_name
    with open('./challenges.json', 'w') as f:
        json.dump(challenges_json, f, indent=4)
    #TODO logging
    return f"Successfully set {channel_name} as ctf announcement channel"

def init_challenges_json():
    challenges_json = {'announcement_channel': '', 'challenges': []}
    with open('./challenges.json', 'w') as f:
        json.dump(challenges_json, f, indent=4)
    return challenges_json