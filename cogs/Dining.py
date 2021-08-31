from bs4 import BeautifulSoup
from discord.ext import commands
from .module.mangoplate import *
import discord
import requests

class Dining(commands.Cog): #클래스 Dining 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Dining Cog is Ready')
    
    #맛집 명령어
    @commands.command(name = '맛집', description = '맛집 검색 결과를 보여줍니다.')
    async def dining(self, ctx, *, keyword):
        url = 'https://www.mangoplate.com/search/' + keyword
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select('li.server_render_search_result_item > div.list-restaurant-item')
        
        #키워드를 검색했을 때 맛집이 존재하지 않는 경우
        if data == []:
            embed = discord.Embed(
                title = '오류 발생',
                description = '해당 키워드에 대한 맛집이 검색되지 않았습니다.',
                color = discord.Color.dark_red()
            )
            await ctx.send(embed = embed)
            raise commands.CommandError('No restaurant was found for these keywords.')
        #키워드를 검색했을 때 맛집이 존재하는 경우
        else:
            embed = discord.Embed(
                title = '맛집 준비',
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

def setup(client):
    client.add_cog(Dining(client))