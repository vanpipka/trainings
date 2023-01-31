import time

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from settings import settings
from chat_gpt import ChatPGT


app = Client("my_account", settings.TG_ID, settings.TG_HASH)


def get_answer(text: str) -> str:

    for i in range(4):
        answer = ChatPGT(text).get_answer()
        if answer:
            return answer
        print("Chat GPT - overloaded")
        time.sleep(3)

    return "Не понял("


@app.on_message(filters.text)
async def my_handler(client, message):

    if message.chat.type != ChatType.PRIVATE:
        print(message.chat.type)
        return

    if message.chat.id not in [124635813, 186378602, 902507223, 5019955107, 109701896]:
        print(f"{message.chat.id} from: {message.from_user.username} text: {message.text}")
        return

    if message.from_user.id != 124635813:

        dialog = []

        while True:
            async for msg in app.get_chat_history(chat_id=message.chat.id, limit=8):
                dialog.append(f"-{msg.text}")

            if len(dialog) != 0:
                break
            else:
                time.sleep(2)

        text = "Ответь на последнюю фразу, отвечай на ТЫ и максимально дерзко:" + str("\n".join(reversed(dialog)) + ".")

        answer = get_answer(text)

        await app.send_message(chat_id=message.chat.id, text=answer)


print("strt")

app.run()
