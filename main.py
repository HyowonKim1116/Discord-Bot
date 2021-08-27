from discord.ext import commands
import discord
import os

def main():
    prefix = '!'
    intents = discord.Intents.all()

    client = commands.Bot(command_prefix = prefix, intents = intents, help_command = None)

    #새로운 멤버 환영 함수
    @client.event
    async def on_member_join(member):
        if member.dm_channel:
            channel = member.dm_channel
        else:
            channel = await member.create_dm()
        name = member.name
        await channel.send(f'{name}님, 안녕하세요! 참깨월드에 오신 것을 환영합니다.\n`!도움말`을 입력하여 명령어 목록을 확인하세요.')
    
    #Cog 새로고침 함수
    @client.command(name = '새로고침')
    async def cog_reload(ctx, extension):
        try:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} 파일 새로고침 완료!')
        except:
            await ctx.send(f'{extension} 파일은 존재하지 않습니다.')

    for filename in os.listdir('./cogs'):
        if '.py' in filename:
            filename = filename.replace('.py', '')
            client.load_extension(f'cogs.{filename}')

    with open('token.txt', 'r') as f:
        client.run(f.read())

if __name__ == '__main__':
    main()
