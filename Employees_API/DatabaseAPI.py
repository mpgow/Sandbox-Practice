### Sample Dataset ###

practice_data = [
    {"name": "Alice Smith", "email": "alice@example.com", "date": "2026-03-15"}, 
    {"name": "Bob Jones", "email": "bob@example.com", "date": "2026-05-22"}, # valid (earliest)
    {"name": "Alice S.", "email": "alice@example.com", "date": "2026-01-10"}, # valid (earliest)
    {"name": "Charlie Brown", "email": "charlie@example.com", "date": "2026-03-05"}, # valid
    {"name": "Bob J.", "email": "bob@example.com", "date": "2026-08-11"},
    {"name": "Diana Prince", "email": "diana@example.com", "date": "2026-01-25"}, # valid
    {"name": "Eve Adams", "email": "eve@example.com", "date": "2026-05-01"} # valid
]

### 1. From a list of dicts(name, email, date), keep earliest record per email and print counts by month ###

ordered_months = {"01" : "January", "02" : "February", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}

# sort_practice_data = sorted(practice_data, key = lambda x: (x["date"][0:4], x["date"][5:7], x["date"][8:]))
sort_practice_data = sorted(practice_data, key = lambda x: (x["date"]))
seen = set()
monthly = {}
kept_data = []
for user in sort_practice_data:
    if user["email"] not in seen:
        seen.add(user["email"])
        monthly[user["date"][5:7]] = monthly.get(user["date"][5:7], 0) + 1
        kept_data += [user]

for month in ordered_months.keys():
    print(f"The month {ordered_months[month]} has {monthly.get(month, 0)} valid users")
for user in kept_data:
    print("Saved user:", user)

### employees.json ###

# [
# {
# "id": 1,
# "name": "Jane Doe",
# "email": "jane.doe@company.com",
# "department": "Engineering"
# },
# {
# "id": 2,
# "name": "John Smith",
# "department": "Marketing"
# },
# {
# "id": "three",
# "name": "Alex Johnson",
# "email": "alex.j@company.com",
# "department": "Sales"
# },
# {
# "id": 4,
# "name": "Sam Taylor",
# "email": "sam.taylor_at_company.com",
# "department": "HR"
# },
# {
# "id": 5,
# "name": "Chris Lee",
# "email": "chris.lee@company.com",
# "department": "Engineering"
# },
# {
# "id": 6,
# "name": "",
# "email": "empty.name@company.com",
# "department": "Support"
# }
# ]

# Dummy Issues: employee #2 missing email field, employee #3 has malformed id, employee #4 has malformed email, employee #6 has empty name

### #2. Read a JSON file of records and write valid ones to a CSV. Print each rejected record with a reason, and handle a missing file and bad JSON. ###

import json

def createCSV(employee_data): # Note, CSV has a DictWriter method meant to safely handle this scenario without so much manual steps, but this is just practice
    import csv
    fieldnames = list(employee_data[0].keys())
    CSV_fn = "employees.csv"
    CSV = open(CSV_fn, "w", newline="")
    try:
        writer = csv.writer(CSV)
        writer.writerow(fieldnames)
        for employee in employee_data:
            if not type(employee.get("id", "N/A, empty id")) == int or employee.get("id", "N/A, empty id") == "N/A, empty id":
                print(f"User id: {employee.get('id', 'N/A')} failed. Reason: invalid id")
                continue
            if not type(employee.get("name", 10)) == str or not employee.get("name"):
                print(f"User id {employee.get('id', 'N/A')} failed. Reason: invalid name")
                continue
            if "@" not in employee.get("email", "dog") or employee.get("email", "dog") == "dog":
                print(f"User id {employee.get('id', 'N/A')} failed. Reason: invalid email")
                continue
            if not type(employee.get("department", 10)) == str or employee.get("department", 10) == 10:
                print(f"User id {employee.get('id', 'N/A')} failed. Reason: invalid department")
                continue
            writer.writerow(employee.values())
    except Exception as e:
        print(f"Exception {e} occurred during CSV processing")
    finally:
        CSV.close()

file_name = input(f"please type in name of employee data with json extension: ") # "employees.json"
print(f"received: {file_name}")
json_file = None
try:
    json_file = open(file_name, "r", encoding="utf-8")
    raw_json = json_file.read() # can also just call dict_data = json.load(json_data), but read gives us a string that's also convertable
    employee_data = json.loads(raw_json)
    createCSV(employee_data)
except json.JSONDecodeError as e:
    print(f"Decode error during JSON handling: {e}")
except FileNotFoundError as e:
    print(f"Filename {file_name} does not exist, error: {e}")
finally:
    if json_file:
        json_file.close()

# [
#   {
#     "id": 1,
#     "name": "Leanne Graham",
#     "username": "Bret",
#     "email": "Sincere@april.biz",
#     "address": {
#       "street": "Kulas Light",
#       "suite": "Apt. 556",
#       "city": "Gwenborough",
#       "zipcode": "92998-3874",
#       "geo": {
#         "lat": "-37.3159",
#         "lng": "81.1496"
#       }
#     },
#     "phone": "1-770-736-8031 x56442",
#     "website": "hildegard.org",
#     "company": {
#       "name": "Romaguera-Crona",
#       "catchPhrase": "Multi-layered client-server neural-net",
#       "bs": "harness real-time e-markets"
#     }
#   },
#   {
#     "id": 2,
#     "name": "Ervin Howell",
#     "username": "Antonette",
#     "email": "Shanna@melissa.tv",
#     "address": {
#       "street": "Victor Plains",
#       "suite": "Suite 879",
#       "city": "Wisokyburgh",
#       "zipcode": "90566-7771",
#       "geo": {
#         "lat": "-43.9509",
#         "lng": "-34.4618"
#       }
#     },
#     "phone": "010-692-6593 x09125",
#     "website": "anastasia.net",
#     "company": {
#       "name": "Deckow-Crist",
#       "catchPhrase": "Proactive didactic contingency",
#       "bs": "synergize scalable supply-chains"
#     }
#   },
# ...
# ]

### #3. Call a public API with a timeout and specific exceptions, store a few fields in SQLite with placeholders, and query them back. ###

import requests
import sqlite3

url = "https://jsonplaceholder.typicode.com/users"
db = "placeholders.db"
try:
    response = requests.get(url, timeout=1) # 1 second timeout
    response.raise_for_status()
    if response.status_code != 200:
        print(f"Error code: {response.status_code}")
    try:
        placeholder_json = response.json()
        # fields = placeholder_json[0].keys()
        cnxn = sqlite3.connect(db)
        cursor = cnxn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL)""")
        for employee in placeholder_json:
            cursor.execute("""INSERT OR IGNORE INTO employees (id, name, email) VALUES (?, ?, ?)""", (employee["id"], employee["name"], employee["email"]))
            if cursor.rowcount == 0:
                print(f"Skipped inserting {employee['name']} since ID {employee['id']} already exists in the db")
        cnxn.commit()
        cursor.execute("""SELECT * FROM employees
                        ORDER BY RANDOM()
                        LIMIT 7""")
        for employee in cursor.fetchall():
            print(employee)
    except json.JSONDecodeError as e:
        print(f"Json decode error: {e}")
        exit()
    except Exception as e:
        print(f"Unknown error: {e}")
        exit()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ReadTimeout as e:
    print(f"Timed out beyond 1 second {e}")
except requests.exceptions.ConnectTimeout as e:
    print(f"Connection Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Exception during request")

