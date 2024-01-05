# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logInfo

# Import from Local Files
from config import flight_hours, roles

# Import Other Necessary Libraries
import datetime
import json
import csv

# Function to assign roles based on flight hours
async def assign_roles(ctx, member : discord.Member):
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
    # Declare Global Variables
    global flight_hours
    global roles
    
    # Remove roles from previous role update
    for role_id in list(roles.keys()):
        await member.remove_roles(discord.utils.get(member.guild.roles, id = role_id))
    
    # Return if the member has not logged any flight hours
    if member.id not in list(flight_hours.keys()): return
    
    # Get the number of Minutes from the Flight Time
    hours = flight_hours[member.name] // 60
    
    # Assign them Roles Based on their Threshold
    for role_id, threshold in roles.items():
    
        # If the Hours Meets the Threshold, Assign the Role
        if hours >= threshold:
            role = discord.utils.get(member.guild.roles, id = role_id)
            await member.add_roles(discord.utils.get(member.guild.roles, id = role_id))
            logInfo(f"{member} was assigned {role} during role updates.")
            break      # Prevents Multiple Role Assignments
                


# Command to update roles based on flight hours
@bot.command()
@commands.has_permissions(manage_roles = True)
async def update_roles(ctx):
    """
    Description:
        When called by an administrator, this function will iterate through every member in the server
        and update their roles by calling the assing_roles helper function
        
    Arguments:
        ctx : The context of the command
        
    Returns:
        None
    """
    
    # Update Logger Information
    logInfo(f"Server Role Updates requested by {ctx.message.author}.")
    logInfo("Starting Role Updates...")
    
    try:
        # For all members in the server, assign their new role
        for member in ctx.guild.members: await assign_roles(ctx, member)
        
        # Update Information to Logger
        logInfo("Role Updates Complete.")
        
        # Clear the Flight Logs for the Next Month
        logInfo("Clearing Flight Hours...")
        flight_hours.clear()
        
    except Exception as e: logInfo(e)

@bot.command()
@commands.has_permissions(manage_roles = True)
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
    
    # Declare Global Variables
    global flight_hours
    
    # Clear the dictionary
    flight_hours.clear()
    
    # Check the Length of the Flight Logs to ensure full reset
    logInfo(f"flight_hours has a total of {len(flight_hours)} entries.")
    


#@bot.command()
#@commands.has_permissions(manage_roles = True)
#async def export_flight_logs(ctx, filename):
#    """
#    Descrptions:
#        Exports data to a JSON file when bot disconnects or role udpates occur.
#
#    Arguments:
#        filename (str) : Name of the Export File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Print Logger Message
#        logInfo(f"Exporting Flight Logs to {filename}...")
#
#        # Call the Helper Function to Save the Logs to a File
#        save_flight_logs_to_file(filename)
#
#        # Print Logger Message
#        logInfo("Exported Flight Logs Successfully.")
#
#    except Exception as e: logger.error(e)
#
#
#def save_flight_logs_to_file(filename):
#    """
#    Descrptions:
#        Helper function to create a flight_logs.json file and save the data there
#
#    Arguments:
#        filename (str) : Name of the Export File
#
#    Returns:
#        None
#    """
#
#    # Declare Global Variables
#    global flight_hours
#
#    # Return File in case we need to return
#    return_file = None
#
#    data = {"flight_hours": flight_hours}
#
#    # Open the JSON file and write the data to it
#    with open(filename, 'w') as json_file:
#        json.dump(data, json_file)
#        return_file = json_file
#
#    # Return the file if needed:
#    return return_file
#
#
#@bot.command()
#@commands.has_permissions(manage_roles = True)
#async def import_flight_logs(ctx, filename = 'data/flight_logs.json'):
#    """
#    Descrptions:
#        Imports data from JSON file when bot reconnecst
#
#    Arguments:
#        filename (str) : Name of the Import File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Declare Global Variables
#        global flight_hours
#
#        # Print Logger Message
#        logInfo(f"Importing Flight Logs from {filename}...")
#
#        # Open the JSON File and Read the Data from it
#        with open(filename, 'r') as json_file:
#            data = json.load(filename)
#            flight_hours = data.get("flight_hours", {})
#
#        # Print Logger Message
#        logInfo("Imported Flight Logs Successfully.")
#
#    except Exception as e: logger.error(e)
#
#
#@bot.command()
#@commands.has_permissions(manage_roles=True)
#async def get_flight_logs(ctx, filename='data/flight_logs.json'):
#    """
#    Description:
#        Returns a CSV file containing the flight hours to the channel.
#
#    Arguments:
#        filename (str) : Name of the JSON Flight Logs File
#
#    Returns:
#        None
#    """
#    try:
#
#        # Get the JSON Flight Logs File
#        logInfo(f"Retrieving Flight Logs from {filename}...")
#        json_file = save_flight_logs_to_file(filename)
#        data = json.load(json_file)
#        flight_hours = data.get("flight_hours", {})
#        logInfo(f"Retrieving Flight Logs from {filename}.")
#
#        # 2. Convert JSON Data to a List of Dictionaries
#        data_list = [{'member_name': key, 'flight_hours': value} for key, value in flight_hours.items()]
#
#        # 3. Write Data to a CSV File
#        csv_file_path = 'data/flight_logs.csv'
#        with open(csv_file_path, 'w', newline='') as csv_file:
#
#            # Specify the Column Names
#            fieldnames = ['member_name', 'flight_hours']
#
#            # Create a CSV writer object
#            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#
#            # Write the header row
#            csv_writer.writeheader()
#
#            # Write the data rows
#            csv_writer.writerows(data_list)
#
#        logInfo(f'Conversion from JSON to CSV completed. CSV file saved as {csv_file_path}')
#
#        # Send the CSV file as an attachment to the channel
#        with open(csv_file_path, 'rb') as file:
#            await ctx.send(file = discord.File(file))
#
#    # Log any Errors
#    except Exception as e: logger.error(e)
