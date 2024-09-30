# save from .sql file to sqlite
import sqlite3
import os

def save2db():
    # delete output.db first, if it exists
    if os.path.exists("output.db"):
        os.remove("output.db")

    conn = sqlite3.connect("output.db")
    c = conn.cursor()

    with open("output.sql", "r") as file:
        sql = file.read()
        c.executescript(sql)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    save2db()