import unittest
from datetime import datetime
import pytz
from unittest.mock import patch

from app.utils.validators import ValidationError
from app.utils.datetime_utils import normalize_timestamp, parse_date


class TestTimestampNormalization(unittest.TestCase):
    def test_iana_timezone_format(self):
        # Test timestamp with IANA timezone
        result = normalize_timestamp("2023-05-15T14:30:45 Europe/London")
        expected = datetime(2023, 5, 15, 13, 30, 45, tzinfo=pytz.UTC)  # London is UTC+1 in summer
        self.assertEqual(result, expected)

    def test_invalid_iana_timezone(self):
        # Test with invalid IANA timezone
        with self.assertRaises(ValidationError) as context:
            normalize_timestamp("2023-05-15T14:30:45 Invalid/Zone")
        self.assertIn("Invalid IANA timezone", str(context.exception))

    def test_utc_offset_positive(self):
        # Test timestamp with positive UTC offset
        result = normalize_timestamp("2023-05-15T14:30:45 UTC+3")
        expected = datetime(2023, 5, 15, 11, 30, 45, tzinfo=pytz.UTC)  # UTC+3 converted to UTC
        self.assertEqual(result, expected)

    def test_utc_offset_negative(self):
        # Test timestamp with negative UTC offset
        result = normalize_timestamp("2023-05-15T14:30:45 UTC-5")
        expected = datetime(2023, 5, 15, 19, 30, 45, tzinfo=pytz.UTC)  # UTC-5 converted to UTC
        self.assertEqual(result, expected)

    def test_iso_format_with_timezone(self):
        # Test ISO format timestamp with Z (UTC) timezone
        result = normalize_timestamp("2023-05-15T14:30:45Z")
        expected = datetime(2023, 5, 15, 14, 30, 45, tzinfo=pytz.UTC)
        self.assertEqual(result, expected)

    def test_iso_format_with_offset(self):
        # Test ISO format timestamp with +HH:MM offset
        result = normalize_timestamp("2023-05-15T14:30:45+02:00")
        expected = datetime(2023, 5, 15, 12, 30, 45, tzinfo=pytz.UTC)  # +02:00 converted to UTC
        self.assertEqual(result, expected)

    def test_missing_timezone_info(self):
        # Test timestamp missing timezone information
        with self.assertRaises(ValidationError) as context:
            normalize_timestamp("2023-05-15T14:30:45")
        self.assertIn("missing timezone information", str(context.exception))

    def test_invalid_timestamp_format(self):
        # Test completely invalid timestamp
        with self.assertRaises(ValidationError) as context:
            normalize_timestamp("not-a-timestamp")
        self.assertIn("Invalid timestamp format", str(context.exception))

    def test_edge_cases(self):
        # Test leap year
        result = normalize_timestamp("2024-02-29T00:00:00Z")
        expected = datetime(2024, 2, 29, 0, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(result, expected)

        # Test DST transition (this depends on the timezone and might need adjustment)
        with patch('pytz.timezone') as mock_timezone:
            mock_tz = mock_timezone.return_value
            mock_tz.localize.return_value = datetime(2023, 3, 26, 2, 30, 0, tzinfo=pytz.UTC)
            result = normalize_timestamp("2023-03-26T02:30:00 Europe/Berlin")
            self.assertEqual(result.tzinfo, pytz.UTC)

class TestParseDate(unittest.TestCase):
    def test_date_with_timezone(self):
        # Test date with timezone
        result = parse_date("2023-05-15T14:30:45+02:00")
        expected = datetime(2023, 5, 15, 12, 30, 45, tzinfo=pytz.UTC)
        self.assertEqual(result, expected)

    def test_date_without_timezone(self):
        # Test date without timezone (should assume UTC)
        result = parse_date("2023-05-15T14:30:45")
        expected = datetime(2023, 5, 15, 14, 30, 45, tzinfo=pytz.UTC)
        self.assertEqual(result, expected)

    def test_date_only(self):
        # Test with just a date (no time)
        result = parse_date("2023-05-15")
        expected = datetime(2023, 5, 15, 0, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(result, expected)

    def test_natural_language_date(self):
        # Test natural language date parsing
        with patch('dateutil.parser.parse') as mock_parse:
            mock_parse.return_value = datetime(2023, 5, 15, 0, 0, 0)
            result = parse_date("May 15, 2023")
            # We can only check that tzinfo is set correctly since the actual parsing is mocked
            self.assertEqual(result.tzinfo, pytz.UTC)

    def test_invalid_date(self):
        # Test invalid date format
        with self.assertRaises(ValidationError) as context:
            parse_date("not-a-date")
        self.assertIn("Invalid date format", str(context.exception))
