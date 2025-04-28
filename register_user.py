import os
import sounddevice as sd
import wavio
from voiceauth.audioUtils import save_audio
import sys

import soundfile as sf
import numpy as np
import librosa
import wave

# def is_valid_wav(filepath):
#     try:
#         with wave.open(filepath, 'rb') as f:
#             return True
#     except wave.Error:
#         return False


# def modify_existing_wav_files(user_dir):
#     """
#     Modify all WAV files in the given directory to match these properties:
#     - Sample rate: 44100 Hz
#     - Channels: 1 (mono)
#     - Float32 format
#     - Sample width: 4 bytes
#     """
#     target_sample_rate = 44100

#     for filename in os.listdir(user_dir):
#         if filename.endswith('.wav'):
#             filepath = os.path.join(user_dir, filename)
#             print(f"[INFO] Processing: {filepath}")

#             if not is_valid_wav(filepath):
#                 print(f"[WARNING] Skipping invalid or corrupted WAV file: {filepath}")
#                 continue

#             try:
#                 data, sr = librosa.load(filepath, sr=target_sample_rate, mono=True)
#                 data = data.astype(np.float32)
#                 wavio.write(filepath, data, target_sample_rate, sampwidth=4)
#                 print(f"[INFO] Modified and saved: {filepath}")
#             except Exception as e:
#                 print(f"[ERROR] Failed to process {filepath}: {e}")


#     print(f"[INFO] All files in '{user_dir}' have been modified.")
# --------------------------------------------------------------------------------------------------------------------------------

# Example usage
# modify_existing_wav_files("Data/username")


# def record_audio_for_user(username):
#     """Record audio samples for the given user and save them."""
#     base_dir = 'Data'
#     user_dir = os.path.join(base_dir, username)

#     # Create a new directory for the user if it doesn't exist
#     os.makedirs(user_dir, exist_ok=True)
#     print(f"Recording will be saved in: {user_dir}")

#     # Predefined longer statement about technology
#     tech_statement = (
#         "Technology has transformed the way we communicate, learn, and interact with the world. "
#         "From smartphones to artificial intelligence, it shapes our daily lives and influences our decisions."
#     )

#     print(f"Please read the following statement:\n\"{tech_statement}\"")

#     # Record multiple samples for the user
#     num_samples = 5  # Change this number for more recordings
#     sample_rate = 44100
#     duration = 10  # Duration in seconds

#     for i in range(num_samples):
#         print(f"Recording {i+1}/{num_samples}... Press Enter to start.")
#         input()  # Wait for user to press Enter
#         recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
#         sd.wait()  # Ensure recording completes
        
#         print("Recording stopped. Press Enter to save the recording...")
#         input()  

#         # Define output file path
#         output_file = os.path.join(user_dir, f"sample_{i+1}.wav")
#         wavio.write(output_file, recording, sample_rate, sampwidth=4)
#         print(f"Recording {i+1} saved as {output_file}")

#     # Save the username to a file for later use
#     with open(os.path.join(base_dir, 'last_username.txt'), 'w') as f:
#         f.write(username)

#     return user_dir  # Return the path where audio samples are stored


# -------------------------------------------------------------------------------------------------------------------------------


import subprocess
import os

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
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <username>")
    #     sys.exit(1)
    
    # username = sys.argv[1]
    username = "sachin"
    user_dir = record_audio_for_user(username)
    print(f"Audio recordings for {username} are saved in {user_dir}")

if __name__ == "__main__":
    main()