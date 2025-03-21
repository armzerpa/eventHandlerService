from typing import Dict, List, Any, Optional
from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.utils.validators import validate_event, validate_uuid
from app.utils.datetime_utils import normalize_timestamp, parse_date
from app.utils.validators import ValidationError


class EventService:
    """Service for handling event operations"""

    def __init__(self):
        self.repository = EventRepository()

    def process_event(self, event_data: Dict[str, Any]) -> None:
        """Process an incoming event"""
        # Validate the event
        validate_event(event_data)

        # Normalize the timestamp
        normalized_timestamp = normalize_timestamp(event_data["timestamp"])

        # Create an event object
        event = Event.from_dict(event_data, normalized_timestamp)

        # Store the event
        self.repository.add(event)

    def get_filtered_events(
            self,
            customer_id: Optional[str] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get events filtered by customer_id and date range"""
        # Validate customer_id if provided
        if customer_id:
            validate_uuid(customer_id, "customer_id")

        # Parse dates if provided
        start_datetime = parse_date(start_date) if start_date else None
        end_datetime = parse_date(end_date) if end_date else None

        # Get filtered events from repository
        filtered_events = self.repository.find_by_customer_and_date_range(
            customer_id=customer_id,
            start_date=start_datetime,
            end_date=end_datetime
        )

        # Convert events to dictionaries
        return [event.to_dict() for event in filtered_events]