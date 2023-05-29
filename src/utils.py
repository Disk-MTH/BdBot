import os
import tradlib
import datetime
import discord
import bdbot


def tl_log(key):
    return tradlib.get_translation(bdbot.language, ["log", 0, key])


def tl_msg(key):
    return tradlib.get_translation(bdbot.language, ["msg", 0, key])


def tl_thread(key):
    return tradlib.get_translation(bdbot.language, ["thread", 0, key])


def picture(name, product=True):
    try:
        if product:
            return discord.File(os.path.join(os.path.dirname(__file__), f"../resources/pictures/products/{name}.png"))
        return discord.File(os.path.join(os.path.dirname(__file__), f"../resources/pictures/{name}.png"))
    except FileNotFoundError:
        print(tl_log("picture_error").format(name, product))
        return discord.File(os.path.join(os.path.dirname(__file__), f"../resources/pictures/not_found.png"))


async def check_command(ctx):
    await ctx.message.delete()
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(tl_msg("no_perm").format(ctx.command.name))
        return False
    print(tl_log("command").format(ctx.author,
                                   ctx.command.name,
                                   datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")))
    return True


async def check_interaction(interaction, product_name, label):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(tl_msg("no_perm").format(label),
                                                ephemeral=True)
        return False
    print(tl_log("interaction").format(interaction.user,
                                       product_name, label,
                                       datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")))
    return True


async def shutdown():
    await bdbot.bd_bot.close()
    print(tl_log("off"))

    bdbot.cursor.close()
    bdbot.connexion.close()
    print(tl_log("db_off"))


def mpd(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS category
        (
            category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(1000) NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS price
        (
            price_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            buy_price  DOUBLE,
            sell_price DOUBLE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product
        (
            product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name  VARCHAR(1000) NOT NULL,
            product_stock INT,
            product_picture,
            price_id      INT           NOT NULL,
            category_id   INT           NOT NULL,
            FOREIGN KEY (price_id) REFERENCES price (price_id),
            FOREIGN KEY (category_id) REFERENCES category (category_id)
        );
        """
    )
