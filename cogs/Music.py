from discord.ext import commands
from os.path import abspath
from youtube_dl import YoutubeDL
from .module.youtube import *
import discord

class Music(commands.Cog): #클래스 Music 선언, commands.Cog 상속
    def __init__(self, client):
        option = {
            'format': 'bestaudio/best',
            'noplaylist': True
        }
        self.client = client
        self.DL = YoutubeDL(option)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music Cog is Ready')
    
    #음악 재생 명령어
    @commands.command(name = '음악재생', description = '키워드를 유튜브에서 검색해 음악을 재생합니다.')
    async def play_music(self, ctx, *, keyword):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(
                    title = '오류 발생',
                    description = '음성 채널에 들어간 후 명령어를 사용해주세요!',
                    color = discord.Color.dark_red()
                )
                await ctx.send(embed = embed)
                raise commands.CommandError('Author is not connected to a voice channel.')
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        
        #키워드를 검색했을 때 음악이 존재하는 경우
        try:
            data = self.DL.extract_info(getUrl(keyword), download = False)
            await ctx.send(embed = getEmbed(data))
        #키워드를 검색했을 때 음악이 존재하지 않는 경우
        except:
            embed = discord.Embed(
                title = '오류 발생',
                description = '해당 키워드에 대한 음악이 검색되지 않았습니다.',
                color = discord.Color.dark_red()
            )
            await ctx.send(embed = embed)
            raise commands.CommandError('No music was found for these keywords.')

        embed = discord.Embed(
            title = '음악 준비',
            description = '음악 재생을 준비하고 있어요. 잠시만 기다려주세요!',
            color = discord.Color.orange()
        )
        await ctx.send(embed = embed)
        
        ffmpeg_path = abspath('ffmpeg/bin/ffmpeg')
        ffmpeg_options = {
            'options': '-vn',
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }

        player = discord.FFmpegPCMAudio(data['url'], **ffmpeg_options, executable = ffmpeg_path)
        ctx.voice_client.play(player)

        embed = discord.Embed(
            title = '음악 재생',
            description = '**%s**\n재생을 시작합니다! (재생 시간:%s)'%(data['title'], getTime(data)),
            color = discord.Color.blue()
        )
        await ctx.send(embed = embed)
    
    #음악 종료 명령어
    @commands.command(name = '음악종료', description = '현재 재생 중인 음악을 종료합니다.')
    async def quit_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(
                title = '음악 종료',
                description = '음악 재생을 종료합니다.',
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
    
    #음악 일시정지 명령어
    @commands.command(name = '일시정지', description = '현재 재생 중인 음악을 일시정지합니다.')
    async def pause_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()
            embed = discord.Embed(
                description = '음악 재생을 일시정지합니다.',
                color = discord.Color.purple()
            )
            await ctx.send(embed = embed)
    
    #음악 재개 명령어
    @commands.command(name = '다시시작', description = '멈춘 부분부터 음악을 재생합니다.')
    async def resume_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_paused():
            voice.resume()
            embed = discord.Embed(
                description = '멈춘 부분부터 음악을 재생합니다.',
                color = discord.Color.purple()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Music(client))
