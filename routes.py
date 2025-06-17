from flask import Flask, request, jsonify
from flask_cors import CORS
from main import addition, subtraction
from crud import create_user, read_users, update_user, delete_user
from post_crud import create_post, get_post, get_all_posts, get_posts_by_author, get_posts_by_category, update_post, delete_post
from connection import create_engine
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database configuration from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = Flask(__name__)
CORS(app)

# wait for the DB to be up
for _ in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except Exception:
        time.sleep(3)
else:
    raise RuntimeError("Could not connect to the database after 10 tries.")

@app.route("/addition", methods=["GET", "POST"])
def additionRoute():
    data = request.get_json(silent=True) or request.args
    x = data.get("x")
    y = data.get("y")
    if x is None or y is None:
        return jsonify({"error": "Please provide x and y"}), 400
    try:
        result = addition(int(x), int(y))
        return jsonify({"result": result}), 200
    except ValueError:
        return jsonify({"error": "x and y must be integers"}), 400

@app.route("/subtraction", methods=["GET", "POST"])
def subtractionRoute():
    data = request.get_json(silent=True) or request.args
    x = data.get("x")
    y = data.get("y")
    if x is None or y is None:
        return jsonify({"error": "Please provide x and y"}), 400
    try:
        result = subtraction(int(x), int(y))
        return jsonify({"result": result}), 200
    except ValueError:
        return jsonify({"error": "x and y must be integers"}), 400

@app.route("/create_user", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    try:
        new_user = create_user(
            data.get("name"),
            data.get("email"),
            data.get("password"),
            data.get("phoneNumber")
        )
        # if email already exists, crud returns a message dict
        status = 200 if isinstance(new_user, dict) and new_user.get("message") else 201
        return jsonify({"new_user": new_user}), status
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_users", methods=["GET"])
def get_all_users():
    data = request.get_json() or {}
    try:
        id = data.get("id")
        users = read_users(id)
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_user", methods=["PUT"])
def modify_user():
    data = request.get_json() or {}
    name = data.get("name")
    try:
        updated = update_user(
            name,
            new_name=data.get("new_name"),
            password=data.get("password"),
            phoneNumber=data.get("phoneNumber")
        )
        status = 200 if "message" not in updated else 404
        return jsonify({"updated_user": updated}), status
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_user", methods=["DELETE"])
def remove_user():
    data = request.get_json() or {}
    name = data.get("name")
    try:
        result = delete_user(name)
        status = 200 if result.get("message") == f"User {name} deleted successfully" else 404
        return jsonify(result), status
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/create_post", methods=["POST"])
def post_create():
    data = request.get_json() or {}
    try:
        new_post = create_post(**data)

        post_dict = {
            "post_id": new_post.post_id,
            "title": new_post.title,
            "content": new_post.content,
            "author_id": new_post.author_id,
            "category": new_post.category,
            "published_at": new_post.published_at.isoformat() if new_post.published_at else None
        }
        return jsonify({"new_post": post_dict}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
