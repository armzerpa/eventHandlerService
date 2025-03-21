import uuid
from typing import Dict, Any


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_uuid(value: str, field_name: str) -> None:
    """Validate if a string is a valid UUID"""
    try:
        uuid.UUID(value)
    except ValueError:
        raise ValidationError(f"Invalid UUID format for {field_name}: {value}")


def validate_event(event: Dict[str, Any]) -> None:
    """Validate event data based on event type"""
    required_fields = ["event_id", "event_type", "customer_id", "timestamp", "email_id"]

    # Check required fields
    for field in required_fields:
        if field not in event:
            raise ValidationError(f"Missing required field: {field}")

    # Validate UUIDs
    validate_uuid(event["event_id"], "event_id")
    validate_uuid(event["customer_id"], "customer_id")
    validate_uuid(event["email_id"], "email_id")

    # Validate event_type
    valid_event_types = ["email_open", "email_unsubscribe", "email_click", "purchase"]
    if event["event_type"] not in valid_event_types:
        raise ValidationError(f"Invalid event_type: {event['event_type']}")

    # Additional validation based on event_type
    if event["event_type"] == "email_click" and "clicked_link" not in event:
        raise ValidationError("Missing clicked_link for email_click event")

    if event["event_type"] == "purchase":
        if "product_id" not in event:
            raise ValidationError("Missing product_id for purchase event")
        if "amount" not in event:
            raise ValidationError("Missing amount for purchase event")
        validate_uuid(event["product_id"], "product_id")

        # Validate amount is a number
        if not isinstance(event["amount"], (int, float)):
            raise ValidationError(f"Amount must be a number, got: {type(event['amount'])}")