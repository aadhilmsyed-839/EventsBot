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
async def add_restricted_channel(ctx, *channels: discord.TextChannel):
    """
    Command to add a channel to the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to restrict.

    Returns:
        None
    """
    
    # Verify that the member is a moderator
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # For each channel to be added
    for channel in channels:
    
        # If it has not already been added
        if channel.id not in config.restricted_channels:
            config.restricted_channels.append(channel.id)
            await ctx.send(f"{channel.mention} is now a restricted announcement channel.")
            await logger.info(f"{channel.mention} was added as a restricted announcement channel by {ctx.author.mention}")
        
        # Otherwise send a message to the command author
        else: await ctx.send(f"{channel.mention} is already a restricted announcement channel.")
    
    # Resave the configurations to the config file
    config.save()
        
        
@bot.command()
async def remove_restricted_channel(ctx, *channels: discord.TextChannel):
    """
    Command to remove a channel from the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        *channels (discord.TextChannel): The text channels to unrestrict.

    Returns:
        None
    """
    # Verify that the member is a moderator
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # For each channel to be removed
    for channel in channels:
    
        # If it has not already been added
        if channel.id in config.restricted_channels:
            config.restricted_channels.remove(channel.id)
            await ctx.send(f"{channel.mention} is no longer a restricted announcement channel.")
            await logger.info(f"{channel.mention} was removed as a restricted announcement channel by {ctx.author.mention}")
        
        # Otherwise send a message to the command author
        else: await ctx.send(f"{channel.mention} was not already a restricted announcement channel.")
    
    # Resave the configurations to the config file
    config.save()


