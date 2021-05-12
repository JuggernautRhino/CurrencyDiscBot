import discord
import os
from discord.ext import commands
from Keep_alive import keep_alive
import sqlite3
from CreatingATable import tableCreation, inv_tableCreation
from Check_if_in_table import *
from sqlie import connection, get_value,get_inv
from Daily import *
from Monthly import *
from Yearly import *
from Gamle import rand_card
from Gamle import checkcard
from Shop import shop
from thing import make_a_word
import time
import math
import random
import yaml  #if it says yaml module not found use 'pip install PyYAML' in the shell    --fixed    added the pyyaml package in the package manager


client = commands.Bot(command_prefix = "^")
client.remove_command('help')
ops = ["heads","tails"]
value = []
admin=['JuggernautRhino#0421', 'LifeIsForFun#9372']

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="^help"), status = discord.Status.online)
    print('We have logged in as {0.user}'.format(client))


@client.group(invoke_without_command = True)
async def help(ctx):
    user = str(ctx.author)
    check(user)
    em = discord.Embed(title = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__Help__", description = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__**Do ^<Command> to use the command!**__", colour = 0x8ceb34)
    
    em.add_field(name = "⠀Owner", value = "add, sub, all⠀⠀⠀⠀⠀⠀⠀⠀")
    em.add_field(name = "⠀⠀⠀⠀⠀Currency", value = "bal, daily, monthly, yearly⠀⠀⠀⠀⠀⠀⠀⠀")
    em.add_field(name = "⠀⠀⠀Games", value = "guess, flip, aob, bj")
    await ctx.send(embed = em)

@client.command(aliases=['ping'])
async def _ping(ctx):
    await ctx.send(f'**Pong!** In {round(client.latency * 1000)}ms')

#Owner/bal commands

