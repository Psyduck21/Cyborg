import discord
from discord.ext import commands
import typing
from datetime import datetime


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pmuser'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def DMuser(self, ctx, user: discord.User, *, msg):
        try:
            await user.send(f'**{ctx.message.author}** has a message for you, \n {msg}')

        except:
            await ctx.send(f'The user has his/her DMs turned off.')

    @commands.command(aliases=['clearuser'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purgeuser(self, ctx, user: discord.Member,
                        num_messages: typing.Optional[int] = 100,
                        ):
        channel = ctx.message.channel
        if ctx.guild.me.top_role < user.top_role:
            return await ctx.send("Admin :(")
        if ctx.message.author.top_role < user.top_role:
            return await ctx.send("You have lower roles.")

        def check(msg):
            return msg.author.id == user.id

        await ctx.message.delete()
        await channel.purge(limit=num_messages, check=check, before=None)
        embed = discord.Embed(title="User Messages cleared",
                              colour=ctx.author.colour)
        embed.add_field(name="Member", value=user.display_name, inline=False)
        embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
        embed.add_field(name="No. of messages", value=f"{num_messages}", inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.timestamp = datetime.utcnow()
        r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if not r:
            return await ctx.send(embed=embed, delete_after=10)
        log_channel = self.bot.get_channel(id=r)
        await log_channel.send(embed=embed)

    @commands.command(name='ban', help='use to ban members.')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if not r:
            await member.ban(reason=reason)
            embed = discord.Embed(title="Member Banned",
                                  colour=ctx.author.colour)
            embed.add_field(name="Member", value=member.display_name, inline=False)
            embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed, delete_after=10)

        log_channel = self.bot.get_channel(id=r)
        await member.ban(reason=reason)
        embed = discord.Embed(title="Member Banned",
                              colour=ctx.author.colour)
        embed.add_field(name="Member", value=member.display_name, inline=False)
        embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.timestamp = datetime.utcnow()
        await log_channel.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, member: discord.Member):
        if isinstance(member, commands.MissingRequiredArgument):
            embed = discord.Embed(description=f'{ctx.author.mention}Please mention the member to be **Banned**.',
                                  colour=ctx.author.colour
                                  )
            await ctx.send(embed=embed, delete_after=10)
        if isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} :x: You need `Ban_Member` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)

    @commands.command(name='clear', help='Using this command you can clear messages in any channel.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount1: int):
        channel = ctx.message.channel
        await ctx.channel.purge(limit=amount1)
        r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if not r:
            embed = discord.Embed(title="Messages Clear",
                                  colour=ctx.author.colour)
            embed.add_field(name="Number of messages clear", value=f"{amount1}", inline=False)
            embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
            embed.add_field(name="Channel", value=channel.mention, inline=False)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed, delete_after=10)

        log_channel = self.bot.get_channel(id=r)

        embed = discord.Embed(title="Messages Clear",
                              colour=ctx.author.colour)
        embed.add_field(name="Number of messages clear", value=f"{amount1}", inline=False)
        embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.timestamp = datetime.utcnow()
        return await log_channel.send(embed=embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f'{ctx.author.mention}Please specify the number of messages to be **purge**',
                colour=ctx.author.colour
            )
            await ctx.send(embed=embed, delete_after=10)

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `Manage_messages` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)

    @commands.command(name='kick', help='This command is used to kick someone from server. Only given to some members.')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if not r:
            embed = discord.Embed(title="Member Kicked",
                                  colour=ctx.author.colour)
            embed.add_field(name="Member", value=member.display_name, inline=False)
            embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.timestamp = datetime.utcnow()

            return await ctx.send(embed=embed, delete_after=10)

        log_channel = ctx.guild.get_channel(r[0])

        embed = discord.Embed(title="Member Kicked",
                              colour=ctx.author.colour)
        embed.add_field(name="Member", value=member.display_name, inline=False)
        embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.timestamp = datetime.utcnow()

        await log_channel.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, member: discord.Member):
        if isinstance(member, commands.MissingRequiredArgument):
            embed = discord.Embed(description=f'{ctx.author.mention}Please mention the member to be **Kicked**.',
                                  colour=ctx.author.colour
                                  )
            await ctx.send(embed=embed, delete_after=10)

        if isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `Kick_Member` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)

    @commands.command(name='unban', help='Unbans member')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()  # names tuple containing user object and reason user is baned
        member_name, member_discriminator = member.split('#')  # splitting name nd discriminator with #
        for ban_entry in banned_users:  # going throw and banned entry in variable banned_user which in server its self
            user = ban_entry.user  # pulling user from banned entry and assigning in variable user

            if (user.name, user.discriminator) == (
                    member_name, member_discriminator):  # taking user name and matching
                # it in banner_users
                await ctx.guild.unban(user)
                # unbanning user
                embed = discord.Embed(title="Member Muted",
                                      colour=ctx.author.colour)
                embed.add_field(name="Member", value=member.display_name, inline=False)
                embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
                embed.timestamp = datetime.utcnow()
                r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
                if not r:
                    await ctx.send(embed=embed, delete_after=10)  # mentioning user which was unbanned
                    return

                log_channel = ctx.guild.get_channel(r[0])
                await log_channel.send(embed=embed)  # mentioning user which was unbanned

    @unban.error
    async def unban_error(self, ctx, member: discord.Member):
        if isinstance(member, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}Please enter name and discriminator of member.', delete_after=10)

        if isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `ban_member` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)

    @commands.command()
    @commands.has_permissions(manage_roles=True, manage_guild=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if role not in guild.roles:
            await ctx.send("You have not setup mute command. to do so use **$setup**")
        else:
            await member.edit(roles=[role])
            embed = discord.Embed(title="Member Muted",
                                  colour=ctx.author.colour)
            embed.add_field(name="Member", value=member.display_name, inline=False)
            embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.timestamp = datetime.utcnow()

            r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
            if not r:
                await ctx.send(embed=embed, delete_after=10)
                return

            log_channel = ctx.guild.get_channel(r[0])
            await log_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True, manage_guild=True)
    async def unmute(self, ctx, member: discord.Member, role: discord.Role):
        await member.edit(roles=[role])
        embed = discord.Embed(title="Member Unmuted",
                              colour=ctx.author.colour)
        embed.add_field(name="Member", value=member.display_name, inline=False)
        embed.add_field(name="Actioned By", value=ctx.author.name, inline=False)
        embed.add_field(name="Role given", value=role.name, inline=False)
        embed.timestamp = datetime.utcnow()
        r = await self.bot.db.fetchval(f"SELECT channel_id FROM logchannel WHERE guild_id = {ctx.guild.id}")
        if not r:
            await ctx.send(embed=embed, delete_after=10)
            return

        log_channel = ctx.guild.get_channel(r[0])
        await log_channel.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, member: discord.Member):
        if isinstance(member, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}Please mention the member to be muted.', delete_after=10)

        if isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `manage_roles` & `manage_server` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)

    @unmute.error
    async def unmute_error(self, ctx, member: discord.Member):
        if isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.author.mention} :x: You need `manage_roles` & `manage_server` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed, delete_after=10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, role: discord.Role):
        await ctx.channel.set_permissions(role, send_messages=False, read_messages=True)
        await ctx.send("Channel locked.", delete_after=10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, role: discord.Role):
        await ctx.channel.set_permissions(role, send_messages=True, read_messages=True)
        await ctx.send("Channel unlocked.", delete_after=10)

    @commands.command(aliases=['invite'])
    async def createbotlink(self, ctx):
        embed = discord.Embed(title="Invite me !",
                              url="https://discord.com/api/oauth2/authorize?client_id=802539167992119296&permissions=8&scope=bot",
                              colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(name="role", description='Gives role to user.')
    async def give_role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f"{member.mention} was given role {role.mention}.")

    @commands.command(name="rrole", description='Removes role to user.')
    async def remove_role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has removed role {role.mention}.")

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Role is the required argument which is missing.", delete_after=10)

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Role is the required argument which is missing.", delete_after=10)
            await ctx.send("Role is the required argument which is missing.", delete_after=10)


def setup(bot):
    bot.add_cog(Mod(bot))
    print("Mod cog is loaded")
