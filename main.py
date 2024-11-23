"""
Copyright (c) 2024 Oceanlight, MancePants 
in collaboration with TUM (Technical University of Munich)

This code is created for hackathon HackaTUM 2024, and is free to use, modify 
and distribute.

This program is a youtube shorts creator, which uses AI to generate news shorts
which are overlaid over preexisting video clips, to create brainrot shorts to
entertain and inform a younger audience.
"""

import os
import uuid

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
        self.ID = self.title + str(self.uuid)
        # create a directory to store generated media for this short
        os.makedirs(self.uuid)


    def create_short(self, video):
        """
        Required arguments:
        - video: String; Path to video file)
        """

        # Generate text using text_generation class
        text_generator = TextGeneration()
        text_generator.generate_text()

        # Split text into sections
        text_generator.split_text()

        # TODO: create mp3 files for each section
        # TODO: create images of the text to be overlaid for each section
        # TODO: overlay images and mp3 files from each section onto the video


if __name__ == "__main__":
    short = Short("Test Short")
    short.create_short("video.mp4")