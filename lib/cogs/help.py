import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
from lib.cogs.utils import Pag

class help(commands.Cog, name='Help'):
    def __init__(self, Bot):
        self.Bot = Bot
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
                name=":crossed_swords: Admin/Mod commands", value=f'`Dmuser`, `purgeuser`, `role`, `ban`, `unban`, `clear`, `kick`, `mute`, `unmute`, `logchannel`, `lock`, `unlock`, `Invite`\n' '**Reaction role / poll Commands**\n' '`poll`, `reactrole`, `createpoll`', inline=False)
            embed1.add_field(
                name=":partying_face: Fun commands", value=f'`fact`, `meme`, `joke`', inline=False)
            embed1.add_field(
                name=":receipt: Handy commands", value=f'`ping`, `invite`', inline=False)
            embed1.add_field(
                name=":nerd: Nerd commands", value=f'`userinfo`, `serverinfo`,`channelstats`, `botinfo`, `roleinfo`',  inline=False)
            embed1.add_field(name="setup", value="use `setup` if you are using bot for first time in this server.")

            """embeds = [embed1]
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()"""
            await ctx.send(embed= embed1)
        else:
            command = self.Bot.get_command(entity)
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
        entity = entity or self.Bot
        title = title or self.Bot.description

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
            cog = self.Bot.get_cog(entity)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.Bot.get_command(entity)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send(f"{entity} not found.")

    @commands.command(alaises=['moderationcommands'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def helpmod(self, ctx):

        embed1 = discord.Embed(color=ctx.author.colour)
        embed1.set_author(name="Mod Commands", icon_url=f'{ctx.me.avatar_url}')
        embed1.add_field(name="Clear", value="**Aliases** : None\n"
                         "**Permission** : Manage messages \n"
                         "**Roles** : Elder or higher\n"
                         "**Usage**\n ```$clear 10```\n\n"
                         )
        """embed1.add_field(name="Clearuser", value="**Aliases** : Purgeuser, Clearuser\n"

                         "**Permission** : Manage messages\n"
                         "**Roles** : Elder or higher\n"
                         "**Usage**\n ```$clearuser @Vein#8177 10```\n\n")"""
        embed1.add_field(name="‎‎‎‏‏‎ ", value='‎‎‎‏‏‎ ')
        """embed1.add_field(name="DM", value=f"**Aliases** : PM\n"

                         "**Permission** : Manage messages\n"
                         "**Roles** : Elder or higher\n"
                         "**Usage**\n ```$dm Idek why this is a command.```\n\n")"""
        embed1.add_field(name="Dmuser", value=f"**Aliases** : Pmuser\n"

                         "**Permission** : Manage messages\n"
                         "**Roles** : Elder or higher\n"
                         '**Usage**\n ```$dmuser @cybord "why is this a command?"```\n\n')
        embed1.set_footer(
            text=f"Tip : All the command names are case insensitive.")

        embed2 = discord.Embed(color=ctx.author.colour)
        embed2.add_field(name="Kick", value=f"**Aliases** : None\n"

                         "**Permission** : Kick users\n"
                         "**Roles** : Outer elder or higher\n"
                         "**Usage**\n ```$kick <user> <Reason>```\n")
        embed2.add_field(name="Ban", value=f"**Aliases** : None\n"

                         "**Permission** : Ban users\n"
                         "**Roles** : Inner elder or higher\n"
                         "**Usage**\n ```$ban <user> <Reason>```\n")
        embed2.add_field(name="Unban", value=f"**Aliases** : None\n"

                         "**Permission** : Administrator\n"
                         "**Roles** : Admin\n"
                         "**Usage**\n ```$unban cyborg#4953```\n"
                         "**Example :** \n\n", inline=False)
        embed2.set_footer(
            text=f"Tip : If you are a new elder feel free to bug your seniors. ")
        embed3 = discord.Embed(color=ctx.author.colour)
        embed3.set_footer(
            text=f"Tip : Altough the commands are insensitive the role names aren't be carefull.")
        embed4 = discord.Embed(color=ctx.author.colour)
        embed4.add_field(name='role', value=f"**Aliases** : None\n"
                                            f'**What for** : To add or remvoe roles to the mentioned user.\n'
                         "**Permission** : Manage roles\n"
                         "**Roles** : Inner elder or higher\n"
                         "**Usage**\n ```$role cyborg#4953 Head Insturctor ```\n"
                         "**Example :** \n\n", inline=False)
        embed4.set_footer(
            text='Tip : Is used on the user who already has the role the Bot will remove the role.')
        embed5 = discord.Embed(color=ctx.author.colour)
        embed5.add_field(name='Channelstats', value=f"**Aliases** : cstats\n"


                         "**Roles** : Outer elder or higher\n"
                         "**Usage**\n ```$Channelstats ```\n", inline=False)
        embed5.set_footer(
            text='Tip : Only read mods use Channelstats. \nTip2 : ".Slowmode remove" will remove the slowmode. ')
        embed6 = discord.Embed(color=ctx.author.colour)
        embed6.add_field(name='Poll', value=f"**Aliases** : None\n"
                         "**Limit** : 10\n"
                         "**Atleast** : 2\n"
                         "**Roles** : Outer elder or higher\n"
                         '**Usage**\n ```$createpoll "Poll title here" "Option1" "Option2" ```\n'
                         "**Example :** \n\n", inline=False)
        embed6.set_footer(
            text=f'Tip : If your options are "yes" and "no", Abode will react with a tick and a cross.')
        embed7 = discord.Embed(color=ctx.author.colour)
        embed7.add_field(
            name='Lock / Unlock', value=f'**Aliases : **None\n**For :** Verified role\n**Roles :** Supreme elder or higher. \n**Usuage :** ```.lock / .unlock```', inline=False)
        embed7.add_field(name='Roleinfo', value=f"**Aliases : **  rinfo\n"

                                                "**Roles :**  Inner elder or higher\n"
                                                '**Usage**\n ```$roleinfo Verified ```\n',)
        embed7.set_footer(
            text=f'You earn a custom role for being an elder, don\'t forget to ask one for yourself.')

        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command()
    async def embedtest(self, ctx):
            embed1 = discord.Embed(title=f'Page1')
            embed1.add_field(name="This is a page", value="Yep itsure is")
            embed2 = discord.Embed( title=f'Page3')
            embed2.add_field(name="This is a page", value="Yep itsure is")
            embed3 = discord.Embed(title=f'Page3')
            embed3.add_field(name="This is a page", value="Yep itsure is")
            embeds = [embed1, embed2, embed3]
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

def setup(Bot):
    Bot.add_cog(help(Bot))
    print("Help cog is loaded.")