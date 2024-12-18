def format_price_update_message(price):
    # Ensure currentPrice and priceChange24 are floats for proper formatting
    currencies_pair = f"{price['symbol']}-{price['convert_to']}"
    current_price = round(float(price['price']), 3)
    price_change_24 = round(float(price['percent_change_24h']), 3)
    price_change_7d = round(float(price['percent_change_7d']), 3)

    # Define the color emoji and trend emoji based on the 7d change
    if price_change_24 < 0:
        change_emoji_24 = "🔴"  # Red circle for negative
    else:
        change_emoji_24 = "🟢"  # Green circle for positive

    # Define the color emoji and trend emoji based on the 7d change
    if price_change_7d < 0:
        change_emoji_7d = "🔴"  # Red circle for negative
    else:
        change_emoji_7d = "🟢"  # Green circle for positive

    # Add + before positive values but keep price_change as a float for formatting
    if price_change_24 > 0:
        price_change_str_24 = f"+{price_change_24:.2f}"  # format with 3 decimal places
    else:
        price_change_str_24 = f"{price_change_24:.2f}"

    # Add + before positive values but keep price_change as a float for formatting
    if price_change_7d > 0:
        price_change_str_7d = f"+{price_change_7d:.2f}"  # format with 3 decimal places
    else:
        price_change_str_7d = f"{price_change_7d:.2f}"

    # Construct the message with Markdown and monospaced font for alignment
    message = (
        f"💰 `{price['symbol']:<4}`: *${current_price:>6}* \n"
        f" *24h:* {price_change_str_24:>4}%  {change_emoji_24}"
        f" *7d:*  {price_change_str_7d:>4}%  {change_emoji_7d}"
    )
    return message
