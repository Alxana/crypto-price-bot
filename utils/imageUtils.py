from PIL import Image, ImageDraw


def add_rounded_corners(image, radius):
    # Ensure the image is in RGBA mode
    image = image.convert("RGBA")

    # Create a mask for rounded corners
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)

    # Apply the rounded corner mask
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, mask=mask)
    return rounded_image
