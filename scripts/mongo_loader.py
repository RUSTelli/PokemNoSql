import logging
from typing import Tuple
from tqdm import tqdm
from app.models import Pokemon, Move
from .data_processor import process_pokemon_data, process_moves_data

logging.basicConfig(level=logging.INFO)

def initialize_collections() -> None:
    """Initialize collections with indexes"""
    Pokemon.create_indexes()
    Move.create_indexes()
    logging.info("Database indexes created")

def load_data() -> Tuple[int, int]:
    """
    Load data into MongoDB
    
    Returns:
        Tuple[int, int]: (Number of Pokémon inserted, Number of moves inserted)
    """
    # Process data
    pokemon_docs = process_pokemon_data()
    move_docs = process_moves_data()
    
    # Clear existing data
    Pokemon.get_collection().delete_many({})
    Move.get_collection().delete_many({})
    
    # Insert new data
    pokemon_result = Pokemon.get_collection().insert_many(pokemon_docs)
    move_result = Move.get_collection().insert_many(move_docs)
    
    # Update relationships
    update_relationships()
    
    return len(pokemon_result.inserted_ids), len(move_result.inserted_ids)

def update_relationships() -> None:
    """Update Pokémon-move relationships"""
    moves = Move.get_collection().find()
    
    for move in tqdm(moves, desc="Updating relationships"):
        users = move.get("users", [])
        
        # Update move with Pokémon references
        Move.get_collection().update_one(
            {"_id": move["_id"]},
            {"$set": {"users": users}}
        )
        
        # Update Pokémon with move references
        for dexnum in users:
            Pokemon.get_collection().update_one(
                {"dexnum": dexnum},
                {"$addToSet": {"moves": move["name"]}},
                upsert=False
            )

if __name__ == "__main__":
    initialize_collections()
    pokemon_count, move_count = load_data()
    logging.info(f"Data load complete: {pokemon_count} Pokémon, {move_count} moves")