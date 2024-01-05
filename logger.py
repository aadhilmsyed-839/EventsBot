# Import Discord Python Libraries
import discord
from discord.ext import commands
from bot import bot

# Import the Log Channel Variable
from config import log_channel

@bot.command()
@commands.has_permissions(manage_channels=True)
async def setLogChannel(ctx, channel: discord.TextChannel):
    """
    Description:
        Sets the Log Channel in the Server to Print Bot Information and Status

    Arguments:
        ctx                             : The context object
        channel (discord.TextChannel)   : The channel to set as the log channel
        
    Returns:
        None
    """
    
    global log_channel
    log_channel = channel
    logInfo(f"Bot Log Channel Set as {channel}")


async def logInfo(info: str):
    """
    Description:
        Sends Logger Information to the Specified Log Channel if it exists

    Arguments:
        info (str) : The message to be sent to the log channel
        
    Returns:
        None
    """
    
    global log_channel
    if log_channel: await log_channel.send(info)

