import os
from tkinter import filedialog
from pytube import YouTube
import requests
from PIL import Image
from io import BytesIO


def load_data():
    # Ask the user whether to download a video file, a YouTube video, a text file, or an audio file
    choice = int(input("Menu : \n1. Upload Video File \n2. YouTube Video \n3. Upload Audio file \n4. Upload Text File \n\nEnter Your Choice:"))
    if choice == 1:
        if os.environ.get("DISPLAY"):
            file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        else:
            # Provide an alternative method for file selection
            # For example, prompt the user to enter the file path via command-line input
            file_path = input("Enter the file path: ")
        # Download the audio from the video file
        ffmpeg_cmd = "ffmpeg -y -i \"{file_path}\" -acodec pcm_s16le -ar 16000 ytaudio.wav"
        os.system(ffmpeg_cmd)
        print("Done!")
        output_path = "ytaudio.wav"

    elif choice == 2:
        # Get the URL of the YouTube video
        # https://youtu.be/HQ8YLR3Rlv0
        VIDEO_URL = input("Enter the URL of the YouTube video: ")
        yt = YouTube(VIDEO_URL)
        thumbnail_url = yt.thumbnail_url
        response = requests.get(thumbnail_url)
        thumbnail_image = Image.open(BytesIO(response.content))
        try:
            yt.streams \
            .filter(only_audio=True, file_extension='mp4') \
            .first() \
            .download(filename='ytaudio.mp4')
            width, height = 800, 400  # Specify the desired width and height
            thumbnail_image = thumbnail_image.resize((width, height))
            #thumbnail_image.show()
        except KeyError:
            print("\n\n\n!!!SORRY!!!\b\bThe video is not available in your region or has been deleted/made private by the uploader.\n\n\n\n")

        # Download the audio from the YouTube video
        ffmpeg_cmd = "ffmpeg -y -i ytaudio.mp4 -acodec pcm_s16le -ar 16000 ytaudio.wav"
        os.system(ffmpeg_cmd)
        output_path = "ytaudio.wav"

    elif choice == 4:
        if os.environ.get("DISPLAY"):
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        else:
            # Provide an alternative method for file selection
            # For example, prompt the user to enter the file path via command-line input
            file_path = input("Enter the file path: ")
        # Process the text file as needed
        print(f"Processing text file: {file_path}")
        output_path = None  # No output path for text files

    elif choice == 3:
        if os.environ.get("DISPLAY"):
            file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        else:
            # Provide an alternative method for file selection
            # For example, prompt the user to enter the file path via command-line input
            file_path = input("Enter the file path: ")
        # Process the audio file as needed
        ffmpeg_cmd = "ffmpeg -y -i \"{file_path}\" -acodec pcm_s16le -ar 16000 .\"{output_path}\".wav"
        os.system(ffmpeg_cmd)
        print("Done")
        output_path = "music.wav"

    else:
        print("Invalid choice.")

    return output_path


