import discord
from discord.ext import commands
import requests
import urllib3
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
    print(f'Logged in as {bot.user}')

@bot.command()
async def blocked(ctx, site: str):
    await ctx.send(f'Checking `{site}`...')
    result = check_blocked(site)
    if result == 'BLOCKED':
        await ctx.send(f'🔴 **BLOCKED**: `{site}`')
    elif result == 'ALLOWED':
        await ctx.send(f'🟢 **ALLOWED**: `{site}`')
    else:
        await ctx.send(f'⚪ **UNKNOWN**: `{site}` (timeout or error)')

bot.run('token')