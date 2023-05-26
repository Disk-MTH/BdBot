import utils
import sqlite3
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bd_bot = commands.Bot(command_prefix="!", intents=intents)


@bd_bot.event
async def on_ready():
    print(f"Bot connected as {bd_bot.user.name}")


@bd_bot.command()
async def ping(ctx):
    log_command(ctx.author, ctx.command.name)
    await ctx.send(f"La latence est de {round(bd_bot.latency * 1000)}ms")


@bd_bot.command()
async def stop(ctx):
    log_command(ctx.author, ctx.command.name)
    print("Bot disconnected")
    await bd_bot.close()


def log_command(user, command):
    print(f"The user {user} used the command {command} at {utils.get_date_time()}")


if __name__ == "__main__":
    print("Database connection")
    connexion = sqlite3.connect("bdgro.db")
    cursor = connexion.cursor()

    print("Database tables creation")
    utils.mdp(cursor)

    bd_bot.run(open('token.txt', 'r').read())

    print("Database disconnection")
    cursor.close()
    connexion.close()
