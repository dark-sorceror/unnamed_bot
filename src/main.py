"""
VERSION 0.0.1

file: main.py
"""

import json
import random
import asyncio
import logging
import logging.handlers
import os
from colorama import Fore

from typing import List, Optional

import discord
import discord
from discord.ext import commands
from discord.ext import commands, tasks

class UnnamedBot(commands.Bot):
    def __init__(
        self, 
        *args, 
        initial_extensions: List[str],
        testing_guild_id: Optional[int] = None, 
        **kwargs
    ):
        super().__init__(command_prefix=".", intents=discord.Intents.all(), owner_ids=[497903117241810945])
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        
    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)
            
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            
async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    exts = ['admin', 'listener', 'misc']
    
    async with UnnamedBot(commands.when_mentioned, initial_extensions=exts) as bot:
        
        @bot.command()
        async def extension(ctx, action, ext): 
            try:
                if action.lower() in ["load", "l"]:
                    if ext.lower() in ["all", 'a']:
                        for a in exts:
                            await bot.load_extension(a)
                    else:
                        await bot.load_extension(ext)
                elif action.lower() in ["reload", "r", "re"]:
                    if ext.lower() in ["all", 'a']:
                        for a in exts:
                            await bot.reload_extension(a)
                    else:
                        await bot.reload_extension(ext)
                elif action.lower() in ["unload", "u", "un"]:
                    if ext.lower() in ["all", 'a']:
                        for a in exts:
                            await bot.unload_extension(a)
                    else:
                        await bot.unload_extension(ext)
                        
            except discord.ext.commands.ExtensionAlreadyLoaded as e:
                await ctx.reply(f"```diff\n- Extension Already Loaded\n---> {e}```")
            except discord.ext.commands.ExtensionError as e:
                await ctx.reply(f"```diff\n- Extension Error\n---> {e}```")
            except discord.ext.commands.ExtensionFailed as e:
                await ctx.reply(f"```diff\n- Extension Failed\n---> {e}```")
            except discord.ext.commands.ExtensionNotFound as e:
                await ctx.reply(f"```diff\n- Extension Not Found\n---> {e}```")
            except discord.ext.commands.ExtensionNotLoaded as e:
                await ctx.reply(f"```diff\n- Extension Not Loaded\n---> {e}```")
                
        print(Fore.LIGHTGREEN_EX + "[SUCCESS]" + Fore.RESET + " Bot is running")
            
        await bot.start("MTA2Mzk5OTM5NzYwOTg2NTMxOA.GS5QYZ.O5nsQ1K56QcoxK5tPmOHkrqeSkdstfPJEYVNm4")

asyncio.run(main())