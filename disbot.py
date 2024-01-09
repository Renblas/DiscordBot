
from __future__ import print_function

import os
import subprocess

import datetime

import re

import time

import validators

# import discord
import discord
from discord.ext import commands


regex = None

# ============================================================================ #
#                               Utility Functions                              #
# ============================================================================ #

# runs command in terminal
def run_cmd(inputstr):
    return subprocess.Popen(inputstr, shell=True, stdout=subprocess.PIPE).stdout.read().decode()


# checks if author has permissions
def check_perms(ctx, arr):
    for n in arr:
        if n == ctx.author.name:
            return True
    return False


# inits discord bot    
def init_bot(): 
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    global bot
    bot = commands.Bot(command_prefix='/', intents=intents)
    
    # ============================================================================ #
    #                               General Commands                               #
    # ============================================================================ #
    
    @bot.command()
    async def repeat(ctx, *args):
        await ctx.send(' '.join(args))
        
    @bot.command()
    async def repndel(ctx, *args):
        await ctx.message.delete()
        await ctx.send(' '.join(args))
        
    @bot.event
    async def on_ready():
        print(f"Logging in as {bot.user}")
        

	# ============================================================================ #
	#                                 CGHS Commands                                #
	# ============================================================================ #s
    
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
        
    
    # ============================================================================ #
    #                                Commands For Me                               #
    # ============================================================================ #
    
    @bot.command()
    async def getsong(ctx, *args):
        
		# getsong command
		getsong = "yt-dlp -x --audio-format flac --audio-quality 1 --embed-thumbnail "
  
        # Check for injection
        if not validators.url(args[1]):
            await ctx.send("Invalid URL")
            return
        
        #	Download
        os.system("mkdir /jellyfin/Music/'" + args[0] + "'")
        await ctx.send("Downloading song(s) to folder '" + args[0] + "'.")
        os.system("cd /jellyfin/Music" + args[0] + " " + getsong + args[1])
        await ctx.send("Downloading Finished.")
        
        
        
    @bot.command()
    async def rokualarm(ctx, *args):
        pass
    
    
    # ============================================================================ #
    #                                 Help Commands                                #
    # ============================================================================ #
        

# main function
def main():
    global regex 
    regex = re.compile(r"\[38;2(;\d{,3}){3}m")
        
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
