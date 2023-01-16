import json
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(".", intents=discord.Intents.all(), owner_ids=[497903117241810945])

titles = {
    "hi",
    "ji"
}

emojis = {
    "le": "<:lb_e:1064031045361619044>",
    "me": "<:mb_e:1064031091196952596>",
    "re": "<:rb_e:1064031122922668112>",
    "fh": "<:lb_health:1064031159425708062>",
    "mh": "<:mb_health:1064031213314117744>",
    "rh": "<:rb_health:1064031278858502175>",
    "len": "<:lb_energy:1064031331144704040>",
    "men": "<:mb_energy:1064031369929445416>",
    "ren": "<:rb_energy:1064031476414423100>",
    "lex": "<:lb_exp:1064031507255148574>",
    "mex": "<:mb_exp:1064031548329951242>",
    "rex": "<:rb_exp:1064031577593610240>"
}

masteries = {
    "Melee": {
        "Punching Style": {
            1: ["*Throw a powerful punch* -10 Energy", (10, 20), 10, 
                ["%s threw a strong punch, dealing **%s damage**",
                 "%s landed a strong punch, dealing **%s damage**"
                 ]
            ]
        }
    }
}

async def a_stats_db(user, action: str, stat: str, amount: int = None):
    with open('database/stats.json', 'r') as f:
        data = json.load(f)

    if "%s %s" % (user.name, user.id) not in data:
        data["%s %s" % (user.name, user.id)] = {}
        data["%s %s" % (user.name, user.id)]["Health"] = 0
        data["%s %s" % (user.name, user.id)]["Energy"] = 0
        data["%s %s" % (user.name, user.id)]["Power"] = 0
        data["%s %s" % (user.name, user.id)]["Weapon"] = 0

        with open('database/stats.json', 'w') as f:
            json.dump(data, f, indent=4)

    if action == "v":
        return data["%s %s" % (user.name, user.id)][stat.title()]
    elif action == "e":
        data["%s %s" % (user.name, user.id)][stat.title()] += amount

    with open('database/stats.json', 'w') as f:
        json.dump(data, f, indent=4)

async def a_exp_db(user, action: str, option: str, amount: int = None):
    with open('database/exp.json', 'r') as f:
        data = json.load(f)

    if "%s %s" % (user.name, user.id) not in data:
        data["%s %s" % (user.name, user.id)] = {}
        data["%s %s" % (user.name, user.id)]["Level"] = 1
        data["%s %s" % (user.name, user.id)]["Experience"] = 0

        with open('database/exp.json', 'w') as f:
            json.dump(data, f, indent=4)

    if action == "v":
        return data["%s %s" % (user.name, user.id)][option.title()]
    elif action == "e":
        data["%s %s" % (user.name, user.id)][option.title()] += amount

async def a_atks_db(user, action: str, option: str, details: str, atk: str = None):
    with open('database/attacks.json', 'r') as f:
        data = json.load(f)

    if "%s %s" % (user.name, user.id) not in data:
        data["%s %s" % (user.name, user.id)] = {}
        data["%s %s" % (user.name, user.id)]["Power"] = {}
        data["%s %s" % (user.name, user.id)]["Sword"] = {}
        data["%s %s" % (user.name, user.id)]["Melee"] = {}
        data["%s %s" % (user.name, user.id)]["Melee"]["Style"] = "Punching Style"
        data["%s %s" % (user.name, user.id)]["Melee"]["Masteries Unlocked"] = 1

        with open('database/attacks.json', 'w') as f:
            json.dump(data, f, indent=4)

    if action == "v":
        return data["%s %s" % (user.name, user.id)][option.title()][details.title()]
    elif action == "e":
        data["%s %s" % (user.name, user.id)][option.title()][details.title()] = atk

    with open('database/attacks.json', 'w') as f:
        json.dump(data, f, indent=4)

@commands.command()
async def start(ctx):
    embed = discord.Embed(title="Welcome to ", description="""
    Power Lists:
    **
    > :white_circle: ┃ :bomb: Bomb
    > :white_circle: ┃ :rock: Rock
    > :green_circle: ┃ :flame: Fire
    > :green_circle: ┃ :droplet: Water
    > :blue_circle: ┃ :cloud_tornado: Wind
    > :purple_circle: ┃ :zap: Lightning
    > :purple_circle: ┃ :ice_cube: Ice    
    > :yellow_circle: ┃ :dna: Gene
    > :red_circle: ┃ <:crack:1059661764377190452> Vibration
    **     
    """)

    await ctx.send(embed=embed)

