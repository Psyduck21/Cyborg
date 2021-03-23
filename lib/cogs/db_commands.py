import discord
from discord.ext import commands

db_path = "./data/db/bot_database.sqlite"


class Ak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="levelingallowed")
    async def lvl(self, ctx):
        if ctx.guild.id == 740418138075693107:
            result = await self.bot.db.fetch(f"SELECT lvl, lvl_server_name FROM allowed")
            name = [i[1] for i in result]
            if not result:
                return await ctx.send("No data found.")
            embed = discord.Embed(title="Leveling allowed")
            embed.add_field(name="\u200B", value=f"name : {name}\n", inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="welcomeallowed")
    async def welcome(self, ctx):
        if ctx.guild.id == 740418138075693107:
            result = await self.bot.db.fetch("SELECT welcome, welcome_server_name FROM wallowed")
            name = [i[1] for i in result]
            if not result:
                return await ctx.send("No data found.")

            embed = discord.Embed(title="Welcome message allowed")
            embed.add_field(name="\u200B", value=f"name : {name}\n")
            await ctx.send(embed=embed)

    @commands.command(name="leaveallowed")
    async def leave(self, ctx):
        if ctx.guild.id == 740418138075693107:
            result = await self.bot.db.fetch(f"SELECT leave, leave_server_name FROM lallowed")
            name = [i[1] for i in result]
            if not result:
                return await ctx.send("No data found.")

            embed = discord.Embed(title="Leave message allowed")
            embed.add_field(name="\u200B", value=f"name : {name}\n")
            await ctx.send(embed=embed)

    @commands.command()
    async def profanity(self, ctx):
        if ctx.guild.id == 740418138075693107:
            result = await self.bot.db.fetch(f"SELECT guild_id, server_name FROM profanity_allowed")
            name = [i[1] for i in result]
            if not result:
                return await ctx.send("No data found.")

            embed = discord.Embed(title="Profanity allowed")
            embed.add_field(name="\u200B", value=f"name : {name}\n")
            await ctx.send(embed=embed)

    @commands.command()
    async def automode(self, ctx):
        if ctx.guild.id == 740418138075693107:
            result = await self.bot.db.fetch(f"SELECT guild_id, server_name FROM automoderation")
            name = [i[1] for i in result]
            if not result:
                return await ctx.send("No data found.")

            embed = discord.Embed(title="Auto moderation allowed")
            embed.add_field(name="\u200B", value=f"name : {name}\n")
            await ctx.send(embed=embed)

    @commands.command()
    async def linksallowed(self, ctx):
        if ctx.guild.id == 740418138075693107:
            result = await self.bot.db.fetch(f"SELECT guild_id, server_name, channel_id, channel_name FROM links_allowed")
            name = [i[1] for i in result]
            channel = [i[3]for i in result]
            print(channel)
            if not result:
                return await ctx.send("No data found.")

            embed = discord.Embed(title="Links moderation allowed")
            embed.add_field(name="\u200B", value=f"server name : {name}\nchannel name : {channel}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Ak(bot))
    print("Db_command cog is loaded~")