@bot.command()
async def view_restricted_channels(ctx):
    """
    Command to view the list of restricted announcement channels.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    # Verify that the member is a moderator
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # If there are no restricted channels, send a message
    if not config.restricted_channels: await ctx.send(f"There are no restricted channels in {ctx.guild.name}")
    
    # Otherwise print all the channels
    channels_str = f"## Restricted Channels in {ctx.guild.name}"
    channels_str += ''.join(f"\n- <#{channel_id}>" for channel_id in config.restricted_channels)
    await ctx.send(channels_str)
    

@bot.command()
async def add_event_vc(ctx, channel: discord.VoiceChannel = None):
    """
    Description:
        Adds the Voice Channel to the tracked list during an Event.
        
    Arguments:
        ctx : The command object
        channels (discord.TextChannel) : Channel to be added as an Event Voice Channel
        
    Returns:
        None
    """
    
    # Verify that the member is an Event Manager
    manager_role = config.guild.get_role(948366879980937297)
    if manager_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if there is an active event
    if not flight_hours_manager.active_event:
        await ctx.send(f"You cannot add {channel.mention} as an event VC. There is currently no active event.")
        return
        
    # Check if the voice channel is already in the list of logged channels
    if channel in flight_hours_manager.voice_channels: await ctx.send(f"{channel.mention} is already an event voice channel."); return
        
    # Add the voice channel to the list of logged voice channels
    flight_hours_manager.voice_channels.append(channel)
    await ctx.send(f"{channel.mention} was added as an event voice channel.")
    await logger.info(f"{channel.mention} was added as an event voice channel by {ctx.message.author.mention}.")
    
    # Log any members who might be in the event voice channel
    for member in channel.members:
        await logger.info(f"{member.mention} joined {channel.mention}. Starting Logging...")
        flight_hours_manager.log_start_time(str(member.id))
        
    # Save the updated flight hours to the file
    flight_hours_manager.save()
    

@bot.command()
async def remove_event_vc(ctx, channel: discord.VoiceChannel = None):
    """
    Description:
        Removes the Voice Channel from the tracked list during an Event.
        
    Arguments:
        ctx : The command object
        channel (discord.VoiceChannel) : Channel to be removed from the Event Voice Channel list
        
    Returns:
        None
    """
    
    # Verify that the member is an Event Manager
    manager_role = config.guild.get_role(948366879980937297)
    if manager_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if there is an active event
    if not flight_hours_manager.active_event:
        await ctx.send(f"You cannot remove {channel.mention} as an event VC. There is currently no active event."); return
        
    # Check if the voice channel is already in the list of logged channels
    if channel not in flight_hours_manager.voice_channels: await ctx.send(f"{channel.mention} is not an event voice channel."); return
        
    # Add the voice channel to the list of logged voice channels
    flight_hours_manager.voice_channels.remove(channel)
    await ctx.send(f"{channel.mention} was removed as an event voice channel.")
    await logger.info(f"{channel.mention} was removed as an event voice channel by {ctx.message.author.mention}.")
    
    # Log any members who might be in the event voice channel
    for member in channel.members:
        elapsed_minutes = flight_hours_manager.log_end_time(str(member.id))
        await logger.info(f"{member.mention} left {channel.mention}. Ending Logging...")
        await logger.info(f"{int(elapsed_minutes)} minutes of flight time were added to {member.mention}. " \
                          f"{member.mention} has a total flight time of {int(flight_hours_manager.flight_hours[str(member.id)])} minutes.")

    # Save the updated flight hours to the file
    flight_hours_manager.save()
    
    
@bot.command()
async def view_event_vc(ctx):
    """
    Description:
        Shows all the Voice Channels being tracked for logging during an Event.
        
    Arguments:
        ctx : The command object
        
    Returns:
        None
    """
    
    # Verify that the member is an Event Manager
    manager_role = config.guild.get_role(948366879980937297)
    if manager_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if there is an active event
    if not flight_hours_manager.active_event: await ctx.send(f"There is currently no active event."); return
    
    # Check if there is at least one event VC being tracked
    if not flight_hours_manager.voice_channels: await ctx.send(f"There are no voice channels currently being tracked."); return
    
    # Send the list of voice channels being tracked
    channels_str = f"## Event Voice Channels"
    channels_str += ''.join(f"\n- <#{channel.id}>" for channel in flight_hours_manager.voice_channels)
    await ctx.send(channels_str)
    
    
@bot.command()
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
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # If the member is not in the flight hours dictionary, create an entry
    if str(member.id) not in flight_hours_manager.flight_hours.keys(): flight_hours_manager.flight_hours[str(member.id)] = 0
    
    # Add the flight hours to the member
    flight_hours_manager.flight_hours[str(member.id)] += minutes
    
    # Send a Message to the Channel and the Logger
    await ctx.send(f"{minutes} minutes of flight time were added to {member.mention}.")
    await logger.info(f"{minutes} minutes were added to {member.mention} by {ctx.message.author.mention}.")
    
    # Save the updated flight hours back to the file
    flight_hours_manager.save()
    

@bot.command()
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
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # If the member is not in the flight hours dictionary, create an entry
    if str(member.id) not in flight_hours_manager.flight_hours.keys():
        await ctx.send(f"{member.mention} does not have any flight time."); return
    
    # Subtract the flight time from the member
    flight_hours_manager.flight_hours[str(member.id)] -= min(minutes, flight_hours_manager.flight_hours[str(member.id)])
    
    # Send a Message to the Channel and the Logger
    await ctx.send(f"{minutes} minutes of flight time were removed from {member.mention}.")
    await logger.info(f"{minutes} minutes were removed from {member.mention} by {ctx.message.author.mention}.")
    
    # Save the updated flight hours back to the file
    flight_hours_manager.save()
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def view_flight_time(ctx):
    """
    Description:
        Shows the flight time of all members in the database
        
    Arguments:
        ctx : The command object
        
    Return:
        None
    """
    
    # Send the Flight Hours as a Text File to the Log Channel
    await ctx.send("Processing Flight Hours Text File (This may take a while)...")
    file_path = "data/role_updates.txt"; await flight_hours_manager.export(file_path)
    with open(file_path, "rb") as file: await ctx.send("Exported flight hours:", file=discord.File(file, file_path))


@bot.command()
async def add_event_attendance(ctx, member: discord.Member, *, event_name: str):
    """
    Adds event attendance for the specified member and event.

    Parameters:
        ctx: The command context object
        member: The Discord member (mention)
        event_name: The event name (enclosed in quotes if it contains spaces)

    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the event exists
    if event_name not in flight_hours_manager.event_history.keys(): await ctx.send(f"Event '{event_name}' could not be found in the database"); return
    
    # Add the Member to the Event Attendance
    flight_hours_manager.event_history[event_name].add(str(member.id))
    
    # Check if the member has a member history entry
    if str(member.id) not in flight_hours_manager.member_history.keys(): flight_hours_manager.member_history[str(member.id)] = set([])
    
    # Add the Event to the Member History
    flight_hours_manager.member_history[str(member.id)].add(event_name)
    
    # Update Logger Information
    await ctx.send(f"{member.mention} was successfully added to the attendance for event '{event_name}'")
    await logger.info(f"{member.mention} was added to the attendance for event '{event_name}' by {ctx.message.author.mention}")
    
    # Save the updated flight hours to the file
    flight_hours_manager.save()


