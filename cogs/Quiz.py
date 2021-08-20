from discord.ext import commands
from random import choice
import asyncio
import csv
import discord
import json

class Quiz(commands.Cog): #클래스 Quiz 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
        self.quizDict = {}
        with open('./data/quiz.csv', 'r', encoding = 'utf-8') as f:
            for row in csv.reader(f):
                self.quizDict[row[0]] = row[1]
        with open('./data/score.json', 'r', encoding = 'utf-8') as f:
            self.scoreDict = json.load(f)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Quiz Cog is Ready')
    
    #퀴즈 명령어
    @commands.command(name = '퀴즈')
    async def quiz(self, ctx):
        name = ctx.author.name
        problems = list(self.quizDict.keys())
        problem = choice(problems)
        answer = self.quizDict[problem]
        embed = discord.Embed(
            title = '퀴즈',
            description = problem,
            color = discord.Color.blue()
        )
        await ctx.send(embed = embed)

        #퀴즈를 채점하는 함수
        def check_answer(message):
            if (message.channel == ctx.channel) and (answer in message.content):
                return True
            else:
                return False
        
        #10초 안에 정답을 맞힌 경우
        try:
            message = await self.client.wait_for('message', timeout = 10.0, check = check_answer)
            name = message.author.name
            embed = discord.Embed(
                title = '',
                description = f'**{name}**님, 정답입니다!',
                color = discord.Color.blue()
            )
            await ctx.send(embed = embed)
            score = 1
        #10초 안에 정답을 맞히지 못한 경우
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title = '',
                description = f'땡! 시간초과입니다~ 정답은 **{answer}**입니다!',
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
            score = 0
        
        #scoreDict에 참가자의 이름이 있을 경우 (점수 갱신)
        try:
            self.scoreDict[name] += score
        #scoreDict에 참가자의 이름이 없을 경우 (점수 생성)
        except KeyError:
            self.scoreDict[name] = score
        
        with open('./data/score.json', 'w', encoding = 'utf-8') as f:
            json.dump(self.scoreDict, f, ensure_ascii = False)
    
    #퀴즈 랭킹 명령어
    @commands.command(name = '퀴즈랭킹')
    async def show_ranking(self, ctx, *, player = None):
        rankDict = dict(sorted(self.scoreDict.items(), key = lambda x: x[1], reverse = True))
        people = list(rankDict.keys()) #퀴즈 참가자 리스트
        
        #퀴즈 참가자가 없을 경우
        if len(people) == 0:
            embed = discord.Embed(
                description = '현재까지 퀴즈에 참여한 사람이 없습니다.',
                color = discord.Color.red()
            )
        
        #개인 퀴즈 랭킹
        elif player != None:
            #참가한 사람의 이름을 입력한 경우
            try:
                score = rankDict[player]
                rank = people.index(player) + 1
                embed = discord.Embed(
                    title = '개인 퀴즈 랭킹',
                    description = '개인 퀴즈 랭킹입니다.',
                    color = discord.Color.blue()
                )
                embed.add_field(
                    name = player,
                    value = f'{player}님은 {score}점으로, 전체 {len(people)}명 중 {rank}등입니다.',
                    inline = False
                )
            #참가하지 않은 사람의 이름을 입력한 경우
            except KeyError:
                embed = discord.Embed(
                    description = f'{player}님의 랭킹 정보는 존재하지 않습니다.',
                    color = discord.Color.red()
                )
        
        #전체 퀴즈 랭킹
        else:
            embed = discord.Embed(
                title = '전체 퀴즈 랭킹',
                description = '전체 퀴즈 랭킹입니다.\n한 문제를 맞힐 때마다 1점씩 증가해요!',
                color = discord.Color.blue()
            )
            
            for i in range(len(people)):
                embed.add_field(
                    name = f'{i+1}등 - {people[i]}',
                    value = f'점수 : {rankDict[people[i]]}점',
                    inline = False
                )
            
            #사용자가 퀴즈에 참가한 경우
            try:
                name = ctx.author.name
                rank = people.index(name) + 1

                #사용자가 1등인 경우
                if rank == 1:
                    txt = '`당신을 퀴즈왕으로 인정합니다!`'
                #사용자가 1등이 아닌 경우
                else:
                    gap = rankDict[people[rank-2]] - rankDict[people[rank-1]]
                    txt = f'`{rank-1}등과의 점수 차이는 {gap}점입니다!`'
                
                embed.add_field(
                    name = 'ㅤ',
                    value = f'`현재 {name}님은 {rank}등입니다.`\n' + txt,
                    inline = False
                )
            #사용자가 퀴즈에 참가하지 않은 경우
            except ValueError:
                embed.add_field(
                    name = 'ㅤ',
                    value = f'`{name}님의 랭킹 정보는 존재하지 않습니다.\n퀴즈에 도전해보세요!`',
                    inline = False
                )
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Quiz(client))
