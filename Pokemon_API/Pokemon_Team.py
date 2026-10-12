import requests
import json
import sqlite3
import webbrowser
import random

urlRoot = "https://pokeapi.co/api/v2/pokemon/"
urlTypeRoot = "https://pokeapi.co/api/v2/type/"
timewait = 1

cnxn = sqlite3.connect("PokemonTeam.db")
cursor = cnxn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT,
                types TEXT)""")

# If your pokemon is 'key' it will be weak when attacked by the types in its 'values'
Defending = {"Normal" : ["Fighting"],
             "Fire" : ["Water", "Ground", "Rock"],
             "Water" : ["Grass", "Electric"],
             "Grass" : ["Fire", "Ice", "Poison", "Flying", "Bug"],
             "Electric" : ["Ground"],
             "Ice" : ["Fire", "Fighting", "Rock", "Steel"],
             "Fighting" : ["Flying", "Psychic", "Fairy"],
             "Poison" : ["Ground", "Psychic"],
             "Ground" : ["Water", "Grass", "Ice"],
             "Flying" : ["Electric", "Ice", "Rock"],
             "Psychic" : ["Bug", "Ghost", "Dark"],
             "Bug" : ["Fire", "Flying", "Rock"],
             "Rock" : ["Water", "Grass", "Fighting", "Ground", "Steel"],
             "Ghost" : ["Ghost", "Dark"],
             "Dragon" : ["Ice", "Dragon", "Fairy"],
             "Dark" : ["Fighting", "Bug", "Fairy"],
             "Steel" : ["Fire", "Fighting", "Ground"],
             "Fairy" : ["Poison", "Steel"]
             }

# If your pokemon is 'key' it will be strong when attacking the types in its 'values'
Attacking = {"Normal" : [],
             "Fire" : ["Grass", "Ice", "Bug", "Steel"],
             "Water" : ["Fire", "Ground", "Rock"],
             "Grass" : ["Water", "Ground", "Rock"],
             "Electric" : ["Water", "Flying"],
             "Ice" : ["Grass", "Ground", "Flying", "Dragon"],
             "Fighting" : ["Normal", "Ice", "Rock", "Dark", "Steel"],
             "Poison" : ["Grass", "Fairy"],
             "Ground" : ["Fire", "Electric", "Poison", "Rock", "Steel"],
             "Flying" : ["Grass", "Fighting", "Bug"],
             "Psychic" : ["Fighting", "Poison"],
             "Bug" : ["Grass", "Psychic", "Dark"],
             "Rock" : ["Fire", "Ice", "Flying", "Bug"],
             "Ghost" : ["Psychic", "Ghost"],
             "Dragon" : ["Dragon"],
             "Dark" : ["Psychic", "Ghost"],
             "Steel" : ["Ice", "Rock", "Fairy"],
             "Fairy" : ["Fighting", "Dragon", "Dark"]
             }

# e.g. your tepig may be weak defending against a water type, but you may have a grass pokemon that's strong when attacking them.

def recruitMon(mon):
    if mon == "full":
        return
    url = urlRoot + mon
    try:
        response = requests.get(url=url, timeout=timewait)
        response.raise_for_status()
        if response.status_code == 200:
            try:
                monJson = response.json()
                ids = []
                names = []
                cursor.execute("""SELECT * FROM pokemon
                                ORDER BY id""")
                for pokemon in cursor.fetchall():
                    ids.append(pokemon[0])
                    names.append(pokemon[1])
                # Check that the mon we're inserting is unique
                if mon in [str(i) for i in ids] or mon in names:
                    print(f"The pokemon you've selected is already part of your team!")
                    return
                # Check if we need to evict a mon to swap in this new one
                # if count == 6:
                if len(ids) == 6:
                    while True:
                        poison = input("Please enter the id or name of the pokemon you'd like to replace: ")
                        if poison in [str(i) for i in ids] or poison in names:
                            break
                        print(f"Invalid id, name, or doesn't exist in your team, try again.")
                    if poison in [str(i) for i in ids]:
                        cursor.execute("""DELETE FROM pokemon
                                        WHERE id = (?)""", (poison,))
                    else:
                        cursor.execute("""DELETE FROM pokemon
                                        WHERE name = (?)""", (poison,))
                    print(f"Pokemon {poison} deleted")
                # Insert the new pokemon!
                types = monJson["types"]
                if len(types) > 1: # 2 base types
                    types = types[0]["type"]["name"] + " " + types[1]["type"]["name"]
                else: # 1 base type
                    types = types[0]["type"]["name"]
                cursor.execute("""INSERT INTO pokemon (id, name, types) VALUES (?, ?, ?)""",
                               (monJson["id"], monJson["name"], types))
                if monJson["sprites"].get("other", "None") != "None" and monJson["sprites"]["other"].get("official-artwork", "None") != "None":
                    if random.randint(1, 4096) == 22:
                        print("what luck!")
                        webbrowser.open(monJson["sprites"]["other"]["official-artwork"]["front_shiny"])
                    else:
                        webbrowser.open(monJson["sprites"]["other"]["official-artwork"]["front_default"])
                else:
                    webbrowser.open(monJson["sprites"]["front_default"]) # unreachable, but cute pixelated sprite
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
            except Exception as e:
                print(f"Unknown exception during json decoding: {e}")
        else:
            print(f"HTTP status code error: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ReadTimeout as e:
        print(f"Timed out after {timewait} seconds: {e} (likely an invalid input)")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
    except Exception as e:
        print(f"Unknown exception: {e}")

def checkGaps(team):
    teamTypes = set()
    for pokemon in team:
        for pType in pokemon[2].split(" "):
            teamTypes.add(pType)
    teamWeaknesses = set()
    teamStrengths = set()
    for pType in teamTypes:
        for enemy in Defending[pType.capitalize()]: # we have at least one pokemon weak to these
            teamWeaknesses.add(enemy)
        for teammate in Attacking[pType.capitalize()]: # we have at least one pokemon who are strong against these
            teamStrengths.add(teammate)
    teamWeaknesses -= teamStrengths
    print(f"Your team is vulnerable against: {teamWeaknesses}!")
    randomType = random.choice(list(teamWeaknesses))
    url = urlTypeRoot + randomType
    try:
        response = requests.get(url=url, timeout=timewait)
        response.raise_for_status()
        try:
            enemyTypeJson = response.json()
            randomEnemyUrl = random.choice(enemyTypeJson["pokemon"])["pokemon"]["url"]
            try:
                response = requests.get(url=randomEnemyUrl, timeout=timewait)
                response.raise_for_status()
                if response.status_code == 200:
                    try:
                        enemyJson = response.json()
                        webbrowser.open(enemyJson["sprites"]["other"]["official-artwork"]["front_default"])
                        print(f"Your random vulnerability typed enemy is {enemyJson['name'].capitalize()}!!!\nThey are a {[i['type']['name'] for i in enemyJson['types']]} pokemon")
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error: {e}")
                    except Exception as e:
                        print(f"Unknown exception during json decoding: {e}")
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error: {e}")
            except requests.exceptions.ReadTimeout as e:
                print(f"Timed out after {timewait} seconds: {e} (likely an invalid input)")
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Request exception: {e}")
            except Exception as e:
                print(f"Unknown exception: {e}")
            # randomEnemy = randomEnemyUrl + ["sprites"]["other"]["official-artwork"]["front_default"]
            # webbrowser.open(randomEnemy)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Unknown exception during json decoding: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ReadTimeout as e:
        print(f"Timed out after {timewait} seconds: {e} (likely an invalid input)")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
    except Exception as e:
        print(f"Unknown exception: {e}")


def main():
    mon = None
    # count = 0 # We can get this from querying db if we saved it, but not part of the design
    while mon != "full":
        mon = input("Please select a pokemon's name or id to add to your team, enter \"full\" once you are done: ").lower()
        recruitMon(mon)
        cursor.execute("""SELECT * FROM pokemon
                        ORDER BY id""")
        team = cursor.fetchall()
        if len(team) == 0 and mon == "full":
            print("Your team has no pokemon!")
            mon = None
            continue
        else:
            print(f"Your team consists of: {team}")
    # TODO: Do something with the team
    checkGaps(team)
    cnxn.close() # no data commit necessary, since not going to be stored

if __name__ == '__main__':
    main()