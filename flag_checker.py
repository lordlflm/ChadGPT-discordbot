import discord
from discord.ext import commands
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from seleniumbase import SB
import logging

import json_database

def leaderboard(args: list[str], logger: logging.Logger) -> str:
    board_len = 5
    if len(args) > 0:
        board_len = int(args[0])
        if board_len == 0:
            board_len = 5
    
    users_json = json_database.read_users()
    board_dict = sorted(users_json['users'], key=lambda user: user['points'], reverse=True)[:board_len]
    
    board = '**Leaderboard**\n--------------'
    for i, user in enumerate(board_dict):
        board += f"\n{i+1}. {user['name']}"
        if i+1 == 1:
            board += '  :first_place:'
        elif i+1 == 2:
            board += '  :second_place:'
        elif i+1 == 3:
            board += '  :third_place:'
    board += '\n--------------'
    
    logger.info("Leaderboard command successful")
    return board
        

async def submit(args: list[str], guild: discord.Guild, ctx: commands.Context, logger: logging.Logger) -> str:
    if len(args) != 2:
        logger.info('Wrong number of arguments. Usage: `!submit <challenge_name> <flag>`')
        return 'Wrong number of arguments. Usage: `!submit <challenge_name> <flag>`'
    
    chall_name = args[0]
    flag = args[1]
    
    logger.info(f"{ctx.author} submission for {chall_name} : {flag}")
    
    challenge_object = json_database.get_challenge_by_name(chall_name)

    if not challenge_object:
        logger.info("Invalid challenge name")
        return "Invalid challenge name"

    if challenge_object['flag'] != "":
        return await compare_flag(challenge_object, flag, guild, ctx, logger)
    
    else:
        credential_object = json_database.get_credential_by_domain(urlparse(challenge_object['url'])[1])
        
        with SB(uc=True, demo=True, headless=True) as sb:
            challenge_plateform_submit_login(sb, challenge_object, credential_object, logger)
            sb.uc_open_with_tab(challenge_object['url'])

            challenge_plateform_submit_flag(sb, flag, logger)
            sb.sleep(2)
            
            if 'incorrect' in str(sb.get_page_source()).lower():
                logger.info(f"Invalid submission for {chall_name}")
                return "Invalid submission, try again"
            elif 'correct' in str(sb.get_page_source()).lower() and 'incorrect' not in str(sb.get_page_source()).lower():
                json_database.update_challenge_flag_by_name(chall_name, flag)
                return await submit([chall_name, flag], guild, ctx)
            else:
                logger.info("Couldn't detect if the flag was correct or incorrect")
                return "Couldn't detect if the flag was correct or incorrect. Check with admin to get your points"

async def compare_flag(challenge_object: dict, flag: str, guild: discord.Guild, ctx: commands.Context, logger: logging.Logger) -> str:
    chall_name = challenge_object['name']
    
    if challenge_object['flag'] == flag:
            if chall_name in json_database.get_user_solved_by_name(ctx.author.name):
                return f"You have already solved '{chall_name}'"
            
            json_database.update_user_points_by_name(ctx.author.name, challenge_object)
            for channel in guild.channels:
                if channel.name == json_database.get_challenges_announcement_channel():
                    if json_database.get_challenge_by_name(chall_name)['solves'] != 0:
                        await channel.send(f"Congratulation to {ctx.author.mention} for solving '{chall_name}!'")
                    else:
                        await channel.send(f"First blood on '{chall_name}'! :drop_of_blood: Congratulation to {ctx.author.mention}! :drop_of_blood:")
                    break
            json_database.increment_challenge_solves_by_name(chall_name)
            logger.info(f"Valid submission for {chall_name}")
            return f"Congratulation, you solved challenge '{chall_name}'"
    else:
        logger.info(f"Invalid submission for {chall_name}")
        return f"Invalid submission for {chall_name}"

#TODO some plateform wont need a login
def challenge_plateform_submit_login(sb: SB, challenge_object: dict, credential_object: dict, logger: logging.Logger):
    sb.driver.get(urljoin(challenge_object['url'], 'login'))
    input_fields_name = []
    submit_button_css_selector = ''
    soup = BeautifulSoup(sb.get_page_source(), 'html.parser')
    logger.info(f"Attempting login into {urljoin(challenge_object['url'], 'login')}.\nHTML is :\n{soup}")
    
    for input_field in soup.find_all('input'):
        input_fields_name.append(input_field.get('name'))
        if input_field.get('type') == 'submit':
            submit_button_css_selector = 'input[type=\'submit\']'
    logger.info(f"Filling in 'input[name='{input_fields_name[0]}']' field with {credential_object['username']}")
    sb.type(f'input[name=\'{input_fields_name[0]}\']', credential_object['username'])
    logger.info(f"Filling in 'input[name='{input_fields_name[1]}']' field with {credential_object['password']}")
    sb.type(f'input[name=\'{input_fields_name[1]}\']', credential_object['password'])
    
    for button in soup.find_all('button'):
        if button.get('type') == 'submit':
            submit_button_css_selector = 'button[type=\'submit\']'
            
    logger.info(f"Clicking on button with css selector {submit_button_css_selector}")
    sb.click(submit_button_css_selector)

