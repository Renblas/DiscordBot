
from __future__ import print_function

import os.path

import datetime

import time

# import google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# import discord
import discord
from discord.ext import commands

'''
Run this script
python disbot.py

install google
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

'''

# NO TOUCHY
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


# The ID and range of a sample spreadsheet, just string in spreadsheet URL
SPREADSHEET_ID = '1yRRLsq67nSzbM3gKAooYt66DCfy-Hrfjh5vCMbf2JZ0'


# inits google connection
def init_google():
    
    global creds
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
 
'''           
    
        '''
    
    
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
    async def getrows(ctx, arg1, arg2):
        try:
            service = build('sheets', 'v4', credentials=creds)
            result = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID, range=arg1 + ":" + arg2).execute()
            rows = result.get('values', [])
            print(f"{len(rows)} rows retrieved")
            for data in rows:
                await ctx.send(' '.join(data))

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
    
    @bot.command()
    async def getsheet(ctx):
        string = ""
        string += "https://docs.google.com/spreadsheets/d/"
        string += SPREADSHEET_ID
        await ctx.send(string)
        
        
    @bot.command()
    async def checkout(ctx, *args):
        try:
            
            # set new rows
            service = build('sheets', 'v4', credentials=creds)
            x = datetime.datetime.now()
            body = {
                "majorDimension": "ROWS",
                "values": [
                    [x.strftime("%c"), ctx.author.name, ctx.author.display_name, ' '.join(args)],
                    ],
                }
            result = service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID, body=body, range="A1:E1", valueInputOption="RAW"
            ).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            await ctx.send("Your attendance has been recorded.")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
    
    
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
        init_google()
        print("Google... YAY")
    except:
        print("Google Bad")
        quit()
        
    try:
        init_bot()
        print("Discord... YAY")
    except:
        print("Discord Bad")
        quit()
        
    bot.run('MTEwMjY4MjI3OTY0NzY1ODAwNA.GrGKto.SiXrOa65m5PewCVzp6iksFtN2AN2Yp8PkFU_U4')

main()
