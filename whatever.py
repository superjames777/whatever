import os
import json
import random
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import checks
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user}")
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="roll", description="roll a random number between min and max (inclusive)")
async def roll(interaction: discord.Interaction, min: int = 0, max: int = 100):
    await interaction.response.send_message(str(random.randint(min, max)))

@bot.tree.command(name="quote", description="get a wise quote")
async def quote(interaction: discord.Interaction):
    lastmsgs = [msg async for msg in interaction.channel.history(limit=2)]
    if len(lastmsgs) > 1:
        lastmsg = lastmsgs[1]
        await interaction.response.send_message(f'"{lastmsg.content}" - {lastmsg.author.display_name}')
    else:
        await interaction.response.send_message('"called it too early" - whatever')

@bot.tree.command(name="calculate", description="calculate an equation")
@app_commands.choices(operator=[
    app_commands.Choice(name="+ (Add)", value="+"),
    app_commands.Choice(name="- (Subtract)", value="-"),
    app_commands.Choice(name="* (Multiply)", value="*"),
    app_commands.Choice(name="/ (Divide)", value="/"),
    app_commands.Choice(name="% (Modulo)", value="%"),
    app_commands.Choice(name="** (Exponent)", value="**"),
    app_commands.Choice(name="// (Floor Divide)", value="//")
])
async def calculate(interaction: discord.Interaction, num1: float = 0.0, operator: str = "+", num2: float = 0.0):
    if operator == "+":
        await interaction.response.send_message(f"{num1 + num2}")
    elif operator == "-":
        await interaction.response.send_message(f"{num1 - num2}")
    elif operator == "*":
        await interaction.response.send_message(f"{num1 * num2}")
    elif operator == "/":
        if num2 == 0.0:
            await interaction.response.send_message("cant divide by zero")
        else:
            await interaction.response.send_message(f"{num1 / num2}")
    elif operator == "%":
        if num2 == 0.0:
            await interaction.response.send_message("cant divide by zero")
        else:
            await interaction.response.send_message(f"{num1 % num2}")
    elif operator == "**":
        await interaction.response.send_message(f"{num1 ** num2}")
    elif operator == "//":
        if num2 == 0.0:
            await interaction.response.send_message("cant divide by zero")
        else:
            await interaction.response.send_message(f"{num1 // num2}")

@bot.tree.command(name="w", description="get some Ws in the CHAT")
async def w(interaction: discord.Interaction, amount: int = 1, up: bool = False):
    version = "W" if up else "w"
    wstring = version * amount

    if len(wstring) > 2000:
        await interaction.response.send_message(version * 2000)
    else:
        await interaction.response.send_message(wstring)

@bot.tree.command(name="yesorno", description="get random yes or no")
async def yesorno(interaction: discord.Interaction):
    answer = random.randint(0, 1)
    await interaction.response.send_message("yes" if answer == 0 else "no")

@bot.tree.command(name="expose", description="expose a user for their HORRIFIC crimes")
async def expose(interaction: discord.Interaction, user: discord.Member):
    to_expose = [msg async for msg in interaction.channel.history(limit=50) if msg.author == user]
    to_expose.reverse()

    if not to_expose:
        await interaction.response.send_message("not enough yap. sorry")
        return

    total_chars = sum(len(msg.content) for msg in to_expose)

    if total_chars <= 1000:
        fmsgs = "\n".join(msg.content for msg in to_expose)
        await interaction.response.send_message(f"{fmsgs}\n\n- {user.display_name}")
    else:
        await interaction.response.send_message("too much yap. sorry")

@bot.tree.command(name="inject", description="inject a user's device with a DEALY virus that will take ALL their personal info (100% REAL)")
async def inject(interaction: discord.Interaction, user: discord.Member):
    try:
        await user.send(
            "your device has been injected with a DEADLY virus.\n"
            "if you believe this is a mistake, please go to https://superjames777.github.io/whatever/"
        )
        await interaction.response.send_message(f"injected {user.display_name}", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"failed to inject {user.display_name}")
    except discord.HTTPException as err:
        await interaction.response.send_message(f"critical error: {err}")

@bot.tree.command(name="log", description="log stuff a user said")
@checks.has_any_role("Admin", "Owner")
async def log(interaction: discord.Interaction, user: discord.Member):
    logs = {}

    if os.path.exists("log.json"):
        with open("log.json", "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = {}

    user_messages = []
    async for message in interaction.channel.history(limit=100):
        if message.author == user:
            user_messages.append(message.content)

    user_messages.reverse()
    logs[str(user.id)] = user_messages

    with open("log.json", "w") as f:
        json.dump(logs, f, indent=4)

    await interaction.response.send_message(f"logged {len(user_messages)} messages for {user.display_name}")

@log.error
async def log_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
        await interaction.response.send_message("only admins+ can use the log command", ephemeral=True)

@bot.tree.command(name="pickagame", description="randomly pick a game from space separated options")
async def pickagame(interaction: discord.Interaction, games: str):
    gameslist = games.split()
    if not gameslist:
        await interaction.response.send_message("no games?")
        return
    result = random.choice(gameslist)
    await interaction.response.send_message(f"chosen game: {result}")

@bot.tree.command(name="selectuser", description="pick a random user")
async def selectuser(interaction: discord.Interaction):
    users = []
    async for member in interaction.guild.fetch_members(limit=None):
        users.append((member.name, member.display_name))

    user = users[random.randint(0, (len(users) - 1))]
    await interaction.response.send_message(f"chosen user: {user[0]} ({user[1]})")

@bot.tree.command(name="greet", description="make whatever greet you")
async def greet(interaction: discord.Interaction):
    await interaction.response.send_message("hello")

bot.run(BOT_TOKEN)
