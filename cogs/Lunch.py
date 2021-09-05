from discord.ext import commands
from random import choice
import discord
import json

class Lunch(commands.Cog): #클래스 Lunch 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
        with open('./data/lunch.json', 'r', encoding = 'utf-8') as f:
            self.lunchDict = json.load(f)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Lunch Cog is Ready')
    
    #점심 추천 명령어
    @commands.command(name = '점심추천', description = '점심 메뉴를 추천합니다. 원하는 음식 종류를 입력할 수 있습니다.')
    async def lunch(self, ctx, arg1 = None, arg2 = None):
        try:
            #음식 종류를 입력하지 않은 경우
            if (arg1 == None) and (arg2 == None):
                category = choice(list(self.lunchDict.keys()))
                lunch = choice(self.lunchDict[category])
                result = f'오늘 점심은 {category}, 그 중에서 **{lunch}** 어떠세요?'
            #음식 종류 1개를 입력한 경우
            elif (arg1 != None) and (arg2 == None):
                lunch = choice(self.lunchDict[arg1])
                result = f'오늘 점심은 **{lunch}** 어떠세요?'
            #음식 종류 2개를 입력한 경우
            else:
                lunch = choice(self.lunchDict[arg1] + self.lunchDict[arg2])
                result = f'{arg1}이랑 {arg2}이면.. 오늘 점심은 **{lunch}** 어떠세요?'
            
            embed = discord.Embed(
                title = '점심 추천',
                description = result,
                color = discord.Color.blue()
            )
        except KeyError:
            #음식 종류를 잘못 입력한 경우
            embed = discord.Embed(
                title = '오류 발생',
                description = '음식 종류는 [한식/중식/양식/일식] 중에서 말씀해주세요!',
                color = discord.Color.dark_red()
            )
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Lunch(client))