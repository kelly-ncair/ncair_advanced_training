from flask import Flask, request, jsonify
from flask_cors import CORS
from crud import create_user, get_user, create_post

app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

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
    
@app.route("/user/<int:user_id>", methods=["GET"])
def fetch_user(user_id):
    try:
       user = get_user(user_id);
       return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)})
                       

@app.route("/create_post", methods=["POST"])
def insert_post():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        title = data.get("title")
        description = data.get("description")
        
        

        if not user_id or not title or not description:
            return jsonify({"message": "Please provide all entries"})

        resp = create_post(user_id, title, description)

        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": f"{e}"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)