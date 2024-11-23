from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO


class ImageGeneration:
    """
    A class for generating transparent images with given text snippets on multiple lines.
    """
    def __init__(self, font_url, font_size, image_size):
        """
        Arguments:
        - param font_url: String; URL to the font file to be used.
        - param font_size: Integer; Size of the font.
        - param image_size: Tuple specifying the size of the image (width, height).
        """
        self.font_size = font_size
        self.image_size = image_size

        try:
            # Fetch the font file from the URL
            response = requests.get(font_url)
            response.raise_for_status()
            font_data = BytesIO(response.content)
            
            # Load the font
            self.font = ImageFont.truetype(font_data, self.font_size)
            
        except requests.RequestException as e:
            print(f"Failed to fetch font: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise(e)

    def create_transparent_image_with_text(self, text_array, output_file):
        """
        Creates a transparent PNG image with centered text.

        - param text_array: [String]; Text to be displayed on the image.
        - param output_file: Name of the output file (e.g., 'output.png').
        """
        try:
            # IMAGE CREATION ------------------------------------------------------
            # Create a transparent image
            image = Image.new("RGBA", self.image_size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)

            def add_text(image, draw, text, font, text_x, text_y):
                # SHADOW LAYER --------------------------------------------------------
                # Create a separate layer for the shadow
                shadow_layer = Image.new("RGBA", self.image_size, (255, 255, 255, 0))
                shadow_draw = ImageDraw.Draw(shadow_layer)

                # Draw the shadow (black) onto the shadow layer
                shadow_offset = 0  # Offset for the shadow
                shadow_draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=(0, 0, 0, 255)) # Black????

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
                image = Image.alpha_composite(image, shadow_layer)
                
                # TEXT LAYER ----------------------------------------------------------
                # Draw the text
                draw = ImageDraw.Draw(image)
                draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))  # White text with full opacity

                return image
            
            for i in range(len(text_array)):
                text = text_array[i]
                # Calculate text size and position
                text_width = draw.textlength(text, font=self.font)
                text_height = text_width
                text_x = (self.image_size[0] - text_width) // 2
                text_y = (self.image_size[1] - text_height) // 2

                image = add_text(image, draw, text, self.font, text_x, text_y + i * self.font_size)

            # Save the image
            image.save(output_file, "PNG")
            print(f"Image saved as {output_file}")
        
        except requests.RequestException as e:
            print(f"Failed to fetch font: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise(e)

if __name__ == "__main__":
    # Example usage
    text = ["Hello, World!", "testytest"]
    font_url = "https://github.com/shipfam/shipfam.com/blob/master/fonts/segoe-ui.ttf?raw=true"  # Example font URL
    # font_url = "https://github.com/samuelngs/apple-emoji-linux/releases/latest/download/AppleColorEmoji.ttf"  # No workies
    font_size = 50
    image_size = (800, 400)
    output_file = "output.png"

    # Initialize the ImageGeneration class
    image_generator = ImageGeneration(font_url, font_size, image_size)

    # Call the create_transparent_image_with_text method
    image_generator.create_transparent_image_with_text(text, output_file)
