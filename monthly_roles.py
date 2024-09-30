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

# Function to assign roles based on flight hours
async def assign_roles(ctx, member: discord.Member):
    """
    Description:
        This function acts as a helper function for the role updates. Given a member, it identifies the
        number of flight hours this member has flown and assigns their roles accordingly.
        
    Arguments:
        ctx : The command context object
        member (discord.Member) : The member that is pending role updates
        
    Returns:
        None
    """
    try:
        
        # Skip over bots
        if member.bot: return
    
        # Remove roles from previous role update
        for role_id in list(config.roles.keys()):
            role = config.guild.get_role(role_id)
            await member.remove_roles(role)
        
        # Return if the member has not logged any flight hours
        if str(member.id) not in list(flight_hours_manager.flight_hours.keys()): return
        
        # Get the number of Minutes from the Flight Time
        hours = (flight_hours_manager.flight_hours[str(member.id)] // 60) + 1
#        await logger.info(f"Member {member.mention} has logged {hours} hours of flight time.")
        
        # Assign them Roles Based on their Threshold
        for role_id, threshold in config.roles.items():
            # If the Hours Meets the Threshold, Assign the Role
            if hours >= threshold:
                role = config.guild.get_role(role_id)
                await member.add_roles(role)
#                await ctx.send(f"{member} was assigned {role} during role updates.")
                await logger.info(f"- {member.mention} was assigned {role} during role updates.")
                break  # Prevents Multiple Role Assignments
                
    except Exception as e: await logger.error(f"An error occurred in assign_roles: {e}")

# Command to update roles based on flight hours
@bot.command()
@commands.has_permissions(manage_roles=True)
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
    # Update Logger Information
    await logger.info(f"Server Role Updates requested by {ctx.message.author}.")
    await logger.info("Starting Role Updates...")
    await ctx.send(f"Starting Role Updates... This may take a while. Please check {config.log_channel.mention} for regular updates.")
    
    try:
        # For all members in the server, assign their new role
        
        members = ctx.guild.members
        member_count = 
        for i, member in enumerate(cmembers):
            await logger.info(f"({i + 1}/{ctx.guild.member_count}) Updating Roles for {member.mention}")
            await assign_roles(ctx, member)
        
        
        # Update Information to Logger
        await logger.info("Role Updates Complete.")
        await ctx.send("Role Updates Complete.")
        
        # Send the Flight Hours as a Text File to the Log Channel
        await logger.info("Processing Flight Hours Text File...")
        file_path = "data/role_updates.txt"
        await flight_hours_manager.export(file_path)
        with open(file_path, "rb") as file:
            await config.log_channel.send("Exported flight hours:", file=discord.File(file, file_path))
        
        # Clear the Flight Logs for the Next Month
        flight_hours_manager.flight_hours.clear()
        
    except Exception as e: await logger.error(f"An error occurred in update_roles: {e}")
    
@bot.command()
@commands.has_permissions(manage_roles=True)
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
    try:
        # Clear the dictionary
        await logger.info("Clearing Flight Hours...")
        await ctx.send("Clearing Flight Hours...")
        flight_hours_manager.flight_hours.clear()
        flight_hours_manager.start_time.clear()
        flight_hours_manager.save()
        await ctx.send("Flight Hours Cleared.")
        await logger.info(f"Flight Hours Cleared.")
    
    except Exception as e: await logger.error(f"An error occurred in clear_flight_logs: {e}")
