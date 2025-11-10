import os
# import ollama
import json
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

def gen_embed(texts):
    x = requests.post("http://localhost:11434/api/embed", json={
        "model" : "bge-m3",
        "input": texts
    })
    y = x.json()["embeddings"]
    return y


dflist = []
# for file in sorted(os.listdir("jsons")):
for file in sorted(os.listdir("modifiedjsons")):
    with open(f"modifiedjsons/{file}") as f:
        # content = f.read()
        data = json.load(f)
    embeddings = gen_embed([c["text"] for c in data["chunk"]])

    for i, chunk in enumerate(data["chunk"]):
        chunk["embedding"] = embeddings[i]
        dflist.append(chunk)
    print(f"embedding done for file {file}")


df = pd.DataFrame.from_records(dflist)
df.to_csv("data.csv")
joblib.dump(df, "dataframe.joblib")