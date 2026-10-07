from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data model
class Event:

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# Initial event collection
events = [Event(1, "Tech Meetup"), Event(2, "Python Workshop")]


def find_event(event_id):
    """Helper function to find an event by ID."""
    return next((e for e in events if e.id == event_id), None)


# 1. GET /events - Retrieve all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200


# 2. POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Missing or invalid 'title' in request body"}), 400

    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(id=new_id, title=data["title"].strip())

    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


# 3. PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event_title(id):
    event = find_event(id)
    if not event:
        return jsonify({"error": f"Event with ID {id} not found"}), 404

    data = request.get_json()
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Missing or invalid 'title' in request body"}), 400

    event.title = data["title"].strip()
    return jsonify(event.to_dict()), 200


# 4. DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = find_event(id)
    if not event:
        return jsonify({"error": f"Event with ID {id} not found"}), 404

    events.remove(event)
    return jsonify({"message": f"Event {id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)