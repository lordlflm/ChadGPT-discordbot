import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

import flag_checker
import prevent_commands
import json_database

guild_id = 0
logger = logging.getLogger(__name__)

def run_discord_bot():
    load_dotenv(override=True)
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.guilds = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.listen()
    async def on_message(message):
        if message.author == bot.user or str(message.channel.type) == 'private':
            return
        if (prevent_commands.prevent(message.content, message.channel.name)):
            print(f"{message.author.name} sent restricted command {message.content} in {message.channel.name}")
            await message.delete()
            await message.channel.send('This command is forbidden in this channel')
        
    @bot.command()
    async def restrict_command(ctx, *args):
        try:
            await ctx.send(prevent_commands.new_restricted_command(args[0], args[1:]))
        except IndexError:
            await ctx.send('Wrong number of arguments. Usage: `!restrict_command <restricted_command> <restricted_channel_1> ...`')
    
    @bot.command()
    async def new(ctx, *args):
        if 'private' != str(ctx.channel.type):
            await ctx.message.delete()
            #TODO logging
            return 'This command must be called in a private channel'
        await ctx.send(await flag_checker.new(args, bot.guilds[0], ctx, logger))
        
    @bot.command()
    async def submit(ctx, *args):
        if 'private' != str(ctx.channel.type):
            await ctx.message.delete()
            #TODO logging
            return 'This command must not be called in private channel'
        
        await ctx.send(await flag_checker.submit(args, bot.guilds[0], ctx, logger))

    @bot.command()
    async def set_ctf_channel(ctx, *args):
        await ctx.send(flag_checker.set_ctf_announcement(args, bot.guilds[0], logger))
            
    @bot.command()
    async def set_ctf_mention(ctx, *args):
        await ctx.send(flag_checker.set_ctf_mention(args, bot.guilds[0], logger))
            
    @bot.command()
    async def leaderboard(ctx, *args):
        await ctx.send(flag_checker.leaderboard(args, logger))
            
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )
    
    json_database.init_challenges()
    json_database.init_credentials()
    json_database.init_users()
    
    logger.info("Starting ChadGPT")
    run_discord_bot()
    logger.info("Stopping ChadGPT")