from flask import Flask, render_template, request, jsonify
from app.models import Pokemon, Move
from config import Config

app = Flask(
    __name__,
    template_folder=Config.TEMPLATE_DIR,
    static_folder=Config.STATIC_DIR
)

@app.route("/")
def index() -> str:
    """Render main interface"""
    return render_template("index.html")

@app.route("/pokemon", methods=["POST"])
def create_pokemon() -> tuple:
    """Create new Pokémon entry"""
    data = request.get_json()
    
    try:
        result = Pokemon.get_collection().insert_one(data)
        return jsonify({
            "status": "success",
            "inserted_id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/pokemon/<dexnum>", methods=["GET"])
def get_pokemon(dexnum: str) -> tuple:
    """Get Pokémon by dex number"""
    pokemon = Pokemon.get_collection().find_one({"dexnum": dexnum.zfill(4)})
    
    if not pokemon:
        return jsonify({"error": "Pokémon not found"}), 404
    
    pokemon["_id"] = str(pokemon["_id"])
    return jsonify(pokemon)

@app.route("/moves/<move_name>/users")
def get_move_users(move_name: str) -> tuple:
    """Get Pokémon that can learn a move (JOIN-like operation)"""
    move = Move.get_collection().find_one({"name": move_name})
    
    if not move:
        return jsonify({"error": "Move not found"}), 404
    
    users = Pokemon.get_collection().find(
        {"dexnum": {"$in": move["users"]}},
        {"_id": 0, "dexnum": 1, "name": 1, "types": 1}
    )
    
    return jsonify({
        "move": move_name,
        "users": list(users)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)