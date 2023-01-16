"""
VERSION 0.0.1

file: listener.py
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
        print("d")
        data["Users"].append("%s %s" % (user, user.id))
        with open('database/users.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    if action == "v":
        return len(data["Users"])

class Command_Listen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("."):
            await a_users_db(message.author)
        
        #await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Command_Listen(bot))
    print(Fore.LIGHTGREEN_EX + "[SUCCESS]" + Fore.RESET + " Loaded listener.py extension")