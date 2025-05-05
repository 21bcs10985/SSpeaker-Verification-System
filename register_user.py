import os
import sounddevice as sd
from voiceauth.audioUtils import save_audio

import soundfile as sf
import numpy as np
import subprocess

def convert_webm_to_wav(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".webm"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.splitext(input_path)[0] + ".wav"
            
            # Use subprocess to call ffmpeg
            command = [
                "ffmpeg",
                "-y",                # Overwrite output without asking
                "-i", input_path,     # Input file
                output_path          # Output file
            ]
            subprocess.run(command, check=True)

            os.remove(input_path)
            print(f"Converted and removed: {filename}")



# -------------------------------------------------------------------------------------------------------------------------------

import os

def record_audio_for_user(username):
    """
    Skip terminal recording. Just return the directory path where frontend uploads audio.
    """

    base_dir = 'Data'
    user_dir = os.path.join(base_dir, username)

    convert_webm_to_wav(user_dir)

    # user_dir = os.path.join("Data", username)  # Match upload path from app.py
    print(f"[INFO] Using uploaded recordings at: {user_dir}")
    return user_dir


def main():

    username = "sachin"
    user_dir = record_audio_for_user(username)
    print(f"Audio recordings for {username} are saved in {user_dir}")

if __name__ == "__main__":
    main()
