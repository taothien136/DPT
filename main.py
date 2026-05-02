from audio import Sound
from features_extract import Init, Extract
from kdtree import CustomKDTree, Queries
import pickle
import os

while True:
    query = input(">")
    if query == "exit": break
    else:
        file_path = "query/" + query
        if not os.path.isfile(file_path): print(f"File {file_path} was not found.")
        else:
            import sqlite3
            import numpy as np
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT path, features, shape FROM sounds")
            rows = c.fetchall()
            sounds = []
            for row in rows:
                path = row[0]
                shape = eval(row[2])
                features = np.frombuffer(row[1], dtype=np.float64).reshape(shape)
                sounds.append(Sound(features=features, path=path))
            conn.close()

            queries = Queries(sounds=sounds)

            extract = Extract(sound_path=file_path)
            vector = extract.features()
            q = Sound(features=vector, path=file_path)
            
            results = queries.query(input=q,k=5)
            for r in results:
                print(r)
            print()
