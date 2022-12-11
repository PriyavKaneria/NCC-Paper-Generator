# IMPORTS
import os
import pyvips
import textwrap
from PIL import *
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random


def generateImageFromText(text: str, width, height):
    rendered_text, feedback = pyvips.Image.text(text,
                                                font='Akshar', fontfile='Akshar-Unicode.ttf',
                                                width=width, height=height,
                                                autofit_dpi=True)
    # rendered_text = rendered_text.gravity('centre', 1500, 1500)
    image = rendered_text.new_from_image([0, 0, 0]).bandjoin(rendered_text)
    # image.write_to_file(f'{random.random()}.png')
    pil_image = Image.fromarray(image.numpy())
    return pil_image

# GENERATE OUTPUT 1


# text = "परिस्थितियां विपरीत हो तो कुछ लोग टूट जाते हैं, और कुछ लोग रिकॉर्ड तोड़ देते हैं..!!"
# bgoutput('new', text)
