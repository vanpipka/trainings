import os
import openai
import asyncio
import requests
from settings import settings as _st


openai.api_key = _st.OPEN_AI_KEY
IMAGE_DIR = "image"


def create_path(image_dir):
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)


class Dalle():

    def __init__(self):

        self.image_dir = os.path.join(os.curdir, IMAGE_DIR)
        self.generation_response = ""
        self.prompt = ""

        create_path(self.image_dir)

    async def create_an_image(self, prompt):

        self.prompt = prompt

        try:
            self.generation_response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="url",
            )

            for i in range(len(self.generation_response["data"])):

                file_name = f"{self.generation_response['created']}_{i}.png"

                Dalle._save_image_(file_name,
                                   self.image_dir,
                                   self.generation_response["data"][i]["url"])

            return file_name

        except openai.error.OpenAIError as e:
            print(e.http_status)
            print(e.error)

        return ""

    @staticmethod
    def _save_image_(file_name, img_dir, url):
        generated_image_name = file_name  # any name you like; the filetype should be .png
        generated_image_filepath = os.path.join(img_dir, generated_image_name)
        generated_image_url = url  # extract image URL from response
        generated_image = requests.get(generated_image_url).content  # download the image

        with open(generated_image_filepath, "wb") as image_file:
            image_file.write(generated_image)  # write the image to the file


async def gather_data():

    phrases = ["a knight cat with tomato sword, digital art",
               "a knight cat with cucumber sword, digital art",
               "a knight cat with icecream sword, digital art"]

    tasks = []

    for i in range(len(phrases)):
        tasks.append(asyncio.create_task(Dalle().create_an_image(phrases[i])))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(gather_data())
