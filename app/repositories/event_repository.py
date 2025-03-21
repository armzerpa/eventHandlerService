from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.event import Event


class EventRepository:
    """Repository for storing and retrieving events"""

    def __init__(self):
        # In-memory storage
        self._events = []

    def add(self, event: Event) -> None:
        """Add an event to the repository"""
        self._events.append(event)

    def find_by_customer_id(self, customer_id: str) -> List[Event]:
        """Find events by customer ID"""
        return [e for e in self._events if e.customer_id == customer_id]

    def find_by_date_range(self, start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Event]:
        """Find events within a date range"""
        filtered_events = self._events

        if start_date:
            filtered_events = [e for e in filtered_events if e.utc_timestamp >= start_date]

        if end_date:
            filtered_events = [e for e in filtered_events if e.utc_timestamp <= end_date]

        return filtered_events

    def find_by_customer_and_date_range(
            self,
            customer_id: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[Event]:
        """Find events by customer ID and date range"""
        filtered_events = self._events

        if customer_id:
            filtered_events = [e for e in filtered_events if e.customer_id == customer_id]

        if start_date:
            filtered_events = [e for e in filtered_events if e.utc_timestamp >= start_date]

        if end_date:
            filtered_events = [e for e in filtered_events if e.utc_timestamp <= end_date]

        return filtered_events