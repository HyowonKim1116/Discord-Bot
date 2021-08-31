from discord.ext import commands
from random import choice
import csv
import discord

class Hangman(commands.Cog): #클래스 Hangman 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
        self.wordDict = {}
        with open('./data/word.csv', 'r', encoding = 'utf-8') as f:
            for row in csv.reader(f):
                self.wordDict[row[0]] = row[1]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Hangman Cog is Ready')
    
    #행맨 게임 시작 명령어
    @commands.command(name = '행맨시작', description = '행맨 게임을 진행합니다.')
    async def hangman(self, ctx):
        
        #메시지 유효성 검사 함수
        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        engWord = choice(list(self.wordDict.keys()))
        korWord = self.wordDict[engWord]
        problem = ['＿' for _ in range(len(engWord))]
        try_cnt = len(engWord) * 2
        print(f'=> 행맨 정답: {engWord}')

        embed = discord.Embed(
            title = '행맨 게임 시작',
            description = f'채워야 하는 글자는 **{len(engWord)}개**입니다!\n기회는 총 {try_cnt}번입니다.',
            color = discord.Color.blue()
        )
        await ctx.send(embed = embed)
        
        explain = ''
        embedColor = discord.Color.blue()
        inputList = []
        total_answer = 0

        while True:
            #영단어의 철자수만큼 밑줄 생성
            letters = problem[0]
            for i in range(1, len(problem)):
                letters += f' {problem[i]}'
            
            rest = len(engWord) - total_answer
            if rest == 0:
                description = '단어의 모든 글자를 채웠습니다!'
            elif try_cnt == 0:
                description = f'기회를 모두 소진했습니다.\n남은 글자: {rest}, 남은 기회: 0'
            else:
                description = f'소문자 a~z 중에서 하나를 입력하세요!\n남은 글자: {rest}, 남은 기회: {try_cnt}'
                        
            embed = discord.Embed(
                title = letters,
                description = explain + description,
                color = embedColor
            )
            await ctx.send(embed = embed)

            #반복문 종료 조건
            if (rest == 0) or (try_cnt == 0): break

            try_cnt -= 1
            message = await self.client.wait_for('message', check = check_message)
            inputLetter = message.content

            #'행맨종료'를 입력한 경우
            if '행맨종료' in inputLetter:
                embed = discord.Embed(
                    title = '행맨 게임 종료',
                    description = '행맨 게임을 종료합니다.',
                    color = discord.Color.red()
                )
                await ctx.send(embed = embed)
                break
            #이전에 입력했던 글자를 다시 입력한 경우
            elif inputLetter in inputList:
                explain = f'`{inputLetter} => 이미 입력한 글자`\n'
                embedColor = discord.Color.dark_red()
                continue
            
            #새로운 글자를 입력한 경우
            curr_answer = 0
            inputList.append(inputLetter)
            for i in range(len(engWord)):
                if engWord[i] == inputLetter:
                    problem[i] = inputLetter
                    curr_answer += 1
            
            #단어에 포함된 글자를 입력한 경우
            if curr_answer:
                total_answer += curr_answer
                explain = f'`{inputLetter} => 단어에 포함된 글자`\n'
                embedColor = discord.Color.dark_green()
            #단어에 포함되지 않은 글자를 입력한 경우
            else:
                explain = f'`{inputLetter} => 단어에 포함되지 않은 글자`\n'
                embedColor = discord.Color.dark_red()
                
        #모든 글자를 채우지 못한 경우 (게임 패배)
        if rest:
            embed = discord.Embed(
                title = '행맨 게임 패배',
                description = '아쉽습니다. 다음에 또 도전해주세요!',
                color = discord.Color.red()
            )
        #모든 글자를 채운 경우 (게임 승리)
        else:
            embed = discord.Embed(
                title = '행맨 게임 승리',
                description = '축하합니다. 다음에 또 도전해주세요!',
                color = discord.Color.blue()
            )
        
        embed.add_field(name = f'정답: {engWord}', value = korWord)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Hangman(client))