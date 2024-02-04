import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
import asyncio
from openai import AsyncOpenAI

import bing_image_creator_api
import asyncio, json
import webbrowser
from getpass import getpass

from re_edge_gpt import Chatbot
from re_edge_gpt import ConversationStyle

# cookies = json.loads(open("bing_cookies_.json.txt", encoding="utf-8").read())  # might omit cookies option

from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
from bard_webapi.client import BardClient
Secure_1PSID = "g.a000gAhVLfi_x9TYZ2N3EqoPXavTK8z3fetx90_oufJKnr6NI2932KhKNUtmUZlLTUz7kjF_CQACgYKAdESAQASFQHGX2Midnijj9nbI-SPMIhjd2v7AhoVAUF8yKpiHay0OI8bFjSXw8Lemdr10076"
Secure_1PSIDTS = "sidts-CjIBPVxjSqfIYv_t3vmgqb5eAdbyef8X2PYm_anzRB0191x2I4KWey90MgC9CB5VrbyXhBAA"
Secure_1PSIDCC = "ABTWhQEJ_33KYFM6JpospwZOJZ6C7mAXxj3ni_Lv2VAiM6iZr1BAy7ueJbFbb36qUZoulxQU4Q"
token = Secure_1PSID



urlProdia = "https://api.prodia.com/v1/sdxl/generate"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Prodia-Key": "1008a105-be30-4564-b5d2-edbd4e6a5c3d"
}

OPEN_AI_TOKEN = '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'
OPEN_AI_TOKEN_1 = "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"

Bing_token = '11lIObjnPIrqXnadfn5I2rznuFqY2o-0iJsrSTyGM_iZLc7IkQkNqJRITEbk0dy28r7QBkKDxUwQHcN9Q3iFljBSL-16U1RMnWsmV5zZUNSr03vZh4P6oljcniupjlK-Uy-nRTUpKDRvJ0HUuys9T0jfRLqRXVUBu2FX06XMfaVPhtelkw1rfQqbfTmsiGz3u3uzOZORQIU5PGNglmH6fKy8M_4y-rcOCM9Y_wxfbHvk'

async def main(text: str):
    client = AsyncOpenAI(api_key=OPEN_AI_TOKEN)
    completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
        model="gpt-3.5-turbo",
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content


BOT_TOKEN = '6835942108:AAGHZaU6eDoPmVbzPJcjopy953eFm7l5P_E'

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # reply = asyncio.run(main())
    # await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    args = context.args
    text = " ".join(args)
    print(text)
    reply = await main(text)
    print(reply)
    await update.message.reply_text(reply)
    return

async def get_image_promt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    text = " ".join(args)
    print(text)
    urls = await bing_image_creator_api.create(Bing_token, text)
    print(urls)
    # await update.message.reply_text(urls[0])
    # await update.message.reply_text(urls[1])
    # await update.message.reply_text(urls[2])
    # await update.message.reply_text(urls[3])
    for url in urls:
        await update.message.reply_photo(url)
    return

async def prodia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    text = " ".join(args)
    print(text)
    payload = {"prompt": text}
    response = requests.post(urlProdia, headers=headers, json=payload)
    print(response.text)
    job = response.json().get("job")
    #wait for 10 seconds
    await asyncio.sleep(10)
    try:
        url = f"https://api.prodia.com/v1/job/{job}"
        response = requests.get(url, headers=headers)
        urlImage = response.json().get("imageUrl")
        # print(urlImage)
        await update.message.reply_photo(urlImage)
        # await update.message.reply_photo(urlImage)
        return
    except:
        await update.message.reply_text("Error wait for 5 more seconds")
        try:
            url = f"https://api.prodia.com/v1/job/{job}"
            response = requests.get(url, headers=headers)
            urlImage = response.json().get("imageUrl")
            # print(urlImage)
            await update.message.reply_photo(urlImage)
            # await update.message.reply_photo(urlImage)
        except:
            await update.message.reply_text("Error cant generate the image")
            return

async def bing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    text = " ".join(args)
    print(text)
    cookies = json.loads(open("bing_cookies_.json.txt", encoding="utf-8").read())
    try:
        reply = await bing_ask(text)
        send = reply.get("text")
        sources = reply.get("sources")
        print(sources)
        #add sources to send
        # for source in sources:
        #     send += "\n" + source.get("text")
        await update.message.reply_text(send)
    except Exception as e:
        print(e)
        return await update.message.reply_text("Error")

async def create_bot():
    cookies = json.loads(open("bing_cookies_.json.txt", encoding="utf-8").read())
    bot = await Chatbot.create(cookies=cookies)
    response = await bot.ask(
        prompt='what time is it in London?',
        conversation_style=ConversationStyle.balanced,
        simplify_response=True
    )
    # If you are using non ascii char you need set ensure_ascii=False
    print(json.dumps(response, indent=2, ensure_ascii=False))
    # Raw response
    # print(response)
    assert response
    return bot.close()

async def bing_ask(prompt) -> None:
    try:
        cookies = json.loads(open("bing_cookies_.json.txt", encoding="utf-8").read())
        bot = await Chatbot.create(cookies=cookies)
        response = await bot.ask(
            prompt=prompt,
            conversation_style=ConversationStyle.balanced,
            simplify_response=True
        )
        # If you are using non ascii char you need set ensure_ascii=False
        print(json.dumps(response, indent=2, ensure_ascii=False))
        # Raw response
        # print(response)
        assert response
        bot.close()
        return response
    except Exception as error:
        raise error

# app.add_handler(CommandHandler("bing", bing))
# app.add_handler(CommandHandler("bard", bard))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("prodia", prodia))
    app.add_handler(CommandHandler("image", get_image_promt))
    app.add_handler(CommandHandler("bing", bing))

    try:
        app.run_polling()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        app.stop_running()
        app.stop()


