# ⚡ PokemNOSql - MongoDB Pokédex Interface 🐱‍👤

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Progress](https://img.shields.io/badge/status-active-brightgreen)]()
[![Code Style: PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://peps.python.org/pep-0008/)

**PokemNOSql** is a minimalist web application built using **Flask** and **MongoDB**, featuring a clean UI for exploring, creating, updating, and deleting Pokémon entries.

---

## 🖼️ Interface Preview

![Pokédex Interface Preview](./c139fce8-e638-4aca-aaef-08eac1d420d0.png)

---

## 🔧 Quick Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/PokemNOSql.git
cd PokemNOSql
```
### Activate the environment
```bash
source pokeEnv/bin/activate  # Linux/MacOS
.\PokeEnv\Scripts\activate   # Windows
```
### Install packages 
```bash
pip install -r requirements.txt
```

---
## 🚀 To load the data into the DB:
```bash
python -m scripts.mongo_loader 
```
---
## 🚀 To run the Flask interface:
```bash
python -m app.routes 
```