# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Bot & Logger Objects
from bot import bot
from logger import logger

@bot.command()
async def help(ctx):
    """
    Description
        Responds with an embed describing commands that a user can issue.

    Parameters:
        ctx (discord.ext.commands.Context): The context object representing the command's context.

    Returns:
        None
    """
        
    # Create an embed
    embed = discord.Embed(
        title = f"GeoFS Events CoPilot",
        color = discord.Color.blue(),
        description = "Your Gateway to an Enhanced Flight Simulation Experience. Version: v2.1"
    )
    
    # Add the Member Commands
    embed.add_field(
        name = "!metar",
        value = "Retrieve the weather information for any airport with its ICAO code. Example Usage: !metar KSFO",
        inline = False
    )
    embed.add_field(
        name = "!ping",
        value = "Returns the latency. Example Usage: !ping",
        inline = False
    )
    embed.add_field(
        name = "!dotspam",
        value = "Spams a specified number of dots (1-20). If no number is specified, then it will dotspam 10 times. Example Usage: !dotspam 15",
        inline = False
    )
    embed.add_field(
        name = "!flighttime",
        value = "Retrieve the amount of flight hours you have logged. Example Usage: !flighttime",
        inline = False
    )
    embed.add_field(
        name = "!leaderboard",
        value = "Checkout who has the most flight hours logged for the current month. Example Usage: !leaderboard",
        inline = False
    )
    embed.add_field(
        name = "!copilotsays.",
        value = "This command will make the bot repeat whatever message that is sent in the command message. (i.e.: `!copilotsays hi` will make the bot say `hi`. This command is unavailable to blacklisted members.",
        inline = False
    )
    embed.add_field(
        name = "!spam",
        value = "This command will make the bot spam whatever message that is sent in the command message. (i.e.: `!spam hi` will make the bot send the message `hi` 5 times. This command is unavailable to blacklisted members.",
        inline = False
    )
    embed.add_field(
        name = "!view_member_history",
        value = "This command has an optional member argument. If a member argument is not specified, the member will be the message author. This command will show the list of events that the specified member has attended for the current month.",
        inline = False
    )
    embed.add_field(
        name = "!view_event_history",
        value = "This command has an optional index argument. When no index argument is passed, the command will list all of the events that have taken place in the server for the current month in the format of an ordered list, which can be used to identify the index for a given event. If an index argument is passed, the command will retrieve the attendance list for the event with the given index.",
        inline = False
    )
    embed.add_field(
        name = "Event Participation.",
        value = "By participating in our events, you can increase your flight hours. At the end of each month, roles will be updated to reflect flight activity, so make sure to join us whenever you can. We are thrilled to have you here at GeoFS Events, and we hope you enjoy your time here. :)",
        inline = False
    )
    
    # Set the server logo as the embed thumbnail
    embed.set_thumbnail(url = ctx.guild.icon.url)
    
    # Set footnote
    embed.set_footer(text = "Developed Proudly by GeoFS Flights Channel (the._.pickle)")
    
    # Send the latency as a message
    await ctx.send(embed = embed)