@bot.command()
async def remove_event_attendance(ctx, member: discord.Member, *, event_name: str):
    """
    Removes event attendance for the specified member and event.

    Parameters:
        ctx: The command context object
        member: The Discord member (mention)
        event_name: The event name (enclosed in quotes if it contains spaces)

    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the event exists
    if event_name not in flight_hours_manager.event_history.keys(): await ctx.send(f"Event '{event_name}' could not be found in the database"); return
    
    # Remove the Member from the Event Attendance
    flight_hours_manager.event_history[event_name].remove(str(member.id))
    
    # Check if the member has a member history entry
    if str(member.id) not in flight_hours_manager.member_history.keys(): return
    
    # Remove the event name from the list of events attended for the member
    if event_name in flight_hours_manager.member_history[str(member.id)]: flight_hours_manager.member_history[str(member.id)].remove(event_name)
    
    # Update Logger Information
    await ctx.send(f"{member.mention} was successfully removed from the attendance for event '{event_name}'")
    await logger.info(f"{member.mention} was removed from the attendance for event '{event_name}' by {ctx.message.author.mention}")
    
    # Save the updated flight hours to the file
    flight_hours_manager.save()
  
  
@bot.command()
async def view_event_attendance(ctx, *, event_name: str):
    """
    Displays the event attendance for a given event name

    Parameters:
        ctx: The command context object
        event_name: The event name (enclosed in quotes if it contains spaces)

    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the event exists
    if event_name not in flight_hours_manager.event_history.keys(): await ctx.send(f"Event '{event_name}' could not be found in the database"); return
    
    # Create a list of member namess
    member_names = []
    for member_id in flight_hours_manager.event_history[event_name]: member = await bot.fetch_user(member_id); member_names.append(f"- {member.name}")

    # Send a message containing the people who attended the event
    attend_str = f"## Attendance for Event '{event_name}'\n"
    attend_str += f"-# This event had a total of {len(flight_hours_manager.event_history[event_name])} participant(s).\n"
    attend_str += "\n".join(member_names)
    await ctx.send(attend_str)


@bot.command()
async def add_blacklist_member(ctx, member: discord.Member):
    """
    Adds a member to the member blacklist, preventing access to commands like !copilotsays and !spam

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        member (discord.Member) : The member to add to the blacklist

    Returns:
        None
    """
    
    # Verify that the member is a moderator
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the member is already in the blacklist
    if str(member.id) in config.blacklist: await ctx.send(f"{member.mention} is already on the blacklist."); return
    
    # Otherwise add the member to the blacklist
    config.blacklist.append(str(member.id))
    
    # Update logger information
    await ctx.send(f"{member.mention} was added to the blacklist.")
    await logger.info(f"{member.mention} was added to the blacklist by {ctx.message.author.mention}")
    
    # Resave the configurations to the config file
    config.save()
        
        
@bot.command()
async def remove_blacklist_member(ctx, member: discord.Member):
    """
    Removes a member from the member blacklist, re-enabling access to commands like !copilotsays and !spam

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        member (discord.Member) : The member to add to the blacklist

    Returns:
        None
    """
    
    # Verify that the member is a moderator
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the member is already in the blacklist
    if str(member.id) not in config.blacklist: await ctx.send(f"{member.mention} is not on the blacklist."); return
    
    # Otherwise add the member to the blacklist
    config.blacklist.remove(str(member.id))
    
    # Update logger information
    await ctx.send(f"{member.mention} was removed from the blacklist.")
    await logger.info(f"{member.mention} was removed from the blacklist by {ctx.message.author.mention}")
    
    # Resave the configurations to the config file
    config.save()

