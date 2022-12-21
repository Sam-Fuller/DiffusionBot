import discord
from discord import app_commands
from discord.ext import commands
import stable_diffusion


async def generate_diffusion(ctx: discord.Interaction, prompt: str):
    print(f"generating \"{prompt}\"")
    await ctx.response.send_message(f"generating \"{prompt}\", this will take 30-60 seconds", ephemeral=True)

    image = stable_diffusion.txt2img(prompt)
    image.save("image.png")

    embed = discord.Embed(title=prompt)
    embed.set_image(url='attachment://image.png')

    await ctx.channel.send(embed=embed, file=discord.File("image.png"))


class Generate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: discord.Interaction):
        commands = await ctx.bot.tree.sync()
        print(f"INFO: {len(commands)} commands synced")

    @app_commands.command(name="generate", description="Generate an image from a prompt")
    async def generate(self, ctx: discord.Interaction, prompt: str):
        await generate_diffusion(ctx, prompt)


async def setup(bot):
    print("INFO: Loading [Generate]... ", end="")
    await bot.add_cog(Generate(bot))

    @bot.tree.context_menu(name="generate")
    async def generate(ctx: discord.ext.commands.context.Context, message: discord.message.Message):
        await generate_diffusion(ctx, message.content)

    print("Done!")


def teardown(bot):
    print("INFO: Unloading [Generate]")
