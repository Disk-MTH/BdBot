import sqlite3
import discord
from discord.ext import commands

def mdp(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product
        (
            name VARCHAR(1000),
            description VARCHAR(1000),
            price DOUBLE,
            sell_price DOUBLE,
            stock INT,
            profil_picture BLOB,
        PRIMARY KEY(name)
        );
        """
    )


if __name__ == "__main__":
    connexion = sqlite3.connect("bdgro.db")
    cursor = connexion.cursor()

    mdp(cursor)





    cursor.close()
    connexion.close()
