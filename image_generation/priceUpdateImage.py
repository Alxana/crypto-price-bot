import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from utils.imageUtils import add_rounded_corners
from utils.price_utils import format_price
from utils.date_utils import get_current_date_or_time

# Colors
black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 0, 0)
green_color = (0, 128, 0)
cobalt_blue_color = (0, 18, 69)

font_path_med = "resources/fonts/Poppins-Medium.ttf"
font_path_bold = "resources/fonts/Poppins-Bold.ttf"
font_path_regular = "resources/fonts/Poppins-Regular.ttf"
font_path_light = "resources/fonts/Poppins-Light.ttf"
font_path_thin = "resources/fonts/Poppins-Thin.ttf"


def generate_crypto_block(prices):
    # Paths
    bg_path = "resources/images/crypto_block_bg_800x796.png"
    logo_path = f"resources/images/crypto_logos/{prices['symbol'].lower()}_logo.png"

    # Coordinates
    logo_coordinates = (40, 40)
    title_coordinates = (520, 148)
    price_coordinates = (400, 390)
    price_change_24_coordinates = (531.5, 592)
    price_change_7d_coordinates = (531.5, 714)

    # Texts
    title_text = prices['symbol']
    curr_price_text = f"$ {format_price(prices['price'])}"
    price_change_24 = round(float(prices['percent_change_24h']), 2)
    if price_change_24 > 0:
        price_change_24_text = f"+{price_change_24}%"
        price_change_24_color = green_color
    else:
        price_change_24_text = f"{price_change_24}%"
        price_change_24_color = red_color

    price_change_7d = round(float(prices['percent_change_7d']), 2)
    if price_change_7d > 0:
        price_change_7d_text = f"+{price_change_7d}%"
        price_change_7d_color = green_color
    else:
        price_change_7d_text = f"{price_change_7d}%"
        price_change_7d_color = red_color

    bg = Image.open(bg_path)
    logo = Image.open(logo_path)
    logo = logo.resize((216, 216))
    bg.paste(logo, logo_coordinates, logo)
    draw_block = ImageDraw.Draw(bg)

    # fonts (using default font as fallback)
    try:
        title_font = ImageFont.truetype(font_path_med, 150)
        price_font = ImageFont.truetype(font_path_bold, 110)
        change_font = ImageFont.truetype(font_path_med, 88.1)
    except OSError:
        print("Custom font not found. Using default font.")
        title_font = ImageFont.load_default()
        price_font = ImageFont.load_default()
        change_font = ImageFont.load_default()

    draw_block.text(title_coordinates, title_text,
                    font=title_font, fill=cobalt_blue_color, anchor='mm', stroke_width=1, stroke_fill=white_color)
    draw_block.text(price_coordinates, curr_price_text,
                    font=price_font, fill=black_color, anchor='mm', stroke_width=1, stroke_fill=white_color)
    draw_block.text(price_change_24_coordinates, price_change_24_text,
                    font=change_font, fill=price_change_24_color, anchor='mb', stroke_width=1, stroke_fill=white_color)
    draw_block.text(price_change_7d_coordinates, price_change_7d_text,
                    font=change_font, fill=price_change_7d_color, anchor='mb', stroke_width=1, stroke_fill=white_color)

    block_image = bg.resize((200, 200), resample=Image.Resampling.LANCZOS)

    # Ensure the resized image has an alpha channel
    if block_image.mode != "RGBA":
        block_image = block_image.convert("RGBA")

    return add_rounded_corners(block_image, 30)


def generate_price_update_image(prices):
    bg_path_6_blocks = "resources/images/bg_3blocks_640x555.png"
    bg = Image.open(bg_path_6_blocks)
    title_font = ImageFont.truetype(font_path_light, 30)
    version_font = ImageFont.truetype(font_path_light, 18)
    date_coordinates = (85, 37)
    time_coordinates = (620, 37)
    block_coordinates = [(10, 80), (220, 80), (430, 80), (10, 290), (220, 290), (430, 290)]
    version_coordinates = (10, 545)

    for index, currency in enumerate(prices):
        block = generate_crypto_block(currency)
        bg.paste(block, block_coordinates[index], block)

    dashboard_img = ImageDraw.Draw(bg)

    # Get the current date and time
    current_date = get_current_date_or_time("UTC+1", "%d %B %Y")
    current_time = get_current_date_or_time("UTC+1", "%H:%M")

    dashboard_img.text(date_coordinates, current_date,
                       font=title_font, fill=white_color, anchor='lm')
    dashboard_img.text(time_coordinates, current_time,
                       font=title_font, fill=white_color, anchor='rm')
    dashboard_img.text(version_coordinates, "v1.1",
                       font=version_font, fill=white_color, anchor='lb')

    ImageDraw.Draw(bg)

    # Save the Pillow image to an in-memory file-like object
    final_image = io.BytesIO()
    bg.save(final_image, format="PNG")
    final_image.seek(0)

    return final_image
