
from __future__ import print_function

import os
import subprocess

import re

import json

import time

# import discord
import discord
from discord.ext import commands


# ============================================================================ #
#                               Global Variables                               #
# ============================================================================ #

LOGGING = False


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


def download(path, cmd):
    
    val = os.fork()
    
    # parent process
    if val > 0:
        return
    
    # if child process
    else:
        
        # download song
        run_cmd("mkdir " + path)
        os.chdir(path)
        output = run_cmd(cmd)
        
        time.sleep(15)
        jf_refresh()
        
        # Log output
        if LOGGING:
            os.chdir("~/DiscordBot/")
            
        exit
    

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


# ============================================================================ #
#                             Discord Bot Commands                             #
# ============================================================================ #

# inits discord bot    
def init_bot(): 
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    global bot
    bot = commands.Bot(command_prefix='/', intents=intents)
    
    
    # ============================================================================ #
    #                                  Bot Events                                  #
    # ============================================================================ #
        
    @bot.event
    async def on_ready():
        print(f"Logging in as {bot.user}")
        #print(discord.Client.get_user("renblas"))
    
    
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
        
        
    @bot.command()
    async def toggle_logging(ctx, *args):
        LOGGING = not LOGGING
        await ctx.send("LOGGING is now " + LOGGING)
        
    
    @bot.command()
    async def update_bot(ctx, *args):
        await ctx.send(run_cmd("rm disbot.py; git pull"))
        
        
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
        
        path="/jellyfin/Music/" + args[0] + "/ "
        cmd = "yt-dlp -x --audio-format flac --audio-quality 1 --embed-thumbnail "
        
        download(path, cmd)
        await ctx.send("Download Request sent to Child")
    
    
    # ============================================================================ #
    #                                 Help Commands                                #
    # ============================================================================ #
        

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
