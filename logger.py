# Import Discord Python Libraries
import discord
from discord.ext import commands

from config import config

class Logger:

    def __init__(self, channel: discord.TextChannel): self.log_channel = channel

    async def setChannel(self, channel: discord.TextChannel):
        self.log_channel = channel
        await self.info(f"Log channel set to {channel.mention}")

    async def info(self, message: str):
        if self.log_channel: await self.log_channel.send(message)

    async def error(self, message: str):
        if self.log_channel: await self.log_channel.send(f"**ERROR:** {message}")


log_channel = config.log_channel
logger = Logger(log_channel)
