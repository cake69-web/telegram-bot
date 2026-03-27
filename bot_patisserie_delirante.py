import requests
import time

BOT_TOKEN ="
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

INSTAGRAM_URL = "https://www.instagram.com/patisseriedelirante?igsh=bjltYjN4bXZmZTc1&utm_source=qr"
CANAL_URL = "https://t.me/patisseriedelirante"
IMAGE_FILE_ID = "AgACAgQAAxkBAAPVacXRfwrVEExOx5nnWQ0l14kZ_4EAAsIMaxs5pjFSnXnSyjIDhawBAAMCAAN5AAM6BA"

def send_main_menu(chat_id):
    caption = (
        "🍰 Pâtisserie Délirante\n\n"
        "Bienvenue sur la Mini App de Pâtisserie Délirante 🌍\n\n"
        "Ici tu accèdes directement à nos menus, nos drops et nos services.\n\n"
        "💎 Produits sélectionnés\n"
        "🚀 Nouveaux drops réguliers\n"
        "📦 Commande simple et rapide\n\n"
        "Utilise les boutons ci-dessous pour voir :\n"
        "• les menus\n"
        "• les disponibilités\n"
        "• les offres du moment\n\n"
        "👇 Choisis une section pour commencer."
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "💾 Canal", "url": CANAL_URL},
                {"text": "🥔 Potato", "callback_data": "potato"}
            ],
            [
                {"text": "📸 Instagram", "url": INSTAGRAM_URL}
            ],
            [
                {"text": "🍽️ Menu Mini-App", "callback_data": "mini_app"}
            ],
            [
                {"text": "📝 Commander", "callback_data": "commander"},
                {"text": "💬 Informations", "callback_data": "infos"}
            ],
            [
                {"text": "📞 Plus de contacts", "callback_data": "contacts"}
            ]
        ]
    }

    response = requests.post(
        f"{BASE_URL}/sendPhoto",
        json={
            "chat_id": chat_id,
            "photo": IMAGE_FILE_ID,
            "caption": caption,
            "reply_markup": reply_markup
        }
    )
    print("send_main_menu:", response.text)

def send_text(chat_id, text):
    response = requests.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )
    print("send_text:", response.text)

def answer_callback(callback_query_id, text=""):
    response = requests.post(
        f"{BASE_URL}/answerCallbackQuery",
        json={
            "callback_query_id": callback_query_id,
            "text": text
        }
    )
    print("answer_callback:", response.text)

offset = None

while True:
    params = {"timeout": 30}
    if offset is not None:
        params["offset"] = offset

    response = requests.get(f"{BASE_URL}/getUpdates", params=params)
    data = response.json()

    for update in data.get("result", []):
        offset = update["update_id"] + 1

        if "message" in update:
            message = update["message"]
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")

            if not chat_id:
                continue

            if text == "/start":
                send_main_menu(chat_id)

        elif "callback_query" in update:
            callback = update["callback_query"]
            callback_id = callback["id"]
            data_clicked = callback.get("data", "")
            chat_id = callback.get("message", {}).get("chat", {}).get("id")

            if not chat_id:
                continue

            if data_clicked == "potato":
                answer_callback(callback_id, "Potato 🥔")
                send_text(chat_id, "Potato 🥔")

            elif data_clicked == "mini_app":
                answer_callback(callback_id, "Menu Mini-App")
                send_text(chat_id, "Ici tu pourras mettre ta mini-app plus tard.")

            elif data_clicked == "commander":
                answer_callback(callback_id, "Commander")
                send_text(
                    chat_id,
                    "📝 Commander\n\nDis-moi ce que tu veux commander 🍰"
                )

            elif data_clicked == "infos":
                answer_callback(callback_id, "Informations")
                send_text(
                    chat_id,
                    "💬 Informations\n\nHoraires : 9h - 19h\nAdresse : à compléter"
                )

            elif data_clicked == "contacts":
                answer_callback(callback_id, "Contacts")
                send_text(
                    chat_id,
                    "📞 Plus de contacts\n\nTéléphone : à compléter\nWhatsApp : à compléter"
                )

    time.sleep(1)
