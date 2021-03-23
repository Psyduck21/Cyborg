import discord
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, guild_only, has_permissions
import datetime




class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='ui', description = "Sends user info if mentioned or sends author info.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        rolelist = []
        for role in member.roles:
            rolelist.append(role.mention)

        """if member.activity is not None:
            activity = 'None'
        else:
            activity = member.activities[-1].name"""

        embed = Embed(color=ctx.author.colour)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member}'s information", icon_url=f'{member.avatar_url}')
        fields = [("\u200B", f'**Nickname :** {str(member)}', False),
                  ("\u200B", f'**ID : ** ||{member.id}||', False),
                  ("\u200B", f'**Account created : ** {member.created_at.strftime("%d/%m/%Y %H:%M:%S")}', False),
                  ("\u200B", f'**Server joined : **{member.joined_at.strftime("%d/%m/%Y %H:%M:%S")}', False),
                  ("\u200B", f'**Role(s) : ** {"|".join(rolelist)}', False),
                  ("\u200B", f'**Highest role : ** {member.top_role.mention}', False),
                  #("\u200B", f'**Color : ** {member.color}', False),
                  ("\u200B", f'**Status : ** {member.status}', False),
                  #("\u200B", f'**Activity : ** {activity}', False),
                  ("\u200B", f'**Boosted : **{bool(member.premium_since)}', False),
                  ("\u200B", f'**Is Bot : ** {member.bot}', False),
                  ("\u200B", "\u200B", False)
                  ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @command(name = "cstats", description = "Send channel info.")
    @guild_only()
    async def cstats(self, ctx):
        channel = ctx.channel
        tmembers = str(len(channel.members))
        nsfw = (ctx.channel.is_nsfw())
        news = (ctx.channel.is_news())
        embed = Embed(title="Channel Information", color=ctx.author.colour)
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        fields = [("\u200B", f'**Channel name : **{channel.name}', False),
                  ("\u200B", f'**Channel ID : **||{channel.id}||', False),
                  ("\u200B", f'**Channel type : **{channel.type}', False),
                  ("\u200B", f'**Channel category : **{channel.category}', False),
                  ("\u200B", f'**Topic : **{channel.topic}', False),
                  ("\u200B", f'**Channel position : **{channel.position}', False),
                  ("\u200B", f'**Created at : **{channel.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")}', False),
                  ("\u200B", f'**Slowmode : **{channel.slowmode_delay}', False),
                  ("\u200B", f'**Channel Permissions Synced : **{channel.permissions_synced}', False),
                  ("\u200B", f'**Channel members : **{tmembers}', False),
                  ("\u200B", f'**Is nsfw : **{nsfw}', False),
                  ("\u200B", f'**Is news : **{news}', False),
                  ("\u200B", "\u200B", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.timestamp = datetime.datetime.utcnow()

        embed.set_author(name=f'{ctx.me.name}', icon_url=f'{ctx.me.avatar_url}')
        embed.set_footer(
            text=f" Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["si"], description = "Sends server info ")
    async def serverinfo(self, ctx):
        embed = Embed(title="*Server Information*", color=ctx.author.color,
                      )

        fields = [("\u200B", f"**Server Name : ** {ctx.guild.name}", False),
                  ("\u200B", f"**ID : ** ||{ctx.guild.id}||", False),
                  ("\u200B", f"**:crown: OWNER : ** {ctx.guild.owner}", False),
                  ("\u200B", f"**:earth_asia: Region : ** {ctx.guild.region}", False),
                  ("\u200B", f'**:clock12: Created at : ** {ctx.guild.created_at.strftime("%d/%m/%y %H:%M:%S")}', False),
                  ("\u200B", f"**:bust_in_silhouette: Members : ** {len(ctx.guild.members)}", False),
                  ("\u200B", f"**:busts_in_silhouette: Humans : ** {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}", False),
                  ("\u200B", f"**:robot: Bots : ** {len(list(filter(lambda m: m.bot, ctx.guild.members)))}", False),
                  #("\u200B", f"**:x: Banned members : ** {len(await ctx.guild.bans())}", False),
                  ("\u200B", f"**:notebook_with_decorative_cover: Categories : ** {len(ctx.guild.categories)}", False),
                  ("\u200B", f"**:notepad_spiral: Text channel : ** {len(ctx.guild.text_channels)}", False),
                  ("\u200B", f"**:loud_sound: Voice channel : ** {len(ctx.guild.voice_channels)}", False),
                  ("\u200B", f'**:medal:  Roles : ** {len(ctx.guild.roles)}', False),
                  ("\u200B", f'**:arrow_double_up: Server boosts : ** {ctx.guild.premium_subscription_count}', False),
                  ("\u200B", "\u200B", False)
                  ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_author(name=f'{ctx.me.name}', icon_url=f'{ctx.me.avatar_url}')
        embed.set_footer(
            text=f" Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        await ctx.send(embed=embed)
    @command(aliases =["bi"])
    async def botinfo(self, ctx):
        bot = Embed(title = "My stats!",
        colour = ctx.author.colour,
        timestamp = datetime.datetime.utcnow())

        fields = [("Bot Version ", "0.0.1", False),
        ("Owner" ,  "<@740416145256874045>", False)]

        for name , value , inline in fields:
            bot.add_field(name=name, value = value , inline = inline)

        bot.set_thumbnail(url=self.bot.user.avatar_url,)

        await ctx.send(embed = bot)
    @command(aliases=['rinfo'], description = "Sends role indo u asked for.")
    @has_permissions(manage_roles=True)
    async def roleinfo(self, ctx, role:discord.Role):
        allowed = []
        try:
            role = discord.utils.get(ctx.message.guild.roles, name=role.name)
            permissions = role.permissions

            for name, value in permissions:
                if value:
                    name = name.replace('_', ' ').replace(
                        'guild', 'server').title()
                    allowed.append(name)
        except:
            return await ctx.send(f"Couldn't find the role")
        time = role.created_at
        em = discord.Embed(description=f'', color=role.colour, timestamp=time)
        em.set_author(name=f'{role.name}')
        em.set_thumbnail(url=f'{ctx.guild.icon_url}')
        em.add_field(name='__Info__', value=f'**ID :** {str(role.id)} \n'
                                            f'**Color :** {role.color}\n'
                                            f'**Hoisted :** {str(role.hoist)}\n'
                                            f'**Position :** {str(role.position)}\n'
                                            f'**Is mentionable :** {str(role.mentionable)}\n'
                                            f'**Members in role :** {str(len(role.members))}\n')
        em.add_field(name='__Role permissions__',
                     value=f', '.join(allowed), inline=False)
        em.set_footer(text="Role created on")
        await ctx.send(embed=em)





def setup(bot):
    bot.add_cog(Info(bot))
    print("Info cog is loaded!")
