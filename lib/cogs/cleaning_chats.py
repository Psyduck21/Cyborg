import discord
from discord.ext import commands
from better_profanity import profanity
from re import search

profanity.load_censor_words_from_file("./data/profanity.txt")


class Chat(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(" \
                         r"\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".," \
                         r"<>?«»“”‘’])) "

    @commands.command(name="autoprofanity")
    async def profanity_add(self, ctx):
        a = await ctx.send("Do you want to enable/disable profanity in your server?\nAnswer (on/off)")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["on",
                                                                                                       "cancel",
                                                                                                       "off"]

        msg = await self.bot.wait_for("message", check=check)

        if msg.content.lower() == "on":
            result = await self.bot.db.fetch("SELECT guild_id FROM profanity_allowed WHERE guild_id =$1", ctx.guild.id)
            if not result:
                await self.bot.db.execute("INSERT INTO profanity_allowed (guild_id, server_name) VALUES($1, $2)", ctx.guild.id, ctx.guild.name)
                return await ctx.send("Profanity is now enabled in your server.")
            await ctx.send("Profanity is already enabled in your sever.")

        elif msg.content.lower() == "off":
            result = await self.bot.db.fetch("SELECT guild_id FROM profanity_allowed WHERE guild_id =$1", ctx.guild.id)
            if result:
                await self.bot.db.execute("DELETE FROM profanity_allowed WHERE guild_id = $1", ctx.guild.id)
                return await ctx.send("Profanity is now disabled in your server.")
            await ctx.send("Profanity is already disabled in your server.")

        elif msg.content.lower() == "cancel":
            await a.delete()

    @commands.command(name="linksmod")
    async def links_allowed(self, ctx, channel: discord.TextChannel):
        embed = discord.Embed(title="Links System", description="In this system you can select particular channels in "
                                                                "your server in which links are allowed*\n*TO enable "
                                                                "this feature make your auto moderation is enabled in "
                                                                "your server.*\nEnable auto moderation feature by - "
                                                                "**$automod** command.\nFor further info use `$help "
                                                                "linksmod`", colour=ctx.author.color)
        a = await ctx.send(embed=embed)
        b = await ctx.send("Do you want to enable/disable links system in your server?\nAnswer (on/off)")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["on",
                                                                                                       "cancel",
                                                                                                       "off"]

        msg = await self.bot.wait_for("message", check=check)
        if msg.content.lower() == "on":
            result = await self.bot.db.fetch("SELECT channel_id FROM links_allowed WHERE guild_id =$1 and channel_id "
                                             "= $2", ctx.guild.id, channel.id)
            if not result:
                await self.bot.db.execute("INSERT INTO links_allowed (guild_id, channel_id, server_name, channel_name) VALUES($1, $2, $3, $4)",
                                          ctx.guild.id, channel.id, ctx.guild.name, channel.name)
                return await ctx.send(f"Links are allowed in {channel.mention}")

            await ctx.send("Links moderation is already enabled in your server.")

        elif msg.content.lower() == "off":
            result = await self.bot.db.fetch("SELECT channel_id FROM links_allowed WHERE guild_id =$1 and channel_id "
                                             "= $2",
                                             ctx.guild.id, channel.id)
            if result:
                await self.bot.db.execute("DELETE FROM links_allowed Where guild_id=$1 and channel_id = $2",
                                          ctx.guild.id, channel.id)
                return await ctx.send(f"Links are not allowed in {channel.mention}")
            await ctx.send("Links moderation is already disabled in your server.")

        elif msg.content.lower() == "cancel":
            await a.delete()
            await b.delete()

    @commands.command(name="addbadwords", aliases=["addcenserwords"])
    @commands.has_permissions(manage_guild=True)
    async def add_profanity(self, ctx, *words):
        with open("./data/profanity.txt", "a", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in words]))
        profanity.load_censor_words_from_file("./data/profanity.txt")
        await ctx.send("Task completed.")

    @commands.command(name="delbadwords", aliases=["removecenserwords", "delcenserwords"])
    @commands.has_permissions(manage_guild=True)
    async def remove_profanity(self, ctx, *words):
        with open("./data/profanity.txt", "r", encoding="utf-8") as f:
            stored = [w.strip() for w in f.readlines()]
        with open("./data/profanity.txt", "w", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in stored if w not in words]))
        profanity.load_censor_words_from_file("./data/profanity.txt")
        await ctx.send("Task completed.")

    @add_profanity.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} :x: You need ``Manage_Server`` permission to use this "
                            f"command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} Please add the word you want to add/remove in profanity",
                colour=ctx.author.colour)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        r = await self.bot.db.fetch("SELECT guild_id from automoderation")
        automod_allowed = [i[0] for i in r]
        result = await self.bot.db.fetch("SELECT channel_id FROM links_allowed where guild_id = $1", message.guild.id)
        link_notallowed = [i[0] for i in result]

        if message.guild.id in automod_allowed:

            if not message.author.bot:
                if profanity.contains_profanity(message.content):
                    result = await self.bot.db.fetch("SELECT guild_id FROM profanity_allowed")
                    profanity_allowed = [i[0] for i in result]
                    if message.guild.id in profanity_allowed:

                        await message.delete()
                        await message.channel.send(f"{message.author.mention}You cant use that word here.")

                elif message.channel.id not in link_notallowed and search(self.url_regex, message.content):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} You can't post links in this channel!")


def setup(bot):
    bot.add_cog(Chat(bot))
    print("clearing_chat cog is loaded!")
