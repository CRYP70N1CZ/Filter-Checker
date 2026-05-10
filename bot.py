import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def check_blocked(site):
    proxy = 'http://ckr01.rsdmo.org:8080'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://{site}',
                proxy=proxy,
                timeout=aiohttp.ClientTimeout(total=2),
                allow_redirects=False
            ) as r:
                text = await r.text()
                if 'ck-block' in text or 'blockpage' in text:
                    return 'BLOCKED'
                return 'ALLOWED'
    except:
        return 'UNKNOWN'

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="check", description="Check if a site is blocked by Rockwood filter")
@app_commands.describe(site="The site to check e.g. tiktok.com")
async def check(interaction: discord.Interaction, site: str):
    await interaction.response.defer()
    result = await check_blocked(site)
    if result == 'BLOCKED':
        await interaction.followup.send(f'🔴 **BLOCKED**: `{site}`')
    elif result == 'ALLOWED':
        await interaction.followup.send(f'🟢 **ALLOWED**: `{site}`')
    else:
        await interaction.followup.send(f'⚪ **UNKNOWN**: `{site}`')

bot.run(os.environ['TOKEN'])
