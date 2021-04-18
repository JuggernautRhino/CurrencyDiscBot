import discord
import os
from discord.ext import commands
from Keep_alive import keep_alive
import sqlite3
from CreatingATable import tableCreation
from Check_if_in_table import check
from sqlie import connection, get_value
import time 
import math

client = commands.Bot(command_prefix = "^")
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="^help"), status = discord.Status.online)
    print('We have logged in as {0.user}'.format(client))


@client.group(invoke_without_command = True)
async def help(ctx):
    user = str(ctx.message.author)
    check(user)
    em = discord.Embed(title = "Help", description = "**Do ^<Command> to use the command!**", colour = 0x8ceb34)
    
    em.add_field(name = "Owner", value = "add, sub, all")
    em.add_field(name = "Currency", value = "bal")
    await ctx.send(embed = em)



@client.command(aliases=["bal"])
async def balance(ctx):
    user = str(ctx.message.author)
    check(user)
    conn = sqlite3.connect('Bal.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user = ?",(user,))
    user = user + "'s"
    for row in c.fetchall():
        em = discord.Embed(title = f'**{user} Balance**', colour = 0xb3f542)
        em.add_field(name = f'**Bank:**', value = row[0])
        await ctx.send(embed = em)

@client.command(aliases=["add"])
async def Add(ctx, amount):
    userr = str(ctx.message.author)
    if userr == ("JuggernautRhino#0421"):
        conn = sqlite3.connect('Bal.db')
        c = conn.cursor()
        c.execute("SELECT balance FROM users WHERE user = ?",(userr,))
        for row in c.fetchall():
            value = row[0]
        value = value + int(amount)
        await ctx.send(f'You now have **{value}** in your account!')
        c.execute("UPDATE users SET balance = ? WHERE user = ? ",(value,userr,))
        conn.commit()
    elif userr != ("JuggernautRhino#0421"):
        await ctx.send("nice try")

@client.command(aliases=["sub"])
async def Remove(ctx, amount):
    userr = str(ctx.message.author)
    if userr == ("JuggernautRhino#0421"):
        conn = sqlite3.connect('Bal.db')
        c = conn.cursor()
        c.execute("SELECT balance FROM users WHERE user = ?",(userr,))
        for row in c.fetchall():
            value = row[0]
        value = value - int(amount)
        await ctx.send(f'You now have **{value}** in your account!')
        c.execute("UPDATE users SET balance = ? WHERE user = ? ",(value,userr,))
        conn.commit()
    elif userr != ("JuggernautRhino#0421"):
        await ctx.send("nice try")

@client.command()
async def all(ctx):
    user = str(ctx.message.author)
    if user == ("JuggernautRhino#0421"):
        conn = sqlite3.connect("Bal.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        await ctx.send(c.fetchall())
        conn.close()
    elif user != ("JuggernautRhino#0421"):
        await ctx.send("required permissions not there")
        await ctx.send(user)



@client.command()
async def daily(ctx):
    user = str(ctx.message.author)
    conn,c = connection()
    if (user in daily) and daily[user] > time.time():
        waittime = daily[user] - time.time()
        await ctx.send(f'Please wait **{math.floor(waittime/3600)}h {math.floor((waittime/60) % 60)}m** to use this again!')
    else:
        await ctx.send('You got 2500!')
        get_value(conn,c,user,2500)
        conn.commit
        conn.close()
        daily[user] = time.time() + 86400


    save_daily()


keep_alive()
client.run(os.getenv('TOKEN'))

