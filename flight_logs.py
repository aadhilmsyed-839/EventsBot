# Import Discord Python Libraries
import discord
from discord.enums import EventStatus
from discord.ext import commands, tasks

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import Necessary Local Files
from config import config, flight_hours_manager

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
    
    # Check if there is an ongoing event
    if not flight_hours_manager.active_event: return
    
    # Check if there was a change in the voice channel
    if before.channel == after.channel: return
    
    # Case 1: Member switches from non-event VC to a non-event VC
    if before.channel not in flight_hours_manager.voice_channels and after.channel not in flight_hours_manager.voice_channels: return
    
    # Case 2: Member switches from event VC to a event VC
    if before.channel in flight_hours_manager.voice_channels and after.channel in flight_hours_manager.voice_channels:
    
        # Simply log the change of channels to the log channel
        await logger.info(f"{member.mention} switched from {before.channel.mention} to {after.channel.mention}. Resuming Logging...")
        
    # Case 3: Member switches from a non-event VC to an event VC (Joining Event)
    if before.channel not in flight_hours_manager.voice_channels and after.channel in flight_hours_manager.voice_channels:
        
        # Check if the member is a human member
        if member.bot: return
        
        # Log the start time for the member
        flight_hours_manager.log_start_time(str(member.id))
        
        # Update Information to the Logger
        await logger.info(f"{member.mention} joined {after.channel.mention}. Starting Logging...")
        
        # Export the updated data back to the file
        flight_hours_manager.save(); return
        
    # Case 4: Members switches from event VC to a non-event VC (Leaving Event)
    if before.channel in flight_hours_manager.voice_channels and after.channel not in flight_hours_manager.voice_channels:
        
        # Check if the member is a human member
        if member.bot: return
        
        # Log the left member and get the elapsed time
        elapsed_minutes = flight_hours_manager.log_end_time(str(member.id))
        
        # Update the logger information to the log channel
        await logger.info(f"{member.mention} left {before.channel.mention}. Ending Logging...")
        await logger.info(f"{int(elapsed_minutes)} minutes of flight time were added to {member.mention}. " \
                          f"{member.mention} has a total flight time of {int(flight_hours_manager.flight_hours[str(member.id)])} minutes.")
                          
        # Export the updated data back to the file
        flight_hours_manager.save(); return
        

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

    # Case 1: Event Status Changes to Active (Start Logging for the Event)
    if after.status == EventStatus.active:
        
        # Update Logger Information
        await logger.info(f"Starting Logging for Event '{after.name}'.")
        
        # Set the active event and add the event VC to the voice channel list
        flight_hours_manager.active_event = after.name
        flight_hours_manager.event_history[after.name] = set()
        if after.channel: flight_hours_manager.voice_channels.append(after.channel)
        
        # Log any members who are already in the voice channel
        if after.channel:
            for member in after.channel.members:
                if member.bot: continue
                flight_hours_manager.log_start_time(member.id)
                await logger.info(f"{member.mention} joined {after.channel.mention}. Starting Logging...")

        # Export the updated data back to the file
        flight_hours_manager.save(); return
        
    # Case 2: Event Status Changes to Ended (End Logging for the Event)
    if after.status == EventStatus.ended:
    
        # End the Logging for all members who joined the event
        for member_id in list(flight_hours_manager.start_time.keys()):
            
            # Log the left member and get the elapsed time
            elapsed_minutes = flight_hours_manager.log_end_time(str(member_id))
            
            # Update the logger information to the log channel
            member = await config.guild.fetch_member(member_id)
            if not member.voice.channel: continue
            await logger.info(f"<@{member_id}> left {member.voice.channel.mention}. Ending Logging...")
            await logger.info(f"{int(elapsed_minutes)} minutes of flight time were added to <@{member_id}>. " \
                              f"<@{member_id}> has a total flight time of {int(flight_hours_manager.flight_hours[str(member_id)])} minutes.")
            
        # Update logger information to the log channel
        await logger.info(f"Ending Logging for Event '{before.name}'. A total of {len(flight_hours_manager.event_history[before.name])} members joined.")
        
        # Reset the active event and clear out the event VCs
        flight_hours_manager.active_event = None
        flight_hours_manager.voice_channels.clear()
        flight_hours_manager.start_time.clear()
                              
        # Export the updated data back to the file
        flight_hours_manager.save(); return
