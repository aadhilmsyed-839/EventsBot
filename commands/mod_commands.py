# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import Necessary Local Files
from config import config, flight_hours_manager

# Import Other Necessary Libraries
import pandas as pd
import io
import datetime
from datetime import timedelta

@bot.command()
@commands.has_permissions(manage_channels=True)
async def add_restricted_channel(ctx, *channels: discord.TextChannel):
    """
    Command to add a channel to the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to restrict.

    Returns:
        None
    """
    try:
        for channel in channels:
            if channel.id not in config.restricted_channels:
                config.restricted_channels.append(channel.id)
                await ctx.send(f"{channel.mention} is now a restricted announcement channel.")
                await logger.info(f"{channel.mention} was added as a restricted announcement channel by {ctx.author}")
            else:
                await ctx.send(f"{channel.mention} is already a restricted announcement channel.")
                
        config.save()
    
    except Exception as e: await logger.error(f"An error occurred in add_restricted_channel: {e}")
        
        
@bot.command()
@commands.has_permissions(manage_channels=True)
async def remove_restricted_channel(ctx, *channels: discord.TextChannel):
    """
    Command to remove a channel from the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to unrestrict.

    Returns:
        None
    """
    try:
        for channel in channels:
            if channel.id in config.restricted_channels:
                config.restricted_channels.remove(channel.id)
                await ctx.send(f"{channel.mention} is no longer a restricted announcement channel.")
                await logger.info(f"{channel.mention} was removed as a restricted announcement channel by {ctx.author}")
            else:
                await ctx.send(f"{channel.mention} is not a restricted announcement channel.")
                
        config.save()
    
    except Exception as e: await logger.error(f"An error occurred in remove_restricted_channel: {e}")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def view_restricted_channels(ctx):
    """
    Command to view the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
        # If no restricted channels
        if not config.restricted_channels:
            await ctx.send(f"There are no restricted channels in {ctx.guild.name}")
            return
        
        # Print every channel that is restricted
        channels_list = f"Restricted Channels in {ctx.guild.name}:"
        for channel_id in config.restricted_channels: channels_list += f"\n- <#{channel_id}>"
        await ctx.send(channels_list)
    
    except Exception as e: await logger.error(f"An error occurred in view_restricted_channels: {e}")
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def toggle_voice_channel(ctx, channel: discord.VoiceChannel = None):
    """
    Description:
        Changes/Adds/Removes the Voice Channel to Track during an Event. If no argument is specified,
        then the voice_channel is set to None. Otherwise if a channel is passed as an argument, then
        that voice channel is assigned to the variable.
        
    Arguments:
        ctx : The command object
        channels (discord.TextChannel) : Channel to be Assigned as the Event Voice Channel
        
    Returns:
        None
    """
    try:
        # Set the Voice Channel to the argument
        flight_hours_manager.voice_channel = channel
        await logger.info(f"Event Voice Channel was set to {channel} by {ctx.message.author}.")
        await ctx.send(f"Event Voice Channel was set to {channel} by {ctx.message.author}.")
        
        flight_hours_manager.save()
    
    except Exception as e: await logger.error(f"An error occurred in toggle_voice_channel: {e}")
    
    
@bot.command()
@commands.has_permissions(manage_channels=True)
async def add_flight_time(ctx, member: discord.Member, minutes: int):
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
    try:
        # If the member is not in the flight hours dictionary, create an entry
        if str(member.id) not in flight_hours_manager.flight_hours.keys():
            flight_hours_manager.flight_hours[str(member.id)] = 0
        
        # Add the flight hours to the member
        flight_hours_manager.flight_hours[str(member.id)] += minutes
        
        # Send a Message to the Channel and the Logger
        await ctx.send(f"{minutes} minutes were added to {member.mention} by {ctx.message.author.mention}.")
        await logger.info(f"{minutes} minutes were added to {member.mention} by {ctx.message.author.mention}.")
        
        flight_hours_manager.save()
    
    except Exception as e: await logger.error(f"An error occurred in add_flight_time: {e}")
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def remove_flight_time(ctx, member: discord.Member, minutes: int):
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
    try:
        # If the member is not in the flight hours dictionary, return from the function
        if str(member.id) not in flight_hours_manager.flight_hours.keys():
            await ctx.send(f"{member.name} does not have any Flight Time.")
            return
        
        # Subtract the Flight Time
        flight_hours_manager.flight_hours[str(member.id)] -= min(minutes, flight_hours_manager.flight_hours[str(member.id)])  # prevent negative flight time
        
        # Send a Message to the Channel and the Logger
        await ctx.send(f"{minutes} minutes were removed from {member.mention} by {ctx.message.author.mention}.")
        await logger.info(f"{minutes} minutes were removed from {member.mention} by {ctx.message.author.mention}.")
        
        flight_hours_manager.save()
    
    except Exception as e: await logger.error(f"An error occurred in remove_flight_time: {e}")
