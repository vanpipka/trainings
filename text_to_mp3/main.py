from typing import List
import os

from gtts import gTTS
import requests
import json

PATH = os.path.join(os.curdir, "mp3")


def get_some_word(url: str) -> List[str]:

    if not url:
        raise ValueError("The URL should not be an empty string")

    try:
        r = requests.get(url)
    except requests.exceptions.HTTPError as e:
        raise ValueError("Invalid HTTP response or regular unsuccesful (4xx/5xx)")
    except requests.exceptions.RequestException as e:
        raise ValueError("Invalid URL: No scheme supplied.")
    except:
        raise ValueError("There was an ambiguous exception that occurred while handling your request.")

    if r.status_code == 200:
        data = json.loads(r.text)
        return [i["text"].split(",")[0] for i in data["data"]]
    else:
        return []


def create_path(image_dir: str) -> None:
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)


def text_to_mp3(text: str, file_name: str, lanuage: str = "de") -> bool:

    if not file_name:
        raise ValueError("The file_name should not be an empty string")

    my_audio = gTTS(text=text, lang=lanuage, slow=False)

    try:
        my_audio.save(file_name)
    except FileNotFoundError:
        raise FileNotFoundError("No such file or directory")

    return True


def main():
    create_path(PATH)

    words_lst = get_some_word("http://start-deutsch.ru/quiz/api/get_random_words?count=10")

    for word in words_lst:
        file_name = f"{PATH}\{word}.mp3"
        if text_to_mp3(word, file_name, "de"):
            print(f"file {word} has been created")
        else:
            print(f"file {word} was not created")


if __name__ == "__main__":
    main()
