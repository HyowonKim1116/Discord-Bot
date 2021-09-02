from discord.ext import commands
import discord

class Help(commands.Cog): #클래스 Help 선언, commands.Cog 상속
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help Cog is Ready')
    
    #도움말 명령어
    @commands.command(name = '도움말', description = '명령어 목록을 보여줍니다.')
    async def help(self, ctx):
        embed = discord.Embed(
            title = '참깨봇 명령어 목록',
            color = discord.Color.purple()
        )
        
        for name, cog in self.client.cogs.items():
            commandList = ''
            for command in cog.walk_commands():
                commandList += f'```!{command.name} {command.signature}```{command.description}\n'
            commandList += '\n'
            embed.add_field(name = name, value = commandList, inline = False)
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Help(client))