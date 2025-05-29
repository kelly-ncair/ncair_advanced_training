from flask import Flask, request, jsonify
from flask_cors import CORS
from crud import create_user

app = Flask(__name__)

CORS(app)

# Route to create a user
@app.route("/create_user", methods=["POST"])
def register_user():
    
    try:
    
        data = request.get_json()
        
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phoneNumber = data.get("phoneNumber")
        
        if not name or not email or not password or not phoneNumber:
            return jsonify({"message": "Please provide all entries"})
        
        resp = create_user(name, email, password, phoneNumber)
        
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": f"{e}"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)