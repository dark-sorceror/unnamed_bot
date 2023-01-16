"""
VERSION 0.0.1

file: admin.py
"""

import json
from colorama import Fore

import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = Bot(command_prefix=".", intents=discord.Intents.all(), owner_ids=[497903117241810945])

async def a_users_db(user, action: str = None, specific = None):
    with open('database/users.json', 'r') as f:
        data = json.load(f)

    if "%s %s" % (user, user.id) not in data["Users"]:
        data["Users"].append("%s %s" % (user, user.id))
        with open('database/users.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    if action == "v":
        return len(data["Users"])

@commands.command()
@commands.is_owner()
async def botstats(ctx):
    users = await a_users_db(ctx.author, action="v")
    
    embed = discord.Embed(
        title="Bot Statistics",
        description=f"```ml\nUnique Registered Users: {users}```"
    )
    
    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(botstats)
    print(Fore.LIGHTGREEN_EX + "[SUCCESS]" + Fore.RESET + " Loaded admin.py extension")