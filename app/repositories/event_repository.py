from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.event import Event
from app import mongo
from pymongo.collection import Collection


class EventRepository:
    """Repository for storing and retrieving events from MongoDB"""

    def __init__(self):
        # Get the events collection from MongoDB
        self.collection: Collection = mongo.db.events

        # Create indexes for better query performance
        self._create_indexes()

    def _create_indexes(self) -> None:
        """Create necessary indexes for efficient querying"""
        # Index for customer_id lookups
        self.collection.create_index("customer_id")

        # Index for timestamp-based queries
        self.collection.create_index("utc_timestamp")

        # Compound index for customer+timestamp queries
        self.collection.create_index([
            ("customer_id", 1),
            ("utc_timestamp", 1)
        ])

        # Ensure unique event_id
        self.collection.create_index("event_id", unique=True)

    def add(self, event: Event) -> str:
        """
        Add an event to the repository

        Returns:
            str: The ID of the inserted document
        """
        # Convert event to MongoDB document
        doc = event.to_mongo_document()

        # Insert into MongoDB
        result = self.collection.insert_one(doc)

        # Return the inserted ID
        return str(result.inserted_id)

    def find_by_customer_id(self, customer_id: str) -> List[Event]:
        """Find events by customer ID"""
        cursor = self.collection.find({"customer_id": customer_id})
        return [Event.from_mongo_document(doc) for doc in cursor]

    def find_by_date_range(
            self,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[Event]:
        """Find events within a date range"""
        # Build query based on provided date filters
        query = {}

        if start_date or end_date:
            date_query = {}

            if start_date:
                date_query["$gte"] = start_date

            if end_date:
                date_query["$lte"] = end_date

            query["utc_timestamp"] = date_query

        # Execute query
        cursor = self.collection.find(query)
        return [Event.from_mongo_document(doc) for doc in cursor]

    def find_by_customer_and_date_range(
            self,
            customer_id: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[Event]:
        """Find events by customer ID and date range"""
        # Build query based on provided filters
        query = {}

        if customer_id:
            query["customer_id"] = customer_id

        if start_date or end_date:
            date_query = {}

            if start_date:
                date_query["$gte"] = start_date

            if end_date:
                date_query["$lte"] = end_date

            if date_query:
                query["utc_timestamp"] = date_query

        # Execute query
        cursor = self.collection.find(query)
        return [Event.from_mongo_document(doc) for doc in cursor]

    def find_by_event_id(self, event_id: str) -> Optional[Event]:
        """Find an event by its event_id"""
        doc = self.collection.find_one({"event_id": event_id})
        return Event.from_mongo_document(doc) if doc else None

    def count_by_customer_id(self, customer_id: str) -> int:
        """Count events for a specific customer"""
        return self.collection.count_documents({"customer_id": customer_id})

    def count_by_event_type(self, event_type: str) -> int:
        """Count events of a specific type"""
        return self.collection.count_documents({"event_type": event_type})

    def delete_by_event_id(self, event_id: str) -> bool:
        """Delete an event by its event_id"""
        result = self.collection.delete_one({"event_id": event_id})
        return result.deleted_count > 0