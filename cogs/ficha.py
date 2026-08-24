import discord
from discord.ext import commands

from models.ficha import Ficha
from repository.ficha_repository import criar_ficha, existe_ficha


class FichaCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ficha")
    async def ficha(self, ctx: commands.Context) -> None:
        if existe_ficha(ctx.author.id):
            await ctx.send("Sua ficha já foi criada.")
            return

        ficha = Ficha(
            user_id=ctx.author.id,
            vida_atual=100,
            vida_max=100,
            ce_atual=100,
            ce_max=100,
            reforco_nivel=1,
            reforco_xp=0,
            controle_nivel=1,
            controle_xp=0,
            tecnica_nivel=1,
            tecnica_xp=0,
            rct_nivel=1,
            rct_xp=0,
            barreira_nivel=1,
            barreira_xp=0,
        )
        criar_ficha(ficha)

        embed = discord.Embed(
            title="Ficha criada!",
            description=f"A ficha de {ctx.author.mention} foi criada com sucesso.",
            color=discord.Color.dark_purple(),
        )
        embed.add_field(name="Vida", value="100 / 100", inline=True)
        embed.add_field(name="Energia Amaldiçoada", value="100 / 100", inline=True)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FichaCog(bot))