@commands.command()
async def sprofile(ctx):
    embed = discord.Embed(
        title="%s's Profile" % ctx.author.name,
        description="""
        **:crown: King
        -〘 :nazar_amulet: Mysterious 〙-
        :flag_ca: Canada
        :red_circle: ┃ <:crack:1059661764377190452> Vibration**
        """,
        color=discord.Color.random()
    )
    embed.add_field(name="Level 5", value=f"""
        `228/1,000`
        {emojis["FS"]}{emojis["FB"]}{emojis["EB"]}{emojis["EE"]}
        """
                    )
    embed.set_thumbnail(url=ctx.author.avatar)

    await ctx.reply(embed=embed)

class Stats_Button(discord.ui.Button['Stats']):
    def __init__(self, label: str, color, disabled: bool):
        super().__init__(style=discord.ButtonStyle.success,
                         label=label, emoji="➕", disabled=disabled)
        self.label = label
        self.color = color

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Stats = self.view

        await a_stats_db(interaction.user, "e", self.label, 1)

        health = await a_stats_db(interaction.user, "v", "Health")
        Energy = await a_stats_db(interaction.user, "v", "Energy")
        power = await a_stats_db(interaction.user, "v", "Power")
        weapon = await a_stats_db(interaction.user, "v", "Weapon")
        level = await a_exp_db(interaction.user, "v", "Level")

        pa = level * 3 - (health + Energy + power + weapon)

        if pa == 0:
            for child in view.children:
                child.disabled = True

            view.stop()

        embed = discord.Embed(
            title=f"Stats for {interaction.user}",
            description=f"""```ml\nHealth  {f"{health:,}".rjust(30)}\nEnergy {f"{Energy:,}".rjust(30)}\nPower   {f"{power:,}".rjust(30)}\nWeapon  {f"{weapon:,}".rjust(30)}```""",
            color=self.color
        )
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.set_footer(text=f"Level: {level} | Points Available: {pa}")

        await interaction.response.edit_message(embed=embed, view=view)

@commands.command()
async def stats(ctx):
    with open('stats.json', 'r') as f:
        data = json.load(f)

    health = await a_stats_db(ctx.author, "v", "Health")
    Energy = await a_stats_db(ctx.author, "v", "Energy")
    power = await a_stats_db(ctx.author, "v", "Power")
    weapon = await a_stats_db(ctx.author, "v", "Weapon")
    level = await a_exp_db(ctx.author, "v", "Level")

    pa = level * 3 - (health + Energy + power + weapon)

    color = discord.Color.random()

    class Stats(discord.ui.View):
        def __init__(self, color):
            super().__init__(timeout=20)

            self.color = color
            self.pa = pa

            for i in ["Health", "Energy", "Power", "Weapon"]:
                self.add_item(Stats_Button(label=i, color=self.color, disabled=True if self.pa == 0 else False))

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user and interaction.user.id == self.author:
                return True
            else:
                await interaction.response.send_message('This interaction is not yours.', ephemeral=True)
                return False

        async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
            await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
            print(error)
            self.stop()

        async def on_timeout(self) -> None:
            for child in self.children:
                child.disabled = True
            await self.message.edit(view=self)
            self.stop()

    view = Stats(color=color)

    embed = discord.Embed(
        title=f"Stats for {ctx.author}",
        description=f"""```ml\nHealth  {f"{health:,}".rjust(30)}\nEnergy {f"{Energy:,}".rjust(30)}\nPower   {f"{power:,}".rjust(30)}\nWeapon  {f"{weapon:,}".rjust(30)}```""",
        color=color
    )
    embed.set_thumbnail(url=ctx.author.avatar)
    embed.set_footer(text=f"Level {level} | Points Available: {pa}")
    view.author = ctx.author.id
    view.message = await ctx.send(embed=embed, view=view)

