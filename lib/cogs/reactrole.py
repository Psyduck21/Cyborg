import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions
import json
import random
import datetime

db_path = "./data/db/bot_database.sqlite"

from discord import Embed

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
           "6⃣", "7⃣", "8⃣", "9⃣", "🔟")


class Reactrole(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.polls = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            pass

        else:
            with open("./data/json/reactrole.json") as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                        role = discord.utils.get(self.client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        with open("./data/json/reactrole.json") as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(self.client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

    @commands.command(name="poll", description="Used for quick polls")
    async def poll(self, ctx, *, message):
        emb = discord.Embed(title="**POLL**",
                            description=f"{message}",
                            colour=random.choice(self.client.color_list)
                            )
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):

        emb = discord.Embed(description=message,
                            colour=random.choice(self.client.color_list)
                            )

        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)

        with open("./data/json/reactrole.json") as json_file:
            data = json.load(json_file)

            new_react_role = {'role_name': role.name,
                              'role_id': role.id,
                              'emoji': emoji,
                              'message_id': msg.id}

            data.append(new_react_role)

        with open("./data/json/reactrole.json", 'w') as f:
            json.dump(data, f, indent=4)

    @reactrole.error
    async def reactrole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} :x: You need ``Manage_Roles`` permission to use this command.",
                colour=ctx.author.colour)
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} Check something is missing in command. Make sure u have used it as ``$reactrole <emoji> <@role> <your_message>",
                colour=ctx.author.colour)
            await ctx.send(embed=embed)

    @commands.command(name="createpoll", aliases=["mkpoll"], description="Used for creating polls.")
    @commands.has_permissions(manage_guild=True)
    async def create_poll(self, ctx, question: str, *options):
        if len(options) > 10:
            await ctx.send("You can only supply a maximum of 10 options.")

        else:
            embed = Embed(title="Poll",
                          description=f"**{question}**",
                          colour=ctx.author.colour,
                          timestamp=datetime.datetime.utcnow())

            fields = [("\u200B", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                      ("Instructions", "React to cast a vote!", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            message = await ctx.send(embed=embed)

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)

        # self.polls.append((message.channel.id, message.id))


def setup(client):
    client.add_cog(Reactrole(client))
    print('Reactrole cog is loaded.')
