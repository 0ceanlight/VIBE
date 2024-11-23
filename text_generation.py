import re

from openai import AzureOpenAI

class TextGeneration:
    """
    A class for generating text. Uses openAI to generate news text for shorts based on given RSS feeds.
    """
    def __init__(self):

        self.full_text = ""
        self.splitted_text = []
        self.tags = []

    def generate_text(self):
        # TODO: only for example/placeholder purposes. to be replaced with openAI generated text
        self.full_text = """🚨 GM’s self-driving unit Cruise is in hot water! They admitted to filing a false report about a robotaxi accident that dragged a pedestrian. Now? A $500K fine and a 3-year agreement to clean up their act. 😬

The fallout? Top execs resigned, 25% of the workforce cut, and stricter rules from the feds. Oh, and an $8M settlement with the victim.

Cruise is rebooting, ditching some vehicles, and promising transparency—but regulators are still watching. Will they make a comeback or crash out of the race? Stay tuned! 🚗💥"""

        self.tags = ['#GM', '#Cruise', '#SelfDrivingCars', '#AutonomousVehicles', '#Robotaxi', '#TechNews', '#TrafficSafety', '#NHTSA', '#AI', '#Transportation', '#FutureOfMobility', '#TechScandal', '#RoadSafety', '#Innovation', '#SmartCar']


    def split_text(self, regex=r'\.', length=None, preserve_split_chars=False):
        """
        Splits the full text into a list of sentences by default. Optionally specify regex to split on example: r'[-.]' splits on dashes and dots, or length to split after.

        Splits first on separator characters (which removes them), then on length.

        Resets self.split_text

        Optional arguments:
        - regex: String; A regex pattern to split on
        - length: Integer; A maximum length for each section
        - preserve_split_chars: Boolean; Whether to keep split characters
        """
        
        # assert text not empty
        if not self.full_text or len(self.full_text) == 0:
            raise ValueError("Text must not be empty")

        self.splitted_text = []

        # Part 1: Split on given characters / regex
        char_splits = []

        if preserve_split_chars:
            # Capture the split characters by surrounding the pattern with parentheses
            split_pattern = f"(?<={regex})"
        else:
            split_pattern = regex

        # Use re.split to split the text
        char_splits = re.split(split_pattern, self.full_text)
        char_splits = [split for split in char_splits if split] 

        # Part 2: Split on length, don't split words apart
        if not length:
            # skip the length splitting
            self.splitted_text = char_splits
        else:
            for text_section in char_splits:
                # Splits text into smaller sections of a specified maximum length,
                # ensuring no words are split.
                words = text_section.split()
                sections = []
                current_section = []

                for word in words:
                    # Check if adding the word exceeds the max_length
                    if len(" ".join(current_section + [word])) <= length:
                        current_section.append(word)
                    else:
                        # If it would exceed, add the current section to sections
                        sections.append(" ".join(current_section))
                        # Start a new section with the current word
                        current_section = [word]

                # Add the last section
                if current_section:
                    sections.append(" ".join(current_section))

                self.splitted_text.extend(sections)

        # Part 3: Remove leading or trailing whitespace
        self.splitted_text = [section.strip() for section in self.splitted_text]
        return self.splitted_text

    # Note: There are no getters or setters for a reason: I dislike them. Just
    # access the variables directly and don't complainin :)
    
# TODO: remove test cases
# main function to test the split text function
if __name__ == "__main__":
    # Create a longer sample text
    sample_text = "This is a sample text. It is long enough to split into multiple sections."
    print(f'Sample text: {sample_text}')

    # Create an instance of the text_generation class
    text_generator = text_generation()

    # Set the text to be split
    text_generator.full_text = sample_text

    # Split the text into sections
    split_args = {
        'regex': r'[.]',
        'length': 25,
        'preserve_split_chars': False
    }
    print(f'split args: {split_args}')
    sections = text_generator.split_text(**split_args)

    # assert sections == ['This is a sample text', 'It is long enough to', 'split into multiple', 'sections']

    print(f'split text: {sections}')