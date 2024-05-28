import flag_checker
import prevent_commands

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


def run_discord_bot():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
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
            return
        try:
            if len(args) == 5:
                await ctx.send(flag_checker.new(args[0], args[1], args[2], args[3], args[4]))
            elif len(args) == 3:
                await ctx.send(flag_checker.new(args[0], args[1], args[2]))
            else:
                raise IndexError
        except IndexError:
            await ctx.send('Wrong number of arguments. Usage: `!new <challenge_name> <challenge_url> <challenge_value>`')
        
    @bot.command()
    async def submit(ctx, *args):
        if 'private' != str(ctx.channel.type):
            return
        try:
            await ctx.send(flag_checker.submit(args[0], args[1]))
        except IndexError:
            await ctx.send('Wrong number of arguments. Usage: `!submit <challenge_name> <flag>`')

            
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    run_discord_bot()
    #TODO testing
    # flag_checker.submit('Stonks', 'picoCTF{s4n1ty_v3r1f13d_f28ac910}')