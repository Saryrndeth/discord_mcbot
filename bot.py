# This example requires the 'message_content' intent.

import discord
from discord.ext import commands

# intents = discord.Intents.all()
# intents.message_content = True

client = commands.Bot(command_prefix = "!", intents=discord.Intents.all())




@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.command()
async def hello(ctx):
    await ctx.send("Hello!")
    
@client.command(pass_context = True)
async def join(ctx):
        
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        # if(ctx.is_connected() == True):
        #     await channel.move_to(channel)
        await channel.connect()
    else :
        await ctx.send("먼저 음성채널에 입장해주세요.")
        voice_client = get(ctx.bot.voice_clients)
        print(voice_client.is_connected())

client.run('MTA3NTEwODExNDM5Njg4OTI0OQ.GX6HzI.j5UYiRmigbBZompMOu-UjLtLCBD32i1Mfgf9nc')