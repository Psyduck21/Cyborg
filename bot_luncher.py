import discord
from discord.ext import commands
import asyncpg
import dhooks
from dhooks import Webhook, Embed

db_path = "./data/db/bot_database.sqlite"
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
bot.remove_command("help")

token = open("./secrets/Token.txt", "r").read()
pg = open("./secrets/pg_pwd.txt", "r").read()
host = open("./secrets/host.txt", "r").read()

status = ['.ping', '.assist', '.clear', '.play']

bot.colors = {
    "WHITE": 0x26fcff,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "who_even_likes_red_bruh!": 0xa5ddff,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "Light_blue": 0x30ffcc,
    "ok": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "cool_color": 0x6891ff,
    "something": 0xfc7bb2,
    "DARK_NAVY": 0xe8c02a,
    "Hm": 0xebf54c,
    "nice_color": 0xfc00f1,
    "nice_color2": 0x21f5fc,
    "very_nice_color": 0x25c059,
    "my_fav": 0xb863f2
}
bot.color_list = [c for c in bot.colors.values()]


async def create_db_pool():
    bot.db = await asyncpg.create_pool(host=host, database="postgres", user="postgres", password=pg)


# status
@bot.event
async def on_ready():
    print("bot is online.")
    return await bot.change_presence(activity=discord.Activity(type=1, name='$help', url='https://www.spotify.com/us/home/'))


# ping

"""if bot.status == "offline":
        print("Print bot is offline.")
        hook = Webhook(
            "https://discord.com/api/webhooks/796664358411304990/QQRNDvywODTRykTPFXHByqYI6Z7a_gg1puj0T39jO8wHWxsJIzNMHqXTtyS7OkEpy5QE")
        embed = Embed(description='Cyborg is offline',
                        color=0x5cdbf0,
                        timestamp='now')
        hook.send(embed=embed)
"""
@bot.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f' Latency: {round(bot.latency * 1000)}ms')
    await ctx.send(f'{bot.user.mention}')


"""@bot.command()
async def dm(ctx):
    r = await bot.db.fetch("SELECT channel_id FROM lvlchannel WHERE guild_id = $1", message.guild.id)
    channel = bot.get_channel(id=r[0])
    print(channel)
@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("you missing something. Check your command again.")"""


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            description=f"{ctx.author.mention} Something is missing in command please check",
            colour=ctx.author.colour)
        await ctx.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            description=f"{ctx.author.mention} Invalid Command . Please use **$help** command for valid commands",
            colour=ctx.author.colour)
        await ctx.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You are missing required permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)
    """else:
        raise error"""


extensions = [
    "lib.cogs.funcounting"
]
if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension(extension)

bot.loop.create_task(create_db_pool())
bot.run(token)
