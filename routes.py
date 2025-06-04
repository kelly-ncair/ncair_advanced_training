from flask import Flask, request, jsonify
from flask_cors import CORS
#from main import addition, subtraction


app = Flask(__name__)

CORS(app)


@app.route("/addition", methods=["GET", "POST"])
def additionRoute():
    # 1. Request for parameters needed
    x=None
    y=None
    
    if request.method == "GET":
        x = request.args.get("x")
        y = request.args.get("y")
    else:
        data = request.get_json() # dictionary {x: 1, y: 2}
        x = data.get("x")
        y = data.get("y")
    
    if x is None or  y is None:
        return jsonify({"error": "Please provide x and y"})
    
    res = addition(int(x), int(y))
    
    return jsonify({"result": res})



@app.route("/addition", methods=["GET", "POST"])
def subtractionRoute():
    # 1. Request for parameters needed
    x=None
    y=None
    
    if request.method == "GET":
        x = request.args.get("x")
        y = request.args.get("y")
    else:
        data = request.get_json() # dictionary {x: 1, y: 2}
        x = data.get("x")
        y = data.get("y")
    
    if x is None or  y is None:
        return jsonify({"error": "Please provide x and y"})
    
    res = subtraction(int(x), int(y))
    
    return jsonify({"result": res})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4200)

# host="0.0.0.0".... exposes the port everywhere on your computer, so that this port is not repeating. It is like you are cleaning this port in your computer so that no other services uses it.

