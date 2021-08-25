from discord.ext import commands
import discord
import os

def main():
    prefix = '!'
    intents = discord.Intents.all()

    client = commands.Bot(command_prefix = prefix, intents = intents)

    for filename in os.listdir('./cogs'):
        if '.py' in filename:
            filename = filename.replace('.py', '')
            client.load_extension(f'cogs.{filename}')

    with open('token.txt', 'r') as f:
        client.run(f.read())

if __name__ == '__main__':
    main()
