from datetime import datetime
from dateutil import parser
import pytz
import re
from app.utils.validators import ValidationError


def normalize_timestamp(timestamp_str: str) -> datetime:

    try:
        # Check if timestamp contains IANA timezone (e.g., Europe/Bucharest)
        iana_pattern = r'([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})\s+([A-Za-z]+/[A-Za-z_]+)'
        iana_match = re.match(iana_pattern, timestamp_str)

        if iana_match:
            # Extract datetime and timezone parts
            dt_part = iana_match.group(1)
            tz_part = iana_match.group(2)

            # Check if the timezone is valid
            if tz_part not in pytz.all_timezones:
                raise ValidationError(f"Invalid IANA timezone: {tz_part}")

            # Parse the datetime part
            dt = datetime.fromisoformat(dt_part)

            # Apply the timezone
            local_tz = pytz.timezone(tz_part)
            dt = local_tz.localize(dt)

            # Convert to UTC
            return dt.astimezone(pytz.UTC)

        # Check if timestamp contains UTC offset format (e.g., UTC+3, UTC-5)
        utc_pattern = r'([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})\s+UTC([+-][0-9]+)'
        utc_match = re.match(utc_pattern, timestamp_str)

        if utc_match:
            # Extract datetime and offset parts
            dt_part = utc_match.group(1)
            offset_part = utc_match.group(2)

            # Convert offset to hours
            offset_hours = int(offset_part)

            # Parse the datetime part
            dt = datetime.fromisoformat(dt_part)

            # Apply the offset
            tzinfo = pytz.FixedOffset(offset_hours * 60)  # Convert hours to minutes
            dt = dt.replace(tzinfo=tzinfo)

            # Convert to UTC
            return dt.astimezone(pytz.UTC)

        # For other formats, try dateutil parser
        dt = parser.parse(timestamp_str)

        # Ensure timezone information is present
        if dt.tzinfo is None:
            raise ValidationError(f"Timestamp missing timezone information: {timestamp_str}")

        # Convert to UTC
        return dt.astimezone(pytz.UTC)

    except (ValueError, OverflowError) as e:
        raise ValidationError(f"Invalid timestamp format: {timestamp_str} - {str(e)}")


def parse_date(date_str: str) -> datetime:
    """Parse a date string to UTC datetime"""
    try:
        dt = parser.parse(date_str)
        if dt.tzinfo is None:
            # Assume UTC if no timezone specified
            dt = dt.replace(tzinfo=pytz.UTC)
        else:
            # Convert to UTC if timezone provided
            dt = dt.astimezone(pytz.UTC)
        return dt
    except ValueError:
        raise ValidationError(f"Invalid date format: {date_str}")