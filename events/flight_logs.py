# Import Discord Python Libraries
import discord
from discord.enums import EventStatus
from discord.ext import commands, tasks

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import Necessary Local Files
from config import flight_hours_manager

# Import Other Necessary Libraries
from datetime import datetime as time
import pytz

@bot.event
async def on_voice_state_update(member, before, after):
    """
    Description:
        This bot event function monitors changes between the voice channel to track flight hours.
        If the is_event_active flag is enabled, this function will track the hours of each
        member in the voice channel until they leave.
    
    Arguments:
        member : The member that is switching voice channels
        before : The voice channel that the member was in before (if any)
        after  : The voice channel that the member was in after (if any)
        
    Returns:
        None
    """
    try:
        # If There is No Ongoing Event, then Ignore
        if not flight_hours_manager.is_event_active: return
        
        # If the voice channel has note changed, then ignore
        if before.channel == after.channel: return
        
        # If The User Joins the Event Voice Channel, Start Logging For Them
        if after.channel in flight_hours_manager.voice_channels and before.channel not in flight_hours_manager.voice_channels:
            await logger.info(f"{member.mention} Joined the Event. Starting Logging...")
            flight_hours_manager.log_start_time(member.id)
            flight_hours_manager.save()
            return
            
        # If The User Leaves the Event Voice Channel, End Their Logging and Update their Flight Hours
        if before.channel in flight_hours_manager.voice_channels and after.channel not in flight_hours_manager.voice_channels:
            await logger.info(f"{member.mention} Left the Event. Ending Logging...")
            elapsed_minutes = flight_hours_manager.log_end_time(member.id)
            await logger.info(f"{int(elapsed_minutes)} minutes of flight time was added to <@{member.id}>")
            await logger.info(f"<@{member.id}> Has a Total Flight Time of {int(flight_hours_manager.flight_hours[str(member.id)])} Minutes.")
            flight_hours_manager.save()
            return
            
        # If the User switches from one event voice channel to another, simple send a message in the log channel
        if before.channel in flight_hours_manager.voice_channels and after.channel in flight_hours_manager.voice_channels:
            await logger.info(f"{member.mention} switched from {before.channel.mention} to {after.channel.mention}. Resuming logging...")
        
    except Exception as e: await logger.error(f"An error occurred in on_voice_state_update: {e}")
    
@bot.event
async def on_scheduled_event_update(before, after):
    """
    Description:
        This bot event function monitors changes made to scheduled events, specifically
        the status. If the status changes to active, then the event has started so the flag
        is enabled. Likewise the flag is disabled when the status changes to ended.
    
    Arguments:
        before : The state of the scheduled event before any changes
        after  : The state of the scheduled event after any changes
        
    Returns:
        None
    """
    try:
        # If the Status of the Event changes to Active, Start Logging for That Event
        if after.status == EventStatus.active:
        
            # Update Logger Information
            await logger.info(f"Starting Flight Logging for Event '{after.name}'.")
            
            # Update the Event Voice Channel & Event Status Flag
            flight_hours_manager.voice_channels.append(after.channel)
            flight_hours_manager.is_event_active = True
            
            # If Members Are Already in the Voice Channel, Log Them
            for member in flight_hours_manager.voice_channels[0].members:
                flight_hours_manager.log_start_time(member.id)
                await logger.info(f"{member.mention} Joined the Event. Starting Logging...")
            
            flight_hours_manager.save()
            return
        
        # If the Status of the Event Changes to Ended, End Logging for the Event
        if after.status == EventStatus.ended:
        
            # End the Logging For All Members Who Joined the Event
            for member_id in list(flight_hours_manager.start_time.keys()):
                await logger.info(f"<@{member_id}> Left the Event. Ending Logging...")
                elapsed_minutes = flight_hours_manager.log_end_time(member_id)
                await logger.info(f"{int(elapsed_minutes)} minutes of flight time was added to <@{member_id}>")
                await logger.info(f"<@{member_id}> Has a Total Flight Time of {int(flight_hours_manager.flight_hours[str(member_id)])} Minutes.")
            
            # Update Logger Information
            await logger.info(f"Ending Flight Logging for Event '{before.name}'.")
            
            # Update the Event Voice Channel and Event Status Flag
            flight_hours_manager.voice_channels.clear()
            flight_hours_manager.is_event_active = False
            
            flight_hours_manager.save()
            return
            
    except Exception as e: await logger.error(f"An error occurred in on_scheduled_event_update: {e}")
