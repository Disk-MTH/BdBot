import json
import os

import utils
import sqlite3
import discord
import tradlib
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bd_bot = commands.Bot(command_prefix="!", intents=intents)

config = json.load(open("config.json", "r"))
language = config["language"]

connexion = sqlite3.connect(config["db_name"])
cursor = connexion.cursor()

channel = None
messages = []

status = False


def tl_log(key):
    return tradlib.get_translation(language, ["log", 0, key])


def tl_msg(key):
    return tradlib.get_translation(language, ["msg", 0, key])


def tl_thread(key):
    if key == "":
        return tradlib.get_translation(language, ["thread", 0])
    return tradlib.get_translation(language, ["thread", 0, key])


def log_command(user, command, *args):
    print(tl_log("command").format(user, command, args, utils.get_date_time()))


@bd_bot.event
async def on_ready():
    global connexion
    global cursor
    global channel

    print(tl_log("on").format(bd_bot.user.name, bd_bot.user.discriminator))

    channel = bd_bot.get_channel(int(config["channel_id"]))

    if not channel or not isinstance(channel, discord.TextChannel):
        print(tl_log("channel_error").format(config["channel_id"]))
        print(tl_log("off"))
        await bd_bot.close()
        return

    utils.mpd(cursor)
    print(tl_log("db_on"))

    await channel.purge(limit=None)
    for thread in channel.threads:
        await thread.delete()
    print(tl_log("purge"))

    for key in tl_thread(""):
        await channel.create_thread(name=tl_thread(key))
        print(tl_log("thread").format(tl_thread(key)))

    print(tl_log("threads").format(len(channel.threads)))


@bd_bot.command()
async def ping(ctx):
    ctx.message.delete()
    log_command(ctx.author, ctx.command.name)
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(tl_msg("no_perm").format(ctx.author.mention))
        return

    await ctx.send(tl_msg("ping").format(round(bd_bot.latency * 1000)))


@bd_bot.command()
async def bdgro(ctx):
    global status

    ctx.message.delete()
    log_command(ctx.author, ctx.command.name)
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(tl_msg("no_perm").format(ctx.author.mention))
        return

    if not status:
        await ctx.send(tl_msg("open").format(
            discord.utils.get(bd_bot.get_guild(config["server_id"]).roles, name=config["role"])
        ))
        await channel.edit(name=tl_msg("status").format(tl_msg("status_open")))
        status = True
    else:
        await ctx.send(tl_msg("close"))
        await channel.edit(name=tl_msg("status").format(tl_msg("status_close")))
        status = False


@bd_bot.command()
async def stop(ctx):
    global connexion
    global cursor

    ctx.message.delete()
    log_command(ctx.author, ctx.command.name)
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(tl_msg("no_perm").format(ctx.author.mention))
        return

    print(tl_log("off"))
    await bd_bot.close()

    cursor.close()
    connexion.close()
    print(tl_log("db_off"))


if __name__ == "__main__":
    tradlib.set_translations_files_path(os.getcwd() + "\\lang")
    tradlib.set_translation_files_extension(".json")
    tradlib.load_translations_files()

    print(tl_log("languages").format(tradlib.get_available_languages()))
    print(tl_log("language").format(language))

    bd_bot.run(config["token"])
