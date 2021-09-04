from bs4 import BeautifulSoup
from discord.ext import commands
from random import choice
from .module.mangoplate import *
import discord
import json
import requests

class Recommendation(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('./data/lunch.json', 'r', encoding = 'utf-8') as f:
            self.lunchDict = json.load(f)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Recommendation Cog is Ready')
    
    #점심 맛집 추천 명령어
    @commands.command(name = '점심맛집추천', description = '점심 메뉴를 추천한 후, 현재 위치 근처의 맛집을 추천합니다.')
    async def recommend_restaurant(self, ctx):

        #메시지 유효성 검사 함수
        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        embedTitle = '점심 맛집 추천'
        embedColor = discord.Color.blue()

        while True:
            embed = discord.Embed(
                title = embedTitle,
                description = '[한식/중식/양식/일식] 중에서 하나를 입력해주세요!\n`[추천종료]를 입력하시면 추천 시스템이 종료됩니다.`',
                color = embedColor
            )
            await ctx.send(embed = embed)

            message = await self.client.wait_for('message', check = check_message)
            category = message.content

            try:
                lunch = choice(self.lunchDict[category])
            except KeyError:
                if '추천종료' in category:
                    embed = discord.Embed(
                        title = '추천 종료',
                        description = '점심 맛집 추천을 종료합니다.',
                        color = discord.Color.red()
                    )
                    await ctx.send(embed = embed)
                    break
                else:
                    embedTitle = '오류 발생'
                    embedColor = discord.Color.dark_red()
                    continue

            embed = discord.Embed(
                title = '점심 추천',
                description = f'오늘 점심은 **{lunch}** 어떠세요?\n`메뉴가 마음에 들면 현재 지역명(ex.수원)을,`\n`마음에 들지 않으면 [싫어요]를 입력해주세요!`',
                color = discord.Color.blue()
            )
            await ctx.send(embed = embed)

            message = await self.client.wait_for('message', check = check_message)
            answer = message.content

            #대답이 '싫어요'인 경우
            if '싫어요' in answer:
                embed = discord.Embed(
                    description = '다른 음식을 추천해 드리겠습니다!',
                    color = discord.Color.orange()
                )
                await ctx.send(embed = embed)
                embedTitle = '점심 맛집 추천'
                embedColor = discord.Color.blue()
                continue
            #대답이 현재 지역명인 경우
            else:
                keyword = f'{answer} {lunch}'
                url = 'https://www.mangoplate.com/search/' + keyword
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                data = soup.select('li.server_render_search_result_item > div.list-restaurant-item')
                
                #키워드를 검색했을 때 맛집이 존재하지 않는 경우
                if data == []:
                    embed = discord.Embed(
                        title = '오류 발생',
                        description = f'**{keyword}**에 대한 맛집이 검색되지 않았습니다.\n다른 맛집을 추천해 드리겠습니다!',
                        color = discord.Color.dark_red()
                    )
                    await ctx.send(embed = embed)
                    embedTitle = '점심 맛집 추천'
                    embedColor = discord.Color.blue()
                    continue
                #키워드를 검색했을 때 맛집이 존재하는 경우
                embed = discord.Embed(
                    title = f'{keyword} 맛집 목록',
                    description = '맛집 정보를 준비하고 있어요. 잠시만 기다려주세요!',
                    color = discord.Color.orange()
                )
                await ctx.send(embed = embed)

                #반복문을 이용한 맛집 정보 추출
                for i in range(len(data)):
                    title = getTitle(data[i])
                    category, rating, view, review, link, photo = getInfo(data[i])
                    
                    embed = discord.Embed(
                        title = title,
                        description = category,
                        color = discord.Color.blue()
                    )
                    embed.add_field(name = '평점', value = rating)
                    embed.add_field(name = '조회수', value = view)
                    embed.add_field(name = '리뷰수', value = review)
                    embed.add_field(name = '링크', value = link, inline = False)
                    embed.set_thumbnail(url = photo)
                    await ctx.send(embed = embed)

                    if i == 4: break
                break

def setup(client):
    client.add_cog(Recommendation(client))