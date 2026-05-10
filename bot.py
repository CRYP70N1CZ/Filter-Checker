import discord
from discord.ext import commands
from discord import app_commands
import requests
import urllib3
import os
urllib3.disable_warnings()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def check_blocked(site):
    proxies = {
        'http': 'http://ckr01.rsdmo.org:8080',
        'https': 'http://ckr01.rsdmo.org:8080'
    }
    try:
        r = requests.get(f'http://{site}', proxies=proxies, timeout=5, allow_redirects=False)
        if 'ck-block' in r.text or 'blockpage' in r.text:
            return 'BLOCKED'
    except:
        pass
    try:
        requests.get(f'https://{site}', proxies=proxies, timeout=5, verify=False)
        return 'ALLOWED'
    except requests.exceptions.ProxyError:
        return 'BLOCKED'
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
    result = check_blocked(site)
    if result == 'BLOCKED':
        await interaction.followup.send(f'🔴 **BLOCKED**: `{site}`')
    elif result == 'ALLOWED':
        await interaction.followup.send(f'🟢 **ALLOWED**: `{site}`')
    else:
        await interaction.followup.send(f'⚪ **UNKNOWN**: `{site}`')

bot.run(os.environ['TOKEN'])