@bot.command()
async def view_blacklist_members(ctx):
    """
    A list of all the members on the blacklist
    
    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    # Verify that the member is a moderator
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # If there are no restricted channels, send a message
    if not config.blacklist: await ctx.send("There are currently no members on the blacklist"); return
    
    # Otherwise print all the channels
    channels_str = f"## Blacklisted Members in {ctx.guild.name}"
    channels_str += ''.join(f"\n- <@{member_id}>" for member_id in config.blacklist)
    await ctx.send(channels_str)


@bot.command()
async def add_event(ctx, *, event_name: str):
    """
    Adds an event to the event history

    Parameters:
        ctx: The command context object
        event_name: The event name (enclosed in quotes if it contains spaces)

    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the event already exists in the event history
    if event_name in flight_hours_manager.event_history.keys(): await ctx.send("This event already exists in the event history."); return
    
    # Add the event to the event history
    flight_hours_manager.event_history[event_name] = set()
    await ctx.send(f"Event '{event_name}' was successfully added to the event history database.")
    
    # Export the updated data back to the file
    flight_hours_manager.save(); return
    
    
@bot.command()
async def remove_event(ctx, *, event_name: str):
    """
    Removes an event from the event history

    Parameters:
        ctx: The command context object
        event_name: The event name (enclosed in quotes if it contains spaces)

    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if the event already exists in the event history
    if event_name not in flight_hours_manager.event_history.keys(): await ctx.send("This event is not in the event history."); return
    
    # Remove all the atendees of the event
    for member_id in flight_hours_manager.event_history[event_name]: flight_hours_manager.member_history[member_id].remove(event_name)
    
    # Add the event to the event history
    del flight_hours_manager.event_history[event_name]
    await ctx.send(f"Event '{event_name}' was successfully removed from the event history database.")
    
    # Export the updated data back to the file
    flight_hours_manager.save(); return
    

@bot.command()
async def start_event(ctx, *, event_name: str):
    """
    Description:
        Starts an unofficial event with the given name
        
    Arguments:
        ctx : The command object
        event_name: The name of the event to be started
        
    Returns:
        None
    """
    
    # Verify that the member is an Event Manager
    manager_role = config.guild.get_role(948366879980937297)
    if manager_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if there is a current active event
    if flight_hours_manager.active_event: await ctx.send("There is already an ongoing event. You cannot start another event.")
    
    # Check that the event does not already exist in the database
    if event_name in flight_hours_manager.event_history.keys(): await ctx.send("An event with this name already exists. Please select a different name."); return
    
    # Update Logger Information
    await ctx.send(f"Logging for event '{event_name}' has started.")
    await logger.info(f"Starting Logging for Event '{event_name}'.")
    
    # Set the active event and add the event VC to the voice channel list
    flight_hours_manager.active_event = event_name
    flight_hours_manager.event_history[event_name] = set()

    # Export the updated data back to the file
    flight_hours_manager.save()
    
    
@bot.command()
async def end_event(ctx):
    """
    Description:
        Ends any event that is currently ongoing
        
    Arguments:
        ctx : The command object
        
    Returns:
        None
    """
    
    # Verify that the member is an Event Manager
    manager_role = config.guild.get_role(948366879980937297)
    if manager_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Check if there is a current active event
    if not flight_hours_manager.active_event: await ctx.send("There is currently no active event."); return
    
    # End the Logging for all members who joined the event
    for member_id in list(flight_hours_manager.start_time.keys()):
        
        # Log the left member and get the elapsed time
        elapsed_minutes = flight_hours_manager.log_end_time(str(member_id))
        
        # Update the logger information to the log channel
        member = await config.guild.get_member(int(member_id))
        vc_channel = member.voice.channel.mention if member.voice.channel else "the event"
        await logger.info(f"{member.mention} left {vc_channel}. Ending Logging...")
        await logger.info(f"{int(elapsed_minutes)} minutes of flight time were added to <@{member_id}>. " \
                          f"{member.mention} has a total flight time of {int(flight_hours_manager.flight_hours[str(member_id)])} minutes.")
        
    # Update logger information to the log channel
    event_name = flight_hours_manager.active_event
    await logger.info(f"Ending Logging for Event '{event_name}'. A total of {len(flight_hours_manager.event_history[event_name])} members joined.")
    await ctx.send(f"Logging for event '{event_name}' has ended. A total of {len(flight_hours_manager.event_history[event_name])} members joined.")
    
    # Reset the active event and clear out the event VCs
    flight_hours_manager.active_event = None
    flight_hours_manager.voice_channels.clear()
    flight_hours_manager.start_time.clear()
                          
    # Export the updated data back to the file
    flight_hours_manager.save()
    
    

