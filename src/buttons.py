from discord.ui import Button
import utils


class ProductButton(Button):
    def __init__(self, label, style, product_name):
        super().__init__(label=label, style=style)
        self.product_name = product_name


class StockButton(ProductButton):
    def __init__(self, label, style, product_name, product_sell_price, connexion, cursor, thread=None, bot_id=None,
                 stock_modif=0):
        super().__init__(label=label, style=style, product_name=product_name)
        self.product_sell_price = product_sell_price
        self.connexion = connexion
        self.cursor = cursor
        self.thread = thread
        self.bot_id = bot_id
        self.stock_modif = stock_modif
        self.reset = stock_modif == 0

    async def callback(self, interaction):
        if await utils.check_interaction(interaction, self.label, self.product_name):
            if self.stock_modif == 0:  # if stock_modif should be get from user message
                message = [message async for message in self.thread.history(limit=1)][0]
                if message.author.id != self.bot_id:
                    await message.delete()
                    try:
                        self.stock_modif = int(message.content)
                    except ValueError:
                        pass

                if self.stock_modif == 0:
                    await interaction.response.send_message(utils.tl_msg("bad_value").format(message.content),
                                                            ephemeral=True)
                    return

            self.cursor.execute(
                f"""
                            SELECT product_stock
                            FROM product
                            WHERE product_name = '{self.product_name}';
                            """
            )  # get product stock

            product_stock = self.cursor.fetchone()[0]

            if product_stock + self.stock_modif < 0:  # if stock_modif is under the limit
                self.stock_modif = -product_stock

            self.cursor.execute(
                f"""
                UPDATE product
                SET product_stock = product_stock + {self.stock_modif}
                WHERE product_name = '{self.product_name}';
                """
            )  # update product stock
            self.connexion.commit()


            print(utils.tl_log("stock").format(self.product_name,
                                               product_stock,
                                               product_stock + self.stock_modif,
                                               interaction.user))

            await interaction.response.edit_message(
                content=utils.tl_msg("product").format(self.product_name,
                                                       self.product_sell_price,
                                                       product_stock + self.stock_modif)
            )  # edit message with new stock

            if self.reset:  # if stock_modif should be get from user message reset the detection
                self.stock_modif = 0


class PriceButton(ProductButton):
    def __init__(self, label, style, product_name, product_buy_price):
        super().__init__(label=label, style=style, product_name=product_name)
        self.product_buy_price = product_buy_price

    async def callback(self, interaction):
        if await utils.check_interaction(interaction, self.label, self.product_name):
            await interaction.user.send(utils.tl_msg("mp_price").format(self.product_name, self.product_buy_price))
            await interaction.response.edit_message()
            print(utils.tl_log("mp_price").format(interaction.user, self.product_buy_price, self.product_name))
