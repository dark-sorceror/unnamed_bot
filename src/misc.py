import json
import random
import datetime

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
    "hl": "<:lb_health:1064031159425708062>",
    "hm": "<:mb_health:1064031213314117744>",
    "hr": "<:rb_health:1064031278858502175>",
    "el": "<:lb_energy:1064031331144704040>",
    "em": "<:mb_energy:1064031369929445416>",
    "er": "<:rb_energy:1064031476414423100>",
    "exl": "<:lb_exp:1064031507255148574>",
    "exm": "<:mb_exp:1064031548329951242>",
    "exr": "<:rb_exp:1064031577593610240>"
}

levels = {
    1: 10
}

# Desc, Damage Range, Energy Cost
masteries = {
    "Melee": {
        "Punching Style": {
            1: ["*Throw a powerful punch* -10 Energy", (50, 100), 10, 
                ["%s threw a strong punch, dealing **%s damage**",
                 "%s landed a strong punch, dealing **%s damage**"
                 ]
            ]
        }
    }
}

fights = {
    
}

async def id_maker():
    return datetime.datetime.now()

async def barcode_maker(i_exp, i_mexp, e_exp, e_mexp, i_h, i_mh, i_e, i_me, e_h, e_mh, e_e, e_me):
    ibl = 0 if i_exp / i_me == 0 else 1 if 0 < i_exp / i_me <= 0.2 else 2 if 0.2 < i_exp / i_me <= 0.4 else 3 if 0.4 < i_exp / i_me <= 0.6 else 4 if 0.6 < i_exp / i_me <= 0.8 else 5
    ibh = 0 if i_h / i_mh == 0 else 1 if 0 < i_h / i_mh <= 0.2 else 2 if 0.2 < i_h / i_mh <= 0.4 else 3 if 0.4 < i_h / i_mh <= 0.6 else 4 if 0.6 < i_h / i_mh <= 0.8 else 5
    ibe = 0 if i_e / i_me == 0 else 1 if 0 < i_e / i_me <= 0.2 else 2 if 0.2 < i_e / i_me <= 0.4 else 3 if 0.4 < i_e / i_me <= 0.6 else 4 if 0.6 < i_e / i_me <= 0.8 else 5
    ebl = 0 if e_exp / e_me == 0 else 1 if 0 < e_exp / e_me <= 0.2 else 2 if 0.2 < e_exp / e_me <= 0.4 else 3 if 0.4 < e_exp / e_me <= 0.6 else 4 if 0.6 < e_exp / e_me <= 0.8 else 5
    ebh = 0 if e_h / e_mh == 0 else 1 if 0 < e_h / e_mh <= 0.2 else 2 if 0.2 < e_h / e_mh <= 0.4 else 3 if 0.4 < e_h / e_mh <= 0.6 else 4 if 0.6 < e_h / e_mh <= 0.8 else 5
    ebe = 0 if e_e / e_me == 0 else 1 if 0 < e_e / e_me <= 0.2 else 2 if 0.2 < e_e / e_me <= 0.4 else 3 if 0.4 < e_e / e_me <= 0.6 else 4 if 0.6 < e_e / e_me <= 0.8 else 5
        
    barcode = [1] * ibl + [0] * (5 - ibl) + [1] * ibh + [0] * (5 - ibh) + [1] * ibe + [0] * (5 - ibe) + [1] * ebl + [0] * (5 - ebl) + [1] * ebh + [0] * (5 - ebh) + [1] * ebe + [0] * (5 - ebe)
    
    prefix = ""
    btoemoji = []
    for a,b in enumerate(barcode, 1):
        if (a <= 5) or (15 < a <= 20):
            prefix = "ex"
        elif (10 >= a > 5) or (20 < a <= 25):
            prefix = "h"
        else:
            prefix = "e"

        btoemoji.append(emojis[prefix + "l" if a in [1,6,11,16,21,26] else prefix + "r" if a in [5,10,15,20,25,30] else prefix + "m"]) if b == 1 else btoemoji.append(emojis["le" if a in [1,6,11,16,21,26] else "re" if a in [5,10,15,20,25,30] else "me"])

    return btoemoji

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

async def a_fight_db(id_, action: str, option: str, edit: str = None):
    if "%s" % id_ not in fights:
        fights["%s" % id_] = {}
        fights["%s" % id_]["Game Over"] = False
        fights["%s" % id_]["Winner"] = None
        fights["%s" % id_]["Stats"] = None
    if action == "v":
        return fights["%s" % id_][option]
    elif action == "e":
        fights["%s" % id_][option] = edit

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

