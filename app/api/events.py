from flask import request, jsonify
from app.api import api_blueprint
from app.services.event_service import EventService
from app.utils.validators import ValidationError

event_service = EventService()


@api_blueprint.route('/events', methods=['POST'])
def create_event():
    """Endpoint to receive and store events"""
    try:
        event_data = request.json

        # Process the event using the service
        event_service.process_event(event_data)

        return jsonify({"status": "success", "message": "Event stored successfully"}), 201

    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500


@api_blueprint.route('/events', methods=['GET'])
def get_events():
    """Endpoint to query events by customer_id and date range"""
    try:
        # Get query parameters
        customer_id = request.args.get('customer_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Get filtered events using the service
        filtered_events = event_service.get_filtered_events(
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date
        )

        return jsonify({"status": "success", "events": filtered_events}), 200

    except ValidationError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500