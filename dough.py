import discord
from discord.ext import commands

import rolldice

import dark_light
from data import DATA
import init
import parse_crits
import parse_nlrme
import random
import quests
import levers

bot = commands.Bot(command_prefix='>')
commands

def format_status(dark: int, light: int):
    return "DARK: " + str(dark) + "\nLIGHT: " + str(light)

@bot.command()
async def ping(ctx):
    """
    Pings the bot to make sure it's online.
    """
    await ctx.send("Pong!")

@bot.command(name="set")
async def set_(ctx, dark: int, light: int):
    """
    Sets the dark and light side points.
    """
    dark_light.set_dark_light(dark, light)
    await ctx.send(format_status(dark, light))

@bot.command()
async def light(ctx):
    """
    Uses a light side point.
    """
    dark, light = dark_light.get_dark_light()
    if light <= 0:
        await ctx.send("No light points remaining.")
    else:
        dark += 1
        light -= 1
        dark_light.set_dark_light(dark, light)
        await ctx.send(format_status(dark, light))

@bot.command()
async def dark(ctx):
    """
    Uses a dark side point.
    """
    dark, light = dark_light.get_dark_light()
    if dark <= 0:
        await ctx.send("No dark points remaining.")
    else:
        light += 1
        dark -= 1
        dark_light.set_dark_light(dark, light)
        await ctx.send(format_status(dark, light))

@bot.command()
async def effect(ctx):
    """
    Rolls on the random magical effect table.
    """
    rolls = parse_nlrme.get_rolls()
    roll = random.choice(rolls)
    await ctx.send(roll)

@bot.command()
async def crit(ctx, table: str):
    """
    Rolls on a critical hit table.
    """
    tables = parse_crits.get_tables()
    matches = [t for t in tables if t.lower().startswith(table.lower())]
    if len(matches) > 1:
        await ctx.send(f"Multiple tables matching '{table}': " + str(matches))
    elif len(matches) == 0:
        await ctx.send(f"No tables matching '{table}'")
    else:
        roll = random.choice(tables[matches[0]])
        await ctx.send(matches[0])
        await ctx.send(roll)

@bot.command(aliases=["r"])
async def roll(ctx, *roll_code):
    """
    Rolls some dice.

    See https://www.critdice.com/roll-advanced-dice/ for syntax.
    """
    roll = " ".join(roll_code)
    mention = ctx.author.mention
    result, explanation = rolldice.roll_dice(roll)
    await ctx.send(f"{mention}\nResult: {result}\nExplanation: {explanation}")

@bot.command(aliases=["aq"])
async def addquest(ctx, *quest):
    """
    Adds a quest to the quest list.
    """
    quests.add(" ".join(quest))
    for quest in quests.get_formatted():
        await ctx.send(quest)

@bot.command(aliases=["rq"])
async def removequest(ctx, num: int):
    """
    Removes a quest from the quest list.
    """
    quests.remove(num)
    for quest in quests.get_formatted():
        await ctx.send(quest)

@bot.command()
async def check(ctx, num: int):
    """
    Checks off a quest from the quest list.
    """
    quests.check(num)
    for quest in quests.get_formatted():
        await ctx.send(quest)

@bot.command()
async def fail(ctx, num: int):
    """
    Marks a quest as failed.
    """
    quests.fail(num)
    for quest in quests.get_formatted():
        await ctx.send(quest)

@bot.command()
async def uncheck(ctx, num: int):
    """
    Resets a quest.
    """
    quests.uncheck(num)
    for quest in quests.get_formatted():
        await ctx.send(quest)

@bot.command(name="quests")
async def quests_(ctx):
    """
    Lists the quests.
    """
    for quest in quests.get_formatted():
        await ctx.send(quest)

@bot.command()
async def server(ctx):
    """
    Gives a link to the Foundry server.
    """
    with DATA.lock:
        await ctx.send(DATA.get()["server"])

@bot.command()
async def setserver(ctx, addr):
    """
    Sets the link to the Foundry server.
    """
    with DATA.lock:
        DATA.get()["server"] = addr
        DATA.write()
    await ctx.send(f"Set the server to `{addr}`.")

@bot.command()
async def pull(ctx, lever):
    """
    Pulls a lever in the museum.
    """
    try:
        message = levers.pull(int(lever))
        await ctx.send(message)
    except ValueError:
        await ctx.send("Invalid lever.")

@bot.command()
async def look(ctx):
    """
    Looks at the status of the museum display.
    """
    await ctx.send(levers.look())

@bot.command()
async def reset(ctx, num_levers, num_objects):
    """
    Creates a new lever puzzle with the given number of levers and objects.
    """
    await ctx.send(levers.reset(num_levers, num_objects))
    

async def on_command_error(ctx, error):
    print(error)
    mention = ctx.author.mention
    if ctx.command:
        usage = usage_string(ctx.command)
        help = ctx.command.help
        await ctx.send(f"{mention}\n{usage}\n\n{help}")
    else:
        await ctx.send(f"{mention}\n{error}")

def usage_string(command) -> str:
    return f"usage: `>{command.name} {command.signature}`"

bot.on_command_error = on_command_error

with DATA.lock:
    api_key = DATA.get()["api-key"]
bot.run(api_key)