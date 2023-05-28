import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

count = 0
channel = None
message = None


@bot.event
async def on_ready():
    global channel
    global message
    print(f"Connecté en tant que {bot.user.name}")
    channel = bot.get_channel(1111630562940174416)
    await channel.send(f"Le compteur est : {count}\n(image.png)")
    async for msg in channel.history(limit=1):
        message = msg


@bot.command()
async def update(ctx, value: int):
    global count
    global message
    count = value

    if message is not None:
        await message.edit(content=f"Le compteur est : {count}\n(image.png)")


bot.run(open("token.txt", "r").read())
