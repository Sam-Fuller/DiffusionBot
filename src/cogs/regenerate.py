import discord
import stable_diffusion

import requests
from PIL import Image
from io import BytesIO


async def regenerate_diffusion(ctx: discord.Interaction, prompt: str, init_image, mask_image=None):
    print(f"regenerating \"{prompt}\"")
    await ctx.response.send_message(f"regenerating \"{prompt}\", this will take 30-60 seconds", ephemeral=True)

    image = stable_diffusion.img2img(prompt, init_image, mask_image)
    image.save("image.png")

    embed = discord.Embed(title=prompt)
    embed.set_image(url='attachment://image.png')

    await ctx.channel.send(embed=embed, file=discord.File("image.png"))


async def setup(bot):
    print("INFO: Loading [Regenerate]... ", end="")

    @bot.tree.context_menu(name="regenerate")
    async def regenerate(ctx: discord.ext.commands.context.Context, message: discord.message.Message):
        prompt = message.embeds[0].title if message.embeds else message.content

        init_url = message.embeds[0].image.url if message.embeds else message.attachments[0].url
        init_response = requests.get(init_url)
        init_image = Image.open(BytesIO(init_response.content))

        mask_image = None
        if (message.embeds and len(message.embeds) > 1 or message.attachments and len(message.attachments) > 1):
            mask_url = message.embeds[1].image.url if message.embeds else message.attachments[1].url
            mask_response = requests.get(mask_url)
            mask_image = Image.open(BytesIO(mask_response.content))

        await regenerate_diffusion(ctx, prompt, init_image, mask_image)

    print("Done!")


def teardown(bot):
    print("INFO: Unloading [Regenerate]")