class Fight_Button(discord.ui.Button['Fight']):
    def __init__(self, label, style, disabled, row, color, i, e, atk_msg, act_msg, turn, attack=None):
        self.i = i
        self.i_h = i[1]
        self.i_e = i[2]
        self.i_l = i[3]
        
        self.e = e
        self.e_h = e[1]
        self.e_e = e[2]
        self.e_l = e[3]
        
        self.turn = turn
        self.atk_msg = atk_msg
        self.act_msg = act_msg
        self.color = color
        self.attack = attack
        
        self.game_over = False
        
        super().__init__(style=style, label=label, disabled=disabled, row=row)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Fight = self.view
        
        #barcode index: 0-4 health | 5-9 energy | 10-14 e health | 15-19 e energy 
        i_exp = await a_exp_db(self.i[0], "v", "Experience")
        e_exp = await a_exp_db(self.e[0], "v", "Experience")
        i_mexp = levels[self.i_l]
        e_mexp = levels[self.e_l]
        i_mh = 100 + (5 * await a_stats_db(self.i[0], "v", "Health"))
        i_me = 100 + (5 * await a_stats_db(self.i[0], "v", "Energy"))
        e_mh = 100 + (5 * await a_stats_db(self.e[0], "v", "Health"))
        e_me = 100 + (5 * await a_stats_db(self.e[0], "v", "Energy"))
        
        i_style = await a_atks_db(self.i[0], "v", self.attack, "Style")
        e_style = await a_atks_db(self.e[0], "v", self.attack, "Style")
            
        if self.turn == self.i[0]:
            damage = random.randint(masteries[self.attack][i_style][int(self.label)][1][0], masteries[self.attack][i_style][int(self.label)][1][1])
            
            self.i_e -= masteries[self.attack][i_style][int(self.label)][2]
            self.e_h -= damage
            self.i[2] = self.i_e
        else:
            damage = random.randint(masteries[self.attack][e_style][int(self.label)][1][0], masteries[self.attack][e_style][int(self.label)][1][1])
            
            self.e_e -= masteries[self.attack][e_style][int(self.label)][2]
            self.i_h -= damage
            self.e[2] = self.e_e
                
        if self.e_h <= 0 or self.i_h <= 0:
            if self.turn == self.i[0]:
                self.e_h = 0
            else:
                self.i_h = 0
            self.game_over = True
            
        self.i[1] = self.i_h
        self.e[1] = self.e_h
            
        btoemoji = await barcode_maker(i_exp, i_mexp, e_exp, e_mexp, self.i_h, i_mh, self.i_e, i_me, self.e_h, e_mh, self.e_e, e_me)
            
        embed = discord.Embed(
            title=f"{self.i[0].name} vs {self.e[0].name}",
            color=self.color
        )
        embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\n" + ''.join(btoemoji[0:5]) + f"\nHealth — {self.i_h}/{i_mh}\n" + ''.join(btoemoji[5:10]) + f"\nEnergy — {self.i_e}/{i_me}\n" + ''.join(btoemoji[10:15]))
        embed.add_field(name=self.e[0] , value=f"Level — {self.e_l}\n" + ''.join(btoemoji[15:20]) + f"\nHealth — {self.e_h}/{e_mh}\n" + ''.join(btoemoji[20:25]) + f"\nEnergy — {self.e_e}/{e_me}\n" + ''.join(btoemoji[25:30]), inline=True)
        embed.add_field(name="Recent Action",value=f"{random.choice(masteries[self.attack][i_style if self.turn == self.i[0] else e_style][int(self.label)][3])}" % (self.turn.name, damage), inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')
        
        await self.atk_msg.edit(content=self.turn.mention, embed=embed)
        if not self.game_over:
            previous_turn = self.turn
            self.turn = self.i[0] if previous_turn == self.e[0] else self.e[0]
            self.game_over = False

            embed = discord.Embed(
                title="It's your turn!",
                description="Choose an attack below"
            )
            am_view = AM_stg1(self.i, self.e, self.turn, self.atk_msg, self.act_msg, self.color)
            await interaction.response.edit_message(content=self.turn.mention, embed=embed, view=am_view)
        else:
            await self.atk_msg.edit(content=self.turn.mention + " has won!! :tada:", view=None) 
            
            await a_fight_db(self.act_msg.id, "e", "Game Over", True)
            await a_fight_db(self.act_msg.id, "e", "Winner", self.turn) 
            await a_fight_db(self.act_msg.id, "e", "Stats", [self.i_h, self.i_e, self.e_h, self.e_e])
                
class AM_stg2(discord.ui.View):
    def __init__(self, i, e, turn, atk_msg, act_msg, attack, style, masteries_unlocked, color):
        self.i = i
        self.i_h = i[1]
        self.i_e = i[2]
        self.i_l = i[3]
        
        self.e = e
        self.e_h = e[1]
        self.e_e = e[2]
        self.e_l = e[3]
        
        self.turn = turn
        self.atk_msg = atk_msg
        self.act_msg = act_msg
        self.attack = attack
        self.style = style
        self.masteries_unlocked = masteries_unlocked
        self.color = color
        
        super().__init__(timeout=10)

        for i in range(1, len(masteries[self.attack][self.style].keys()) + 1):
            self.add_item(Fight_Button(i, discord.ButtonStyle.grey, False if i <= self.masteries_unlocked else True, 1, self.color, self.i, self.e, self.atk_msg, self.act_msg, self.turn, attack="Melee"))
        
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
    
    async def on_timeout(self):
        i_exp = await a_exp_db(self.i[0], "v", "Experience")
        i_mexp = levels[self.i_l]
        i_mh = 100 + (5 * await a_stats_db(self.i[0], "v", "Health"))
        i_me = 100 + (5 * await a_stats_db(self.i[0], "v", "Energy"))
        
        e_exp = await a_exp_db(self.e[0], "v", "Experience")
        e_mexp = levels[self.e_l]
        e_mh = 100 + (5 * await a_stats_db(self.e[0], "v", "Health"))
        e_me = 100 + (5 * await a_stats_db(self.e[0], "v", "Energy"))
        
        go = await a_fight_db(self.act_msg.id, "v", "Game Over")
            
        embed = discord.Embed(
            title=f"{self.i[0].name} vs {self.e[0].name}",
            color=self.color
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')

        if go:
            winner = await a_fight_db(self.act_msg.id, "v", "Winner")
            stats = await a_fight_db(self.act_msg.id, "v", "Stats")
            
            btoemoji = await barcode_maker(i_exp, i_mexp, e_exp, e_mexp, stats[0], i_mh, stats[1], i_me, stats[2], e_mh, stats[3], e_me)
            
            embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\n" + ''.join(btoemoji[0:5]) + f"\nHealth — {stats[0]}/{i_mh}\n" + ''.join(btoemoji[5:10]) + f"\nEnergy — {stats[1]}/{i_me}\n" + ''.join(btoemoji[10:15]))
            embed.add_field(name=self.e[0] , value=f"Level — {self.e_l}\n" + ''.join(btoemoji[15:20]) + f"\nHealth — {stats[2]}/{e_mh}\n" + ''.join(btoemoji[20:25]) + f"\nEnergy — {stats[3]}/{e_me}\n" + ''.join(btoemoji[25:30]), inline=True)
            embed.add_field(name="Recent Action",value=f"{winner.mention} has won with **{stats[0] if stats[0] != 0 else stats[2]} health** remaining! :tada:", inline=False)
            await self.atk_msg.edit(content=f"{winner.mention} has won!! :tada:", embed=embed, view=None)
        else:
            btoemoji = await barcode_maker(i_exp, i_mexp, e_exp, e_mexp, self.i_h, i_mh, self.i_e, i_me, self.e_h, e_mh, self.e_e, e_me)
            
            embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\n" + ''.join(btoemoji[0:5]) + f"\nHealth — {self.i_h}/{i_mh}\n" + ''.join(btoemoji[5:10]) + f"\nEnergy — {self.i_e}/{i_me}\n" + ''.join(btoemoji[10:15]))
            embed.add_field(name=self.e[0] , value=f"Level — {self.e_l}\n" + ''.join(btoemoji[15:20]) + f"\nHealth — {self.e_h}/{e_mh}\n" + ''.join(btoemoji[20:25]) + f"\nEnergy — {self.e_e}/{e_me}\n" + ''.join(btoemoji[25:30]), inline=True)
            embed.add_field(name="Recent Action",value=f"Fight has ended with {self.turn.mention} losing on time", inline=False)
            await self.atk_msg.edit(content=f"{self.i[0].mention if self.turn == self.e[0] else self.e[0].mention} has won!! :tada:", embed=embed, view=None)
        
        try:
            await self.act_msg.delete()
        except discord.errors.NotFound:
            pass
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
        await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
        print(error)
        self.stop()
    
class Attack_Selection(discord.ui.Select['Fight']):
    def __init__(self, options, i, e, turn, atk_msg, act_msg, color):
        self.i = i
        self.e = e
        
        self.turn = turn
        self.atk_msg = atk_msg
        self.act_msg = act_msg
        self.color = color
        
        super().__init__(placeholder="Choose an Attack", options=options)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Fight = self.view
        
        style = await a_atks_db(self.turn, "v", self.values[0], "Style")
        masteries_unlocked = await a_atks_db(self.turn, "v", self.values[0], "Masteries Unlocked")
        
        embed = discord.Embed(
            title=f"{self.values[0]}: {style}",
            description=f"""**__Mastery__**\n```md\n1. {masteries[self.values[0]][style][1][0]}\n{f"2. {masteries[self.values[0]][style][2][0] if masteries_unlocked > 1 else '— LOCKED —'}" if len(masteries[self.values[0]][style].keys()) >= 2 else ''}\n{f"3. {masteries[self.values[0]][style][3][0] if masteries_unlocked > 2 else ''}" if len(masteries[self.values[0]][style].keys()) >= 3 else ''}\n{f"4. {masteries[self.values[0]][style][4][0] if mm > 3 else '— LOCKED —'}" if len(masteries[self.values[0]][style].keys()) >= 4 else ''}```""",
            color=discord.Color.from_rgb(47, 49, 54)
        )
        
        view = AM_stg2(self.i, self.e, self.turn, self.atk_msg, self.act_msg, self.values[0].title(), style, masteries_unlocked, self.color)
        await interaction.response.edit_message(embed=embed, view=view)
class AM_stg1(discord.ui.View):
    def __init__(self, i, e, turn, atk_msg, act_msg, color):
        self.i = i
        self.i_h = i[1]
        self.i_e = i[2]
        self.i_l = i[3]
        
        self.e = e
        self.e_h = e[1]
        self.e_e = e[2]
        self.e_l = e[3]
        
        self.turn = turn
        self.atk_msg = atk_msg
        self.act_msg = act_msg
        self.color = color
        
        super().__init__(timeout=10)
        
        self.add_item(Attack_Selection(
            [
                discord.SelectOption(label='Melee', description='Punching Style', emoji='👊')
            ],
            self.i,
            self.e,
            self.turn,
            self.atk_msg,
            self.act_msg,
            self.color
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and (interaction.user.id == self.i[0].id or interaction.user.id == self.e[0].id):
            return True
        else:
            await interaction.response.send_message('This fight is not yours', ephemeral=True)
            return False
    
    async def on_timeout(self):
        i_exp = await a_exp_db(self.i[0], "v", "Experience")
        i_mexp = levels[self.i_l]
        i_mh = 100 + (5 * await a_stats_db(self.i[0], "v", "Health"))
        i_me = 100 + (5 * await a_stats_db(self.i[0], "v", "Energy"))
        
        e_exp = await a_exp_db(self.e[0], "v", "Experience")
        e_mexp = levels[self.e_l]
        e_mh = 100 + (5 * await a_stats_db(self.e[0], "v", "Health"))
        e_me = 100 + (5 * await a_stats_db(self.e[0], "v", "Energy"))
        
        go = await a_fight_db(self.act_msg.id, "v", "Game Over")
            
        embed = discord.Embed(
            title=f"{self.i[0].name} vs {self.e[0].name}",
            color=self.color
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')

        if go:
            winner = await a_fight_db(self.act_msg.id, "v", "Winner")
            stats = await a_fight_db(self.act_msg.id, "v", "Stats")
            
            btoemoji = await barcode_maker(i_exp, i_mexp, e_exp, e_mexp, stats[0], i_mh, stats[1], i_me, stats[2], e_mh, stats[3], e_me)
            
            embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\n" + ''.join(btoemoji[0:5]) + f"\nHealth — {stats[0]}/{i_mh}\n" + ''.join(btoemoji[5:10]) + f"\nEnergy — {stats[1]}/{i_me}\n" + ''.join(btoemoji[10:15]))
            embed.add_field(name=self.e[0] , value=f"Level — {self.e_l}\n" + ''.join(btoemoji[15:20]) + f"\nHealth — {stats[2]}/{e_mh}\n" + ''.join(btoemoji[20:25]) + f"\nEnergy — {stats[3]}/{e_me}\n" + ''.join(btoemoji[25:30]), inline=True)
            embed.add_field(name="Recent Action",value=f"{winner.mention} has won with **{stats[0] if stats[0] != 0 else stats[2]} health** remaining! :tada:", inline=False)
            await self.atk_msg.edit(content=f"{winner.mention} has won!! :tada:", embed=embed, view=None)
        else:
            btoemoji = await barcode_maker(i_exp, i_mexp, e_exp, e_mexp, self.i_h, i_mh, self.i_e, i_me, self.e_h, e_mh, self.e_e, e_me)
            
            embed.add_field(name=self.i[0] ,value=f"Level — {self.i_l}\n" + ''.join(btoemoji[0:5]) + f"\nHealth — {self.i_h}/{i_mh}\n" + ''.join(btoemoji[5:10]) + f"\nEnergy — {self.i_e}/{i_me}\n" + ''.join(btoemoji[10:15]))
            embed.add_field(name=self.e[0] , value=f"Level — {self.e_l}\n" + ''.join(btoemoji[15:20]) + f"\nHealth — {self.e_h}/{e_mh}\n" + ''.join(btoemoji[20:25]) + f"\nEnergy — {self.e_e}/{e_me}\n" + ''.join(btoemoji[25:30]), inline=True)
            embed.add_field(name="Recent Action",value=f"Fight has ended with {self.turn.mention} losing on time", inline=False)
            await self.atk_msg.edit(content=f"{self.i[0].mention if self.turn == self.e[0] else self.e[0].mention} has won!! :tada:", embed=embed, view=None)
        
        try:
            await self.act_msg.delete()
        except discord.errors.NotFound:
            pass
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
        await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
        print(error)
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
        await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
        print(error)
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error, item: discord.ui.Item) -> None:
        await interaction.response.send_message(content="An error occured. Please retry the command", ephemeral=True)
        print(error)
        self.stop()

@commands.command()
async def fight(ctx, enemy: discord.Member):
    color = discord.Color.random()

    i_l = await a_exp_db(ctx.author, "v", "Level")
    i_exp = await a_exp_db(ctx.author, "v", "Experience")
    i_mexp = levels[i_l]
    i_h = 100 + (5 * await a_stats_db(ctx.author, "v", "Health"))
    i_e = 100 + (5 * await a_stats_db(ctx.author, "v", "Energy"))
    i_mstyle = await a_atks_db(ctx.author, "v", "Melee", "Style")
    
    e_l = await a_exp_db(enemy, "v", "Level")
    e_exp = await a_exp_db(enemy, "v", "Experience")
    e_mexp = levels[e_l]
    e_h = 100 + (5 * await a_stats_db(enemy, "v", "Health"))
    e_e = 100 + (5 * await a_stats_db(enemy, "v", "Energy"))
    e_mstyle = await a_atks_db(enemy, "v", "Melee", "Style")

    turn = random.choice([ctx.author, enemy])
    game_over = False
    
    btoemoji = await barcode_maker(i_exp, i_mexp, e_exp, e_mexp, i_h, i_h, i_e, i_e, e_h, e_h, e_e, e_e)

    embed = discord.Embed(
        title=f"{ctx.author.name} vs {enemy.name}",
        color=color
    )
    embed.add_field(name=ctx.author, value=f"Level — {i_l}\n" + ''.join(btoemoji[0:5]) + f"\nHealth — {i_h}/{i_h}\n" + ''.join(btoemoji[5:10]) + f"\nEnergy — {i_e}/{i_e}\n" + ''.join(btoemoji[10:15]))
    embed.add_field(name=enemy, value=f"Level — {e_l}\n" + ''.join(btoemoji[15:20]) + f"\nHealth — {e_h}/{e_h}\n" + ''.join(btoemoji[20:25]) + f"\nEnergy — {e_e}/{e_e}\n" + ''.join(btoemoji[25:30]), inline=True)
    embed.add_field(name="Recent Action",value=f"Fight has started. It is {turn.mention}'s turn, you have 120 seconds.", inline=False)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1052801038597496916/1061039440975372330/crossed-swords_2694-fe0f.png')
    
    embed2 = discord.Embed(
        title="It's your turn!",
        description="Choose an attack below",
        color=discord.Color.from_rgb(47, 49, 54)
    )
    
    atk_msg = await ctx.send(embed=embed)
    act_msg = await ctx.send(embed=embed2)
    view = AM_stg1([ctx.author, i_h, i_e, i_l], [enemy, e_h, e_e, e_l], turn, atk_msg, act_msg, color)
    await act_msg.edit(content=turn.mention, view=view)

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