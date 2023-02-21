import sqlite3
import os
import json


class DB:
    db_url: str

    def __init__(self, db_url: str):
        self.db_url = db_url

        if not os.path.exists(self.db_url):
            self.init_db()

    def call_db(self, query, *args):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        res = cur.execute(query, args)
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def init_db(self):
        init_db_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            title TEXT NOT NULL
        );
        """
        
        seed_data = """
        INSERT INTO users (
        first_name,
        last_name,
        age,
        gender,
        title 
        ) VALUES (
        ?, ?, ?, ?, ?
        )
        """
        
        self.call_db(init_db_query)
        with open("seed.json", "r") as seed:
            data = json.load(seed)
        
        #logiken, tar varje objekt från data, och kallas för "user". Skapar sen en "person" med respektive charateristics nedan
        for user in data:
            self.call_db(seed_data, user["first_name"], user["last_name"],user["age"],user["gender"],user["title"])