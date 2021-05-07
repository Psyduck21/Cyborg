import discord
from discord.ext import commands
import json


class Funcounting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        await ctx.guild.create_text_channel("fun-counting")
        fun_channel = discord.utils.get(ctx.guild.channels, name="fun-counting")
        await ctx.send(f"Game has started check out {fun_channel.mention}")
        emb = discord.Embed(
            description="*Rules of the game*\n1. No Member :octagonal_sign: should send 2 numbers in a row.\n2. Member should send consecutive numbers.\n*Disobeying any of the above Rule the game will be restarted*",
            colour=discord.Colour.blue())
        await fun_channel.send(embed=emb)
        await fun_channel.send("1")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        fun_channel = discord.utils.get(message.guild.channels, name="fun-counting")
        if message.channel == fun_channel and message.guild.id == 740418138075693107 and message.content not in ["$start", "<@740416145256874045> has disobeyed the rules\nRestarting the game"]:
            def check(msg):
                return msg.channel == fun_channel and msg.content not in ["$start",
                                                                          "<@740416145256874045> has disobeyed the rules\nRestarting the game"]

            msg = await self.bot.wait_for("message", check=check)
            with open("fun.json") as json_file:
                data = json.load(json_file)

                fun_entry = {'user_id': message.author.id,
                             'content': message.content
                             }

                data.append(fun_entry)

            with open("fun.json", 'w') as f:
                json.dump(data, f, indent=4)

            i = data[-1]
            n = i['content']
            member_id = i['user_id']
            next_number = int(n) + 1
            next_number = str(next_number)
            if msg.content == next_number and msg.author.id != member_id:
                print("passed")

            else:
                await fun_channel.delete()
                await message.guild.create_text_channel("fun-counting")
                fun_channel = discord.utils.get(message.guild.channels, name="fun-counting")
                await fun_channel.send(f"{msg.author.mention} has disobeyed the rules\nRestarting the game")
                emb = discord.Embed(
                    description="*Rules of the game*\n1. No Member :octagonal_sign: should send 2 numbers in a row.\n2. Member should send consecutive numbers.\n*Disobeying any of the above Rule the game will be restarted*",
                    colour=discord.Colour.blue())
                await fun_channel.send(embed=emb)
                await fun_channel.send("1")


def setup(bot):
    bot.add_cog(Funcounting(bot))
    print("Fun counting Added")
