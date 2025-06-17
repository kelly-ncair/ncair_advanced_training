import time
from sqlalchemy.exc import OperationalError
from flask import Flask, request, jsonify
from flask_cors import CORS
from main import addition, subtraction

from connection import engine
from models import Base
from crud import users, posts


max_attempts = 30
for attempt in range(1, max_attempts + 1):
    try:
        conn = engine.connect()
        conn.close()
        print(f"Database is up (on attempt {attempt})")
        break
    except OperationalError:
        print(f"Database not ready (attempt {attempt}/{max_attempts}), retrying")
        time.sleep(1)
else:
    raise RuntimeError(f"Could not connect to the database after {max_attempts} attempts")

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

CORS(app)

def chk_numbers(data):
    # Confirming data is a JSON
    if not isinstance(data, dict):
        return None, None, (jsonify({"error": "Please check if data is JSON"}))

    x = data.get("x")
    y = data.get("y")

    if x is None or y is None:
        return None, None, (jsonify({"error": "Please provide both x and y"}))

    try:
        x_val = float(x)
        y_val = float(y)
    except (TypeError, ValueError):
        return None, None, (jsonify({"error": "Please make sure x and y are numeric"}))

    return x_val, y_val, None


## Maths Route
@app.route("/addition", methods=["POST"])
def additionRoute():
    # 1. Request for parameters needed
    data = request.get_json() # dictionary {x: 1, y: 2}

    x = data.get("x")
    y = data.get("y")
    
    if not x or not y:
        return jsonify({"error": "Please provide x and y"})
    
    res = addition(x, y)
    
    return jsonify({"result": res})



@app.route("/subtraction", methods=["GET", "POST"])
def subtractRoute():
    data = request.get_json() # dictionary {x: 1, y: 2}

    x, y, err_msg = chk_numbers(data)
    if err_msg:
        return err_msg

    result = subtraction(x, y)

    return jsonify({"result": result})



## --- Users Routes ---
@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    try:
        user = users.create_user(
            name = data.get("name"),
            email = data.get("email"),
            password = data.get("password"),
            phoneNumber = data.get("phoneNumber"),
        )
        if user is None:
            return jsonify({"error": "Could not create user"}), 400
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "phoneNumber": user.phoneNumber}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/read_users", methods=["GET"])
def read_users():
    try:
        users = users.read_users()
        return jsonify([{"id": u.id, "name": u.name, "email": u.email, "phoneNumber": u.phoneNumber} for u in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_user", methods=["GET"])
def get_user():
    data = request.get_json() or {}
    try:
        id = data.get("id")
        user = users.read_user(id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "phoneNumber": user.phoneNumber}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/update_user", methods=["PUT", "PATCH"])
def update_user():
    data = request.get_json() or {}
    try:
        id = data.get("id")
        user = users.update_user(id=id, name=data.get("name"), password=data.get("password"), phoneNumber=data.get("phoneNumber"), email=data.get("email"))
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "phoneNumber": user.phoneNumber}), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        msg = e if isinstance(e, str) else getattr(e, "message", str(e))
        return jsonify({"error": msg}), 400



@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    data = request.get_json() or {}
    try:
        id = data.get("id")
        user = users.read_user(id)
        tgt_user = users.delete_user(id)
        user_name = user.name
        if tgt_user:
            return jsonify({"message": f"User {user_name} with id: {id} deleted"}), 200
        else:
            return jsonify({"error": "User not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


## --- Posts Routes ---


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
