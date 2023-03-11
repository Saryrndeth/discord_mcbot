import discord
from discord.ext import commands
import time

from mcpi.minecraft import Minecraft 
mc = Minecraft.create()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())




'''
봇이 반응을 해야하는 명령어인지 구분하기 위해 메세지 앞에 붙이는 접두사(prefix)를 설정합니다. 현재 !로 
설정되어있습니다. 이곳을 변경시 해당 문자로 명령어를 시작해야합니다. ext에선 discord.Client처럼 
str.startswith 메서드를 사용할 필요가 없습니다.
'''

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) # 토큰으로 로그인 된 bot 객체에서 discord.User 클래스를 가져온 뒤 name 프로퍼티를 출력
    print(bot.user.id) # 위와 같은 클래스에서 id 프로퍼티 출력
    print('------')

@bot.command()
async def 감지(ctx):
    # try :
        while True:
                # 블록 히트 이벤트 가져오기
            blockHits = mc.events.pollBlockHits()
            chatPosts = mc.events.pollChatPosts()
            for blockHit in blockHits:
            # 버튼 블록인지 확인
                block = mc.getBlockWithData(blockHit.pos)
                # for chatPost in chatPosts:
                #     print(chatPost.message)
                print(block)
                if block.id == 77 or block.id == 143:  # 버튼 블록 ID
                    player = mc.entity.getName(blockHit.entityId)
                    await ctx.send(">>> 버튼 눌림 : {0}".format(player))
                    time.sleep(0.2) # 디바운스 대기
        
            for chatPost in chatPosts:
                player = mc.entity.getName(chatPost.entityId)
                await ctx.send(">>> <{0}> {1}".format(player, chatPost.message))
    # except :
    #     pass     

@bot.command()
async def bt(ctx):
    await ctx.send("!명령 gamemode survival Saryrndeth")

bot.run('MTA3NjE3NzAyMzc0OTMyODk0Nw.G9mauZ.mIyn2w1p99B4vElRk5dTP_f5RvLZs2fsy9HSj4')