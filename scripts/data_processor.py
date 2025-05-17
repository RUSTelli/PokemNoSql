import csv
from pathlib import Path
from typing import List, Dict
from config import Config

def process_pokemon_data() -> List[Dict]:
    """
    Process Pokémon CSV data into MongoDB documents
    
    Returns:
        List[Dict]: List of processed Pokémon documents
    """
    pokemon_data = []
    data_path = Config.DATA_DIR / "pokemon.csv"
    
    with open(data_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            doc = {
                "dexnum": row["dexnum"].zfill(4),
                "name": row["name"],
                "types": [t for t in [row["type1"], row["type2"]] if t],
                "stats": {
                    "hp": int(row["hp"]),
                    "attack": int(row["attack"]),
                    "defense": int(row["defense"]),
                    "sp_atk": int(row["sp_atk"]),
                    "sp_def": int(row["sp_def"]),
                    "speed": int(row["speed"]),
                    "total": int(row["total"])
                },
                "moves": [],
                "height": float(row["height"]),
                "weight": float(row["weight"]),
                "abilities": {
                    "primary": row["ability1"],
                    "secondary": row["ability2"] if row["ability2"] else None,
                    "hidden": row["hidden_ability"] if row["hidden_ability"] else None
                }
            }
            pokemon_data.append(doc)
    
    return pokemon_data

def process_moves_data() -> List[Dict]:
    """
    Process Moves CSV data into MongoDB documents
    
    Returns:
        List[Dict]: List of processed Move documents
    """
    moves_data = []
    data_path = Config.DATA_DIR / "moves.csv"
    
    with open(data_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            doc = {
                "name": row["Name"],
                "type": row["Type"],
                "category": row["Cat."],
                "power": int(row["Power"]) if row["Power"] else None,
                "accuracy": str(row["Acc."]) if row["Acc."] else None,
                "pp": int(row["PP"]) if row["PP"] else None,
                "effect": row["Effect"],
                "probability": int(row["Prob. (%)"]) if row["Prob. (%)"] else None,
                "users": [u.strip() for u in row["Users"].split(",")] if row["Users"] else [],
            }
            moves_data.append(doc)
    
    return moves_data