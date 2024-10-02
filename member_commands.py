# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logger

# Import Necessary Local Files
from config import config, flight_hours_manager

# Import Other External Libraries
from random import randrange
    
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
    try:
        # Convert the Argument to Integer, throw Error if not an integer
        limit = int(limit)
        
        # Check if the user provided a valid limit
        if limit < 1 or limit > 15:
            await ctx.send("Please enter an integer value between 1 and 15.")
            return
            
        await ctx.message.delete()
            
        # Print as many times as the limit
        for _ in range(limit): await ctx.send(".")
    
    except ValueError: await ctx.send("Please enter an integer value between 1 and 15.")
    except Exception as e: await logger.error(f"An error occurred in dotspam: {e}")

    
def expected_role(minutes):
    """
    Description
        Returns the expected role given the person's flight time for the month

    Parameters:
        minutes (int) : Flight Time in minutes

    Returns:
        str: The expected role based on flight time
    """

    if   minutes > (config.roles[989232534313369630] * 60): return "First Class"
    elif minutes > (config.roles[1110680241569017966] * 60): return "Business Class"
    elif minutes > (config.roles[1110680332879011882] * 60): return "Premium Economy"
    elif minutes > (config.roles[1112981412191146004] * 60): return "Economy Class"
    else:                    return "Member"


@bot.command()
async def flighttime(ctx, member: discord.Member = None):
    """
    Description
        Returns the flight time of the command message author

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
    try:
        flight_time = flight_hours_manager.flight_hours.copy()
        
        # Retrieve the message author as the member name
        if member is None: member = ctx.message.author
        highest_role = max(member.roles, key=lambda role: role.position)
        embed_color = highest_role.color
        
        # Check if the member has flight hours recorded
        hours, minutes = 0, 0
        if str(member.id) in flight_time.keys(): hours, minutes = divmod(flight_time[str(member.id)], 60)
        
        # Format flight hours as a string
        flight_time_str = f"{int(hours)} hours {int(minutes)} minutes"
            
        # Create an embed
        embed = discord.Embed(title=f"Flight Time for {member.display_name}", color=embed_color)
        embed.add_field(name="Current Flight Hours", value=flight_time_str)
        embed.add_field(name="Expected Role", value=expected_role((hours * 60 + minutes)))
        embed.set_thumbnail(url = member.avatar.url if member.avatar else "https://sm.mashable.com/mashable_me/seo/default/discord_4r4y.jpg")
        
        await ctx.send(embed=embed)
        
    except Exception as e: await logger.error(f"An error occurred in flighttime: {e}")
    

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
    try:
        flight_time = flight_hours_manager.flight_hours.copy()

        # Sort the Dictionary by Highest flight hours
        sorted_flight_hours = dict(sorted(flight_time.items(), key=lambda item: item[1], reverse=True))

        # Convert the sorted dictionary items into a list of tuples
        sorted_items = list(sorted_flight_hours.items())
        
        # Display the top 10 values
        limit = min(10, len(sorted_items))
        
        # Print No Members Found if Limit is 0
        if limit == 0:
            await ctx.send("There are currently no people on the leaderboard.")
            return
        
        # Create the embed
        embed = discord.Embed(
            title="Flight Time Leaderboard",
            color=discord.Color.blue(),
            description="Members with the Highest Flight Hours in GeoFS Events"
        )
            
        # Set the server logo as the embed thumbnail
        embed.set_thumbnail(url=ctx.guild.icon.url)
        
        # For every member
        for i, (member_id, flight_time) in enumerate(sorted_items[:limit], start=1):
            
            # Calculate the Flight Hours
            hours, minutes = divmod(flight_time, 60)
            flight_time_str = f"{int(hours)} hours {int(minutes)} minutes"
            
            # Add the Information to the Embed
            member = await config.guild.fetch_member(member_id)
            embed.add_field(name=f"#{i}: {member.name}", value=flight_time_str, inline=False)
        
        # Send the Embed
        await ctx.send(embed=embed)
    
    except Exception as e: await logger.error(f"An error occurred in leaderboard: {e}")
    
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
    
    # Don't send "SAW" if the channel is a restricted channel
    if message.channel.id in config.restricted_channels: return
    
    # if the message is a bot command, then ignore
    if message.content.split(" ")[0] == "!copilotsays": return
    
    # Otherwise send "SAW" for every one in three messages
    try:
        if randrange(1,4) == 1: await message.channel.send("SAW")
    except Exception as e: await logger.error(f"An error occurred in on_message_delete: {e}")
    
@bot.event
async def on_reaction_remove(reaction, user):
    """
    Description:
        Sends "SAW" to the channel when a reaction is removed if the channel is not a restricted channel

    Parameters:
        reaction (discord.Reaction): The deleted reaction
        user (discord.User): The user who sent the reaction

    Returns:
        None
    """
    
    # Don't send "SAW" if the channel is a restricted channel
    if reaction.message.channel.id in config.restricted_channels: return
    
    # Otherwise send "SAW" for every one in three messages
    try:
        if randrange(1,4) == 1: await reaction.message.channel.send("SAW")
    except Exception as e: await logger.error(f"An error occurred in on_reaction_add: {e}")

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
    try:
        latency = round(bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f'Pong! Latency is {latency} ms')
    
    except Exception as e: await logger.error(f"An error occurred in ping command: {e}")

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
    try: await ctx.send(':duck:')
    except Exception as e: await logger.error(f"An error occurred in quack command: {e}")
    
@bot.command()
async def copilotsays(ctx, *, message: str):
    """
    Command to repeat the input message and delete the command message.
    
    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        message (str): The message to repeat.
    
    Returns:
        None
    """
    
    # Check if the message author is on the blacklist
    if str(ctx.message.author.id) in config.blacklist: await ctx.send("You have been blacklisted from using this command."); return
    
    # Check if the message contains a ping
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles:
        if message.mentions or message.role_mentions or message.mentions_everyone:
            ctx.send("You cannot ping a role or member with the bot."); return

    # Delete the command message
    await ctx.message.delete()

    # Send the input message to the channel
    await ctx.send(message)
    

@bot.command()
async def spam(ctx, *, message: str):
    """
    Command to resend the input message 5 times and delete the command message.
    
    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.
        message (str): The message to repeat.
    
    Returns:
        None
    """
    
    # Check if the message author is on the blacklist
    if str(ctx.message.author.id) in config.blacklist: await ctx.send("You have been blacklisted from using this command."); return
    
    # Check if the message contains a ping
    moderator_role = config.guild.get_role(766386531681435678)
    if moderator_role not in ctx.message.author.roles:
        if message.mentions or message.role_mentions or message.mentions_everyone:
            ctx.send("You cannot ping a role or member with the bot."); return

    # Delete the command message
    await ctx.message.delete()

    # Send the input message to the channel
    for _ in range(5): await ctx.send(message)
