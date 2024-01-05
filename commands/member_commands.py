# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logInfo

# Import Necessary Local Files
from config import flight_hours, restricted_channels

@bot.event
async def on_message_delete(message):
    """
    Description:
        Sends "SAW" to the channel when a message is deleted if the channel is not a restricted channel

    Parameters:
        message (discord.Message): The deleted message object.

    Returns:
        None
    """
    
    global restricted_channels
    if message.channel.id in restricted_channels: return
    try: await message.channel.send("SAW")
    except Exception as e: logInfo(e)

    
@bot.command()
async def dotspam(ctx, limit: int = 10):
    """
    Description:
        Responds with a spam of dots when the !dotspam command is issued

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        limit (int) : Number of times a dot should be spammed

    Returns:
        None
    """
    
    # Convert the Argument to Integer, throw Error if not an integer
    try: limit = int(limit)
    except ValueError:
        await ctx.send("Please enter an integer value between 1 and 20.")
        return
    
    # Check if the user provided a valid limit
    if limit < 1 or limit > 20:
        await ctx.send("Please enter an integer value between 1 and 20.")
        return
        
    # Print as many times as the limit
    for _ in range(limit): await ctx.send(".")

    
def expected_role(minutes):
    """
    Description
        Returns the expected role given the person's flight time for the month

    Parameters:
        minutes (int) : Flight Time in minutes

    Returns:
        None
    """

    if   minutes > (8 * 60): return "First Class"
    elif minutes > (5 * 60): return "Business Class"
    elif minutes > (3  * 60): return "Premium Economy"
    elif minutes > (1  * 60): return "Economy Class"
    else: return "Member"


@bot.command()
async def flighttime(ctx):
    """
    Description
        Returns the flight time of the command message author

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    # Declare Global Variable
    global flight_hours
    flight_time = flight_hours.copy()
    
    # Retrieve the message author as the member name
    member = ctx.message.author
    highest_role = max(member.roles, key=lambda role: role.position)
    embed_color = highest_role.color
    
    # Check if the member has flight hours recorded
    hours, minutes = 0, 0
    if member in list(flight_time.keys()): hours, minutes = divmod(flight_time[member.id], 60)
    
    # Format flight hours as a string
    flight_time = f"{int(hours)} hours {int(minutes)} minutes"
        
    # Create an embed
    embed = discord.Embed(title = f"Flight Time for {member_name}", color = embed_color)
    embed.add_field(name = "Current Flight Hours", value = flight_time)
    embed.add_field(name = "Expected Role", value = expected_role((hours * 60 + minutes)))
    embed.set_thumbnail(url=ctx.message.author.avatar)
    
    await ctx.send(embed = embed)
    

@bot.command()
async def leaderboard(ctx):
    """
    Description
        Responds with leaderboard of members with the highest flight times

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """

    # Declare Global Variable
    global flight_hours
    flight_time = flight_hours.copy()

    # Sort the Dictionary by Highest flight hours
    logInfo("Sorting Leaderboard...")
    sorted_flight_hours = dict(sorted(flight_time.items(), key=lambda item: item[1], reverse=True))

    # Convert the sorted dictionary items into a list of tuples
    sorted_items = list(sorted_flight_hours.items())
    
    # Display the top 10 values
    limit = (10 if len(sorted_items) > 10 else len(sorted_items))
    
    # Print No Members Found if Limit is 0
    if limit == 0: await ctx.send("There are currently no people on the leaderboard."); return;
    
    #Create the embed
    embed = discord.Embed(
        title = f"Flight Time Leaderboard",
        color = discord.Color.blue(),
        description = "Members with the Highest Flight Hours in GeoFS Events"
    )
           
    # Set the server logo as the embed thumbnail
    embed.set_thumbnail(url = ctx.guild.icon.url)
    
    # For every member
    for i, (member_id, flight_time) in enumerate(sorted_items[:limit], start=1):
        
        # Calculate the Flight Hours
        hours, minutes = divmod(flight_time, 60)
        flight_time = f"{int(hours)} hours {int(minutes)} minutes"
        
        # Add the Information to the Embed
        embed.add_field(name = f"#{i}: <@{member_id}>", value = flight_time, inline = False)
    
    # Send the Embed
    await ctx.send(embed=embed)
    

@bot.command()
async def ping(ctx):
    """
    Description
        Responds with the bot's current latency (ping) when issued the !ping command.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    try: latency = round(bot.latency * 1000)  # Convert to milliseconds
    except Exception as e: logInfo(e)
    await ctx.send(f'Pong! Latency is {latency} ms')

@bot.command()
async def quack(ctx):
    """
    Description
        Responds with a duck whenever the quack command is called

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    
    await ctx.send(':duck:')
