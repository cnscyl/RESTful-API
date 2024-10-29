from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd


app = FastAPI()


class PillowData(BaseModel):
    id: int
    snore_rate: float
    respiration_rate: float
    body_temperature: float
    limb_movement: float
    blood_oxygen: float
    eye_movement: float
    sleeping_hours: float
    heart_rate: float
    stress_level: float


file_path = "C:\\Users\\cansu\\OneDrive\\Desktop\\SaYoPillow.csv"


def get_db_connection():
    conn = sqlite3.connect("pillow_data.db", check_same_thread=False)
    return conn

def populate_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS pillow_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snore_rate REAL,
        respiration_rate REAL,
        body_temperature REAL,
        limb_movement REAL,
        blood_oxygen REAL,
        eye_movement REAL,
        sleeping_hours REAL,
        heart_rate REAL,
        stress_level REAL
    )''')
    
    
    df = pd.read_csv(file_path)
    
    
    first_10_rows = df.head(10)
    
    
    for _, row in first_10_rows.iterrows():
        cursor.execute('''INSERT INTO pillow_data 
                          (snore_rate, respiration_rate, body_temperature, limb_movement, blood_oxygen, 
                          eye_movement, sleeping_hours, heart_rate, stress_level) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (row['snore_rate'], row['respiration_rate'], row['body_temperature'], row['limb_movement'], 
                        row['blood_oxygen'], row[' eye_movement'], row['sleeping_hours'], 
                        row['heart_rate'], row['stress_level']))
    
    conn.commit()
    conn.close()


populate_initial_data()

def clean_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        
        cursor.execute('''DELETE FROM pillow_data 
                          WHERE id NOT IN (SELECT id FROM pillow_data ORDER BY id LIMIT 10)''')
        conn.commit()
    except Exception as e:
        print(f"Error cleaning database: {e}")
    finally:
        conn.close()


clean_database()




@app.get("/data")
def get_all_data():
    conn = get_db_connection()  
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pillow_data LIMIT 10")  
        data = cursor.fetchall()
        return data
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()  



@app.get("/data/{item_id}")
def get_data_by_id(item_id: int):
    conn = get_db_connection()  
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pillow_data WHERE id=?", (item_id,))
        data = cursor.fetchone()
        if not data:
            return {"message": f"No data found for ID {item_id}"}
        return data
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()  


@app.post("/data")
def create_data(item: PillowData):
    conn = get_db_connection()  
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO pillow_data 
                          (snore_rate, respiration_rate, body_temperature, limb_movement, blood_oxygen, 
                          eye_movement, sleeping_hours, heart_rate, stress_level) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (item.snore_rate, item.respiration_rate, item.body_temperature, item.limb_movement, 
                        item.blood_oxygen, item.eye_movement, item.sleeping_hours, 
                        item.heart_rate, item.stress_level))
        conn.commit()
        return {"message": "Data added successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()  

@app.put("/data/{item_id}")
def update_data(item_id: int, item: PillowData):
    conn = get_db_connection()  
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE pillow_data SET 
                          snore_rate=?, respiration_rate=?, body_temperature=?, limb_movement=?, blood_oxygen=?, 
                          eye_movement=?, sleeping_hours=?, heart_rate=?, stress_level=? 
                          WHERE id=?''', 
                       (item.snore_rate, item.respiration_rate, item.body_temperature, item.limb_movement, 
                        item.blood_oxygen, item.eye_movement, item.sleeping_hours, 
                        item.heart_rate, item.stress_level, item_id))
        conn.commit()
        return {"message": "Data updated successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()  

@app.delete("/data/{item_id}")
def delete_data(item_id: int):
    conn = get_db_connection()  
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pillow_data WHERE id=?", (item_id,))
        conn.commit()
        return {"message": "Data deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()  