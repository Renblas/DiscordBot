
from __future__ import print_function

import os
import subprocess

import re

import validators
import json

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


# ============================================================================ #
#                              Jellyfin Functions                              #
# ============================================================================ #

JELLYFIN_SERVER='http://127.0.0.1:8096'
JELLYFIN_API_KEY=open("jellyapi.env").read()

if JELLYFIN_API_KEY is None:
    print("No supplied Jellyfin API Key...")


def jf_media_updated(mediapaths):
    reqdata = { 'Updates': [{'Path': p} for p in mediapaths] }
    reqstr = json.dumps(reqdata)
    print(reqstr)
    command = ['curl', '-v',
        '-H','Content-Type: application/json',
        '-H','X-MediaBrowser-Token: '+JELLYFIN_API_KEY,
        '-d',reqstr,
        JELLYFIN_SERVER+'/Library/Media/Updated']
    subprocess.run(command)

def jf_refresh():
    command = ['curl', '-v',
        '-H','X-MediaBrowser-Token: '+JELLYFIN_API_KEY,
        '-d','',
        JELLYFIN_SERVER+'/Library/Refresh']
    subprocess.run(command)


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
        #print(discord.Client.get_user("renblas"))
        
        

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
  
        # Check for injection
        if not validators.url(args[1]):
            await ctx.send("Invalid URL")
            return
        
        path=args[0].replace("-", "\ ")
        
        # getsong command
        getsong = "yt-dlp -x --audio-format flac --audio-quality 1 --embed-thumbnail -P /jellyfin/Music/{path}/ "
        
        # Download
        os.system("mkdir /jellyfin/Music/'" + args[0].replace("-", "\ ") + "'")
        await ctx.send("Downloading song(s) to folder '" + args[0] + "'.")
        subprocess.run(getsong + args[1])
        await ctx.send("Downloading Finished.")
        jf_refresh() 
        await ctx.send("Reloading Jellyfin Library...")
        
        
        
    @bot.command()
    async def rokualarm(ctx, *args):
        pass
    
    
    @bot.command()
    async def bot_update(ctx, *args):
        await ctx.send(subprocess.run("cd /home/renblas/DiscordBot; rm disbot.py; git pull", shell=True, check=True))
    
    
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
