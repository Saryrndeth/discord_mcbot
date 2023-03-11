import discord
from discord.ext import commands
import time
import json
import schedule
import os
import sys
import urllib.request
import pymysql

from mcpi.minecraft import Minecraft 
from mcpi.minecraft import Connection

from rcon.source import Client

global mc 
global conn

mc = None
conn = None



try:
    sql_conn = pymysql.connect(host='127.0.0.1', user='root', password='0207', db='server',charset='utf8')
    cur = sql_conn.cursor()
    cur.execute("select * from `server`.`status`")
    stat_result = cur.fetchall()
    cur.execute("select * from `server`.`permission`")
    permission_result = cur.fetchall()
except:
    pass

server_ip = stat_result[0][4]
rcon_password = stat_result[0][3]
bot_token = stat_result[0][0]


client_id = stat_result[0][1]
client_secret = stat_result[0][2]

try :
    mc = Minecraft.create()
    conn = Connection(server_ip, 4711)
except :
    pass

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

host = server_ip
port = 25575  # RCON 포트 번호
password = rcon_password

def sql_refresh():
    cur.execute("select * from `server`.`status`")
    stat_result = cur.fetchall()
    cur.execute("select * from `server`.`permission`")
    permission_result = cur.fetchall()

def check(author):
    # f = open("C:\\Users\\iou2b\\Downloads\\minecraft_python\\python\\permission.txt", 'r')
    # while True:
    #     line = f.readline()
    #     if not line : break
    #     if int(author) == int(line):
    #         f.close() 
    #         return True
    # f.close()
    # return False
    if len(permission_result) == 0:
        return False
    for i in permission_result[0]:
        if int(author) == int(i):
            return True
    return False

def re_connect():
    global mc
    global conn
    if mc != None and conn != None:
        return
    try:
        mc = Minecraft.create()
        conn = Connection(server_ip, 4711)
        if mc != None and conn != None:
            return True
    except:
        return False
    
    
def ToEN (Text, lang) :
    encText = urllib.parse.quote(Text)
    data = "source={0}&target=en&text=".format(lang) + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        print(d['message']['result']['translatedText'])
        return d['message']['result']['translatedText'] 
    else:
        print("Error Code:" + rescode)
        
def checklang (Text) :
    encQuery = urllib.parse.quote(Text)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        print(d['langCode'])
        return d['langCode']
    else:
        print("Error Code:" + rescode)
        
def NtoR (Name) :
    encText = urllib.parse.quote(Name)
    url = "https://openapi.naver.com/v1/krdict/romanization?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        return d['aResult'][0]['aItems'][0]
        
    else:
        print("Error Code:" + rescode)


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
    print(mc, conn)
    print('------')
    print(stat_result)
    print(permission_result)
    if mc == None:
        print("서버에 연결할 수 없음.")

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms') # 봇의 핑을 pong! 이라는 메세지와 함께 전송한다. latency는 일정 시간마다 측정됨에 따라 정확하지 않을 수 있다.

@bot.command(name="1234")
async def _12345(ctx):
        await ctx.send("5678")
    
#파이썬 문법에 따라 함수를 만들 때에는 첫글자에는 숫자를 넣을 수 없는데, 숫자를 사용하고싶다면 함수 이름 자리는 다른 아무것으로 대체하고 괄호 안에 name=""을 사용하여 명령어를 제작할 수 있다.


@bot.command()
async def isc(ctx):
    await ctx.message.author.voice.channel.connect()

@bot.command()
async def move(ctx , *arg):
    member = ctx.guild.get_member_named(arg[0])
    if member != None and len(arg) == 1:
        await ctx.send("사용자는 입력되었지만 채널이 입력되지 않았습니다. 채널을 입력해주세요")
        return
    if member != None:
        await member.move_to(discord.utils.get(ctx.guild.channels, name = "{0}".format(arg[1])))
    else :
        await ctx.message.author.move_to(discord.utils.get(ctx.guild.channels, name = "{0}".format(arg[0])))


@bot.command()
async def guild(ctx, arg):
    await ctx.send(commands.VoiceChannelConverter('{0}'.format(arg)))
    
@bot.command()
async def 박서준(ctx):
    await ctx.send("병신")
    
@bot.command()
async def 좌표(ctx, *arg):
    if mc == None: return await ctx.send("서버에 연결할 수 없습니다.")
    if len(arg) == 0:
        playerList = mc.getPlayerEntityIds()
        for playerId in playerList:
            player = mc.entity.getName(playerId)
            pos = mc.entity.getTilePos(playerId)
            pos.x += 16
            pos.y += 69
            pos.z -= 32
            real_pos = str(pos.x) + ", " + str(pos.y) + ", " + str(pos.z)
            if playerId == playerList[0]:
                string = ">>> {0} 의 좌표 : ({1})".format(player, real_pos)
                continue
            string += "\n\n{0} 의 좌표 : ({1})".format(player, real_pos)
        await ctx.send(string)
        return
    if len(arg) > 1:
        string = ""
        for i in range(len(arg)):
            try :
                pos = mc.entity.getTilePos(mc.getPlayerEntityId(arg[i]))
                pos.x += 16
                pos.y += 69
                pos.z -= 32
                real_pos = str(pos.x) + ", " + str(pos.y) + ", " + str(pos.z)
                if i == 0 :
                    string = ">>> {0} 의 좌표 : ({1})".format(arg[0], real_pos)
                    continue
                string += "\n\n{0} 의 좌표 : ({1})".format(arg[i], real_pos)
            except :
                break
        await ctx.send(string)
        return 
    pos = mc.entity.getTilePos(mc.getPlayerEntityId(arg[0]))
    pos.x += 16
    pos.y += 69
    pos.z -= 32
    real_pos = str(pos.x) + ", " + str(pos.y) + ", " + str(pos.z)
    await ctx.send(">>> {0} 의 좌표 : ({1})".format(arg[0], real_pos))

