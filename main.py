import utils
import sqlite3
import discord
import tradlib
from discord.ext import commands

language = "english"
intents = discord.Intents.default()
intents.message_content = True

bd_bot = commands.Bot(command_prefix="!", intents=intents)


def tl_log(key):
    return tradlib.get_translation(language, ["log", 0, key])


def tl_msg(key):
    return tradlib.get_translation(language, ["msg", 0, key])


def log_command(user, command):
    print(tl_log("command").format(user, command, utils.get_date_time()))


@bd_bot.event
async def on_ready():
    print(tl_log("on").format(bd_bot.user.name, bd_bot.user.discriminator))


@bd_bot.command()
async def ping(ctx):
    log_command(ctx.author, ctx.command.name)
    await ctx.send(tl_msg("ping").format(round(bd_bot.latency * 1000)))


@bd_bot.command()
async def stop(ctx):
    log_command(ctx.author, ctx.command.name)
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(tl_msg("stop").format(ctx.author.mention))
        return
    print(tl_log("off"))
    await ctx.send(tl_msg("stop"))
    await bd_bot.close()


if __name__ == "__main__":
    tradlib.set_translation_files_extension(".json")
    tradlib.load_translations_files()

    print(tl_log("languages").format(tradlib.get_available_languages()))
    print(tl_log("language").format(language))

    connexion = sqlite3.connect("bdgro.db")
    cursor = connexion.cursor()
    utils.mpd(cursor)
    print(tl_log("db_on"))

    bd_bot.run(open("token.txt", "r").read())

    cursor.close()
    connexion.close()
    print(tl_log("db_off"))
