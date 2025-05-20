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

# ----------------------
# Pokémon CRUD Routes
# ----------------------

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

@app.route("/pokemon/<identifier>", methods=["GET"])
def get_pokemon(identifier: str) -> tuple:
    """Get Pokémon by dex number or name"""
    # Determine lookup field: numeric => dexnum, otherwise name
    if identifier.isdigit():
        query = {"dexnum": identifier.zfill(4)}
    else:
        query = {"name": identifier}

    pokemon = Pokemon.get_collection().find_one(query)
    if not pokemon:
        return jsonify({"error": "Pokémon not found"}), 404

    pokemon["_id"] = str(pokemon["_id"])
    return jsonify(pokemon), 200

@app.route("/pokemon/<dexnum>", methods=["PUT"])
def update_pokemon(dexnum: str) -> tuple:
    """Update existing Pokémon entry by dex number"""
    data = request.get_json()
    filter_ = {"dexnum": dexnum.zfill(4)}
    try:
        result = Pokemon.get_collection().update_one(filter_, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Pokémon not found"}), 404
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/pokemon/<dexnum>", methods=["DELETE"])
def delete_pokemon(dexnum: str) -> tuple:
    """Delete Pokémon entry by dex number"""
    filter_ = {"dexnum": dexnum.zfill(4)}
    result = Pokemon.get_collection().delete_one(filter_)
    if result.deleted_count == 0:
        return jsonify({"error": "Pokémon not found"}), 404
    return jsonify({"status": "deleted"}), 200

# ----------------------
# Move-Users Route
# ----------------------

@app.route("/moves/<move_name>/users", methods=["GET"])
def get_move_users(move_name: str) -> tuple:
    """Get Pokémon that can learn a move (JOIN-like operation)"""
    move = Move.get_collection().find_one({"name": move_name})
    if not move:
        return jsonify({"error": "Move not found"}), 404

    users_cursor = Pokemon.get_collection().find(
        {"dexnum": {"$in": move.get("users", [])}},
        {"_id": 0, "dexnum": 1, "name": 1, "types": 1}
    )
    users = list(users_cursor)

    return jsonify({
        "move": move_name,
        "users": users
    }), 200

@app.route("/move/<name>", methods=["GET"])
def get_move(name: str) -> tuple:
    """Get Move details by name"""
    move = Move.get_collection().find_one({"name": name})
    if not move:
        return jsonify({"error": "Move not found"}), 404

    # Return only the fields our UI needs
    return jsonify({
        "name": move["name"],
        "type": move.get("type"),
        "power": move.get("power"),
        "accuracy": move.get("accuracy")
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
