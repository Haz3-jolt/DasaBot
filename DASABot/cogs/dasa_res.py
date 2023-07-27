import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

class DASAResults(commands.Cog):
    DASA_GUILD_ID = int(os.getenv("DASA_GUILD_ID"))
    DASA_RES_CHANNEL_ID = int(os.getenv("DASA_RES_CHANNEL_ID"))

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

        self.DASA_GUILD_ID = int(os.getenv("DASA_GUILD_ID"))
        self.DASA_RES_CHANNEL_ID = int(os.getenv("DASA_RES_CHANNEL_ID"))


    @commands.Cog.listener()
    async def on_ready(self):
        print("resupd cog loaded")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resupd(self, ctx, year = None):
        if ctx.guild.id != self.DASA_GUILD_ID:
            await ctx.send("Command cannot be used in this guild.")
            return

        if year == None:
            await ctx.send("Specify the year.")
            return

        dasa_res_channel = self.bot.get_channel(self.DASA_RES_CHANNEL_ID)

        year_role_id = {
            "DASA 2021" : 812198929671389184,
            "DASA 2022" : 868067556609642546,
            "DASA 2023" : 898816198614077450,
            "DASA 2024" : 1027220947792572457,
            "DASA 2025" : 1100645171676332094
        }

        year_messsage_id = {
            "2023" : 1130897268766167160,
        }

        role_ids = {
            'NIT Trichy'            : 917466756933644328,
            'NITK Surathkal'        : 917466764646973471,
            'NIT Warangal'          : 917466768392458251,
            'NIT Rourkela'          : 917467466060402758,
            'NIT Calicut'           : 917467011142004746,
            'NIT Durgapur'          : 1030829299491676212,
            'NIT Jamshedpur'        : 1030828050021109840,
            'NIT Kurukshetra'       : 1030731847484833856,
            'NIT Jalandhar'         : 1131213217776021545,
            'MNNIT Allahabad'       : 917466771001323540,
            'MNIT Jaipur'           : 1030828019482382446,
            'MANIT Bhopal'          : 917466771680804865,
            'VNIT Nagpur'           : 1030828146242621532,
            'SVNIT Surat'           : 1030827808060080179,
            'IIEST Shibpur'         : 1030731216460185682,
            'IIIT Allahabad'        : 966386557135253595,
            'IIIT Gwalior'          : 917467473710841918,
            'IIIT Sonepat'          : 917467473371078766,
            'IIIT Jabalpur'         : 1030833185258475632,
            'IIIT Kottayam'         : 917467472205062225,
            'IIIT Hyderabad'        : 917467010126983209,
            'IIIT Delhi'            : 917467007761403976,
            'BITS'                  : 917467010307346502,
            'NSUT'                  : 917466772892950568,
            'DTU'                   : 917466773236875355,
            'MIT Manipal'           : 932870289577111642,
            'Anna University'       : 1131213158783139891,
            'Jadavpur University'   : 1126177447939932350,

            #'IIT'            : (1030905894629810208, 985959694147416085, 996690379346812959)
        }

        present = False
        for year_name in year_role_id.keys():
            if year in year_name: present = True


        if present == False:
            yrs = list(year_role_id.keys())
            await ctx.send(f"Invalid year, must be between 2023 and {yrs[-1][5:]}.")
            return


        year_mems = ctx.guild.get_role(year_role_id[f"DASA {year}"]).members

        output = ""

        for role in role_ids.keys():
            role_id = role_ids[role]
            mems = ctx.guild.get_role(role_id).members

            cur = ""
            for member in mems:
                if member in year_mems:
                    cur += member.mention + "\n"

            if len(cur) > 0:
                output += "**" + role + "**" + "\n"
                output += cur
                output += "\n"


        if year in year_messsage_id.keys():
            message = await dasa_res_channel.fetch_message(year_messsage_id[year])
            await message.edit(content = output)

        else:
            message = await dasa_res_channel.send(".")
            await message.edit(content = output)


        await ctx.send("updated")

    #Legacy bot announcement
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def online(self, ctx, year = None):
        if ctx.guild.id != 1123237875941654659:
            await ctx.send("Command cannot be used in this guild.")
            return

        dasa_res_channel = self.bot.get_channel(1133509381116399616)

        output = self.bot.get_message(1133487304250495086)

        await dasa_res_channel.send(output)

        await ctx.send("updated")


async def setup(bot):
    await bot.add_cog(DASAResults(bot))