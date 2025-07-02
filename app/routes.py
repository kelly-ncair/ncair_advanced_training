from flask import Flask, request, jsonify
from flask_cors import CORS
from crud import create_company, read_companies, get_company, update_company, delete_company, create_staff, read_staff, get_staff, update_staff, delete_staff, get_staff_by_company_name, get_staff_and_company
from connection import create_engine
import time
from dotenv import load_dotenv
import os
load_dotenv()

env_mode = os.getenv('ENV_MODE')

if env_mode == "local":
    load_dotenv(".env")
else: load_dotenv(".env.docker")
print(env_mode)
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



# Company CRUD API
@app.route("/create_company", methods=["POST"])
def register_company():
    data = request.get_json() or {}
    try:
        new_company = create_company(
            data.get("name"),
            data.get("location"),
        )
        company_dict = {
            "name": new_company["name"],
            "location": new_company["location"]
        }
        return jsonify({"new_company": company_dict}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_company", methods=["GET"])
def get_company_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        company = get_company(identifier)
        return jsonify({"company": company}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/get_companies", methods=["GET"])
def get_companies_route():
    try:
        companies = read_companies()
        companies_list = [
            {"id": c.id, "name": c.name, "location": c.location} for c in companies
        ]
        return jsonify({"companies": companies_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_company", methods=["PUT"])
def update_company_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        updated = update_company(
            identifier,
            name=data.get("name"),
            location=data.get("location")
        )
        company_dict = {
            "id": updated["id"],
            "name": updated["name"],
            "location": updated["location"]
        }
        return jsonify({"updated_company": company_dict}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/delete_company", methods=["DELETE"])
def delete_company_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        result = delete_company(identifier)
        if result:
            return jsonify({"message": f"Company {result['name']} located at {result['location']} deleted successfully"}), 200
        else:
            return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Staff CRUD API

@app.route("/create_staff", methods=["POST"])
def register_staff():
    data = request.get_json() or {}
    try:
        new_staff = create_staff(
            data.get("name"),
            data.get("role"),
            data.get("company_id"),
            data.get("salary"),
            data.get("email"),
            data.get("phoneNumber")
        )
        staff_dict = {
            "id": new_staff["id"],
            "name": new_staff["name"],
            "role": new_staff["role"],
            "salary": new_staff["salary"],
            "email": new_staff["email"],
            "phoneNumber": new_staff["phoneNumber"],
            "company_id": new_staff["company_id"]
        }
        return jsonify({"new_staff": staff_dict}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_staff", methods=["GET"])
def get_staff_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        staff = get_staff(identifier)
        staff_dict = {
            "id": staff["id"],
            "name": staff["name"],
            "role": staff["role"],
            "salary": staff["salary"],
            "email": staff["email"],
            "phoneNumber": staff["phoneNumber"],
            "company_id": staff["company_id"]
        }
        return jsonify({"staff": staff_dict}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    
@app.route("/get_staffs", methods=["GET"])
def get_staffs_route():
    try:
        staffs = read_staff()
        staffs_list = [
            {"id": c.id, "name": c.name, "role": c.location, "salary": c.salary, "email": c.email, "phoneNumber": c.phoneNumber} for c in staffs
        ]
        return jsonify({"staffs": staffs_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_staff", methods=["PUT"])
def update_staff_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        updated = update_staff(
            identifier,
            name=data.get("name"),
            role=data.get("role"),
            salary=data.get("salary"),
            email=data.get("email"),
            phoneNumber=data.get("phoneNumber")
        )
        staff_dict = {
            "name": updated["name"],
            "role": updated["role"],
            "salary": updated["salary"],
            "email": updated["email"],
            "phoneNumber": updated["phoneNumber"],
            "company_id": updated["company_id"]
        }
        return jsonify({"updated_staff": staff_dict}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/delete_staff", methods=["DELETE"])
def delete_staff_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        result = delete_staff(identifier)
        if result:
            return jsonify({"message": f"Staff named {result['name']} with the role {result['role']} deleted successfully"}), 200
        else:
            return jsonify({"error": "Staff not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/get_staff_by_company_name", methods=["GET"])
def get_staff_by_company_name_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        staff_list = get_staff_by_company_name(identifier)
        return jsonify({"staff": staff_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/get_staff_and_company", methods=["GET"])
def get_staff_and_company_route():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    try:
        result = get_staff_and_company(identifier)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
