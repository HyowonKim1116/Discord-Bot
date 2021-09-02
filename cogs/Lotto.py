from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import requests

class Lotto(commands.Cog): #클래스 Lotto 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Lotto Cog is Ready')
    
    #로또 결과 명령어
    @commands.command(name = '로또결과', description = '로또 당첨번호와 1등 당첨금액을 보여줍니다.')
    async def lotto(self, ctx):
        url = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one('div.win_result > h4').text
        date = soup.select_one('p.desc').text[1:-4]
        balls = soup.select('span.ball_645')
        money = soup.select('td.tar')[1].text

        #당첨번호 문자열 생성
        nums = ', '.join([balls[i].text for i in range(6)])

        embed = discord.Embed(
            title = f'로또 {title}',
            url = url,
            description = f'{date}에 추첨한 결과입니다.',
            color = discord.Color.blue()
        )
        embed.add_field(name = '당첨번호', value = nums)
        embed.add_field(name = '보너스', value = balls[6].text)
        embed.add_field(name = '1등 당첨금액 (개당)', value = money, inline = False)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Lotto(client))