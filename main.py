"""
Copyright (c) 2024 Oceanlight, MancePants 
in collaboration with TUM (Technical University of Munich)

This code is created for hackathon HackaTUM 2024, and is free to use, modify 
and distribute.

This program is a youtube shorts creator, which uses AI to generate news shorts
which are overlaid over preexisting video clips, to create brainrot shorts to
entertain and inform a younger audience.
"""

import logging
import os
import uuid

from image_generation import ImageGeneration
from text_generation import *


class Short:
    def __init__(self, title=""):
        """
        Construct a new Short instance.

        Optional arguments:
        - title: String; A title for the short
        """

        # assert that title is less than 100 characters long
        if len(title) > 100:
            raise ValueError("Title must be less than 100 characters long")

        self.title = title

        # create a unique uuid for each short (avoid overwriting other short's files)
        self.uuid = str(uuid.uuid4())
        self.directory = self.title + '_' + str(self.uuid)
        # create a directory to store generated media for this short
        os.makedirs(self.directory)


    def create_short(self, video):
        """
        Required arguments:
        - video: String; Path to video file)
        """

        # Generate text using text_generation class
        text_generator = TextGeneration()
        text_generator.generate_text()

        # Split text into sections
        text_generator.split_text(length=35)
        print(text_generator.splitted_text)

        # TODO: create mp3 files for each section
        # TODO: create images of the text to be overlaid for each section
        font_url = "https://github.com/shipfam/shipfam.com/blob/master/fonts/segoe-ui.ttf?raw=true"  # Example font URL
        font_path = "fonts/NotoSansSC-Regular.otf"
        font_size = 30
        image_size = (800, 400)
        image_generator = ImageGeneration(font_url, font_size, image_size)
        for i in range(len(text_generator.splitted_text)):
            text = text_generator.splitted_text[i]
            output_file = self.directory + "/" + str(i) + ".png"
            image_generator.create_transparent_image_with_text([text], output_file)

        # TODO: create video clip from video
        # TODO: overlay images and mp3 files from each section onto the video


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    short = Short("Test Short")
    short.create_short("video.mp4")