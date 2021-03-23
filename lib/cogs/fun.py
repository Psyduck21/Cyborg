import discord
from discord.ext.commands import command, Cog
from aiohttp import request
from discord.ext.commands.errors import MissingRequiredArgument
from aiohttp import ClientSession


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="fact", description="Sends the fact of animal name entered")
    async def fact(self, ctx, animal: str):
        if animal.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal.lower()}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal.lower() == 'bird' else animal.lower()}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(title=f'{animal.title()} fact',
                                          description=data["fact"],
                                          colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                        embed.add_field(name="Note:-", value="*Image shown below is not related to fact*")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"API returned {response.status} status")
        else:
            await ctx.send(f"No fact are available for **{animal}**")

    @fact.error
    async def error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                description=f'Please enter name of the animal from list  of animal `("dog", "cat", "panda", "fox", "bird", "koala")` {ctx.author.mention}',
                colour=ctx.author.colour
            )
            await ctx.send(embed=embed)

    @command(name="meme", description="Sends meme.")
    async def meme(self, ctx):

        image_url = "https://some-random-api.ml/meme"

        async with request("GET", image_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(data["image"])

    @command(name="joke", description="Sneds dad jokes.")
    async def joke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/joke"
        headers = {
            'x-rapidapi-key': "4480a12ab4msh4e9abaa4ba3041fp1b5980jsnd47881ff5b0e",
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
        }

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                r = await response.json()
                r = r["body"][0]
                embed = discord.Embed(title=f"{r['type']} Joke", color=ctx.author.color)
                embed.add_field(name=f"{r['setup']}", value=f"||{r['punchline']}||", inline=False)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
    print("fun cog is loadede")
