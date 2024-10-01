# Import Discord Python Library
import discord
from discord.enums import EventStatus
from discord.ext import commands

from logger import logger
from config import config, flight_hours_manager

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
    
    # Load in Configuration Data from File
    config.load()
    flight_hours_manager.load()
    
    # Update Logger with Login Information
    config.guild = bot.get_guild(553718744233541656)
    config.log_channel = config.guild.get_channel(1184292134258479176)
    await logger.setChannel(config.log_channel)
    await logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # If there is an ongoing event retrieve the event VC
    if flight_hours_manager.active_event: await logger.info(f'Resuming Event Logging...'); return
        
    # If an event has already started, then start logging for that event
    for event in config.guild.scheduled_events:
        if event.status == EventStatus.active:
            
            # Update Logger Information
            await logger.info(f"Starting Flight Logging for Event '{event.name}'.")
            
            # Update the Event Voice Channel & Event Status Flag
            flight_hours_manager.active_event = event.name
            flight_hours_manager.event_history[event.name] = set()
            if event.channel: flight_hours_manager.voice_channels.append(event.channel)
            
            # If Members Are Already in the Voice Channel, Log Them
            if event.channel:
                for member in event.channel.members:
                    flight_hours_manager.log_start_time(member.id)
                    await logger.info(f"{member.mention} Joined {event.channel.mention}. Starting Logging...")
                
            break
            
@bot.event
async def on_command_error(ctx, error): await logger.error(error)

