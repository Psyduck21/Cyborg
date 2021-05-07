import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
from lib.cogs.utils import Pag


class Help(commands.Cog, name='Help'):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 10

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, *, entity=None):
        if ctx.channel.id == 757108786497585172:
            return

        if not entity:
            embed1 = discord.Embed(color=ctx.author.colour,
                                   title='[$help <command name>`] for more info on commands.')
            embed1.set_thumbnail(url=f'{ctx.me.avatar_url}')
            embed1.add_field(
                name=":partying_face: Fun commands", value=f'`fact`, `meme`, `joke`', inline=False)
            embed1.add_field(
                name=":receipt: Handy commands", value=f'`ping`, `invite`, `rank`', inline=False)
            embed1.add_field(
                name=":nerd: Nerd commands", value=f'`userinfo`, `serverinfo`,`channelstats`, `botinfo`, `roleinfo`\n\n',
                inline=False)

            embed1.add_field(
                name="DB-command", value=f'`profanity`, `linkmod`', inline=False)
            embed1.add_field(
                name=":musical_note: Music-Commands", value=f'`Play`, `queue`, `connect`, `disconnect`, `pause`, `stop`, `next`, `previous`, `shuffle`, `repeat`', inline=False)

            embed1.add_field(name="setup", value="use `setup` if you are using bot for first time in this server.\n\n"
                                                 "**Support**\n"
                                                 "[invite me to your server](https://discord.com/api/oauth2/authorize?client_id=802539167992119296&permissions=8&scope=bot) , [Join server](https://discord.gg/7CgTvNKeWC)\n")
            embed1.set_footer(text="Made with love and py | © akshu (The Professor)", icon_url=ctx.me.avatar_url)
            await ctx.author.send(embed=embed1)
            await ctx.send("Check ur Dm!")
        else:
            command = self.bot.get_command(entity)
            if command:
                await self.setup_help_pag(ctx, command, command.name)

            else:
                await ctx.send(f"{entity} not found.")

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []
        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue
                elif c.parent:
                    continue
                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue
        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "| ".join(command.aliases)
        cmd_invoke = f'[{command.name} aliases: {command.aliases}]' if command.aliases else command.name
        full_invoke = command.qualified_name.replace(command.name, "")
        signature = f'${full_invoke}{cmd_invoke} {command.signature}'
        return signature

    async def setup_help_pag(self, ctx, entity=None, title=None):
        entity = entity or self.bot
        title = title or self.bot.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )
            filtered_commands.insert(0, entity)
        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i: i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd, ctx)
                subcommands = "Has subcommands " if hasattr(
                    cmd, "all_commands") else ""
                commands_entry += (
                    f" ```{signature}\n```\n**Description:** {desc}\n"
                    if isinstance(entity, commands.Command)
                    else f"**{cmd.name}**\n{desc}\n    {subcommands}\n"
                )
            pages.append(commands_entry)
        await Pag(title=title, color=ctx.author.colour, entries=pages, length=1).start(ctx)

    @commands.command()
    async def help_default(self, ctx, *, entity=None):
        if not entity:
            await self.setup_help_pag(ctx)
        else:
            cog = self.bot.get_cog(entity)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.bot.get_command(entity)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send(f"{entity} not found.")

    @commands.command(alaises=['moderationcommands'])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def helpmod(self, ctx):

        embed1 = discord.Embed(color=ctx.author.colour)
        embed1.set_author(name="Mod Commands", icon_url=f'{ctx.me.avatar_url}')
        embed1.add_field(name="Clear", value="**Aliases** : None\n"
                                             "**Permission** : Manage messages \n"
                                             "**Roles** : Elder or higher\n"
                                             "**Usage**\n `$clear 10`\n\n", inline=False
                         )
        embed1.add_field(name="Clearuser", value="**Aliases** : Purgeuser, Clearuser\n"

                                                 "**Permission** : Manage messages\n"
                                                 "**Roles** : Elder or higher\n"
                                                 "**Usage**\n `$clearuser <@740416145256874045> 10`\n\n", inline=False)

        embed1.add_field(name="Dmuser", value=f"**Aliases** : Pmuser\n"

                                              "**Permission** : Manage messages\n"
                                              "**Roles** : Elder or higher\n"
                                              '**Usage**\n `$dmuser @cybord "why is this a command?"`\n\n',
                         inline=False)
        embed1.set_footer(
            text=f"Tip : All the command names are case insensitive.")

        embed2 = discord.Embed(color=ctx.author.colour)
        embed2.add_field(name="Kick", value=f"**Aliases** : None\n"

                                            "**Permission** : Kick users\n"
                                            "**Roles** : Outer elder or higher\n"
                                            "**Usage**\n `$kick <user> <Reason>`\n")
        embed2.add_field(name="Ban", value=f"**Aliases** : None\n"

                                           "**Permission** : Ban users\n"
                                           "**Roles** : Inner elder or higher\n"
                                           "**Usage**\n `$ban <user> <Reason>`\n")
        embed2.add_field(name="Unban", value=f"**Aliases** : None\n"

                                             "**Permission** : Administrator\n"
                                             "**Roles** : Admin\n"
                                             "**Usage**\n `$unban cyborg#4953`\n"
                                             "**Example :** \n\n", inline=False)
        embed2.set_footer(
            text=f"Tip : If you are a new elder feel free to bug your seniors. ")
        embed3 = discord.Embed(color=ctx.author.colour)
        embed3.set_footer(
            text=f"Tip : Although the commands are insensitive the role names aren't be carefully.")
        embed4 = discord.Embed(color=ctx.author.colour)
        embed4.add_field(name='role', value=f"**Aliases** : None\n"
                                            f'**What for** : To add and for remove roles (use $rrole) to the mentioned user.\n'
                                            "**Permission** : Manage roles\n"
                                            "**Roles** : Inner elder or higher\n"
                                            "**Usage**\n `$role cyborg#4953 Head Instructor`\n"
                                            "**Example :** \n\n", inline=False)
        embed4.set_footer(
            text='Tip : Is used on the user who already has the role the Bot will remove the role.')
        embed5 = discord.Embed(color=ctx.author.colour)
        embed5.add_field(name='Channelstats', value=f"**Aliases** : cstats\n"


                                                    "**Roles** : Outer elder or higher\n"
                                                    "**Usage**\n `$Channelstats `\n", inline=False)
        embed5.set_footer(
            text='Tip : Only read mods use Channelstats. \nTip2 : ".Slowmode remove" will remove the slowmode. ')
        embed6 = discord.Embed(color=ctx.author.colour)
        embed6.add_field(name='Poll', value=f"**Aliases** : None\n"
                                            "**Limit** : 10\n"
                                            "**Atleast** : 2\n"
                                            "**Roles** : Outer elder or higher\n"
                                            '**Usage**\n `$createpoll "Poll title here" "Option1" "Option2" `\n'
                                            "**Example :** \n\n", inline=False)
        embed6.set_footer(
            text=f'Tip : If your options are "yes" and "no", cyborg will react with a tick and a cross.')
        embed7 = discord.Embed(color=ctx.author.colour)
        embed7.add_field(
            name='Lock / Unlock',
            value=f'**Aliases : **None\n**For :** Verified role\n**Roles :** Supreme elder or higher. \n**Usuage :** `.lock / .unlock`',
            inline=False)
        embed7.add_field(name='Roleinfo', value=f"**Aliases : **  rinfo\n"

                                                "**Roles :**  Inner elder or higher\n"
                                                '**Usage**\n `$roleinfo @servermanager `\n', )
        embed7.set_footer(
            text=f'You earn a custom role for being an elder, don\'t forget to ask one for yourself.')

        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command()
    async def embedtest(self, ctx):
        embed1 = discord.Embed(title=f'Page1')
        embed1.add_field(name="This is a page", value="Yep itsure is")
        embed2 = discord.Embed(title=f'Page3')
        embed2.add_field(name="This is a page", value="Yep itsure is")
        embed3 = discord.Embed(title=f'Page3')
        embed3.add_field(name="This is a page", value="Yep itsure is")
        embeds = [embed1, embed2, embed3]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command(aliases=['databasecommands'])
    @commands.has_permissions(manage_guild=True)
    async def helpdb(self, ctx):
        embed = discord.Embed(colour=ctx.author.colour)
        embed.set_author(name="DB Commands", icon_url=f'{ctx.me.avatar_url}')
        embed.add_field(name="profanity", value="**Info** : show weather profanity is allowed or not in your server.\n"
                                                "**Usage** : `$profanity`")
        embed.add_field(name="linkmod", value="**Info** : show weather profanity is allowed or not in your server.\n"
                                              "**Usage** : `linkmod`")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
    print("Help cog is loaded.")
