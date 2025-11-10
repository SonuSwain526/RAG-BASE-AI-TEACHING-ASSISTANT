import subprocess
import os

inpdir = "videos/"
opdir = "audios/"

if(os.path.exists(opdir)):
    print("exist")
else:
    os.makedirs("audios")
    print("audio dir created")

listdir = os.listdir("videos/")

for i in range(0,12):
    # inpfile = f"videos/vid{i}.mp4"
    # opfile = f"audios/aud{i}.mp3"

    command = [
        "ffmpeg",
        "-i",
        f"videos/{listdir[i]}",
        f"audios/{listdir[i].split(".")[0]}.mp3"
    ]
    print(listdir[i])

    subprocess.run(command)
    print(f"audio {i} createed !")

#