import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import requests
import joblib
import json

# # QUARY SECTION

df = joblib.load("dataframe.joblib")

def gen_embed(texts):
    x = requests.post("http://localhost:11434/api/embed", json={
        "model" : "bge-m3",
        "input": texts
    })
    y = x.json()["embeddings"]
    return y


qust = input("Enter ur prompt : ")
qust_embed = gen_embed([qust])
# print(qust_embed[0])

shape_arr = np.array(qust_embed[0])
print(shape_arr.ndim)

print(df["embedding"])

similirity = cosine_similarity(np.vstack(df["embedding"]), [shape_arr])
maxSimilarities = similirity.flatten().argsort()[::-1][:5]
print(maxSimilarities)

simlar_Texts = df.loc[maxSimilarities]
print(simlar_Texts)


prompt = f"""
You are an intelligent teaching assistant for Krish Naik's Natural Language Processing (NLP) YouTube playlist, which has 12 videos.
Below are the subtitle chunks from the videos. Each chunk includes the video title, start time (in seconds), end time (in seconds), and the transcript text:

{simlar_Texts[["title", "start", "end", "text"]].to_json(orient="records")}

---------------------------------
"{qust}"

The user has asked this question related to the video content.

Your task:
- Answer the question in a **natural, human-like, and helpful way** (as if you are guiding a student).  
- Clearly mention **which video** and **what timestamp range** covers the explanation.  
- Encourage the user to **go to that video section** for more clarity.  
- If the question is **not related** to Krish Naik’s NLP course, politely reply:
  "I can only answer questions related to Krish Naik’s NLP course."

Important instructions:
- Do NOT mention or refer to the JSON or data format above in your answer.
- Do NOT fabricate timestamps or videos — only refer to information that appears in the given chunks.
- Keep your response **concise, natural, and easy to understand**.
"""


with open("quary.txt", "w") as f:
    f.write(prompt)


url = "http://localhost:11434/api/generate"
data = {
    "model": "tinyllama:1.1b",
    "prompt": prompt
}

# Send request
response = requests.post(url, json=data, stream=True)

# Process streaming response line by line
full_text = ""
for line in response.iter_lines():
    if line:
        json_data = json.loads(line.decode("utf-8"))
        if "response" in json_data:
            print(json_data["response"], end="", flush=True)
            full_text += json_data["response"]

print("\n\nFinal output:")
print(full_text)