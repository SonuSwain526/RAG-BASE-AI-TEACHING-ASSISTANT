import whisper
import os
import json

# # aud = whisper.transcribe("aud1.mp3")


# # mel = whisper.log_mel_spectrogram(aud, n_mels=model.dims.n_mels).to(model.device)
# # result = whisper.decode(model, aud)

# print(result["segments"])


# for x in result["segments"]:
#     chunk.append({"id": x["id"], "start": x["start"], "end": x["end"], "text": x["text"]})

# print(chunk)

# with open("chunk.json", "w") as f:
#     json.dump(chunk, f)

model = whisper.load_model("large-v3")

chunk = []

audios = os.listdir("audios")

for audio in audios:
    result = model.transcribe(audio=f"audios/{audio}", language = "hi", task = "translate", word_timestamps=False)
    title = audio.split(".")[0]

    for x in result["segments"]:
        chunk.append({"title": title,"id": x["id"], "start": x["start"], "end": x["end"], "text": x["text"]})

        final_chunk = {"chunk" : chunk, "text": result["text"]}

        with open(f"jsons/{title}.json", "w") as f:
            json.dump(final_chunk, f)

        
