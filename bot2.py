import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext
from keys import TELEGRAM_API_KEY, SECRET_CODE
import hashlib
import base64
import time

base_url = "http://127.0.0.1:8000/"

def generate_token(timestamp):
    code = hashlib.sha256((timestamp + SECRET_CODE).encode()).digest()
    encoded_code = base64.urlsafe_b64encode(code).decode().rstrip("=")
    return encoded_code

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def short(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    link = update.message.text.split()[1]

    timestamp = str(int(time.time()))
    token = generate_token(timestamp)

    headers = {
        'timestamp': timestamp,
        'token': token
    }
    params = {
        'link': link,
        'username': username,
        'first_name': first_name,
        'chat_id': chat_id
    }
    response = requests.get(base_url + 'short/', headers=headers, params=params)
    data = response.json()

    if data['status'] == 'success':
        update.message.reply_text(f"Shortened link: {data['shortened_link']}")
    else:
        update.message.reply_text("You have reached the trial limit. Please subscribe to continue.")

def check_user(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    timestamp = str(int(time.time()))
    token = generate_token(timestamp)

    headers = {
        'timestamp': timestamp,
        'token': token
    }
    params = {
        'chat_id': chat_id
    }
    response = requests.get(base_url + 'check_user/', headers=headers, params=params)
    data = response.json()

    update.message.reply_text(f"Subscription status: {data['sub_status']}")

def subscribe(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name

    timestamp = str(int(time.time()))
    token = generate_token(timestamp)

    headers = {
        'timestamp': timestamp,
        'token': token
    }
    params = {
        'user_id': chat_id,
        'first_name': first_name
    }
    response = requests.get(base_url + 'subscribe/', headers=headers, params=params)
    data = response.json()

    update.message.reply_text(f"Subscription status: {data['status']}")

def main() -> None:
    updater = Updater(TELEGRAM_API_KEY)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("short", short))
    dispatcher.add_handler(CommandHandler("check_user", check_user))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
