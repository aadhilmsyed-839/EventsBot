# Get the Token from the OS environment
import os
TOKEN = os.environ['DISCORD_TOKEN']
#from data.token import TOKEN

# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from config import config
from logger import logger

# Import Commands
from commands.help import help
from commands.metar import metar
from commands.mod_commands import *
from commands.member_commands import *

# Import Flight Logging
from events.flight_logs import *
from events.monthly_roles import *

# Start the Bot
bot.run(TOKEN)
