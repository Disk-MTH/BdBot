import os
import json
import utils
import sqlite3
import discord
import tradlib
import buttons
from discord.ext import commands
from discord import ChannelType
from discord.ui import View

"""---------------------------------------- Variables ----------------------------------------"""

intents = discord.Intents.default()
intents.message_content = True
bd_bot = commands.Bot(command_prefix="!", intents=intents)

config = json.load(open(os.path.join(os.path.dirname(__file__), "../resources/config.json"), "r"))
language = config["language"]

connexion = None
cursor = None

guild = None
channel = None
role = None

status = False
messages = {}

"""---------------------------------------- Bot events ----------------------------------------"""


@bd_bot.event
async def on_ready():
    global connexion
    global cursor
    global guild
    global channel
    global role
    global status

    print(utils.tl_log("on").format(bd_bot.user.name, bd_bot.user.discriminator))

    """------------------------------ Check config validity ------------------------------"""
    guild = bd_bot.get_guild(int(config["guild_id"]))

    if not guild:
        print(utils.tl_log("guild_error").format(config["guild_id"]))
        await utils.shutdown()
        return

    channel = bd_bot.get_channel(int(config["channel_id"]))

    if not channel or not isinstance(channel, discord.TextChannel):
        print(utils.tl_log("channel_error").format(config["channel_id"]))
        await utils.shutdown()
        return

    role = discord.utils.get(guild.roles, name=config["role"])

    if not role:
        print(utils.tl_log("role_error").format(config["role"]))
        await utils.shutdown()
        return

    """------------------------------ Connect to database ------------------------------"""
    connexion = sqlite3.connect("resources/" + config["db_name"])
    cursor = connexion.cursor()
    print(utils.tl_log("db_on"))

    """------------------------------ Prepare the bot channel ------------------------------"""
    await channel.purge(limit=None)
    for thread in channel.threads:
        await thread.delete()
    print(utils.tl_log("purge"))

    await channel.edit(name=utils.tl_msg("channel"))
    print(utils.tl_log("channel").format(channel.name))

    """------------------------------ Create products ------------------------------"""
    cursor.execute(
        """
        SELECT category_name 
        FROM category;
        """
    )  # get categories

    for category in [category[0] for category in cursor.fetchall()]:  # walk through categories
        thread = await channel.create_thread(name=utils.tl_thread(category), type=ChannelType.public_thread)

        cursor.execute(
            f"""
            SELECT product_id, product_name, product_stock, product_picture, buy_price, sell_price 
            FROM product
                    JOIN category ON product.category_id = category.category_id
                    JOIN price ON product.price_id = price.price_id
            WHERE category_name = '{category}';
            """
        )  # get products from category

        for product_id, product_name, product_stock, product_picture, product_buy_price, product_sell_price \
                in cursor.fetchall():  # walk through products

            """--------------------- Create buttons --------------------"""
            re_stock = buttons.StockButton(label=utils.tl_msg("btn_add"),
                                           style=discord.ButtonStyle.green,
                                           product_name=product_name,
                                           product_sell_price=product_sell_price,
                                           connexion=connexion,
                                           cursor=cursor,
                                           thread=thread,
                                           bot_id=bd_bot.user.id)

            de_stock = buttons.StockButton(label=utils.tl_msg("btn_remove"),
                                           style=discord.ButtonStyle.red,
                                           product_name=product_name,
                                           product_sell_price=product_sell_price,
                                           connexion=connexion,
                                           cursor=cursor)

            get_price = buttons.PriceButton(label=utils.tl_msg("btn_get"),
                                            style=discord.ButtonStyle.blurple,
                                            product_name=product_name,
                                            product_buy_price=product_buy_price)

            """--------------------- Send message --------------------"""
            message = await thread.send(
                utils.tl_msg("product").format(product_name, product_sell_price, product_stock),
                file=utils.picture(product_picture),  # add picture
                view=View().add_item(re_stock).add_item(de_stock).add_item(get_price)
            )
            messages[message.id] = product_id

            print(utils.tl_log("product").format(product_name))

    """------------------------------ Prepare the bot channel ------------------------------"""
    await channel.send(utils.tl_msg("closed"), file=utils.picture("closed", False))

    print(utils.tl_log("ready"))


"""---------------------------------------- Bot commands ----------------------------------------"""


@bd_bot.command()
async def ping(ctx):
    if not await utils.check_command(ctx):
        return

    await ctx.send(utils.tl_msg("ping").format(round(bd_bot.latency * 1000)))


@bd_bot.command()
async def bdgro(ctx):
    global status

    if not await utils.check_command(ctx):
        return

    await channel.purge(limit=1)
    if not status:
        await channel.send(utils.tl_msg("open").format(role.mention), file=utils.picture("open", False))
    else:
        await channel.send(utils.tl_msg("closed"), file=utils.picture("closed", False))
    status = not status


"""---------------------------------------- Main script ----------------------------------------"""

if __name__ == "__main__":
    tradlib.set_translations_files_path(os.getcwd() + "\\resources\\langs")
    tradlib.set_translation_files_extension(".json")
    tradlib.load_translations_files()
    print(utils.tl_log("language").format(language))

    bd_bot.run(config["token"])
