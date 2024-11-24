# from PIL import Image, ImageDraw, ImageFont, ImageFilter
from PIL import Image, ImageFont, ImageFilter
import requests
import logging
from io import BytesIO

# TODO: use pilmoji?
from pilmoji import Pilmoji

class ImageGeneration:
    """
    A class for generating transparent images with given text snippets on multiple lines.
    """
    def __init__(self, font_path, font_size, image_size):
        """
        Arguments:
        - param font_path: String; URL or path to the font file to be used.
        - param font_size: Integer; Size of the font.
        - param image_size: Tuple specifying the size of the image (width, height).
        """
        self.font_size = font_size
        self.image_size = image_size

        try:
            if font_path.startswith("http://") or font_path.startswith("https://"):
                # Fetch the font file from the URL
                response = requests.get(font_path)
                response.raise_for_status()
                font_data = BytesIO(response.content)
            else:
                # Use the local font file
                font_data = font_path
            
            # Load the font
            self.font = ImageFont.truetype(font_data, self.font_size)
            
        except requests.RequestException as e:
            logging.error(f"Failed to fetch font: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise(e)

    def create_transparent_image_with_text(self, text_array, output_file):
        """
        Creates a transparent PNG image with centered text.

        - param text_array: [String]; Text to be displayed on the image.
        - param output_file: Name of the output file (e.g., 'output.png').
        """
        assert len(text_array) <= 3

        def new_image():
            logging.info(f"Creating image with size {self.image_size}")
            image = Image.new("RGBA", self.image_size, (255, 255, 255, 0))
            draw = Pilmoji(image)
            return image, draw

        def add_text(image, draw, text, font, text_x, text_y):
            # IMAGE CREATION ------------------------------------------------------

            # TEXT LAYER ----------------------------------------------------------
            # New layer so we don't mess up existing image
            text_layer, text_layer_draw = new_image()
            # Draw the text
            logging.info(f"Drawing text at {text_x}, {text_y}")
            # See pilmoji README: https://github.com/jay3332/pilmoji
            # Adjust emoji scale and offset as needed for specific font
            text_layer_draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255), embedded_color=True, emoji_scale_factor=1.01, emoji_position_offset=(0, 10))

            # SHADOW LAYER --------------------------------------------------------
            # Create a separate layer for the shadow
            shadow_layer = text_layer.copy()

            # Apply Gaussian blur to the shadow layer
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(3))  # Adjust the blur radius as needed

            # Convert the blurred layer to ensure all colors are black while retaining alpha
            def make_black_with_alpha(image):
                # intensity to scale alpha up by
                intensity = 2.0
                r, g, b, a = image.split()
                # Replace RGB with black (0, 0, 0), keep alpha channel
                return Image.merge("RGBA", (r.point(lambda _: 0), g.point(lambda _: 0), b.point(lambda _: 0), a.point(lambda x: x * intensity)))
            
            shadow_layer = make_black_with_alpha(shadow_layer)

            # Paste the shadow layer onto the main image
            new_layer = Image.alpha_composite(shadow_layer, text_layer)
            image = Image.alpha_composite(image, new_layer)
            
            return image

        # Create a transparent image
        image, draw = new_image()
        
        for i in range(len(text_array)):
            text = text_array[i]
            # Calculate text size and position
            print(draw.getsize(text, font=self.font))
            text_width = draw.getsize(text, font=self.font)[0]
            text_height = draw.getsize(text, font=self.font)[1]
            text_x = (self.image_size[0] - text_width) // 2
            text_y = (self.image_size[1] - text_height) // 2

            image = add_text(image, draw, text, self.font, text_x, text_y + i * self.font_size)

        # Save the image
        image.save(output_file, "PNG")
        print(f"Image saved as {output_file}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Example usage
    text = ["Hello, World!❤️💥", "testytest"]

    fonts = {
        "segoeui": ["https://github.com/shipfam/shipfam.com/blob/master/fonts/segoe-ui.ttf?raw=true", 50],
        "segoeui-loc": ["fonts/segoe-ui.ttf", 50],
        # why we use size 109: https://github.com/python-pillow/Pillow/issues/6166
        "notoemoji": ["https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf", 109],
        # why we use size 137
        "appleemoji": ["https://github.com/samuelngs/apple-emoji-linux/releases/latest/download/AppleColorEmoji.ttf", 137],
        "appleemoji-loc": ["fonts/AppleColorEmoji.ttf", 137],
        # has text and emoji, size doesn't matter
        "notosans": ["https://github.com/kartotherian/osm-bright.fonts/blob/master/fonts/NotoSansSC-Regular.otf?raw=true", 40],
        "notosans-loc": ["fonts/NotoSansSC-Regular.otf", 40]
    }

    font_size = 109
    image_size = (800, 400)
    output_file = "output.png"
    font = "notosans-loc"

    # Initialize the ImageGeneration class
    image_generator = ImageGeneration(fonts[font][0], fonts[font][1], image_size)

    # Call the create_transparent_image_with_text method
    image_generator.create_transparent_image_with_text(text, output_file)
