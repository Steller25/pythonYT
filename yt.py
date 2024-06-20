from pytube import YouTube
import os
import subprocess
import re

def sanitize_filename(filename):
    # Usunięcie znaków specjalnych
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_youtube_video(url):
    try:
        # Tworzenie obiektu YouTube
        yt = YouTube(url)

        # Pobieranie strumienia wideo o najwyższej dostępnej jakości
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()

        # Pobieranie strumienia audio o najwyższej dostępnej jakości
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()

        # Pobieranie wideo
        print(f"Pobieranie wideo: {yt.title}")
        video_stream.download(filename='video.mp4')

        # Pobieranie audio
        print(f"Pobieranie audio: {yt.title}")
        audio_stream.download(filename='audio.mp4')

        # Sanitacja nazwy pliku wyjściowego
        output_filename = sanitize_filename(yt.title) + ".mp4"

        # Łączenie wideo i audio za pomocą ffmpeg
        print("Łączenie wideo i audio...")
        command = f"ffmpeg -i video.mp4 -i audio.mp4 -c copy \"{output_filename}\""
        subprocess.run(command, shell=True, check=True)

        # Usuwanie tymczasowych plików
        os.remove('video.mp4')
        os.remove('audio.mp4')

        print(f"Pobieranie zakończone! Plik zapisany jako: {output_filename}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    # Przykładowy URL filmu z YouTube
    url = input("Podaj URL filmu z YouTube: ")
    download_youtube_video(url)
