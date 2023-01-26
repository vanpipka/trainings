import os
from pytube import YouTube, Stream
from services import create_path, get_file_name, get_path_from_file_name

PATH_FOR_DATA = os.path.join(os.curdir, "data")

def on_progress_callback(stream: Stream, chunk: int, bytes_remaining: int) -> None:
    print(f"downloading {stream.title} {stream.mime_type}")
    print(f"bytes_remaining: {bytes_remaining}")


def download_stream(stream: Stream, file_name: str) -> bool:

    if not file_name:
        raise ValueError("The file_name should not be an empty string")

    stream.download(output_path=get_path_from_file_name(file_name), filename=get_file_name(file_name))

    if not os.path.isfile(file_name):
        print(f"{stream.title} {stream.mime_type} was not download")
        return False

    print(f"{stream.title} {stream.mime_type} has been downloaded")

    return True


def download_data_from_youtube(url: str, save_audio: bool) -> dict:
    if not url:
        raise ValueError("The url should not be an empty string")

    yt = YouTube(url, on_progress_callback=on_progress_callback)

    create_path(f"{PATH_FOR_DATA}\{yt.video_id}")
    streams = yt.streams

    video_480 = streams.filter(res='480p').desc().first()

    if video_480 is None:
        return {"audio": {
                    "has_been_downloaded": False,
                    "url": ""},
                "video": {
                    "has_been_downloaded": False,
                    "url": ""}
                }

    video_file_name = f"{PATH_FOR_DATA}\{yt.video_id}\\video.webm"
    video_has_been_downloaded = download_stream(video_480, video_file_name)

    if save_audio:
        audio_file_name = f"{PATH_FOR_DATA}\{yt.video_id}\\audio.mp3"
        audio_best = streams.filter(only_audio=True).desc().first()
        audio_has_been_downloaded = download_stream(audio_best, audio_file_name)
    else:
        audio_has_been_downloaded = False
        audio_file_name = ""

    return {"audio": {
                "has_been_downloaded": audio_has_been_downloaded,
                "url": audio_file_name},
            "video": {
                "has_been_downloaded": video_has_been_downloaded,
                "url": video_file_name},
            }

