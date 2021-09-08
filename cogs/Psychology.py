from discord.ext import commands
from random import choice
import discord
import json

class Psychology(commands.Cog): #클래스 Personality 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
        with open('./data/test.json', 'r', encoding = 'utf-8') as f:
            self.testDict = json.load(f)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Psychology Cog is Ready')
    
    #심리 테스트 명령어
    @commands.command(name = '심리테스트', description = '랜덤 심리 테스트를 진행합니다.')
    async def psychology(self, ctx):
        
        #메시지 유효성 검사 함수
        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        #에러 임베드 함수
        def error_embed(count):
            embed = discord.Embed(
                description = f'답변 번호의 범위는 **1~{count}**입니다. 범위 내의 숫자를 입력해주세요!',
                color = discord.Color.dark_red()
            )
            return embed
        
        question = choice(list(self.testDict.keys()))
        result = self.testDict[question]
        answer = list(result.keys())
        
        example = f'(1) {answer[1]}'
        for i in range(2, len(answer)):
            example += f'\n({i}) {answer[i]}'
        
        embed = discord.Embed(
            title = '심리 테스트',
            description = question,
            color = discord.Color.blue()
        )
        embed.add_field(name = '다음 보기 중 해당되는 답변의 번호를 입력해주세요.', value = example)
        await ctx.send(embed = embed)
        
        while True:
            try:
                message = await self.client.wait_for('message', check = check_message)
                number = int(message.content)
                if number in range(1, len(answer)+1):
                    select = answer[number]
                    break
                else:
                    await ctx.send(embed = error_embed(len(answer)-1))
            except ValueError:
                await ctx.send(embed = error_embed(len(answer)-1))
        
        embed = discord.Embed(
            title = f'{number}번({select}) 선택 결과',
            description = f'당신은 {result[select]}',
            color = discord.Color.purple()
        )
        embed.add_field(name = '더 자세한 설명은', value = result['url'])
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Psychology(client))