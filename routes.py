import time
from sqlalchemy.exc import OperationalError
from flask import Flask, request, jsonify
from flask_cors import CORS
from main import addition, subtraction

from connection import engine
from models import Base
from crud import users, posts, teams, players


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
        usrs = users.read_users()
        return jsonify([{"id": u.id, "name": u.name, "email": u.email, "phoneNumber": u.phoneNumber} for u in usrs]), 200
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
@app.route("/create_post", methods=["POST"])
def create_post():
    data = request.get_json() or {}
    try:

        post = posts.create_post(user_id = data.get("user_id"),
                                password = data.get("password"),
                                title = data.get("title"),
                                description= data.get("description"))
        if post is None:
            return jsonify({"error": "Could not create post"}), 400
        
        return jsonify({"user_id": post.user_id, "post_id": post.post_id, "title": post.title, "description": post.description}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route("/read_posts", methods=["GET"])
def read_posts():
    try:
        psts = posts.read_posts()
        return jsonify([{"user_id": p.user_id, "post_id": p.post_id,  "title": p.title, "description": p.description} for p in psts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_post", methods=["GET"])
def get_post():
    data = request.get_json() or {}
    try:
        post_id = data.get("post_id")
        post = posts.read_post(post_id)
        if not post:
            return jsonify({"error": "Article not found"}), 404
        return jsonify({"post_id": post.post_id, "title": post.title, "description": post.description, "user_id": post.user_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_post", methods=["PUT", "PATCH"])
def update_post():
    data = request.get_json() or {}
    try:
        post = posts.update_post(post_id=data.get("post_id"),
            user_id=data.get("user_id"),
            password=data.get("password"),
            title=data.get("title"),
            description=data.get("description"))
        
        return jsonify({"user_id": post.user_id, "post_id": post.post_id, "title": post.title, "description": post.description}), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        msg = e if isinstance(e, str) else getattr(e, "message", str(e))
        return jsonify({"error": msg}), 400


@app.route("/delete_post", methods=["DELETE"])
def delete_post():
    data = request.get_json() or {}
    try:
        post = posts.read_post(post_id=data.get("post_id"))

        tgt_post = posts.delete_post(post_id=data.get("post_id"),
            user_id=data.get("user_id"),
            password=data.get("password"))
        
        post_title = post.title
        post_id = post.post_id
        if tgt_post:
            return jsonify({"message": f"Article '{post_title}' with id: '{post_id}' deleted"}), 200
        else:
            return jsonify({"error": "Article not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


## --- Teams Routes ---
@app.route("/create_team", methods=["POST"])
def create_team():
    data = request.get_json() or {}
    try:
        team = teams.create_team(
            name       = data.get("name"),
            city       = data.get("city"),
            coach_name = data.get("coach_name"),
        )
        if team is None:
            return jsonify({"error": "Could not create team"}), 400
        return jsonify({
            "id":         team.id,
            "name":       team.name,
            "city":       team.city,
            "coach_name": team.coach_name
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/read_teams", methods=["GET"])
def read_teams():
    try:
        tms = teams.read_teams()
        return jsonify([
            {
                "id":         t.id,
                "name":       t.name,
                "city":       t.city,
                "coach_name": t.coach_name
            }
            for t in tms
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_team", methods=["GET"])
def get_team():
    data = request.get_json() or {}
    try:
        id   = data.get("id")
        team = teams.read_team(id)
        if not team:
            return jsonify({"error": "Team not found"}), 404
        return jsonify({
            "id":         team.id,
            "name":       team.name,
            "city":       team.city,
            "coach_name": team.coach_name
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_team", methods=["PUT", "PATCH"])
def update_team():
    data = request.get_json() or {}
    try:
        id   = data.get("id")
        team = teams.update_team(
            id         = id,
            name       = data.get("name"),
            city       = data.get("city"),
            coach_name = data.get("coach_name")
        )
        return jsonify({
            "id":         team.id,
            "name":       team.name,
            "city":       team.city,
            "coach_name": team.coach_name
        }), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        msg = e if isinstance(e, str) else getattr(e, "message", str(e))
        return jsonify({"error": msg}), 400

@app.route("/delete_team", methods=["DELETE"])
def delete_team():
    data = request.get_json() or {}
    try:
        id        = data.get("id")
        team      = teams.read_team(id)
        deleted   = teams.delete_team(id)
        team_name = team.name
        if deleted:
            return jsonify({"message": f"Team {team_name} with id: {id} deleted"}), 200
        else:
            return jsonify({"error": "Team not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


## --- Players Routes ---
@app.route("/create_player", methods=["POST"])
def create_player():
    data = request.get_json() or {}
    try:
        player = players.create_player(
            name          = data.get("name"),
            position      = data.get("position"),
            age           = data.get("age"),
            jersey_number = data.get("jersey_number"),
            team_id       = data.get("team_id"),
        )
        if player is None:
            return jsonify({"error": "Could not create player"}), 400
        return jsonify({
            "id":            player.id,
            "name":          player.name,
            "position":      player.position,
            "age":           player.age,
            "jersey_number": player.jersey_number,
            "team_id":       player.team_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/read_players", methods=["GET"])
def read_players():
    try:
        pls = players.read_players()
        return jsonify([
            {
                "id":            p.id,
                "name":          p.name,
                "position":      p.position,
                "age":           p.age,
                "jersey_number": p.jersey_number,
                "team_id":       p.team_id
            }
            for p in pls
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_player", methods=["GET"])
def get_player():
    data = request.get_json() or {}
    try:
        id     = data.get("id")
        player = players.read_player(id)
        if not player:
            return jsonify({"error": "Player not found"}), 404
        return jsonify({
            "id":            player.id,
            "name":          player.name,
            "position":      player.position,
            "age":           player.age,
            "jersey_number": player.jersey_number,
            "team_id":       player.team_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_player", methods=["PUT", "PATCH"])
def update_player():
    data = request.get_json() or {}
    try:
        id     = data.get("id")
        player = players.update_player(
            id            = id,
            name          = data.get("name"),
            position      = data.get("position"),
            age           = data.get("age"),
            jersey_number = data.get("jersey_number"),
            team_id       = data.get("team_id")
        )
        return jsonify({
            "id":            player.id,
            "name":          player.name,
            "position":      player.position,
            "age":           player.age,
            "jersey_number": player.jersey_number,
            "team_id":       player.team_id
        }), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        msg = e if isinstance(e, str) else getattr(e, "message", str(e))
        return jsonify({"error": msg}), 400

@app.route("/delete_player", methods=["DELETE"])
def delete_player():
    data = request.get_json() or {}
    try:
        id         = data.get("id")
        player     = players.read_player(id)
        deleted    = players.delete_player(id)
        player_name = player.name
        if deleted:
            return jsonify({"message": f"Player {player_name} with id: {id} deleted"}), 200
        else:
            return jsonify({"error": "Player not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