@client.command(aliases=["bal"])
async def balance(ctx):
    user = str(ctx.author)
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
    if userr in admin:
        try:
            conn = sqlite3.connect('Bal.db')
            c = conn.cursor()
            c.execute("SELECT balance FROM users WHERE user = ?",(userr,))
            for row in c.fetchall():
                value = row[0]
            value = value + int(amount)
            await ctx.send(f'You now have **{value}** in your account!')
            c.execute("UPDATE users SET balance = ? WHERE user = ? ",(value,userr,))
            conn.commit()
        except OverflowError:
            await ctx.send("Bruh, you know thats too large")
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
    if user in admin:
        conn = sqlite3.connect("Bal.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        await ctx.author.send(c.fetchall())
        conn.close()
    elif user != ("JuggernautRhino#0421"):
        await ctx.send("required permissions not there")
        await ctx.send(user)

@client.command()
async def All(ctx):
    user = str(ctx.message.author)
    if user in admin:
        conn = sqlite3.connect("Bal.db")
        c = conn.cursor()
        c.execute("SELECT * FROM inv")
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


"""
games to make money start here
"""


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

@client.command(aliases=['aboveorbelow','aob']) 
async def _aob(ctx, amount : int):
    user = ctx.author # oh shoot i didn't realise you didnt have to put .message.
    num = random.randint(0,100)
    await ctx.send('0-100 inclusive. 10 goes. hurry up nad go')
    for att in range(10):
        await ctx.send(f'You have **`{10-att}`** goes left')
        attempt = await client.wait_for("message", check=lambda m: m.author == user)
        if attempt.author == user:
            if att == 9: 
                break
            if attempt.content == str(num):
                value = amount * 2
                await ctx.send(f"GG, you got it. As a reward you get **`{value}`**.")
                conn,c = connection()
                get_value(conn,c,str(user),value)
                conn.close()
                return
            elif int(attempt.content) > num:
                await ctx.send('guess lower')
            else:
                await ctx.send('guess higher')
    await ctx.send('u lost lol')
    conn,c = connection()
    get_value(conn,c,user,(amount * -1))

#cardgames start here

@client.command(aliases=["blackjack","bj"])
async def _blackjack(ctx, amount = 0):
    user = ctx.author
    handvalue = 0
    otherhandvalue = 0
    temp = random.randint(1,13)
    otherhand1 = temp
    temp = random.randint(1,13)
    otherhand2 = temp
    temp = random.randint(1,13)
    hand1 = temp
    temp = random.randint(1,13)
    hand2 = temp
    if amount != 0:
        if hand1 == 11:
            hand1out = ("a Jack")
        elif hand1 == 12:
            hand1out = ("a Queen")
        elif hand1 == 13:
            hand1out = ("a King")   
        elif hand1 == 1:
            hand1out = ("an Ace")
        else:
            hand1out = str(hand1)
        if hand2 == 11:
            hand2out = ("a Jack")
        elif hand2 == 12:
            hand2out = ("a Queen")
        elif hand2 == 13:
            hand2out = ("a King")
        elif hand2 == 1:
            hand2out = ("an Ace")
        else:
            hand2out = str(hand2)
        em = discord.Embed(title="BlackJack", description=f"Your hand is **{hand1out}** and **{hand2out}**", colour = 0xb3f542)
        await ctx.send("Do you want to stick or twist?")
        again = (await client.wait_for("message", check=lambda m: m.author == user)).content.lower()
        if again == ("stick"):
            pass
        elif again == ("twist"):
            temp = random.randint(1,13)
            hand3 = temp
            if hand3 == 11:
                hand3out = ("a Jack")
            elif hand3 == 12:
                hand3out = ("a Queen")
            elif hand3 == 13:
                hand3out = ("a King")
            elif hand3 == 1:
                hand3out = ("an Ace")
            else:
                hand3out = str(hand2)
            em = discord.Embed(title="BlackJack", description=f"Your new hand is **{hand1out}**, **{hand2out}** and **{hand3out}**", colour = 0xb3f542)
            await ctx.send(embed = em)
        else:
          await ctx.send(f"Learn to spell please")
        if hand1 > 10:
            handvalue += 10
        elif hand1 == 1:
            handvalue += 11 # or 1, sort it out later
        else:
            handvalue += hand1
        if hand2 > 10:
            handvalue += 10
        elif hand2 == 1:
            handvalue += 11
        else:
            handvalue += hand2
        if again == ("twist"):
            if hand3 > 10:
                handvalue += 10
            elif hand3 == 1:
                handvalue += 11
            else:
                handvalue += hand3
        if otherhand1 > 10:
            otherhandvalue += 10
        elif otherhand1 == 1:
            otherhandvalue += 11
        else:
            otherhandvalue += otherhand1
        if otherhand2 > 10:
            otherhandvalue += 10
        elif otherhand2 == 1:
            otherhandvalue += 11
        else:
            otherhandvalue += otherhand2
        
        if otherhandvalue > handvalue:
            await ctx.send(f"You have failed, the opponent had {otherhandvalue} and you only had {handvalue}")
            conn,c = connection()
            user = ctx.author
            loss = amount * -1
            get_value(conn,c,user,loss)
            conn.close()
        elif handvalue > otherhandvalue:
            await ctx.send(f"You have succeeded, the opponent had {otherhandvalue} and you had {handvalue}")
            conn,c = connection()
            user = ctx.author
            win = amount * 2
            get_value(conn,c,user,win)
            conn.close()
        elif handvalue == otherhandvalue:
            await ctx.send(f"You drew, you both had {handvalue}")
        else:
          await ctx.send(f"Why am I so bad at avoiding bugs?")
    else:
      await ctx.send(f"You need to actually bet something you know")



@client.command(aliases=['pont','pontune'])
async def _pontune(ctx, amount=50):
    user = ctx.author
    firstcard = str(rand_card()) 
    secondcard = str(rand_card())
    ace = '0'
    temp = firstcard
    em = discord.Embed(title=':diamonds::hearts:Pontune:clubs::spades:', description='These are your **first** cards. Would you like to **`twist`** (+1 card) or **`stick`** (finish your turn without picking up a card)?', colour=ctx.author.colour)
    em.add_field(name='Card 1:', value=f"{firstcard}")#oka im dum
    em.add_field(name='Card 2:', value=f"{secondcard}")
    for i in range(2):
        if 'Ace' in temp:
            await ctx.send(f'You have a {firstcard} and a {secondcard} in your hand! Is the ace a 1 or an 11?')
            ace = (await client.wait_for("message", check=lambda m: m.author == user)).content #  omg im actually stupid omfg
        temp = secondcard
    em.add_field(name='total value:', value=checkcard(firstcard,secondcard,ace))

    await ctx.send(embed=em)


#inv starts here


@client.command(aliases=["inv"])
async def _inv(ctx):
    user = ctx.author
    conn,c = connection()
    result = check_inv(user,conn,c)
    if result is None:
        await ctx.send("Created Your Inv, please use this command again to show it!")
    else:
        await ctx.send(result[::])

@client.command(aliases = ["shop"])
async def Shop(ctx):
    user = ctx.author
    em = discord.Embed(title = f"{user}'s shop!", description = f"{yaml.dump(shop)}", colour = 0xb3f542)
    await ctx.send(embed = em)

@client.command()
async def check(ctx):
    user = ctx.author
    conn,c=connection()
    hi = str("item1")
    c.execute("SELECT item1 FROM inv WHERE user = ?",(str(user),))
    ha = c.fetchone()
    await ctx.send(ha)
    print(ha)

@client.command(aliases=["b"])
async def buy(ctx,item1 = "0",item2 = "0",item3 ="0",item4 = "0", item5 = "0",item6="0"):
    user = str(ctx.message.author)
    item = make_a_word(item1,item2,item3,item4,item5,item6)
    if item == "0":
        await ctx.send("Please specify an item!")
    else:
        if item in shop:
            conn,c = connection()
            value = shop[item]
            get_value(conn,c,user,value)
            get_inv(conn,c,user,item)  #<-- this is the thing that i need to do first
            await ctx.send("Test Message **(means succesful purchase when completed)**")
            #need to remove the amount and give it to User
        elif item not in shop:
            await ctx.send("**Please specify an item that you can actually buy!**")
            

            
@help.command(aliases=['ping'])
async def __ping(ctx):
    em = discord.Embed(title="'ping' command help", description="Returns the bot's latency", colour=ctx.author.colour)
    await ctx.send(embed=em)

@help.command(aliases=['bal','balance'])
async def _balance(ctx):
    em = discord.Embed(title="'bal' command help", description="shows ur balance, idiot", colour = 0xb3f542)
    await ctx.send(embed = em)

@help.command(aliases=['add'])
async def no_perms(ctx):
    user = ctx.author
    if str(user) not in admin:
        await ctx.send(f"{user.mention} you don't have perms for admin commands :joy:")


keep_alive()
client.run(os.environ['TOKEN'])


