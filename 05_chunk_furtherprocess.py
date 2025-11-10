import json
import os

files = os.listdir("jsons")


for file in files:    
    with open(f"jsons\{file}", "r") as f:
        content = json.load(f)
    summed_chunk = []


    for i in range(0, len(content["chunk"]), 5):
        group = content["chunk"][i:i+5]

        combined_text = " ".join(item["text"].strip() for item in group)
        start_time = group[0]["start"]
        end_time = group[-1]["end"]

        summed_chunk.append({
            "title": group[0]["title"],
            "start": start_time,
            "end": end_time,
            "text": combined_text
        })
        # print([item["text"] for item in content["chunk"][1:6]])

        # print((summed_chunk))
        final_json = {
        "chunk": summed_chunk,
        "text": content["text"]
        }

    with open(f"modifiedjsons/{file}", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)