import os
import time

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from settings import settings
from chat_gpt import ChatPGT
from open_ai_dalle.main import Dalle

app = Client("my_account", settings.TG_ID, settings.TG_HASH)

COMMANDS = {"image": "/image"}


def get_answer(text: str) -> str:

    for i in range(4):
        answer = ChatPGT(text).get_answer()
        if answer:
            return answer
        time.sleep(5)
    print("Chat GPT did not respond")
    return ""


@app.on_message(filters.text)
async def my_handler(client, message):

    print(message.chat.id)

    if message.chat.id not in settings.CHATS_ID:
        # print(f"{message.chat.id} from: {message.from_user.username} text: {message.text}")
        return

    if message.from_user.id != settings.MY_ID or True:

        if message.text[0] == "*":
            return

        if COMMANDS["image"].lower() in message.text.lower():
            request = message.text.replace(COMMANDS["image"], "")

            img_name = await Dalle().create_an_image(request)

            if not img_name:
                await app.send_message(chat_id=message.chat.id, text="Повторите запрос позже")
                return

            img_path = os.path.join("image", img_name)

            await app.send_photo(chat_id=message.chat.id, photo=img_path)

        else:

            dialog = []

            while True:
                prev = None
                async for msg in app.get_chat_history(chat_id=message.chat.id, limit=8):

                    if not msg.text:
                        continue
                    if COMMANDS["image"].lower() in msg.text.lower():
                        continue

                    message_text = msg.text[1:] if msg.text[0] == "*" else msg.text

                    if msg.from_user.id != prev:
                        dialog.append(f"-{message_text}")
                    else:
                        prev = msg.from_user.id
                        dialog[-1] += f". {message_text}"

                if len(dialog) != 0:
                    print(dialog)
                    break
                else:
                    time.sleep(2)

            text = settings.REQUEST_PRFX + str("\n".join(reversed(dialog)) + ".")

            answer = get_answer(text)

            if not answer:
                return

            await app.send_message(chat_id=message.chat.id, text=f"*{answer}")


print("strt")

app.run()
