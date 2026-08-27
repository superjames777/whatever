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
    elif operator == "**":
        await ctx.send(f"{num1 ** num2}")
    elif operator == "//":
        if num2 == 0.0:
            await ctx.send("cant divide by zero")
        else:
            await ctx.send(f"{num1 // num2}")
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
async def expose(ctx, user: discord.Member):
    to_expose = [msg async for msg in ctx.channel.history(limit=50) if msg.author == user]
    to_expose.reverse()

    if not to_expose:
        await ctx.send("not enough yap. sorry")

    total_chars = sum(len(msg.content) for msg in to_expose)

    if total_chars <= 1000:
        fmsgs = "\n".join(msg.content for msg in to_expose)
        await ctx.send( f"{fmsgs}\n\n- {user.display_name}")
    else:
        await ctx.send("too much yap. sorry")

@bot.command
async def inject(ctx, user: discord.Member):
    try:
        await user.send("your device has been injected with a DEADLY virus.\nif you believe this is a mistake, please go to _")
    except discord.Forbidden:
        await ctx.send(f"failed to inject {user.display_name}")
    except discord.HTTPException as err:
        await ctx.send(f"critical error: {err}")
        
bot.run("MTU0MjA0NTgwNTE2OTM0ODYxOQ.GJYK93.8e_WvfuM12b3xX1ar68XrAXMcmVDWmTrdHK3uQ")
