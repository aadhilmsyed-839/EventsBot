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
from help import help
from metar import metar
from mod_commands import *
from member_commands import *

# Import Flight Logging
from flight_logs import *
from monthly_roles import update_roles, clear_flight_logs

# Start the Bot
bot.run(TOKEN)
