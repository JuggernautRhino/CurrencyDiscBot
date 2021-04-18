import discord
import os
from discord.ext import commands
from Keep_alive import keep_alive
import sqlite3
from CreatingATable import tableCreation
from Check_if_in_table import check
from sqlie import connection, get_value
from Daily import *
from Monthly import *
from Yearly import *
import time 
import math
import random

client = commands.Bot(command_prefix = "^")
client.remove_command('help')
ops = ["heads","tails"]

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="^help"), status = discord.Status.online)
    print('We have logged in as {0.user}'.format(client))


@client.group(invoke_without_command = True)
async def help(ctx):
    user = str(ctx.message.author)
    check(user)
    em = discord.Embed(title = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__Help__", description = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__**Do ^<Command> to use the command!**__", colour = 0x8ceb34)
    
    em.add_field(name = "⠀Owner", value = "add, sub, all⠀⠀⠀⠀⠀⠀⠀⠀")
    em.add_field(name = "⠀⠀⠀⠀⠀Currency", value = "bal, daily, monthly, yearly⠀⠀⠀⠀⠀⠀⠀⠀")
    em.add_field(name = "⠀Games", value = "guess, flip")
    await ctx.send(embed = em)

@client.command(aliases=['ping'])
async def _ping(ctx):
    await ctx.send(f'**Pong!** In {round(client.latency * 1000)}ms')

#Owner/bal commands

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
    conn = sqlite3.connect('Bal.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user = ?",(userr,))
    for row in c.fetchall():
        value = row[0]
    value = value - int(amount)
    await ctx.send(f'You now have **{value}** in your account!')
    c.execute("UPDATE users SET balance = ? WHERE user = ? ",(value,userr,))
    conn.commit()


@client.command()
async def all(ctx):
    user = str(ctx.message.author)
    if user == ("JuggernautRhino#0421"):
        conn = sqlite3.connect("Bal.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        await ctx.author.send(c.fetchall())
        conn.close()
    elif user != ("JuggernautRhino#0421"):
        await ctx.send("required permissions not there")
        await ctx.send(user)

#Timed Commands start here

@client.command(aliases=["daily"])
async def _daily(ctx):
    user = str(ctx.message.author)
    conn,c = connection()
    if (user in daily) and daily[user] > time.time():
        waittime = daily[user] - time.time()
        await ctx.send(f'Please wait **{math.floor(waittime/3600)}h {math.floor((waittime/60) % 60)}m** to use this again!')
    else:
        await ctx.send('You got **2500!**')
        get_value(conn,c,user,2500)
        conn.close()
        daily[user] = time.time() + 86400

    save_daily()

@client.command(aliases=["monthly"])
async def _monthly(ctx):
    user = str(ctx.message.author)
    conn,c = connection()
    if (user in monthly) and monthly[user] > time.time():
        waittime = monthly[user] - time.time()
        await ctx.send(f'Please wait **{math.floor(waittime/3600)}h {math.floor((waittime/60) % 60)}m** to use this again!')
    else:
        await ctx.send('You got **50000!**')
        get_value(conn,c,user,50000)
        conn.close()
        monthly[user] = time.time() + 2592000

    save_monthly()

@client.command(aliases=["yearly"])
async def _yearly(ctx):
    user = str(ctx.message.author)
    conn,c = connection()
    if (user in yearly) and yearly[user] > time.time():
        waittime = yearly[user] - time.time()
        await ctx.send(f'Please wait **{math.floor(waittime/3600)}h {math.floor((waittime/60) % 60)}m** to use this again!')
    else:
        await ctx.send('You got **50000!**')
        get_value(conn,c,user,50000)
        conn.close()
        yearly[user] = time.time() + 31536000

    save_yearly()

#games to make money start here

@client.command(aliases=["Coin","Flip","flip"])
async def coin(ctx,guess = "0", amount = 0):
    user = str(ctx.message.author)
    conn,c = connection()
    result = random.choice(ops)
    value = amount * 2
    loss = amount * -1
    if guess == "0":
        await ctx.send("Please put either **heads** or **tails** after the command!")
    elif amount == 0:
        await ctx.send("Please specify an **amount of money** you would like to bet")
    elif result == guess.lower():
        get_value(conn,c,user,value)
        await ctx.send(f'**You Got it Right!**')
        time.sleep(0.1)
        await ctx.send(f'**{value}** was added to your account')
    elif result != guess.lower():
        await ctx.send(f"You lost **{amount}**")
        get_value(conn,c,user,loss)
    else:
        await ctx.send("I don't honestly know how this has happened but you broke it") #I love putting error messages just incase
    conn.close()

#understandably, it is pretty fun


@client.command(aliases=["guess"])
async def _numbergame(ctx,guess = 100, amount = 0):
    user = str(ctx.message.author)
    result = random.randint(0,99)
    value = amount * 4
    conn,c = connection()
    loss = amount * -1   
    if guess == 100:
        await ctx.send("Please put your **guess** after the command")
    elif amount == 0:
        await ctx.send("Please specify an **amount of money** you would like to bet")
    elif result == guess:
        get_value(conn,c,user,value)
        await ctx.send(f'**You Got it Right!**')
        time.sleep(0.1)
        await ctx.send(f'**{value}** was added to your account')
    elif result != guess:
        await ctx.send(f'The number was {result}')
        time.sleep(0.1)
        await ctx.send(f"You lost **{amount}**")
        get_value(conn,c,user,loss)
    else:
        await ctx.send("I don't honestly know how this has happened but you broke it")



  



keep_alive()
client.run(os.getenv('TOKEN'))


