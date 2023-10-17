
from __future__ import print_function

import os.path

import datetime

import time

# import discord
import discord
from discord.ext import commands


# inits discord bot    
def init_bot(): 
    intents = discord.Intents.default()
    intents.message_content = True
    
    global bot
    bot = commands.Bot(command_prefix='/', intents=intents)
    
    @bot.command()
    async def repeat(ctx, *args):
        await ctx.message.delete()
        await ctx.send(' '.join(args))

    
    @bot.command()
    async def decree(ctx, *args):
        
        await ctx.message.delete()
        
        string = ""
        
        for role in ctx.author.roles:
            if role.name == "President":
                string += '@everyone BY THE ORDER OF PRESIDENT ROSS, I DO DOTH DECLARE: \n\n " '
            if role.name == "Vice President":
                string += '@everyone BY THE ORDER OF VICE PRESIDENT CAIMAN, I DO DOTH DECLARE: \n\n " '
            if role.name == 'Club Mod':
                string += '@everyone BY THE ORDER OF CLUB MODERATOR, MS. CRISSY, I DO DOTH DECLARE: \n\n " '
            if ctx.author.name == "Renblas":
                string += '@everyone BY THE ORDER OF MY CREATOR, CALEB THE ANCIENT ONE, I DO DOTH DECREE: \n\n " '
            
        if string == "":
            await ctx.send("You are a peasant and therefore cannot decree")
            return
                
        string += ' '.join(args)
        string += ' " \n\n IN THE NAME OF THE LORD ALMIGHTY, THY MESSAGE IS PROCLAIMED'
        
        await ctx.send(string)

        
    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')


# main function
def main():
        
    try:
        init_bot()
        print("Discord... YAY")
    except:
        print("Discord Bad")
        quit()
        
    with open("bot.env") as f:
        TOKEN = f.read()
        bot.run(TOKEN)


main()
