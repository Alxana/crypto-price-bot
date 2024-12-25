from datetime import datetime
import pytz


def get_timezone_from_offset(offset):
    # Map user input to a valid pytz time zone
    return parse_utc_offset(offset)  # Default to UTC if not found


def parse_utc_offset(offset):
    # Parse strings like "UTC+1" or "UTC-5"
    if not offset.startswith("UTC"):
        raise ValueError("Invalid format. Expected 'UTC+X' or 'UTC-X'.")

    sign = 1 if "+" in offset else -1
    hours = int(offset.split("+")[-1] if "+" in offset else offset.split("-")[-1])
    return pytz.FixedOffset(sign * hours * 60)


def get_current_date_or_time(timezone_name, date_time_format):
    # Define the time zone
    timezone = get_timezone_from_offset(timezone_name)  # UTC+1 (Amsterdam as an example)
    # Get the current time in UTC
    utc_time = datetime.now(pytz.utc)
    # Convert UTC time to the desired time zone
    local_time = utc_time.astimezone(timezone)

    return local_time.strftime(date_time_format)
