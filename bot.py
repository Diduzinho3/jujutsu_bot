import asyncio

import discord
from discord.ext import commands

from config import BOT_PREFIX, DISCORD_TOKEN
from db import init_db


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


async def main() -> None:
    init_db()
    await bot.load_extension("cogs.ficha")
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
