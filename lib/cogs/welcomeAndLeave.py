import discord
from discord.ext import commands
import random
import datetime

db_path = "./data/db/bot_database.sqlite"


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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

    @commands.Cog.listener()
    async def on_member_join(self, member):

        result = await self.bot.db.fecth("SELECT welcome FROM wallowed")
        allowed_welcome = [i[0] for i in result]
        print(allowed_welcome)
        if member.guild.id in allowed_welcome:
            result = await self.bot.db.fecth("SELECT welcome_channel FROM welcome WHERE guild_id =$1", member.guild.id)
            if result is None:
                return

            else:
                result1 = await self.bot.db.fecth(f"SELECT message FROM welcome WHERE guild_id = {member.guild.id}")
                channel = self.bot.get_channel(id=int(result['welcome_channel']))
                embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=datetime.datetime.utcnow())

                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/808664729366560789/808664820001144852/images_8.jpg")
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_author(name="Greetings!",
                                 icon_url="https://cdn.discordapp.com/attachments/808664729366560789"
                                          "/808699847090896896/bot_logo.png")
                embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
                embed.add_field(name="\u200B", value="Greetings!", inline=False)
                embed.add_field(name="\u200B", value=f"Welcome to {member.guild}", inline=False)
                embed.add_field(name="\u200B", value="**﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎**", inline=False)
                embed.add_field(name='\u200B', value=str(result1[0]), inline=False)
                embed.add_field(name="\u200B", value="**﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎**", inline=False)
                embed.add_field(name="\u200B", value="\u200B", inline=False)
                await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send(
            "Available Setup commands :\n Welcome wchannel <#channel>\n Welcome message <message>\n "
            "*Ignore `< >` in both commands.*")

    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def wchannel(self, ctx, channel: discord.TextChannel):
        result = await self.bot.db.fetch("SELECT welcome_channel FROM welcome WHERE guild_id = $1", ctx.guild.id)
        if not result:
            await self.bot.db.execute("INSERT INTO welcome (guild_id, welcome_channel) VALUES($1,$2)", ctx.guild.id,
                                      channel.id)
            return await ctx.send(f"welcome channel has been set to {channel.mention}")
        await self.bot.db.execute("UPDATE welcome SET welcome_channel = $1 WHERE guild_id = $2", channel.id,
                                  ctx.guild.id)
        await ctx.send(f"welcome channel has been updated to {channel.mention}")

    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def message(self, ctx, *, message):
        result = await self.bot.db.fetchrow("SELECT message FROM welcome WHERE guild_id = $1", ctx.guild.id)
        if not result:
            await self.bot.db.execute("INSERT INTO welcome(guild_id, message) VALUES($1,$2)", ctx.guild.id, message)
            return await ctx.send(f"Message has been set to {message}`")
        await self.bot.db.execute("UPDATE welcome SET message = $1 WHERE guild_id = $2", message, ctx.guild.id)
        await ctx.send(f"Message has been set updated to `{message}`")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        result = await self.bot.db.fecth("SELECT leave FROM lallowed")
        allowed_leave = [i[0] for i in result]
        print(allowed_leave)
        if member.guild.id in allowed_leave:
            result = await self.bot.db.fecth(f"SELECT leave_channel FROM leave WHERE guild_id = {member.guild.id}")
            if result is None:
                return

            else:

                embed = discord.Embed(
                    description=f"{member.mention} has left the server!",
                    colour=random.choice(self.bot.color_list))
                embed.set_author(name=f'Cyborg',
                                 icon_url='https://cdn.discordapp.com/attachments/808664729366560789'
                                          '/808699847090896896/bot_logo.png')
                embed.timestamp = datetime.datetime.utcnow()
                channel = self.bot.get_channel(id=int(result[0]))
                await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def leave(self, ctx):
        await ctx.send(
            "Available Setup commands :\n leave channel <#channel>\n "
            "*Ignore `< >` in commands.*")

    @leave.command()
    @commands.has_permissions(manage_guild=True)
    async def lchannel(self, ctx, channel: discord.TextChannel):
        result = await self.bot.db.fecth("SELECT leave_channel FROM leave WHERE guild_id = $1", ctx.guild.id)
        if not result:
            await self.bot.db.execute("INSERT INTO leave (guild_id, leave_channel) VALUES(?,?)", ctx.guild.id,
                                      channel.id)
            return await ctx.send(f"Leave channel has been set to {channel.mention}")

        await self.bot.db.execute("UPDATE leave SET leave_channel = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
        await ctx.send(f"leave channel has been updated to {channel.mention}")


def setup(bot):
    bot.add_cog(Welcome(bot))
    print('Welcome cog is loaded.')
