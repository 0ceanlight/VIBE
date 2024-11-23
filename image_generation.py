from PIL import Image, ImageDraw, ImageFont
import textwrap

# TODO: actually wrap the text
# TODO: center the text
# TODO: add emojis

def create_text_image(text, width, height, padding=20, output_path='output.png'):
    """
    Creates a transparent image with specified width and height,
    and displays the given text centered in the image with optional padding and multi-line wrapping.

    :param text: The text to display (supports emojis)
    :param width: Width of the image
    :param height: Height of the image
    :param padding: Padding around the text
    :param output_path: Path to save the output image
    """
    # Create a transparent image
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    
    # Prepare to draw on the image
    draw = ImageDraw.Draw(image)
    
    # Load a font that supports emojis (macOS uses Apple Color Emoji font)
    try:
        font_path = "SFNS.ttf"  # macOS system font
        # TODO: make this work
        # font_path = "AppleColorEmoji.ttf"
        font = ImageFont.truetype(font_path, size=24)  # Adjust font size as needed
    except IOError:
        raise Exception("Font file not found. Install a font that supports emojis.")
    
    # Wrap text into multiple lines if it exceeds the image width
    wrapper = textwrap.TextWrapper(width=width - 2 * padding)  # Leave padding space on both sides
    wrapped_text = wrapper.fill(text=text)
    
    # Get the size of the wrapped text
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]  # width = right - left
    text_height = bbox[3] - bbox[1] # height = bottom - top
    
    # Calculate position to center the text (including padding)
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Add padding to the top-left position
    x += padding
    y += padding
    
    # Draw the wrapped text on the transparent image
    draw.text((x, y), wrapped_text, fill="black", font=font)
    
    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage
if __name__ == "__main__":
    text = "Will they make a comeback or crash out of the race? Stay tuned! 🚗💥"
    width = 800
    height = 400
    padding = 40  # You can change the padding to adjust space around the text
    output_file = "output.png"
    create_text_image(text, width, height, padding, output_file)
