from collections.abc import Awaitable, Callable

import discord
from discord.ext import commands

from config import BARRIER_ROLE_ID, CURSED_TECHNIQUE_ROLE_ID, RCT_ROLE_ID
from models.ficha import Ficha
from repository.ficha_repository import criar_ficha, existe_ficha, get_ficha, salvar_ficha
from training_logic import treinar_atributo


class TrainingView(discord.ui.View):
    def __init__(self, role_ids: set[int]) -> None:
        super().__init__()

        botoes = [
            ("reforco", "Reforço", "💪"),
            ("controle", "Controle", "🧠"),
            ("tecnica", "Técnica", "⚔️"),
        ]

        if RCT_ROLE_ID in role_ids:
            botoes.append(("rct", "Energia Reversa", "❤️‍🩹"))

        if BARRIER_ROLE_ID in role_ids:
            botoes.append(("barreira", "Barreira", "🛡️"))

        for atributo, label, emoji in botoes:
            botao = discord.ui.Button(
                label=label,
                emoji=emoji,
                custom_id=f"treinar:{atributo}",
            )
            botao.callback = self._criar_callback(atributo)
            self.add_item(botao)

    def _criar_callback(
        self, atributo: str
    ) -> Callable[[discord.Interaction], Awaitable[None]]:
        async def callback(interaction: discord.Interaction) -> None:
            await self.processar_treinamento(interaction, atributo)

        return callback

    async def processar_treinamento(
        self, interaction: discord.Interaction, atributo: str
    ) -> None:
        ficha = get_ficha(interaction.user.id)

        if ficha is None:
            await interaction.response.edit_message(
                content="Você ainda não possui uma ficha. Utilize !ficha.",
                embed=None,
                view=None,
            )
            return

        resultado = treinar_atributo(ficha, atributo)
        salvar_ficha(ficha)

        emojis = {
            "Reforço": "💪",
            "Controle": "🧠",
            "Técnica": "⚔️",
            "Energia Reversa": "❤️‍🩹",
            "Barreira": "🛡️",
        }
        nome_atributo = resultado.nome_atributo
        emoji = emojis[nome_atributo]

        if resultado.subiu_de_nivel:
            embed = discord.Embed(
                title=f"🎉 {nome_atributo} evoluiu!",
                description=(
                    f"Lv.{resultado.nivel_anterior} → Lv.{resultado.nivel_atual}\n\n"
                    "XP restante:\n"
                    f"{resultado.xp_atual}/{resultado.xp_necessario}"
                ),
                color=discord.Color.dark_purple(),
            )
        else:
            embed = discord.Embed(
                title="🏋️ Treinamento",
                description=(
                    f"{emoji} {nome_atributo} treinado.\n\n"
                    f"+{resultado.xp_ganho} XP\n\n"
                    f"Lv.{resultado.nivel_atual}\n\n"
                    f"XP: {resultado.xp_atual}/{resultado.xp_necessario}"
                ),
                color=discord.Color.dark_purple(),
            )

        await interaction.response.edit_message(embed=embed, view=self)


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

    @commands.command(name="treinar")
    async def treinar(self, ctx: commands.Context) -> None:
        if not existe_ficha(ctx.author.id):
            await ctx.send("Você ainda não possui uma ficha. Utilize !ficha.")
            return

        role_ids = {role.id for role in ctx.author.roles}
        embed = discord.Embed(
            title="🏋️ Treinamento",
            description=(
                "Escolha qual atributo deseja treinar.\n\n"
                "Cada treinamento concede XP ao atributo escolhido."
            ),
            color=discord.Color.dark_purple(),
        )
        await ctx.send(embed=embed, view=TrainingView(role_ids))

    @commands.command(name="status")
    async def status(self, ctx: commands.Context) -> None:
        ficha = get_ficha(ctx.author.id)

        if ficha is None:
            await ctx.send("Você ainda não possui uma ficha.\nUse !ficha primeiro.")
            return

        embed = discord.Embed(
            title=f"Status de {ctx.author.display_name}",
            color=discord.Color.dark_purple(),
        )
        atributos = [
            f"\❤️ Vida.............{ficha.vida_atual}/{ficha.vida_max}",
            f"\🔷 Energia..........{ficha.ce_atual}/{ficha.ce_max}",
            "━━━━━━━━━━━━━━━━━━━━",
            f"\💪 Reforço..........Lv.{ficha.reforco_nivel} ({ficha.reforco_xp}/100)",
            f"\🧠 Controle.........Lv.{ficha.controle_nivel} ({ficha.controle_xp}/100)",
            f"\⚔️ Técnica..........Lv.{ficha.tecnica_nivel} ({ficha.tecnica_xp}/100)",
        ]
        detalhes = []

        role_ids = {role.id for role in ctx.author.roles}

        if RCT_ROLE_ID in role_ids:
            atributos.extend(
                [
                    f"\❤️‍🩹 RCT............Lv.{ficha.rct_nivel} ({ficha.rct_xp}/100)",
                ]
            )

        if BARRIER_ROLE_ID in role_ids:
            atributos.extend(
                [
                    f"\🛡️ Barreira.........Lv.{ficha.barreira_nivel} ({ficha.barreira_xp}/100)",
                ]
            )

        if CURSED_TECHNIQUE_ROLE_ID in role_ids:
            tecnicas = {
                "limitless": "Limitless",
                "ten shadows": "Ten Shadows",
                "blood manipulation": "Blood Manipulation",
            }
            tecnica_amaldicoada = next(
                (
                    tecnicas[role.name.casefold()]
                    for role in ctx.author.roles
                    if role.name.casefold() in tecnicas
                ),
                "Desconhecida",
            )
            detalhes.extend(["\🌑 Técnica Amaldiçoada", tecnica_amaldicoada])

        detalhes.extend(["\📌 Estado", "Normal", "\✨ Efeitos", "Nenhum"])
        embed.add_field(
            name="\u200b",
            value="\n".join(atributos),
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value="\n".join(detalhes),
            inline=False,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FichaCog(bot))
