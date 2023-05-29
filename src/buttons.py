from discord.ui import Button
import utils
import bdbot


class ProductButton(Button):
    def __init__(self, label, style, product_name):
        super().__init__(label=label, style=style)
        self.product_name = product_name


class StockButton(ProductButton):
    def __init__(self, label, style, product_name, product_sell_price, connexion, cursor, remove):
        super().__init__(label=label, style=style, product_name=product_name)
        self.product_sell_price = product_sell_price
        self.connexion = connexion
        self.cursor = cursor
        self.stock_modif = -1 if remove else 1

    async def callback(self, interaction):
        if await utils.check_interaction(interaction, self.label, self.product_name):
            self.cursor.execute(
                f"""
                UPDATE product
                SET product_stock = product_stock + {self.stock_modif}
                WHERE product_name = '{self.product_name}';
                """
            )
            self.connexion.commit()

            self.cursor.execute(
                f"""
                SELECT product_stock
                FROM product
                WHERE product_name = '{self.product_name}';
                """
            )

            product_stock = self.cursor.fetchone()[0]
            print(utils.tl_log("stock").format(self.product_name,
                                               product_stock - self.stock_modif,
                                               product_stock,
                                               interaction.user))

            await interaction.response.edit_message(
                content=utils.tl_msg("product").format(self.product_name,
                                                       self.product_sell_price,
                                                       product_stock)
            )


class PriceButton(ProductButton):
    def __init__(self, label, style, product_name, product_buy_price):
        super().__init__(label=label, style=style, product_name=product_name)
        self.product_buy_price = product_buy_price

    async def callback(self, interaction):
        if await utils.check_interaction(interaction, self.label, self.product_name):
            await interaction.user.send(utils.tl_msg("mp_price").format(self.product_name, self.product_buy_price))
            await interaction.response.edit_message()
            print(utils.tl_log("mp_price").format(interaction.user, self.product_buy_price, self.product_name))
