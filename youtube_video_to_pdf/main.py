import os
from typing import List
from download_video import download_data_from_youtube

from create_pictures_from_video import create_pictures_from_video


def get_url_list() -> List[str]:
    url_lst = [{"url": "https://www.youtube.com/watch?v=JpyIwVhmEtM", "save_mp3": True},
               {"url": "https://www.youtube.com/watch?v=FYwVTA4CL8A", "save_mp3": False}]
    return url_lst


def main():

    for i in get_url_list():
        files_data = download_data_from_youtube(i["url"], i["save_mp3"])
        video_data = files_data.get("video", {})
        if video_data.get("has_been_downloaded", False):
            video_file_name = video_data.get("url", "")
            create_pictures_from_video(video_file_name)
            os.remove(video_file_name)


if __name__ == "__main__":
    main()
