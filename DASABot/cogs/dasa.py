import connectRankDB
from connectRankDB import connectDB
import discord
from discord.ext import commands
from discord.ui import *
from discord.ext.commands import BucketType
import Paginator
import asyncio

db = connectDB()

delete = Button(label="Delete", style=discord.ButtonStyle.danger)
dms = Button(label="Send in DMs", style=discord.ButtonStyle.green)
view = View()
view.add_item(dms)
view.add_item(delete)


class DASACommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbconnect = connectRankDB.connectDB()

    @commands.Cog.listener()
    async def on_ready(self):
        print("DASA COMMANDS cog loaded")

    @commands.hybrid_command()
    @commands.cooldown(1, 10, type=BucketType.user)
    async def cutoff(self, ctx: discord.Interaction,
                        college: str = commands.parameter(
                            description="example: nitc, nitt, nitk, nits, nsut, (use quotes for split names)"),
                        year: str = commands.parameter(description="example: 2021, 2022"), ciwg: str = commands.parameter(description="example: y, n, Y, N"),
                        round: str = commands.parameter(
                            description="example: 1, 2, 3"),
                        branch: str = commands.parameter(default=None,
                                                        description="example: CSE, ECE, EEE, MEC")):
        """Displays the ranks of a specified college and branch based on the user-provided year and round"""

        embed = None

        college = college.lower()
        # checks if the year is given as 2021 or 2022
        if year not in ['2021', '2022', '2023']:
            return await ctx.send("Invalid year.")

        if int(round) not in [1, 2, 3]:  # checks if the round is 1,2 or 3
            await ctx.send("Invalid round.")
            return

        if ciwg.lower() not in ['y', 'n', 'yes', 'no', 'true', 'false', 'ciwg', 'dasa']:
            await ctx.send("Invalid Category. Please enter y/n for ciwgc status")

        try:
            college = db.nick_to_college(str(year), str(round), str(college))
        except:
            return await ctx.send("Invalid Round.")

        ciwg = True if ciwg in ['y', 'yes', 'true', 'ciwg'] else False
        branch_list = db.request_branch_list(year, round, college,  ciwg)
        if branch is not None:
            if ciwg:
                branch = f"{branch.upper()}1"
            while branch.upper() not in branch_list:
                await ctx.send("Invalid branch name, re-enter. Press Q to Quit.")
                branch_msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author)
                branch = branch_msg.content
                if branch == 'Q':
                    return await ctx.send('Quitting...')

            stats = db.get_statistics(
                year, round, college, branch.upper(), ciwg)
            embed = discord.Embed(
                title=f'Cutoffs for {college}',
                description=f'Course: {stats[0]} (CIWG)\nBranch Code: {branch.upper()}\nRound {round}({year})' if ciwg else f'Course: {stats[0]}\nBranch Code: {branch.upper()}\nRound {round}({year})',
                            color=discord.Color.random())
            embed.set_thumbnail(
                url='https://dasanit.org/dasa2023/images/dasa_new.png')
            embed.add_field(name="JEE Opening Rank: ", value=stats[1])
            embed.add_field(name="JEE Closing Rank: ", value=stats[2])
            embed.add_field(
                name="DASA Opening Rank: " if not ciwg else f"CIWG Opening Rank: ", value=stats[3])
            embed.add_field(
                name="DASA Closing Rank: " if not ciwg else f"CIWG Closing Rank: ", value=stats[4])
            embed.set_footer(
                text='This message will be automatically deleted in 120s.\nTo receive this message in your DMs, press "Send in DMs".\nTo delete this message, press "Delete".')
            m = await ctx.send(embed=embed, delete_after=120, view=view)

            async def dms_callback(interaction):
                await self.bot.send_message(ctx.message.author, embed=embed)
                await interaction.response.send_message("Cutoffs have been sent in your DMs.")

        else:
            stats = db.get_statistics_for_all(year, round, college, ciwg)
            embed = discord.Embed(
                title=f"Cutoffs for {college}", description=f"Round {round} in ({year})\n## NOTE: To get the full form and cutoffs for a specific branchcode, please specify branch in </cutoff:1131246029531004968> command", color=discord.Color.random())
            embed.set_thumbnail(
                url='https://dasanit.org/dasa2023/images/dasa_new.png')
            for i in stats:
                if ciwg == False:
                    embed.add_field(
                        name=i[0],
                        value=f"JEE OPENING: {i[1][0]}\nJEE CLOSING: {i[1][1]}\nDASA OPENING: {i[1][2]}\nDASA CLOSING: {i[1][3]}",
                        inline=True)
                else:
                    if i[0][-1] != '1':
                        continue
                    else:
                        embed.add_field(
                            name=f"{i[0][:-1]} (CIWG)",
                            value=f"JEE OPENING: {i[1][0]}\nJEE CLOSING: {i[1][1]}\nCIWG OPENING: {i[1][2]}\nCIWG CLOSING: {i[1][3]}",
                            inline=True)
            embed.set_footer(
                text='This message will be automatically deleted in 120s.\nTo receive this message in your DMs, press "Send in DMs".\nTo delete this message, press "Delete".')

            m = await ctx.send(embed=embed, delete_after=120, view=view)

        async def dms_callback(interaction):
            dmuser = await self.bot.fetch_user(interaction.user.id)
            embed.remove_footer()
            await dmuser.send(embed=embed)
            await ctx.send(f"Cutoffs have been sent in your DMs.{interaction.user.mention}")

        async def delete_callback(interaction):
            if interaction.user.id == ctx.author.id:
                await m.delete()

        delete.callback = delete_callback
        dms.callback = dms_callback

    @cutoff.error
    async def cutoff_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Command on Cooldown!",
                                description=f"Try again in {error.retry_after:.1f}s.", color=discord.Color.random())
            em.set_thumbnail(
                url="https://dasanit.org/dasa2023/images/dasa_new.png'")
            await ctx.send(embed=em)

    @commands.hybrid_command()
    @commands.cooldown(1, 10, type=BucketType.user)
    async def airport(self, ctx:discord.Interaction,
                      college_name: str = commands.parameter(description="example: nitc, nitt, nitk, nits, nsut, (use quotes for split names)")):
        """Displays data about the airport closest to the college specified by the user.
        """

        embed = None

        college_name = college_name.lower()
        try:
            stats = db.get_airport_stats(college_name)
        except:
            return await ctx.send("Invalid college name.")

        embed = discord.Embed(
            title=f'Airport closest to {stats[0]}', color=discord.Color.random())
        embed.set_thumbnail(
            url='https://dasanit.org/dasa2023/images/dasa_new.png')
        embed.add_field(name="College name: ", value=stats[0])
        embed.add_field(name="State: ", value=stats[1])
        embed.add_field(
            name="Closest Airport: ", value=stats[2])
        embed.add_field(
            name="Airport Code: ", value='(' + stats[3] + ')')
        embed.add_field(
            name="Distance of airport from college: ", value=stats[4] + 'KM')
        embed.set_footer(
            text='This message will be automatically deleted in 120s.\nTo receive this message in your DMs, press "Send in DMs".\nTo delete this message, press "Delete".')
        m = await ctx.send(embed=embed, delete_after=120, view=view)

        async def dms_callback(interaction):
            dmuser = await self.bot.fetch_user(interaction.user.id)
            embed.remove_footer()
            await dmuser.send(embed=embed)
            await ctx.send(f"Airport details have been sent in your DMs.{interaction.user.mention}")


        async def delete_callback(interaction):
            if interaction.user.id == ctx.author.id:
                await m.delete()

        delete.callback = delete_callback
        dms.callback = dms_callback

    @airport.error
    async def airport_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Command on Cooldown!",
                               description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.random())
            em.set_thumbnail(
                url="https://dasanit.org/dasa2023/images/dasa_new.png'")
            await ctx.send(embed=em)

    @commands.hybrid_command()
    @commands.cooldown(1, 10, type=BucketType.user)
    async def analyse(self, ctx:discord.Interaction, rank: str, ciwg: str, branch: str = None):
        """Displays a list of colleges and branches whose closing ranks closely match the user-provided rank."""
        embed = None
        m = None
        if ciwg.lower() not in ['y', 'n', 'yes', 'no', 'true', 'false', 'ciwg', 'dasa']:
            return await ctx.send('Invalid Category.')
        ciwg = True if ciwg.lower() in ['y', 'yes', 'true', 'ciwg'] else False
        if branch is not None:
            cutoffs, colleges = db.reverse_engine(rank, ciwg, branch)
            embed = discord.Embed(
                title="Chances based off of your JEE(Main) CRL-Rank",
                color=discord.Color.random(),
                description=f"Closing ranks for {branch.upper()}{'' if not ciwg else '(CIWG)'}")
            embed.set_thumbnail(
                url='https://dasanit.org/dasa2023/images/dasa_new.png')
            for i in range(10):
                embed.add_field(
                    name=f"{i+1}. {colleges[i]}", value=f"JEE CLOSING RANK: {cutoffs[i]}", inline=True)
                embed.set_footer(
                    text='This message will be automatically deleted in 120s.\nTo receive this message in your DMs, press "Send in DMs".\nTo delete this message, press "Delete".')
            m = await ctx.send(embed=embed, delete_after=120, view=view)
        else:
            # print(1)
            cutoffs, colleges, branches = db.reverse_engine(rank, ciwg, branch)
            # print(2)
            dic = {}  # {college : [[branch, cutoff], [branch, cutoff]}
            for i in range(len(colleges)):
                if colleges[i] not in list(dic.keys()):
                    dic[colleges[i]] = [[branches[i], cutoffs[i]]]
                else:
                    dic[colleges[i]] += [[branches[i], cutoffs[i]]]
            pages = []
            for i in dic:
                embed = discord.Embed(title=f"Closing Ranks for {i} in all branches {'(UNDER CIWG CATEGORY)' if ciwg else ''}",color=discord.Color.random())
                embed.set_thumbnail(
                    url='https://dasanit.org/dasa2023/images/dasa_new.png')
                for j in dic[i]:
                    embed.add_field(
                        name=f"{j[0][:-1]}" if ciwg else f"{j[0]}", value=f"JEE CLOSING RANK: {j[1]}", inline=True)
                    embed.set_footer(
                        text='This message will be automatically deleted in 5 minutes.\n')
                pages.append(embed)
            m = await Paginator.Simple(timeout=300).start(ctx, pages=pages)
            await asyncio.sleep(300)
            await m.delete()

        async def dms_callback(interaction):
            dmuser = await self.bot.fetch_user(interaction.user.id)
            embed.remove_footer()
            await dmuser.send(embed=embed)
            await ctx.send(f"Cutoffs have been sent in your DMs. {interaction.user.mention}")

        async def delete_callback(interaction):
            if interaction.user.id == ctx.author.id:
                await m.delete()

        delete.callback = delete_callback
        dms.callback = dms_callback
        await asyncio.sleep(5)
        await ctx.message.delete()

    @analyse.error
    async def analyse_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Command on Cooldown!",
                            description=f"Try again in {error.retry_after:.1f}s.", color=discord.Color.random())
            em.set_thumbnail(
                url="https://dasanit.org/dasa2023/images/dasa_new.png'")
            await ctx.send(embed=em)

    # @commands.command()
    # @commands.is_owner()
    # async def welcome(self, ctx):
    #     await ctx.send("Hey @everyone! So I am finally live. It's no well kept secret that I have been in development for the past month as I'm sure you would have seen my creators testing my beta versions or showcasing them for use but I am proud to announce that today is the day DASABot 1.0 is finally active! My creators have given me the following functionalities to help all of you with your future college endeavours.\n- </cutoff:1131246029531004968> which enables me to take in your college, year, round and branch to tell you the cutoff of what you asked! I even have a CIWG filter!\n- </analyse:1131969029968502918> lets me take in your JEE CRL to tell you what colleges have closing ranks close to yours so you can get a brief idea of what you can and can not get! ***This command does not signify guaranteed seats at any mentioned college. This is solely as algorithm based on CRL and Closing ranks and can not predict the ranks of forthcoming years.***\n- </airport:1133054254203011082> lets me tell you about the airports nearby the college you ask.\nAll in all, I'm glad I can finally be of service to every one of you and I look forward to helping everyone out on this server! I was made by <@536919776522534973> <@275609153274380289> <@540964533884289044> and <@506887352380162048>. Please report any bugs you encounter to them.")
    #     await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def gandu(self, ctx):
        await ctx.send("gandu.")
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def sudeep(self, ctx):
        await ctx.send("What😡 ra⁉️Sudeep🧔🏾too much😮 cock🍆you're showing 🧐bro frankly🤭tell you🗣️Sudeep-you're showing too😅 much cock🍆bro you come to Malleshwaram area 🌴pop 👊🏾you with my gang👿I said you once 😐and I'm saiding 🗣️you once more time 💪ra Sudeep🧔🏾‍ I'll pop you 😋if you show too 🤏")
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def nsut(self, ctx):
        await ctx.send("NSUT is like that one ex who refuses to tell you anything and is super toxic to you but she's a 10/10")
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def spiderman(self, ctx):
        await ctx.send("https://media.tenor.com/GIbER2Fy3UUAAAAC/spiderman-sad-spiderman.gif")
        await ctx.message.delete()
    

async def setup(bot):
    await bot.add_cog(DASACommands(bot))
