from flask import Flask, render_template, request, jsonify
import requests, joblib, json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load embeddings
df = joblib.load("dataframe.joblib")

def gen_embed(texts):
    x = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": texts
    })
    y = x.json()["embeddings"]
    return y

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    qust = request.json["question"]

    qust_embed = gen_embed([qust])
    shape_arr = np.array(qust_embed[0])

    similirity = cosine_similarity(np.vstack(df["embedding"]), [shape_arr])
    maxSimilarities = similirity.flatten().argsort()[::-1][:5]
    simlar_Texts = df.loc[maxSimilarities]

    prompt = f"""
    You are an intelligent teaching assistant for Krish Naik's *Natural Language Processing (NLP)* YouTube playlist, which has 12 videos.

    Below are some related subtitle chunks from the course videos.
    Each chunk includes:
    - The video title
    - Start and end timestamps (in seconds)
    - The spoken text during that segment

    Subtitle Chunks:
    {simlar_Texts[["title", "start", "end", "text"]].to_json(orient="records")}

    ---------------------------------
    Student's Question:
    "{qust}"

    ---------------------------------
    Your task:
    - Answer the question in a **natural, teacher-like, and helpful** way.
    - Clearly mention **which video title** and **timestamp range** contain the answer.
    - Politely guide the student to **watch that part** of the video for better understanding.
    - If the question is **not related** to Krish Naik’s NLP course, respond:
    "I can only answer questions related to Krish Naik’s NLP course."

    Additional Instructions:
    - Do **NOT** mention or reference the JSON or data format above.
    - Do **NOT** invent timestamps or video titles — use only what’s provided.
    - Do **NOT** decribe any rules, just answer the qurary.
    - Keep your answer **short, friendly, and easy to understand**, like a real tutor.
    - ✅ At the end, output **only the final answer**, without showing your reasoning or internal analysis.
    """

    # prompt = "what is machine learning"
    # Send request to local Ollama

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "phi",
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
    # print(full_text)

    return jsonify({"answer": full_text})

if __name__ == "__main__":
    app.run(debug=True)
