import requests
import json
import sqlite3
from collections import namedtuple
import hashlib

# Define a Pokemon model
Pokemon = namedtuple('Pokemon', ['name', 'id', 'stats'])

# Function to fetch Pokemon data from PokeAPI
def fetch_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_id = data['id']
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        return Pokemon(name=data['name'], id=pokemon_id, stats=stats)
    else:
        return None

# Function to simulate a battle between two Pokemon
def simulate_battle(pokemon1, pokemon2):
    stats_change1 = sum(pokemon1.stats.values())
    stats_change2 = sum(pokemon2.stats.values())
    if stats_change1 > stats_change2:
        return pokemon1.name
    elif stats_change2 > stats_change1:
        return pokemon2.name
    else:
        return "It's a tie!"

# Function to create a hash key for caching
def create_cache_key(pokemon_name):
    return hashlib.sha256(pokemon_name.encode()).hexdigest()

# Function to retrieve data from cache or fetch from API
def get_pokemon_data_with_cache(pokemon_name, cache):
    cache_key = create_cache_key(pokemon_name)
    if cache_key in cache:
        return cache[cache_key]
    else:
        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data:
            cache[cache_key] = pokemon_data
            return pokemon_data
        else:
            return None

# Function to initialize SQLite database
def initialize_database():
    conn = sqlite3.connect('pokemon_battles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS battles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pokemon1 TEXT,
                  pokemon2 TEXT,
                  winner TEXT)''')
    conn.commit()
    conn.close()

# Function to save battle data to SQLite database
def save_battle_to_database(pokemon1, pokemon2, winner):
    conn = sqlite3.connect('pokemon_battles.db')
    c = conn.cursor()
    c.execute("INSERT INTO battles (pokemon1, pokemon2, winner) VALUES (?, ?, ?)", (pokemon1.name, pokemon2.name, winner))
    conn.commit()
    conn.close()

# Main function to run the program
def main(pokemon_name1, pokemon_name2):
    cache = {}
    initialize_database()

    # Fetch Pokemon data
    pokemon1 = get_pokemon_data_with_cache(pokemon_name1, cache)
    pokemon2 = get_pokemon_data_with_cache(pokemon_name2, cache)

    if pokemon1 and pokemon2:
        print(f"Pokemon 1: {pokemon1.name}, ID: {pokemon1.id}, Stats: {pokemon1.stats}")
        print(f"Pokemon 2: {pokemon2.name}, ID: {pokemon2.id}, Stats: {pokemon2.stats}")

        # Simulate battle
        winner = simulate_battle(pokemon1, pokemon2)
        print(f"The winner is: {winner}")

        # Save battle data to database
        save_battle_to_database(pokemon1, pokemon2, winner)
    else:
        print("Error: Pokemon data not found.")

if __name__ == "__main__":
    pokemon_name1 = input("Enter the name of the first Pokemon: ")
    pokemon_name2 = input("Enter the name of the second Pokemon: ")
    main(pokemon_name1, pokemon_name2)
