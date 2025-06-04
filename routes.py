from flask import Flask, request, jsonify, render_template # Added render_template
from flask_cors import CORS
import crud # Our CRUD functions
from models import User # For type hinting or direct use if needed, good to have
from models import Base # For table creation
from connection import engine # For table creation

# --- Flask App Setup ---
app = Flask(__name__)
# Allow Cross-Origin requests
CORS(app)

# --- API Routes ---

@app.route("/", methods=["GET"])
def home_route():
    """A simple 'welcome' route to check if the API is running."""
    return jsonify({"message": "Welcome to the NCAIR API!"}), 200

@app.route("/user", methods=["POST"])
def register_user_route():
    """
    API Route to create a new user.
    Expects JSON data: {"name": "...", "email": "...", "password": "...", "phoneNumber": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phoneNumber = data.get("phoneNumber")

    user, message = crud.create_user(name, email, password, phoneNumber)

    if user:
        return jsonify({"message": message, "user": user.to_dict()}), 201
    else:
        status_code = 409 if "already exists" in message.lower() else 400
        return jsonify({"message": message}), status_code

@app.route("/users", methods=["GET"])
def get_users_route():
    """API Route to fetch all users."""
    users, message = crud.read_users()

    if users is not None:
        users_dict = [user.to_dict() for user in users]
        return jsonify({"message": message, "users": users_dict}), 200
    else:
        # This case implies an issue in crud.read_users if it returns (None, message)
        # For a more specific error, crud.read_users should manage its return.
        return jsonify({"message": message or "Failed to fetch users"}), 500

@app.route("/user/<int:user_id>", methods=["PUT", "PATCH"])
def update_user_route(user_id):
    """
    API Route to update a user by ID.
    Expects JSON data with fields to update.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided for update"}), 400

    user, message = crud.update_user(
        user_id=user_id,
        name=data.get("name"),
        password=data.get("password"), # Remember: In a real app, handle password updates securely
        phoneNumber=data.get("phoneNumber")
    )

    if user:
        # Check if the message indicates "no changes" to potentially return a different status or message
        if "no changes" in message.lower():
             return jsonify({"message": message, "user": user.to_dict()}), 200 # Or 304 Not Modified, but 200 is fine
        return jsonify({"message": message, "user": user.to_dict()}), 200
    else:
        status_code = 404 if "not found" in message.lower() else 400 # Or 500 for other errors
        return jsonify({"message": message}), status_code

@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    """API Route to delete a user by ID."""
    success, message = crud.delete_user(user_id)

    if success:
        return jsonify({"message": message}), 200
    else:
        status_code = 404 if "not found" in message.lower() else 400 # Or 500
        return jsonify({"message": message}), status_code

# --- Frontend Route ---
@app.route("/app_ui", methods=["GET"])
def user_interface_route():
    """
    Serves the main HTML page for the user interface.
    """
    # Flask will look for 'index.html' in a folder named 'templates'
    return render_template("index.html")

# --- Run the App ---
if __name__ == "__main__":
    # This section runs when 'python routes.py' is executed directly
    # or when the CMD in Dockerfile runs this script.
    try:
        print("Creating database tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        print("Tables check/creation complete.")
    except Exception as e:
        print(f"!!! Error creating tables: {e}")

    # Starts the Flask development server
    # host='0.0.0.0' makes it accessible from outside the container (via port mapping)
    # debug=True enables auto-reloading on code changes and provides a debugger
    app.run(debug=True, host="0.0.0.0", port=4200)