#TODO this wont work for every plateform
def challenge_plateform_submit_flag(sb: SB, flag: str, logger: logging.Logger):
    soup = BeautifulSoup(sb.get_page_source(), 'html.parser')
    logger.info(f"Attempting flag submission.\nHTML is:\n{soup}")
    for input_field in soup.find_all('input'):
        if 'flag' in str(input_field.get('name')).lower() or 'flag' in str(input_field.get('placeholder')).lower():
            logger.info(f"Filling in 'input[name='{input_field.get('name')}']' field with {flag}")
            sb.type(f'input[name=\'{input_field.get("name")}\']', flag)
        if input_field.get('type') == 'submit' and ('submit' in str(input_field.get('name')).lower() or 'submit' in str(input_field.text).lower()):
            submit_button_css_selector = f'//input[text()=\'{button.get_text()}\']'
        if input_field.get('type') == 'button' and ('submit' in str(input_field.get('name')).lower() or 'submit' in str(input_field.text).lower()):
            submit_button_css_selector = f'//input[text()=\'{button.get_text()}\']'
    
    for button in soup.find_all('button'):
        if 'submit' in str(button.get('name')).lower() or 'submit' in str(button.get_text()).lower():
            submit_button_css_selector = f'//button[text()=\'{button.get_text()}\']'
    
    logger.info(f"Clicking on button with css selector {submit_button_css_selector}")
    sb.click(submit_button_css_selector)

async def new(args: list[str], guild: discord.Guild, ctx: commands.Context, logger: logging.Logger) -> str:
    if len(args) != 3 and len(args) != 5:
        logger.info('Wrong number of arguments. Usage: `!new <challenge_name> <challenge_url> <challenge_value>`')
        return 'Wrong number of arguments. Usage: `!new <challenge_name> <challenge_url> <challenge_value>`'
    
    chall_name = args[0]
    chall_url = args[1]
    chall_pts_str = args[2]
    cred_user = None
    cred_pass = None
    if len(args) == 5:
        cred_user = args[3]
        cred_pass = args[4]
        
    credentials_json = json_database.read_credentials()

    if urlparse(chall_url).netloc not in [credential['domain'] for credential in credentials_json['credentials']]:
        if not cred_user or not cred_pass:
            logger.info(f"No credential found for {urlparse(chall_url).netloc}")
            return 'No credentials found for this CTF platform. You should provide a username and a password for ChadGPT as 4th and 5th arguments'
        else:
            credential_object = {
                "domain": urlparse(chall_url).netloc,
                "username": cred_user,
                "password": cred_pass
            }
            json_database.append_credentials(credential_object)

    challenge_object = {
        'name': chall_name,
        'url': chall_url,
        'flag': '',
        'solves': 0,
        'points': int(chall_pts_str)
    }

    challenges_json = json_database.read_challenges()

    if challenge_object['name'] not in [challenge['name'] for challenge in challenges_json['challenges']]:
        json_database.append_challenges(challenge_object)

        for channel in guild.channels:
            if channel.name == challenges_json['announcement_channel']:
                mention = json_database.get_challenges_mention()
                for role in guild.roles:
                    if role.name == mention:
                        mention = role.mention
                await channel.send(f"{mention}! New challenge available!\n'{chall_name}' for {chall_pts_str} points at {chall_url}\nGood hacking!")
                break
        logger.info(f"Successfully added '{challenge_object.get('name')}' challenge")
        return f"Successfully added '{challenge_object.get('name')}' challenge"
    else:
        logger.info(f"A challenge with the name {chall_name} already exists.")
        return "A challenge with the same name already exists."
    
def set_ctf_announcement(args: list[str], guild: discord.Guild, logger: logging.Logger) -> str:
    if len(args) < 1:
        logger.info('Wrong number of arguments. Usage: `!set_ctf_channel <channel_name>`')
        return 'Wrong number of arguments. Usage: `!set_ctf_channel <channel_name>`'
    channel_name = args[0]
    
    text_channels = []
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            text_channels.append(channel.name)
    if channel_name not in text_channels:
        logger.info(f"'{channel_name}' is not a valid text channel")
        return f"'{channel_name}' is not a valid text channel"
        
    json_database.update_challenges_announcement_channel(channel_name)
    logger.info(f"Successfully set '{channel_name}' as ctf announcement channel")
    return f"Successfully set '{channel_name}' as ctf announcement channel"

def set_ctf_mention(args: list[str], guild: discord.Guild, logger: logging.Logger) -> str:
    if len(args) < 1:
        logger.info('Wrong number of arguments. Usage: `!set_ctf_mention <mention_name>`')
        return 'Wrong number of arguments. Usage: `!set_ctf_mention <mention_name>`'
    mention_name = args[0]
    
    roles = []
    for role in guild.roles:
        roles.append(role.name)
    if mention_name not in roles:
        return f"'{mention_name}' is not a valid role"
    
    json_database.update_challenges_mention(mention_name)
    logger.info(f"Successfully set '{mention_name}' as role to be mentionned for ctf updates")
    return f"Successfully set '{mention_name}' as role to be mentionned for ctf updates"