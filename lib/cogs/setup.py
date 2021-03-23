import discord
from discord.ext import commands

db_path = "./data/db/bot_database.sqlite"


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_(self, ctx):
        embed = discord.Embed(colour=ctx.author.colour)
        embed.add_field(name="SETUP CYBORG", value="Please enter what do you want to setup.\n"
                                                   "1.**enable**: it will enable leveling system and welcome system as per your choice.use it as <enable> ignore `<>`.\n"
                                                   "2.**disable**: it will disable leveling system and welcome system as per your choice.use it as <disable> ignore `<>`\n"
                                                   "3.**mute**: set up mute system in your sever\n"
                                                   "4.**cancel**: to cancel the process.\n"
                                                   "*Rest of two commands are* \n"
                                                   "5.**$logchannel**: it will set up the log channel where bot will send message and \n"
                                                   "6.**$lvlchannel**: this will set up level channel were bot will send level message.\n"
                                                   "*(This command is recommended if you are setting up leveling system.)*",
                        inline=False
                        )
        sent = await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["enable",
                                                                                                       "cancel", "mute",
                                                                                                       "disable"]

        msg = await self.bot.wait_for("message", check=check)

        if msg.content.lower() == "enable":
            sent1 = await ctx.send(
                "what you want to enable `leveling`, `welcome`, `leave`.\n *If you want to exit the setup type `cancel`*")

            def check1(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["welcome",
                                                                                                           "cancel",
                                                                                                           "leveling",
                                                                                                           "leave"]

            msg1 = await self.bot.wait_for("message", check=check1)
            if msg1.content.lower() == "leveling":
                await self.bot.db.execute("INSERT INTO allowed (lvl, lvl_server_name) VALUES($1, $2)",
                                          ctx.guild.id, str(ctx.guild.name))
                await ctx.send("Task complete!")

                a = await ctx.send("Do you want to enable roles also (yes/no)")

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["yes",
                                                                                                               "no"]

                msg = await self.bot.wait_for("message", check=check)
                if msg.content.lower() == "yes":
                    guild = ctx.guild
                    await guild.create_role(name="level 5+")
                    await guild.create_role(name="level 10+")
                    await guild.create_role(name="level 20+")
                    await guild.create_role(name="level 30+")
                    await guild.create_role(name="level 40+")
                    await guild.create_role(name="level 50+")

                elif msg.content.lower() == "no":
                    await a.delete()

            elif msg1.content.lower() == "welcome":
                await self.bot.db.execute("INSERT INTO wallowed (welcome, welcome_server_name) VALUES($1,$2)",
                                          ctx.guild.id, str(ctx.guild.name))
                await ctx.send("processing")
                await ctx.send(
                    "To setup welcome using cyborg. You have to setup following \n1. Welcome channel by **$welcome wchannel**\n2. Welcome message by **$welcome message**\n*Use the command in the same way as they are in **BOLDS**.*")
            elif msg1.content.lower() == "leave":
                await self.bot.db.execute("INSERT INTO lallowed (leave, leave_server_name) VALUES($1,$2)", ctx.guild.id,
                                          str(ctx.guild.name))
                await ctx.send(
                    "To setup leave using cyborg. You have to setup following\n1. Leave channel by **$leave lchannel**\n*Use the command in the same way as they are in **BOLDS**.*")
            elif msg1.content.lower() == "cancel":
                await ctx.send("Cancelling.", delete_after=2)
                await sent1.delete()
        elif msg.content.lower() == "disable":
            sent2 = await ctx.send(
                "what you want to enable `leveling`, `welcome`, `leave`.\n *If you want to exit the setup type `cancel`*")

            def check2(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["welcome",
                                                                                                           "cancel",
                                                                                                           "leveling",
                                                                                                           "leave"]

            msg2 = await self.bot.wait_for("message", check=check2)
            if msg2.content.lower() == "leveling":
                b = await ctx.send("Do you wanna disable leveling ? Answer `(yes/no)`")

                def check2(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["yes",
                                                                                                               "no"]

                msg = await self.bot.wait_for("message", check=check2)

                if msg.content.lower() == "yes":
                    await self.bot.db.execute("DELETE FROM allowed WHERE lvl = $1", ctx.guild.id)
                    await ctx.send("Task completed!")
                elif msg.content.lower() == "no":
                    await ctx.send("Cancelling.", delete_after=2)
                    await b.delete()
            elif msg2.content.lower() == "welcome":
                await self.bot.db.execute("DELETE FROM wallowed WHERE welcome = $1", ctx.guild.id)
                await ctx.send("Task completed!")
            elif msg2.content.lower() == "leave":
                await self.bot.db.execute("DELETE FROM lallowed WHERE leave = $1", ctx.guild.id)
                await ctx.send("Task completed!")
            elif msg2.content.lower() == "cancel":
                await ctx.send("Cancelling.", delete_after=2)
                await sent2.delete()

        elif msg.content.lower() == "cancel":
            await ctx.send("Cancelling.", delete_after=2)
            await sent.delete()
        elif msg.content.lower() == "mute":
            guild = ctx.guild
            perms = discord.Permissions(send_messages=False, speak=False)
            await guild.create_role(name="Muted", permissions=perms)
            await ctx.send("Done!")

    @commands.command()
    async def verify(self, ctx, member: discord.Member = None):
        member = ctx.author or member
        sent = await ctx.send("Enter this code `34134`.")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["34134",
                                                                                                       "cancel"]

        msg = await self.bot.wait_for("message", check=check)

        if msg.content.lower() == "34134":
            guild = ctx.guild
            perms = discord.Permissions(manage_messages=False, manage_guild=False)
            await guild.create_role(name="Verified", permissions=perms)

            role = discord.utils.get(guild.roles, name="Verified")
            if role in guild.roles:
                await member.add_roles(role)
                await ctx.send("Verified!")

        elif msg.content.lower() == "cancel":
            await sent.delete()

    @setup_.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `Administrator` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def lvlchannel(self, ctx, channel: discord.TextChannel):
        result = await self.bot.db.fetch(f"SELECT channel_id FROM lvlchannel WHERE guild_id = {ctx.guild.id}")
        if result is not None:
            await self.bot.db.execute("INSERT INTO lvlchannel (guild_id, channel_id) VALUES($1,$2)", ctx.guild.id,
                                      channel.id)
            return await ctx.send(f"Level channel has been set to {channel.mention}")

        await self.bot.db.execute("UPDATE lvlchannel SET channel_id = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
        await ctx.send(f"Level channel has been updated to {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def logchannel(self, ctx, channel: discord.TextChannel):
        result = await self.bot.db.fetch(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if result is not None:
            await self.bot.db.execute("INSERT INTO logchannel (guild_id, channel_id) VALUES($1,$2)", ctx.guild.id,
                                      channel.id)
            return await ctx.send(f"Log channel has been set to {channel.mention}")

        await self.bot.db.fecthrow("UPDATE logchannel SET channel_id = $1 WHERE guild_id = $2", channel.id,
                                   ctx.guild.id)
        await ctx.send(f"Log channel has been updated to {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rlogchannel(self, ctx):
        result = await self.bot.db.fetch(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if result:
            await self.bot.db.execute("DELETE FROM logchannel WHERE guild_id =$1", ctx.guild.id)
            return await ctx.send("Log channel has been removed")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rlvlchannel(self, ctx):
        result = await self.bot.db.fetch(f"SELECT channel_id FROM lvlchannel WHERE guild_id = {ctx.guild.id}")
        if result:
            await self.bot.db.execute("DELETE FROM lvlchannel WHERE guild_id =$1", ctx.guild.id)
            return await ctx.send("lvl channel has been removed")

    @commands.command(name="automod")
    @commands.has_permissions(manage_guild=True)
    async def automod_(self, ctx):
        sent = await ctx.send("Do you want to (on/off) auto moderation.\nAnswer (on/off)")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["on",
                                                                                                       "off", "cancel"]

        msg = await self.bot.wait_for("message", check=check)

        if msg.content.lower() == "on":
            await self.bot.db.execute("INSERT INTO automoderation (guild_id, server_name) VALUES($1,$2)", ctx.guild.id,
                                      ctx.guild.name)
            await ctx.send("Auto moderation is enabled in your sever.")

        elif msg.content.lower() == "off":
            await self.bot.db.execute("DELETE FROM automoderation WHERE guild_id =$1", ctx.guild.id)
            await ctx.send("Auto moderation is disabled in your sever.")
        elif msg.content.lower() == "cancel":
            await sent.delete()

    @automod_.error
    async def automod_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `Manage_server` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Setup(bot))
    print("setup cog is loaded!")
