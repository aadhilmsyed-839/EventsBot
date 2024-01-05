# Get the Token from the OS environment
import os
TOKEN = os.environ['DISCORD_TOKEN']

# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logInfo

# Start the Bot
logInfo('Starting the bot...')
bot.run(TOKEN)
