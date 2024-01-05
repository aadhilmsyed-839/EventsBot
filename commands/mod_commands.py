# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logInfo

# Import Necessary Local Files
from config import restricted_channels
from config import flight_hours, start_time
from config import is_event_active, voice_channel

# Import Other Necessary Libraries
import pandas as pd
import io
import datetime
from datetime import timedelta

@bot.command()
@commands.has_permissions(manage_channels=True)
async def addRestrictedChannel(ctx, *channels: discord.TextChannel):
    """
    Command to add a channel to the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to restrict.

    Returns:
        None
    """
    
    for channel in channels:
        if channel.id not in restricted_channels:
            restricted_channels.append(channel.id)
            await ctx.send(f"{channel.mention} is now a restricted announcement channel.")
            logInfo(f"{channel.mention} was added as a restricted announcement channel by {ctx.author}")
        else:
            await ctx.send(f"{channel.mention} is already a restricted announcement channel.")
        
        
@bot.command()
@commands.has_permissions(manage_channels=True)
async def removeRestrictedChannel(ctx, *channels: discord.TextChannel):
    """
    Command to remove a channel from the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to unrestrict.

    Returns:
        None
    """

    for channel in channels:
        if channel.id in restricted_channels:
            restricted_channels.remove(channel.id)
            await ctx.send(f"{channel.mention} is no longer a restricted announcement channel.")
            logInfo(f"{channel.mention} was removed as a restricted announcement channel by {ctx.author}")
        else:
            await ctx.send(f"{channel.mention} is not a restricted announcement channel.")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def viewRestrictedChannels(ctx):
    """
    Command to view the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
        
    # Print Header Message
    await ctx.send(f"Restricted Channels in {ctx.guild.name}:")
    
    channel_list = ""
    
    # Print every channel that is restricted
    for channel_id in restricted_channels: channel_list += f"<#{channel_id}>, "
    
    await ctx.send(channel_list)
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def toggle_voice_channel(ctx, channel: discord.VoiceChannel = None):
    """
    Description:
        Changes/Adds/Removes the Voice Channel to Track during an Event. If no argument is specified,
        then the voice_channel is set to None. Otherwise if a channel is passed as an argument, then
        that voice channel is assigned to the variable
        
    Arguments:
        ctx : The command object
        channels (discord.TextChannel) : Channel to be Assigned as the Event Voice Channel
        
    Returns:
        None
    """
    try:
        # Declare Global Variable
        global voice_channel
        
        # Set the Voice Channel to the argument
        voice_channel = channel
        logInfo(f"Event Voice Channel was set to {channel} by {ctx.message.author}.")
        await ctx.send(f"Event Voice Channel was set to {channel} by {ctx.message.author}.")
    
    except Exception as e: logger.error(e)
    
    
@bot.command()
@commands.has_permissions(manage_channels=True)
async def addFlightTime(ctx, member: discord.Member, minutes: int):
    """
    Description:
        Adds a Specified amount of Flight Time in minutes for a Specified Member.
        
    Arguments:
        ctx : The command object
        member : The member to add flight time to
        minutes : The amount of flight time to be added
        
    Return:
        None
    """
    
    # Declare Global Variables
    global flight_hours

    # If the member is not in the flight hours dictionary, create an entry
    if member.id not in flight_hours.keys(): flight_hours[member.id] = 0
    
    # Add the flight hours to the member
    flight_hours[member.id] += minutes
    
    # Send a Message to the Channel and the Logger
    await ctx.send(f"{minutes} minutes were added to {member} by {ctx.message.author}.")
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def removeFlightTime(ctx, member: discord.Member, minutes: int):
    """
    Description:
        Removes a Specified amount of Flight Time in minutes for a Specified Member.
        
    Arguments:
        ctx : The command object
        member : The member to remove flight time from
        minutes : The amount of flight time to be removed
        
    Return:
        None
    """
    
    # Declare Global Variables
    global flight_hours

    # If the member is not in the flight hours dictionary, return from the function
    if member.name not in list(flight_hours.keys()):
        ctx.send(f"{member.name} does not have any Flight Time.")
        return
    
    # Subtract the Flight Time
    flight_hours[member.name] -= min(minutes, flight_hours[member.name]) # prevent negative flight time
    
    # Send a Message to the Channel and the Logger
    await ctx.send(f"{minutes} minutes were removed from {member} by {ctx.message.author}.")