class Attack_Menu(discord.ui.View):
    def __init__(self, i: list, e: list, color: discord.Color, message, message2, turn, users, style=None, attack=None, hm=None):
        super().__init__(timeout=10)

        self.i = i
        self.e = e
        self.i_h = self.i[1]
        self.i_s = self.i[2]
        self.e_h = self.e[1]
        self.e_s = self.e[2]
        self.i_l = self.i[3]
        self.e_l = self.e[3]
        
        self.attack = attack
        self.message = message
        self.message2 = message2
        self.color = color
        self.hm = hm
        self.turn = turn
        self.users = users
        self.style = style
        
        self.add_item(Attack_Selection(
            [
                discord.SelectOption(label='Melee', description='Punching Style', emoji='👊')
            ], 
            self.i, 
            self.e, 
            self.color, 
            self.message,
            self.message2,
            self.turn,
            self.users
        ))
        if self.attack:
            for i in range(1, len(masteries[self.attack][self.style].keys()) + 1):
                self.add_item(Fight_Button(i, discord.ButtonStyle.grey, False if i <= self.hm else True, self.color, 1, self.i, self.e, self.message, self.message2, self.turn, self.users, attack="Melee"))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.i[0].id or interaction.user.id == self.e[0].id:
            if interaction.user.id == self.turn.id:
                return True
            else:
                await interaction.response.send_message('It is not your turn', ephemeral=True)
                return False
        else:
            await interaction.response.send_message('This fight is not yours', ephemeral=True)
            return False
        
    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
            
        embed = discord.Embed(
            title=f"{self.i[0].name} vs {self.e[0].name}",
            color=self.color
        )
        embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\nHealth — {self.i_h}\nEnergy — {self.i_s}")
        embed.add_field(name=self.e[0], value=f"Level — {self.e_l}\nHealth — {self.e_h}\nEnergy — {self.e_s}", inline=True)
        embed.add_field(name="Recent Action",value=f"`Fight has ended due to timeout on {self.turn}.`", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')
        await self.message.edit(content=f":tada: {self.e[0].mention if self.turn == self.i[0] else self.i[0].mention} wins! :tada:", embed=embed, view=None)
        await self.message2.delete()
        self.stop()

    """
    async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
        await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
        print(error)
        self.stop()
    """

class Fight_Button(discord.ui.Button['Fight']):
    def __init__(self, label: str, style: discord.ButtonStyle, disabled: bool, e_c, row: int, i, e, message, message2, turn, users, attack=None, emoji: str = None):
        super().__init__(style=style, label=label, emoji=emoji, disabled=disabled, row=row)
        self.i = i
        self.e = e
        self.i_h = self.i[1]
        self.i_s = self.i[2]
        self.e_h = self.e[1]
        self.e_s = self.e[2]
        self.i_l = self.i[3]
        self.e_l = self.e[3]
        self.color = e_c
        self.label = label
        self.message = message
        self.message2 = message2
        self.turn = turn
        self.users = users
        self.attack = attack

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Fight = self.view
        
        """
        if self.label == "Forfeit":
            for child in view.children:
                child.disabled = True
                
            embed = discord.Embed(
                title=f"{self.i[0].name} vs {self.e[0].name}",
                color=self.color
            )
            embed.add_field(name=self.i[0],value=f"Level — {self.i_l}\nHealth — {self.i_h}\nEnergy — {self.i_s}")
            embed.add_field(name=self.e[0], value=f"Level — {self.e_l}\nHealth — {self.e_h}\nEnergy — {self.e_s}", inline=True)
            embed.add_field(name="Recent Action",value="`Fight has ended due to .`", inline=False)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')
            
            await self.message.edit(embed=embed, view=view)
            
            embed = discord.Embed(
                title="Fight has ended!",
                description="Choose an attack below"
            )
            
            Attack_Menu(self.i, self.e, self.color, self.message, finished=True)
            await interaction.edit_original_response(content="hi")
            await interaction.response.send_message(content="Successfully forfeited", ephemeral=True)
            view.stop()
        """
            
        if self.turn == self.i[0]:
            style = await a_atks_db(self.i[0], "v", self.attack, "Style")
            
            damage = random.randint(masteries[self.attack][style][int(self.label)][1][0], masteries[self.attack][style][int(self.label)][1][1])
            
            self.i_s -= masteries[self.attack][style][int(self.label)][2]
            self.e_h -= damage
            self.i[2] = self.i_s
            self.e[1] = self.e_h
                
        else:
            style = await a_atks_db(self.e[0], "v", self.attack, "Style")
            
            damage = random.randint(masteries[self.attack][style][int(self.label)][1][0], masteries[self.attack][style][int(self.label)][1][1])
            
            self.e_s -= masteries[self.attack][style][int(self.label)][2]
            self.i_h -= damage
            self.e[2] = self.e_s
            self.i[1] = self.i_h
            
        embed = discord.Embed(
            title=f"{self.i[0].name} vs {self.e[0].name}",
            color=self.color
        )
        embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\nHealth — {self.i_h}\nEnergy — {self.i_s}")
        embed.add_field(name=self.e[0] , value=f"Level — {self.e_l}\nHealth — {self.e_h}\nEnergy — {self.e_s}", inline=True)
        embed.add_field(name="Recent Action",value=f"{random.choice(masteries[self.attack][style][int(self.label)][3])}" % (self.turn.name, damage), inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')
        
        await self.message.edit(embed=embed)
        
        for a in self.users:
            if a != self.turn:
                self.turn = a

                embed = discord.Embed(
                    title="It's your turn!",
                    description="Choose an attack below"
                )
                am_view = Attack_Menu(self.i, self.e, self.color, self.message, self.message2, self.turn, self.users)
                await interaction.response.edit_message(content=self.turn.mention, embed=embed, view=am_view)
                break

class Attack_Selection(discord.ui.Select['Fight']):
    def __init__(self, options, i, e, color, message, message2, turn, users):
        super().__init__(placeholder="Choose an Attack", options=options)
        self.i = i
        self.e = e
        self.color = color
        self.message = message
        self.message2 = message2
        self.turn = turn
        self.users = users

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Fight = self.view
        
        if self.turn == self.i[0]:
            melee = await a_atks_db(self.i[0], "v", "Melee", "Style")
            mm = await a_atks_db(self.i[0], "v", "Melee", "Masteries Unlocked")
        else:
            melee = await a_atks_db(self.e[0], "v", "Melee", "Style")
            mm = await a_atks_db(self.e[0], "v", "Melee", "Masteries Unlocked")
        
        embed = discord.Embed(
            title=f"{self.values[0]}: {melee}",
            description=f"""**__Mastery__**\n```md\n1. {masteries[self.values[0]][melee][1][0]}\n{f"2. {masteries[self.values[0]][melee][2][0] if mm > 1 else '— LOCKED —'}" if len(masteries[self.values[0]][melee].keys()) >= 2 else ''}\n{f"3. {masteries[self.values[0]][melee][3][0] if mm > 2 else ''}" if len(masteries[self.values[0]][melee].keys()) >= 3 else ''}\n{f"4. {masteries[self.values[0]][melee][4][0] if mm > 3 else '— LOCKED —'}" if len(masteries[self.values[0]][melee].keys()) >= 4 else ''}```""",
            color=discord.Color.random()
        )
        
        await interaction.response.edit_message(embed=embed, view=Attack_Menu(self.i, self.e, self.color, self.message, self.message2, self.turn, self.users, style=melee, attack=self.values[0].title(), hm=mm))

@commands.command()
async def fight(ctx, enemy: discord.Member):
    color = discord.Color.random()

    i_l = await a_exp_db(ctx.author, "v", "Level")
    e_l = await a_exp_db(enemy, "v", "Level")
    i_hs = await a_stats_db(ctx.author, "v", "Health")
    i_ss = await a_stats_db(ctx.author, "v", "Energy")
    e_hs = await a_stats_db(enemy, "v", "Health")
    e_ss = await a_stats_db(enemy, "v", "Energy")

    i_h = 100 + (5 * i_hs)
    i_s = 100 + (5 * i_ss)
    e_h = 100 + (5 * e_hs)
    e_s = 100 + (5 * e_ss)
    
    melee = await a_atks_db(ctx.author, "v", "Melee", "Style")
    melee_e = await a_atks_db(enemy, "v", "Melee", "Style")
    
    users = [ctx.author, enemy]
    turn = random.choice(users)

    class Fight(discord.ui.View):
        def __init__(self, i: list, e: list, color, message, turn, users):
            super().__init__()

            self.i = i
            self.e = e
            self.message = message
            self.color = color
            self.turn = turn
            self.users = users

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user and (interaction.user.id == self.i[0].id or interaction.user.id == self.e[0].id):
                return True
            else:
                await interaction.response.send_message('This fight is not yours', ephemeral=True)
                return False

        async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
            await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
            print(error)
            self.stop()

    embed = discord.Embed(
        title=f"{ctx.author.name} vs {enemy.name}",
        color=color
    )
    embed.add_field(name=ctx.author,value=f"Level — {i_l}\nHealth — {i_h}\nEnergy — {i_s}")
    embed.add_field(name=enemy, value=f"Level — {e_l}\nHealth — {e_h}\nEnergy — {e_s}", inline=True)
    embed.add_field(name="Recent Action",value="`Fight has started.`", inline=False)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')
    message = await ctx.send(embed=embed)
    view = Fight(i=[ctx.author, i_h, i_s, i_l], e=[enemy, e_h, e_s, e_l], color=color, message=message, turn=turn, users=users)
    await message.edit(view=view)
    
    embed2 = discord.Embed(
        title="It's your turn!",
        description="Choose an attack below"
    )

    message2 = await ctx.send(embed=embed2)
    am_view = Attack_Menu([ctx.author, i_h, i_s, i_l], [enemy, e_h, e_s, e_l], color, message, message2, turn, users, style=melee if turn==ctx.author else melee_e)
    await message2.edit(content=turn.mention, view=am_view)

@commands.command()
async def train(ctx):
    embed = discord.Embed(
        description="""
            **EXP +25**
            """,
        color=discord.Color.random()
    )
    await ctx.send(embed=embed)

@commands.command()
async def boss(ctx):
    pass

async def setup(bot):
    bot.add_command(start)
    bot.add_command(sprofile)
    bot.add_command(stats)
    bot.add_command(fight)
    bot.add_command(train)
    bot.add_command(boss)