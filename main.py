import discord
from discord.ext import commands
import flag_checker
import os
from dotenv import load_dotenv

def run_discord_bot():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    #client = discord.Client(intents=client_intents)
    bot = commands.Bot(command_prefix='!', intents=intents)

    # @client.event
    # async def on_ready():
    #     print("Bot running!")

    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return
        
    #     channel = str(message.channel)
    #     content = str(message.content)

    #     if 'Direct Message' in channel:
    #         if content.startswith('check'):
    #             await message.channel.send(flag_checker.check(content))
    #         elif content.startswith('new'):
    #             await message.channel.send(flag_checker.new(content))
    #         else:
    #             await message.channel.send(UNRECOGNIZED_CMD)
    #     else:
    #         #TODO block `m!play in certain channels`
    #         pass
    
    @bot.command()
    async def new(ctx, *args):
        try:
            if len(args) == 5:
                await ctx.send(flag_checker.new(args[0], args[1], args[2], args[3], args[4]))
            elif len(args) == 3:
                await ctx.send(flag_checker.new(args[0], args[1], args[2]))
            else:
                raise IndexError
        except IndexError:
            #TODO wrong number of arguments
            print('wrong number of arguments')
            return
        
    @bot.command()
    async def submit(ctx, *args):
        try:
            await ctx.send(flag_checker.submit(args[0], args[1]))
        except IndexError:
            #TODO wrong number of arguments
            print('wrong number of arguments')
            return
            
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    run_discord_bot()