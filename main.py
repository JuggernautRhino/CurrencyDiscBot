import discord
import os
from discord.ext import commands
from Keep_alive import keep_alive
import sqlite3

client = commands.Bot(command_prefix = "^")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="^help"), status = discord.Status.online)
    print('We have logged in as {0.user}'.format(client))











keep_alive()
client.run(os.getenv('TOKEN'))


