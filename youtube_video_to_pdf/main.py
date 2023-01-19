import os
from typing import List

from pytube import YouTube, Stream

PATH_FOR_DATA = os.path.join(os.curdir, "data")
PATH_FOR_VIDEO = os.path.join(os.curdir, "data\\videos")
PATH_FOR_PDF = os.path.join(os.curdir, "data\\pdf")
PATH_FOR_MP4 = os.path.join(os.curdir, "data\\mp4")


def check_or_create_paths() -> None:
    def create_path(folder: str) -> None:
        if not os.path.isdir(folder):
            os.mkdir(folder)

    create_path(PATH_FOR_DATA)
    create_path(PATH_FOR_PDF)
    create_path(PATH_FOR_VIDEO)
    create_path(PATH_FOR_MP4)


def on_progress_callback(stream: Stream, chunk: int, bytes_remaining: int) -> None:
    print(f"downloading {stream.title} {stream.mime_type}")
    print(f"bytes_remaining: {bytes_remaining}")


def download_stream(stream: Stream, path: str, file_name: str) -> bool:
    if not path:
        raise ValueError("The path should not be an empty string")
    if not file_name:
        raise ValueError("The file_name should not be an empty string")

    stream.download(output_path=path, filename=file_name)

    if not os.path.isfile(f"{path}\{file_name}"):
        print(f"{stream.title} {stream.mime_type} was not download")
        return False

    print(f"{stream.title} {stream.mime_type} has been downloaded")

    return True


def download_data_from_youtube(url: str) -> str:
    if not url:
        raise ValueError("The url should not be an empty string")

    yt = YouTube(url, on_progress_callback=on_progress_callback)
    streams = yt.streams

    video_480 = streams.filter(res='480p').desc().first()
    audio_best = streams.filter(only_audio=True).desc().first()

    if video_480 is None:
        return ""

    video_has_downloaded = download_stream(video_480, PATH_FOR_VIDEO, f"{yt.video_id}.webm")
    audio_has_downloaded = download_stream(audio_best, PATH_FOR_MP4, f"{yt.video_id}.mp4")

    return f"{yt.video_id}"


def get_url_list() -> List[str]:
    url_lst = ["https://www.youtube.com/watch?v=VaywXwjQ84c&list=PLg78ckjpHfZy5lkbq8bw26rLXkZ8jLRUN"]
    return url_lst


def main():
    check_or_create_paths()

    for i in get_url_list():
        file_name = download_data_from_youtube(i)
        if file_name:
            # create_pdf
            pass


if __name__ == "__main__":
    main()
