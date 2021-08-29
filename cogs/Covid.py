from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import requests

class Covid(commands.Cog): #클래스 Covid 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Covid Cog is Ready')
    
    #코로나 현황 명령어
    @commands.command(name = '코로나현황', description = '국내 코로나 발생 현황을 보여줍니다.')
    async def covid(self, ctx):
        url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        date = soup.select_one('span.t_date').text
        boxes = soup.select('div.caseTable > div')

        embed = discord.Embed(
            title = f'국내 코로나 발생 현황 {date}',
            url = url,
            description = '코로나바이러스감염증-19 국내 발생 현황입니다.',
            color = discord.Color.blue()
        )

        #반복문을 이용한 확진자 유형, 누적 인원수, 전일대비 변화량 추출
        for box in boxes:
            patient_type = box.select_one('strong.ca_top').text
            patient_acc = box.select_one('dd.ca_value').text
            try:
                patient_today = box.select_one('span.txt_ntc').text
            except:
                patient_today = box.select_one('p.inner_value').text
            
            embed.add_field(name = patient_type, value = f'누적 : {patient_acc}\n전일대비 : {patient_today}')
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Covid(client))