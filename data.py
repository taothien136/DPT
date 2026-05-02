import sqlite3
import numpy as np

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("SELECT path, features, shape FROM sounds")
rows = c.fetchall()

with open("data.txt","w") as f:   
    for row in rows:
        path = row[0]
        shape = eval(row[2])
        features = np.frombuffer(row[1], dtype=np.float64).reshape(shape)
        f.write(f"{path}:\n{features}\n")

conn.close()
