import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def roll(ctx, min: int = 0, max: int = 100):
    await ctx.send(random.randint(min, max))

@bot.command()
async def quote(ctx):
    lastmsgs = [msg async for msg in ctx.channel.history(limit=2)]
    if len(lastmsgs) > 1:
        lastmsg = lastmsgs[1]
        await ctx.send(f'"{lastmsg.content}" - {lastmsg.author.display_name}')
    else:
        await ctx.send(f'"called it too early" - whatever')

@bot.command()
async def calculate(ctx, num1: float = 0.0, operator: str = "+", num2: float = 0.0):
    if operator == "+":
        await ctx.send(f"{num1 + num2}")
    elif operator == "-":
        await ctx.send(f"{num1 - num2}")
    elif operator == "*":
        await ctx.send(f"{num1 * num2}")
    elif operator == "/":
        if num2 == 0.0:
            await ctx.send("cant divide by zero")
        else:
            await ctx.send(f"{num1 / num2}")
    elif operator == "%":
        if num2 == 0.0:
            await ctx.send("cant divide by zero")
        else:
            await ctx.send(f"{num1 % num2}")
    else:
        await ctx.send("not an operator")

@bot.command()
async def w(ctx, amount: int = 1, up: bool = False):
    version = "W" if up else "w"
    wstring = version * amount

    if len(wstring) > 2000:
        await ctx.send(version * 2000)
    else:
        await ctx.send(wstring)

@bot.command()
async def YorN(ctx):
    answer = random.randint(0, 1)
    if answer == 0:
        await ctx.send("yes")
    else:
        await ctx.send("no")

@bot.command()
async def expose(ctx, user):
    msghistory = [msg async for msg in ctx.channel.history(limit=50)]
    to_expose = []
    for msg in msghistory:
        if msg.author.display_name == user:
            to_expose.append(msg.content)
    total_chars = 0
    if len(to_expose) > 0:
        for msg in to_expose:
            for char in msg.content:
                total_chars += 1
        if total_chars <= 1000:
            await ctx.send(f"{to_expose} - {user}")
        else:
            await ctx.send("too much yap. sorry")
    else:
        await ctx.send("not enough yap. sorry")

bot.run("MTU0MjA0NTgwNTE2OTM0ODYxOQ.GJYK93.8e_WvfuM12b3xX1ar68XrAXMcmVDWmTrdHK3uQ")
