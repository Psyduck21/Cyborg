import discord
from discord.ext import commands
import datetime

pg = open("./secrets/pg_pwd.txt", "r").read()


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        result = await self.bot.db.fetch("SELECT lvl FROM allowed")
        allowed_leveling = [i[0] for i in result]
        if message.guild.id in allowed_leveling:
            if message.author.bot is True or message.guild is None:
                return

            result = await self.bot.db.fetch(f"SELECT xp, lvl FROM users WHERE userid = $1 and guild_id = $2",
                                             message.author.id, message.guild.id)
            if not result:
                await self.bot.db.execute('INSERT INTO users (userid, guild_id, xp, lvl) VALUES($1, $2, $3, $4)',
                                          message.author.id, message.guild.id, 0, 0)
            else:
                result1 = await self.bot.db.fetchrow(
                    "SELECT userid, xp, lvl FROM users WHERE userid = $1 and guild_id = $2", message.author.id,
                    message.guild.id)
                exp = result1[1]
                await self.bot.db.execute("UPDATE users SET xp =$1 WHERE guild_id = $2 and userid = $3", exp + 10,
                                          message.guild.id, message.author.id)

                result = await self.bot.db.fetchrow("SELECT xp FROM users WHERE userid =$1 and guild_id = $2",
                                                    message.author.id, message.guild.id)
                xp = result[0]

                lvl = 0
                while True:
                    if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                        break
                    lvl += 1
                    await self.bot.db.fetchrow('UPDATE users SET lvl=$1 WHERE userid=$2 and guild_id=$3', lvl,
                                               message.author.id, message.guild.id)

                xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))

                if xp == 0:

                    r = await self.bot.db.fetchrow("SELECT channel_id FROM lvlchannel WHERE guild_id = $1",
                                                   message.guild.id)
                    channel = self.bot.get_channel(id=r[0])

                    if not r:
                        await message.channel.send(f"{message.author.mention} has leveled up. Now level *{lvl}*")
                        print('LEVEL UP')
                    else:
                        await channel.send(f"{message.author.mention} has leveled up. Now level *{lvl}*")
                        print('LEVEL UP')

                    r = await self.bot.db.fetchrow('SELECT lvl from users WHERE userid = $1 and guild_id = $2',
                                                   message.author.id, message.guild.id)
                    lvlnum = r[0]
                    print(lvlnum)
                    if lvlnum == 5:
                        await message.author.add_roles(
                                discord.utils.get(message.author.guild.roles, name=f"level 5+"))
                    elif lvlnum == 11:
                        await message.author.add_roles(
                                discord.utils.get(message.author.guild.roles, name=f"level 10+"))

                    elif lvlnum == 20:
                        await message.author.add_roles(
                                discord.utils.get(message.author.guild.roles, name=f"level 20+"))

                    elif lvlnum == 30:
                        await message.author.add_roles(
                                discord.utils.get(message.author.guild.roles, name=f"level 30+"))

                    elif lvlnum == 40:
                        await message.author.add_roles(
                                discord.utils.get(message.author.guild.roles, name=f"level 40+"))

                    elif lvlnum == 50:
                        await message.author.add_roles(
                                discord.utils.get(message.author.guild.roles, name=f"level 50+"))

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        result = await self.bot.db.fetchrow(
            "SELECT userid, guild_id, xp, lvl FROM users WHERE userid = $1 and guild_id = $2", member.id,
            member.guild.id)
        if not result:
            embed = discord.Embed(description="Oops! User is unrated!")
            await ctx.send(embed=embed)
        else:
            level = result[3]
            # cursor.execute("SELECT Count(*) from users xp < ? where guild_id = ? ", (xp, ))
            embed = discord.Embed(title=f"{member.display_name}'s stats", colour=ctx.author.colour)
            embed.add_field(name="Name", value=member.mention, inline=True)
            embed.add_field(name="XP", value=result[2], inline=True)
            embed.add_field(name="Level", value=level, inline=True)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(
                text=f" Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)


"""    @commands.command()
    async def dm(self, ctx):
        r = await self.bot.db.fetchrow("SELECT channel_id FROM lvlchannel WHERE guild_id = $1", ctx.guild.id)
        channel = self.bot.get_channel(id=r[0])
        id = r[0]
        print(id)
"""


def setup(bot):
    bot.add_cog(Level(bot))
    print("Level cog is loaded.")
