# Import Discord Python Library
import discord
from discord.ext import commands

# Define Intents & Create Bot Object
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents, help_command = None)

# Remove the help command
bot.remove_command('help')

# Function to Determine Successful Connection
@bot.event
async def on_ready():
    """
    Description:
        An event handler triggered when the bot successfully connects to Discord.
        This function is automatically called when the bot logs in and is ready to operate.
        It prints the bot's username and user ID to the console as a confirmation of successful login.

    Arguments:
        None

    Returns:
        None
    """
    
    # Update Logger with Login Information
    logInfo(f'Logged in as {bot.user.name} ({bot.user.id})')
