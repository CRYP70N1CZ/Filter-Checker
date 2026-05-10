import discord
from discord.ext import commands
from discord import app_commands
import requests
import urllib3
import asyncio
import os
urllib3.disable_warnings()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def check_blocked(site):
    proxies = {'http': 'http://ckr01.rsdmo.org:8080'}
    try:
        r = requests.get(f'http://{site}', proxies=proxies, timeout=3, allow_redirects=False)
        if 'ck-block' in r.text or 'blockpage' in r.text:
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
    result = await asyncio.get_event_loop().run_in_executor(None, check_blocked, site)
    if result == 'BLOCKED':
        await interaction.followup.send(f'🔴 **BLOCKED**: `{site}`')
    elif result == 'ALLOWED':
        await interaction.followup.send(f'🟢 **ALLOWED**: `{site}`')
    else:
        await interaction.followup.send(f'⚪ **UNKNOWN**: `{site}`')

bot.run(os.environ['TOKEN'])
