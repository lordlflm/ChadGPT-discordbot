import discord
import flag_checker

def run_discord_bot():
    DISCORD_TOKEN = 'MTI0MDczNTAyNjM2MzEwNTM3MA.G36MRk.JiXgmf_yNof1-ZwNnx0Z_LZ7DjMhQC7FWss8_c'
    UNRECOGNIZED_CMD = '''Unrecognized command. Shame on you.
Try:
`new("challenge name", "flag", points)`
or
`check("challenge name", "flag")`'''

    client_intents = discord.Intents(messages=True, message_content=True)
    client = discord.Client(intents=client_intents)

    @client.event
    async def on_ready():
        print("Bot running!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        channel = str(message.channel)
        content = str(message.content)

        if 'Direct Message' in channel:
            if content.startswith('check'):
                await message.channel.send(flag_checker.check(content))
            elif content.startswith('new'):
                await message.channel.send(flag_checker.new(content))
            else:
                await message.channel.send(UNRECOGNIZED_CMD)
        else:
            #TODO block `m!play in certain channels`
            pass
            
    client.run(DISCORD_TOKEN)