import torch

from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionInpaintPipeline


DEVICE = "cuda"
MODEL = "runwayml/stable-diffusion-v1-5"
INPAINTING_MODEL = "runwayml/stable-diffusion-inpainting"


def txt2img(prompt):
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL, torch_dtype=torch.float16)
    pipe = pipe.to(DEVICE)

    images = pipe(prompt)

    return images.images[0]


def img2img(prompt, init_image, mask_image=None):
    init_image = init_image.convert("RGB").resize((512, 512))

    if mask_image:
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            INPAINTING_MODEL, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")

        mask_image = mask_image.convert("1").resize(
            (512, 512)) if mask_image else None
        images = pipe(prompt=prompt, image=init_image,
                      mask_image=mask_image).images

    else:
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            MODEL, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")

        images = pipe(prompt=prompt, image=init_image).images

    return images[0]
