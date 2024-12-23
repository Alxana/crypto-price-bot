import io

from PIL import Image, ImageDraw, ImageFont

def generate_crypto_block(currency, prices):




def generate_price_image(btc_price, btc_change, trx_price, trx_change):
    # Image size and background color
    width, height = 800, 400
    background_color = (10, 25, 50)  # Dark blue

    # Create an empty image
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Fonts (using default font as fallback)
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        price_font = ImageFont.truetype("arial.ttf", 30)
        change_font = ImageFont.truetype("arial.ttf", 25)
    except OSError:
        print("Custom font not found. Using default font.")
        title_font = ImageFont.load_default()
        price_font = ImageFont.load_default()
        change_font = ImageFont.load_default()

    # Title text
    title_text = "Cryptocurrency Prices"
    title_width = draw.textlength(title_text, font=title_font)
    draw.text(((width - title_width) // 2, 20), title_text, fill=(255, 255, 255), font=title_font)

    # BTC section
    btc_x, btc_y = 100, 100
    draw.text((btc_x, btc_y), "Bitcoin (BTC)", fill=(255, 165, 0), font=price_font)
    draw.text((btc_x, btc_y + 50), f"Price: {btc_price}$", fill=(255, 255, 255), font=price_font)

    btc_change_color = (0, 255, 0) if btc_change >= 0 else (255, 0, 0)
    draw.text((btc_x, btc_y + 100), f"Change: {btc_change:+.2f}$", fill=btc_change_color, font=change_font)

    # TRX section
    trx_x, trx_y = 450, 100
    draw.text((trx_x, trx_y), "Tron (TRX)", fill=(0, 191, 255), font=price_font)
    draw.text((trx_x, trx_y + 50), f"Price: {trx_price}$", fill=(255, 255, 255), font=price_font)

    trx_change_color = (0, 255, 0) if trx_change >= 0 else (255, 0, 0)
    draw.text((trx_x, trx_y + 100), f"Change: {trx_change:+.2f}$", fill=trx_change_color, font=change_font)

    # Save image to BytesIO object
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)  # Rewind the BytesIO buffer
    return output


