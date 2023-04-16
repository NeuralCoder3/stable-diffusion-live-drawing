import webuiapi
import os
import time
from pathlib import Path
from psd_tools import PSDImage
from PIL import Image
import IPython
import IPython.display
import argparse

parser = argparse.ArgumentParser(description='Automatically runs stable diffusion on an image.')
parser.add_argument('-i', '--input', dest='input', type=str, default='base.kra', help='Input file name')
parser.add_argument('-o', '--output', dest='output', type=str, default='out.png', help='Output file name')
parser.add_argument('--steps', dest='steps', type=int, default=20, help='Number of steps')
parser.add_argument('--image-steps', dest='image_steps', type=int, default=40, help='Number of image steps')
parser.add_argument('-p', '--prompt', dest='prompt', type=str, default='prompt.txt', help='Prompt file name')
parser.add_argument('-n', '--negative-prompt', dest='negative_prompt', type=str, default='negative.txt', help='Negative prompt file name')
parser.add_argument('-d', '--denoising-strength', dest='denoising_strength', type=float, default=0.55, help='Denoising strength')
parser.add_argument('-s', '--seed', dest='seed', type=int, default=515553, help='Seed')
parser.add_argument('-c', '--cfg-scale', dest='cfg_scale', type=int, default=7, help='Scale')
parser.add_argument('--sampler', dest='sampler', type=str, default='Euler a', help='Sampler')

args = parser.parse_args()

def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        elif shell == 'TerminalInteractiveShell':
            return False
        else:
            return False
    except NameError:
        return False

# create API client
try:
    api = webuiapi.WebUIApi(sampler=args.sampler, steps=args.steps)
    api.util_wait_for_ready()
except:
    print("Please start the webui server with the api switch first.")
    exit(1)

# if api.get_endpoint() is None:
#     print("Please start the webui server with the api switch first.")
#     exit(1)

jupyter = is_notebook()
save_image = True
display_image = jupyter

# if not jupyter and feh installed:
if not jupyter and os.system("which feh") == 0:
    os.system("feh --reload 0.2 out.png &")

file_base = args.input
format = file_base.split(".")[-1]
def open_image(path=file_base, format=format):
    if format == "kra":
        os.system(f"./kra2png.sh {path} tmp.png")
        path = "tmp.png"
    elif format == "psd":
        psd = PSDImage.open(path)
        return psd.composite()
    return Image.open(path)
    
file_prompt = args.prompt
negative_file_prompt = args.negative_prompt
f_base_new = 0
f_prompt_new = 0

while True:
    f_base = os.path.getmtime(file_base)
    f_prompt = os.path.getmtime(file_prompt)
    if f_base == f_base_new and f_prompt == f_prompt_new:
        time.sleep(0.5)
    else:
        f_base_new = f_base
        f_prompt_new = f_prompt
        prompt_txt = Path(file_prompt).read_text()
        negative_prompt_txt = Path(file_prompt).read_text()

        im = open_image()
        if im is None:
            continue
        width, height = im.size
        result2 = api.img2img(
            images=[im],
            prompt=prompt_txt,
            negative_prompt=negative_prompt_txt,
            steps=args.image_steps,
            styles=[],
            seed=args.seed,
            cfg_scale=args.cfg_scale,
            width=width,
            height=height,
            denoising_strength=args.denoising_strength)
        if jupyter and display_image:
            IPython.display.clear_output(wait=False)
        img = result2.image
        if display_image:
            display(img)
        img.save(args.output)
