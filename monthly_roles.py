# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import from Local Files
from config import flight_hours_manager, config

# Import Other Necessary Libraries
import datetime
import json
import csv

@bot.command()
async def update_roles(ctx):
    """
    Description:
        When called by an administrator, this function will iterate through every member in the server
        and update their roles by calling the assign_roles helper function
        
    Arguments:
        ctx : The context of the command
        
    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Otherwise start the role updates
    await ctx.send(f"Starting Role Updates... This may take a while. Please check {config.log_channel.mention} for regular updates.")
    await logger.info(f"Role Updates Requested by {ctx.message.author.mention}.")
    
    # Get the list of members and the number of members
    members, member_count = ctx.guild.members, ctx.guild.member_count
    
    # Iterate through every member and update roles as necessary
    for i, member in enumerate(members):
        
        # Send logger message, and verify that members is a human member
        logger.info(f"({(i + 1)}/{member_count}) Updating Roles for {member.mention}")
        if member.bot: continue
        
        # Remove any pre-existing class roles
        for role_id in list(config.roles.keys()):
            await member.remove_roles(config.guild.get_role(role_id))
            
            
        # Check if the member has logged any flight time in the previous month
        minutes = 0
        if str(member.id) in list(flight_hours_manager.flight_hours.keys()): minutes = flight_hours_manager.flight_hours[str(member.id)]
        if minutes == 0: continue
        
        # Get the number of hours logged
        hours = (minutes / 60) + 1
        
        # Assign roles based on thresholds
        for role_id, threshold in config.roles.items():
        
            # If the threshold is not met, move onto the next available role
            if hours < threshold: continue
            
            # Otherwise assign the earned role for that member
            try: await member.add_roles(config.guild.get_role(role_id))
            except Exception as e: await logger.error(e)
            
            # Update the logger information and break from role assignments
            await logger.info(f"- {member.mention} was assigned {role.name} during role updates")
            break
            
        # Update logger and channel information
        await ctx.send(f"Role Updates Complete.")
        await logger.info("Role Updates Completing. Now Exporting Flight Hours...")
        
        # Send the exported file to the log channel
        file_path = "data/role_updates.txt"
        await flight_hours_manager.export(file_path)
        with open(file_path, "rb") as file: await config.log_channel.send(file = discord.File(file, file_path))
        
        # Send the total number of events and members joined to the log channel
        num_events, num_joined = len(flight_hours_manager.event_history), len(flight_hours_manager.flight_hours)
        await logger.info("There were a total of {num_events} during the current month. A total of {num_joined} logged flight time during the current month.")
        
    # Update logger information
    await ctx.send("Clearing Flight Hours");
    
    # Clear the Flight Hours Dictionary
    try:
        flight_hours_manager.start_time.clear()
        flight_hours_manager.flight_hours.clear()
        flight_hours_manager.event_history.clear()
        flight_hours_manager.member_history.clear()
        
    except Exception as e: await logger.error(e)
    
    # Export the updated data back to the file
    flight_hours_manager.save();
    
    # Update logger Information
    await ctx.send("Flight Hours Cleared."); await logger.info(f"Flight Hours Were Cleared by {ctx.message.author.mention}")
            
        
@bot.command()
async def clear_flight_logs(ctx):
    """
    Description:
        When called by an administrator, this function will reset all of the flight logs by removing
        every entry in the flight_hours dictionary.

    Arguments:
        ctx : The context of the command

    Returns:
        None
    """
    
    # Check if the message author is an executive
    executive_role = config.guild.get_role(948366800712773635)
    if executive_role not in ctx.message.author.roles: await ctx.send("Your role is not high enough to use this command."); return
    
    # Update logger information
    await ctx.send("Clearing Flight Hours");
    
    # Clear the Flight Hours Dictionary
    try:
        flight_hours_manager.start_time.clear()
        flight_hours_manager.flight_hours.clear()
        flight_hours_manager.event_history.clear()
        flight_hours_manager.member_history.clear()
        
    except Exception as e: await logger.error(e)
    
    # Export the updated data back to the file
    flight_hours_manager.save();
    
    # Update logger Information
    await ctx.send("Flight Hours Cleared."); await logger.info(f"Flight Hours Were Cleared by {ctx.message.author.mention}")
            
