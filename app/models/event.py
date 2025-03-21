from typing import Dict, Any, Optional
from datetime import datetime


class Event:
    """Model representing an email event"""

    def __init__(
            self,
            event_id: str,
            event_type: str,
            customer_id: str,
            source_timestamp: str,
            email_id: str,
            utc_timestamp: datetime,
            clicked_link: Optional[str] = None,
            product_id: Optional[str] = None,
            amount: Optional[float] = None
    ):
        self.event_id = event_id
        self.event_type = event_type
        self.customer_id = customer_id
        self.source_timestamp = source_timestamp
        self.email_id = email_id
        self.utc_timestamp = utc_timestamp
        self.clicked_link = clicked_link
        self.product_id = product_id
        self.amount = amount

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary representation"""
        result = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "customer_id": self.customer_id,
            "source_timestamp": self.source_timestamp,
            "email_id": self.email_id,
            "utc_timestamp": self.utc_timestamp.isoformat()
        }

        # Add optional fields if they exist
        if self.clicked_link:
            result["clicked_link"] = self.clicked_link

        if self.product_id:
            result["product_id"] = self.product_id

        if self.amount is not None:
            result["amount"] = self.amount

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], utc_timestamp: datetime) -> 'Event':
        """Create an Event from a dictionary"""
        return cls(
            event_id=data["event_id"],
            event_type=data["event_type"],
            customer_id=data["customer_id"],
            source_timestamp=data["timestamp"],
            email_id=data["email_id"],
            utc_timestamp=utc_timestamp,
            clicked_link=data.get("clicked_link"),
            product_id=data.get("product_id"),
            amount=data.get("amount")
        )