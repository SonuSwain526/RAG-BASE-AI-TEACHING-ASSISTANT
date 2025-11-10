import os
import subprocess

vidList = os.listdir("videos")
print(vidList)

for video in vidList:
    if(vidList != "Hindi-Introduction And Roadmap To Learn Natural Language Processing(NLP)_Krish Naik(1).mp4"):
    # video = "input.mp4"  # Replace with your actual video filename
        output_pattern = f"ex/{video}_%03d.mp4"

        subprocess.run([
            "ffmpeg",
            "-i", f"videos/{video}",
            "-acodec", "copy",
            "-vcodec", "copy",
            "-f", "segment",
            "-segment_time", "240",
            "-reset_timestamps", "1",
            output_pattern
        ])