@bot.command()
async def 엔티티(ctx):
    entityIds = mc.getPlayerEntityIds()
    await ctx.send(entityIds)
    
@bot.command()
async def 테스트(ctx):
    await ctx.send(chatEvents)
    
# @bot.command()
# async def 감지(ctx):
#     while True:
#         # 블록 히트 이벤트 가져오기
#         blockHits = mc.events.pollBlockHits()
#         for blockHit in blockHits:
#         # 버튼 블록인지 확인
#             block = mc.getBlockWithData(blockHit.pos)
#             if block.id == 77:  # 버튼 블록 ID
#                 await ctx.send("버튼 눌림")
#                 time.sleep(0.2) # 디바운스 대기 

@bot.command()
async def 명령(ctx, *arg):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        try:
            string = ""
            for i in range(len(arg)):
                if i == 0:
                    string = arg[i]
                    continue
                string += " " + arg[i]
            words = string.split()
            with Client(host, port, passwd=password) as client:
                response = client.run(*words)
            if response == "" :
                await ctx.send(">>> 반응 메시지가 비어있습니다.")
                return    
            await ctx.send(">>> {0}".format(response))
        except :
            await ctx.send("서버에 연결할 수 없습니다.")
        
@bot.command()
async def 관리자추가(ctx, *arg):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        if len(arg) == 0:
            await ctx.send("관리자로 추가할 유저의 이름 또는 ID를 입력해주세요.")
            return
        f = open("C:\\Users\\iou2b\\Downloads\\minecraft_python\\python\\permission.txt", 'a')
        for i in range(len(arg)):
            data = "\n{0}".format(arg[i])
            f.write(data)
            await ctx.send("유저 id({0})가 관리자로 추가되었습니다.".format(arg[i]))
        f.close()
        
@bot.command()
async def 관리자제거(ctx, *arg):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        if len(arg) == 0:
            await ctx.send("관리자로 제거할 유저의 이름 또는 ID를 입력해주세요.")
            return
        with open("C:\\Users\\iou2b\\Downloads\\minecraft_python\\python\\permission.txt", 'r') as f:
            lines = f.readlines()
        with open("C:\\Users\\iou2b\\Downloads\\minecraft_python\\python\\permission.txt", 'w') as f:
            for i in range(len(arg)):
                for line in lines:
                    if line.strip("\n") != arg[i] :
                        f.write(line)
                        await ctx.send("유저 id({0})가 관리자에서 제거되었습니다.".format(arg[i]))
        f.close()                
                    
        

@bot.command()
async def 관리자목록(ctx):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        f = open("C:\\Users\\iou2b\\Downloads\\minecraft_python\\python\\permission.txt", 'r')
        lines = f.readlines()
        await ctx.send(">>> {0}".format((str(lines).strip('[')).strip(']')))
        f.close()
        

@bot.command()
async def 마크_관리자목록(ctx):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        with open('C:\\Users\\iou2b\\Downloads\\minecraft_python\\ops.json') as f:
            json_object = json.load(f)
        string = ""    
        for i in range(len(json_object)):
            if i == 0:
                string = ">>> " +  str(json_object[i]["name"]) + "\n"
                continue
            string += str(json_object[i]["name"])+ "\n"
            
        await ctx.send(string);

@bot.command()
async def 재연결(ctx):
    sql_refresh()
    print(mc, conn)
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        if mc != None and conn != None:
            return await ctx.send("서버에 연결되어있습니다.")
        if re_connect() == True:
            await ctx.send("서버에 재연결되었습니다.")
        else :
            await ctx.send("서버에 재연결 할 수 없습니다.")
            
@bot.command()
async def 연결해제(ctx):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        global mc
        global conn
        if mc == None and conn == None:
            return await ctx.send("서버에 연결되어 있지 않습니다.")
        mc = None
        conn = None
        await ctx.send("연결이 해제되었습니다.")
        
@bot.command()
async def 종료(ctx):
    sql_refresh()
    if check(ctx.message.author.id) != True:
        await ctx.send("권한이 없습니다.")
    else:
        await ctx.send("종료됩니다.")
        await bot.close()
        
@bot.command()
async def 번역(ctx, *arg):
    if arg == None:
        await ctx.send("API by 네이버 파파고")
        return
    string = ""
    for word in arg :
        string += word
    await ctx.send(ToEN(string, checklang(string)))
    
@bot.command()
async def 언어감지(ctx, *arg):
    string = ""
    for word in arg :
        string += word
    await ctx.send(checklang(string))
    
@bot.command()
async def 로마자이름(ctx, arg):
    await ctx.send(NtoR(arg)['name'] + " / 점수 : {0}".format(NtoR(arg)['score']))

bot.run(bot_token)


