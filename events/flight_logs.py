# Import Discord Python Libraries
import discord
from discord.enums import EventStatus
from discord.ext import commands, tasks

# Import Bot & Logger Objects
from bot import bot
from logger import logInfo

# Import Necessary Local Files
from config import flight_hours, start_time
from config import voice_channel, is_event_active

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
    
    # Declare Global Variables
    global flight_hours, start_time, isEventActive, voiceChannel
    
    # If There is No Ongoing Event, then Ignore
    if not isEventActive: return
    
    # If The User Joins the Event Voice Channel, Start Logging For Them
    if after.channel == voiceChannel:
        logInfo(f"{member} Joined the Event. Starting Logging...")
        start_time[member.id] = time.now(pytz.utc)
        
    # If The User Leaves the Event Voice Channel, End Their Logging and Update their Flight Hours
    elif before.channel == voiceChannel:
        logInfo(f"{member} Left the Event. Ending Logging...")
        log_left_member(member.id)
        
            
    
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
    
    # Declare Global Variables
    global flight_hours, start_time, isEventActive, voiceChannel
    
    # If the Status of the Event changes to Active, Start Logging for That Event
    if after.status == EventStatus.active:
        
        # Update Logger Information
        logInfo(f"Starting Flight Logging for Event '{after.name}'.")
        
        # Update the Event Voice Channel & Event Status Flag
        voiceChannel, isEventActive = after.channel, True
        
        # If Members Are Already in the Voice Channel, Log Them
        for member in voiceChannel.members:
            start_time[member.id] = time.now(pytz.utc)
            logInfo(f"{member} Joined the Event. Starting Logging...")
    
    
    # If the Status of the Event Changes to Ended, End Logging for the Event
    if after.status == EventStatus.ended:
        
        # End the Logging For All Members Who Joined the Event
        for member_id in start_time.keys():
            logInfo(f"{member} Left the Event. Ending Logging...")
            log_left_member(member_id)
        
        # Update Logger Information
        logInfo(f"Ending Flight Logging for Event '{before.name}'.")
        
        # Update the Event Voice Channel and Event Status Flag
        voiceChannel, isEventActive = None, False
        
        # Clear Start Times
        start_time.clear()
        

async def log_left_member(member_id):
    """
    Descrption:
        This helper function logs any members who have left the voice channel or if an event
        has eneded. This function will calculate the amount of time the member has been in
        the voice channel and it will update their flight hours accordingly.
        
    Arguments:
        member_name (str) : Name of member - key to access flight hours and start times
        
    Returns:
        None
    """
    
    # Declare Global Variables
    global flight_hours, start_time

    # Calculate How Long the Member Has Been in the Voice Channel
    elapsed = time.now(pytz.utc) - start_time[member_id]
    
    # If the Member is Not Already in the Flight Hours Dictionary, Add Them
    if member_id not in flight_hours.keys(): flight_hours[member_id] = 0
    
    # Append their Elapsed Time to their Existing Flight Time
    flight_hours[member_id] += (elapsed.total_seconds() // 60)
    logInfo(f"{(elapsed.total_seconds() // 60)} minutes of flight time was added to <@{member_id}>")
    logInfo(f"<@{member_id}> Has a Total Flight Time of {flight_hours[member_id]} Minutes.")
    
    # Remove The Member From the Start Time Dictionary
    del start_time[member_id]
