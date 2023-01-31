import os
import openai
import asyncio
import requests
from settings import settings as _st


openai.api_key = _st.OPEN_AI_KEY  # os.environ.get("OPENAI_API_KEY")


class ChatPGT:

    def __init__(self, phrase: str) -> None:

        self.phrase = phrase
        self._response = {}

    def get_answer(self) -> str:

        result = ""

        try:

            self._response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=self.phrase,
                        max_tokens=200,
                        temperature=0.8)

            for answer in self._response.get("choices", []):
                result += answer["text"]

        except openai.error.OpenAIError as e:
            print(e.http_status)
            print(e.error)
            print(e.args)

        return result


def main():

    phrase = "I have already told everyone no hookahs in our house and other smoking.Well, " \
             "like let them do what they want, but if not with us)"

    print(ChatPGT(phrase).get_answer())


if __name__ == "__main__":
    main()


