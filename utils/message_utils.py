def format_price_update_message(price):
    # Ensure currentPrice and priceChange24 are floats for proper formatting
    current_price = float(price['currentPrice'])
    price_change = float(price['priceChange24'])

    # Define the color emoji and trend emoji based on the 24h change
    if price_change < 0:
        change_emoji = "🔴"  # Red circle for negative
        trend_emoji = "📉"   # Graph down
    else:
        change_emoji = "🟢"  # Green circle for positive
        trend_emoji = "📈"   # Graph up

    # Add + before positive values but keep price_change as a float for formatting
    if price_change > 0:
        price_change_str = f"+{price_change:.2f}"  # format with 3 decimal places
    else:
        price_change_str = f"{price_change:.2f}"

    # Construct the message with Markdown and monospaced font for alignment
    message = (
        f"💰 `{price['coin']:<7}` price: *${current_price:>6.4f}*, 24h change: {change_emoji} {price_change_str:>6}% {trend_emoji}"
    )
    return message
