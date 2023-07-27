import os
from dotenv import load_dotenv
from connectRankDB import connectDB
from discord.ext import commands
from discord import app_commands
import asyncio
import discord

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix="/",
                    intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Bot is online")
    try:
        synched = await bot.tree.sync()
        print(f'Synched {len(synched)} command(s)')
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('/help'))
    except Exception as e:
        print(e)

@bot.tree.command(name = 'ping', description = 'Get the DASA Bot response time')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')


@bot.tree.command(name = 'help', description='Help for DASA Bot')
async def help(interaction: discord.Interaction):
    em = discord.Embed(title="DASA Bot Commands",
                        description="Display DASA cutoffs and more onto discord chat with these commands! \n", color=discord.Color.random())
    em.add_field(name='</cutoff:1131246029531004968>  `<college> <year> <ciwg> <round> [branch]`',
                    value='Displays the ranks of a specified college and branch based on the user-provided year and round',
                    inline=False)
    em.add_field(name='</analyse:1131969029968502918>  `<rank>, <ciwg>, [branch]`',
                    value='Displays a list of colleges and branches whose closing ranks closely match the user-provided rank.',
                    inline=False)
    em.add_field(name='</airport:1133054254203011082>  `<college]>`',
                    value='Displays data about the nearest airport to the college specified by the user.',
                    inline=False)
    em.set_footer(text="This message will be deleted after 1 minute.")
    await interaction.response.send_message(embed=em, delete_after=60)

@bot.command(description='Reload a cog.')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'`{extension}` `has been reloaded.`')
    except:
        await ctx.send("`Invalid module.`")

@bot.command(hidden=True)
@commands.is_owner()
async def status(ctx, stats:str):
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(stats))
    await ctx.send(f'Status has been changed to `{status}.`')

@bot.command(description='Turns off the bot.')
@commands.is_owner()
async def shut(ctx):
    await ctx.send('`Bot going offline!`👋')
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()
    exit()

async def load():
    for file in os.listdir("DASABot\cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await bot.start(BOT_TOKEN)

asyncio.run(main())
