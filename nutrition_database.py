import sqlite3
import time
import requests
from ultralytics import YOLO    
from pathlib import Path


api_key = "rDnxbpHdHIfPXGxEsbEKZbvd8ic18vBtroBKAEVu"
print("DEBUG — текущий ключ:", api_key)
search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

db_path = "calories.db"
request_delay = 0.35

def fetch_nutrition(food_name:str) -> dict | None:
    params = {"api_key": api_key,"query":food_name,"pageSize":1,"dataType":["Foundation","SR Legacy"]}
    try:
        r = requests.get(search_url,params=params,timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"fail of network {e}")
        return None
    data = r.json()
    foods = data.get("foods",[])
    if not foods:
        return None
    
    food = foods[0]
    nutrients = {n["nutrientName"]: n.get("value") for n in food.get("foodNutrients", [])}
    return {
        "calories": nutrients.get("Energy"),
        "protein" : nutrients.get("Protein"),
        "fat" : nutrients.get("Total lipid (fat)"),
        "carbohydrates" : nutrients.get("Carbohydrate, by difference")
    }

def build_database(class_names:list[str],DB_PATH: str = db_path):
    conn = sqlite3.connect("calories.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_nutrition (
            class_name TEXT PRIMARY KEY,
            calories REAL,
            protein REAL,
            fat REAL,
            carbohydrates REAL,
            needs_review INTEGER DEFAULT 0
        )
        """)
    conn.commit()
    not_found = []
    found = 0

    for i,class_name in enumerate(class_names,1):
        query = class_name.replace("_"," ")
        print(f"[{i}/{len(class_names)}] search : {query}")
        data = fetch_nutrition(query)


        if data is None:
            print(f" -> Not Found")
            not_found.append(class_name)
            cur.execute("INSERT OR REPLACE INTO food_nutrition "
                "(class_name, calories, protein, fat, carbohydrates) "
                "VALUES (?, NULL, NULL, NULL, NULL)",
                (class_name,),
                )
        else:
            print(f"-> found:  ({data['calories']} ccal/100g)")
            found+=1
            cur.execute( "INSERT OR REPLACE INTO food_nutrition "
                "(class_name, calories, protein, fat, carbohydrates) "
                "VALUES (?, ?, ?, ?, ? )",
                (
                class_name,
                data['calories'],
                data['protein'],
                data['fat'],
                data['carbohydrates'] , 
            ) 
            ,
                )

        conn.commit()
        time.sleep(request_delay)

    conn.close()

    print("\n" + "=" * 50)
    print(f"Ready found:{found}/{len(class_names)}")
    if not_found:
        print(f"\nNot found({len(not_found)} -> add manually to your base)")
        for name in not_found:
            print(f'  - {name}')
        print(f"These lines are underlined needs_review = 1 in the table Food_nutrition"
        f"You can find them quickly by query:\n"
        f"  SELECT * FROM food_nutrition WHERE needs_review = 1;")

def get_nutrition(class_name:str) -> dict | None:
    conn = sqlite3.connect("calories.db")
    cur = conn.cursor()
    cur.execute("SELECT calories, protein, fat, carbohydrates FROM food_nutrition WHERE class_name = ?",
    (class_name,),)
    row = cur.fetchone()
    if row is None or row[0] is None:
        return None
    conn.close()
    if row is None:
        return None
    return {"calories": row[0], "protein": row[1], "fat": row[2], "carbohydrates": row[3]}

if __name__ == "__main__":



    model = YOLO("yolov8s.pt")
    class_names = list(model.names.values())

    build_database(class_names)

