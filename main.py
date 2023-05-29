import json
import os
import sqlite3
import discord
import tradlib
import datetime
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
bd_bot = commands.Bot(command_prefix="!", intents=intents)

config = json.load(open("config.json", "r"))
language = config["language"]

connexion = None
cursor = None

guild = None
channel = None
role = None

status = False
messages = {}


def tl_log(key):
    return tradlib.get_translation(language, ["log", 0, key])


def tl_msg(key):
    return tradlib.get_translation(language, ["msg", 0, key])


def tl_thread(key):
    return tradlib.get_translation(language, ["thread", 0, key])


def picture(name, product=True):
    try:
        if product:
            return discord.File(f"resources/pictures/products/{name}.png")
        return discord.File(f"resources/pictures/{name}.png")
    except FileNotFoundError:
        print(tl_log("picture_error").format(name, product))
        return discord.File(f"resources/pictures/not_found.png")


async def check_command(ctx):
    await ctx.message.delete()
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(tl_msg("no_perm").format(ctx.command.name))
        return False
    print(tl_log("command").format(ctx.author,
                                   ctx.command.name,
                                   datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")))
    return True


async def check_interaction(interaction, label):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(tl_msg("no_perm").format(label),
                                                ephemeral=True)
        return False
    print(tl_log("interaction").format(interaction.user,
                                       messages.get(interaction.message.id),  # sql query to get product name
                                       label,
                                       datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")))
    return True


async def shutdown():
    await bd_bot.close()
    print(tl_log("off"))

    cursor.close()
    connexion.close()
    print(tl_log("db_off"))


@bd_bot.event
async def on_ready():
    global connexion
    global cursor
    global guild
    global channel
    global role
    global status

    print(tl_log("on").format(bd_bot.user.name, bd_bot.user.discriminator))

    guild = bd_bot.get_guild(int(config["guild_id"]))

    if not guild:
        print(tl_log("guild_error").format(config["guild_id"]))
        await shutdown()
        return

    channel = bd_bot.get_channel(int(config["channel_id"]))

    if not channel or not isinstance(channel, discord.TextChannel):
        print(tl_log("channel_error").format(config["channel_id"]))
        await shutdown()
        return

    role = discord.utils.get(guild.roles, name=config["role"])

    if not role:
        print(tl_log("role_error").format(config["role"]))
        await shutdown()
        return

    connexion = sqlite3.connect(config["db_name"])
    cursor = connexion.cursor()
    print(tl_log("db_on"))

    await channel.purge(limit=None)
    for thread in channel.threads:
        await thread.delete()
    print(tl_log("purge"))

    await channel.edit(name=tl_msg("channel"))
    print(tl_log("channel_set").format(channel.name))

    await channel.send(tl_msg("closed"), file=picture("closed", False))

    cursor.execute(
        """
        SELECT category_name 
        FROM category;
        """
    )

    for category in [category[0] for category in cursor.fetchall()]:
        thread = await channel.create_thread(name=tl_thread(category))

        cursor.execute(
            f"""
            SELECT product_id, product_name, product_stock, product_picture, buy_price, sell_price 
            FROM product
                    JOIN category ON product.category_id = category.category_id
                    JOIN price ON product.price_id = price.price_id
            WHERE category_name = '{category}';
            """
        )

        for product_id, product_name, product_stock, product_picture, product_buy_price, product_sell_price \
                in cursor.fetchall():

            re_stock = Button(label="Add", style=discord.ButtonStyle.green)

            async def re_stock_callback(interaction):
                if await check_interaction(interaction, re_stock.label):
                    # sql query to add stock
                    # log
                    pass

            re_stock.callback = re_stock_callback



            de_stock = Button(label="Remove", style=discord.ButtonStyle.red)

            async def de_stock_callback(interaction):
                if await check_interaction(interaction, de_stock.label):
                    # sql query to remove stock
                    # log
                    pass

            de_stock.callback = de_stock_callback



            get_price = Button(label="Get", style=discord.ButtonStyle.blurple)

            async def get_price_callback(interaction):
                if await check_interaction(interaction, get_price.label):
                    # private message to the user with the sell price
                    await interaction.user.send(product_sell_price)
                    # log

            get_price.callback = get_price_callback


            message = await thread.send(
                tl_msg("product").format(product_name, product_sell_price, product_stock),
                file=picture(product_picture), view=View().add_item(re_stock).add_item(de_stock).add_item(get_price)
            )
            messages[message.id] = product_id

            print(tl_log("product").format(product_name))

    print(tl_log("ready"))


@bd_bot.command()
async def ping(ctx):
    if not await check_command(ctx):
        return

    await ctx.send(tl_msg("ping").format(round(bd_bot.latency * 1000)))


@bd_bot.command()
async def bdgro(ctx):
    global status

    if not await check_command(ctx):
        return

    await channel.purge(limit=None)
    if not status:
        await channel.send(tl_msg("open").format(role.mention), file=picture("open", False))
    else:
        await channel.send(tl_msg("closed"), file=picture("closed", False))
    status = not status


if __name__ == "__main__":
    tradlib.set_translations_files_path(os.getcwd() + "\\resources\\langs")
    tradlib.set_translation_files_extension(".json")
    tradlib.load_translations_files()

    print(tl_log("languages").format(tradlib.get_available_languages()))
    print(tl_log("language").format(language))

    bd_bot.run(config["token"])
