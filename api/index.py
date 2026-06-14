import osimport requestsfrom flask import Flask, request, jsonifyapp = Flask(__name__)# Environment Variables থেকে টোকেন ও কি নিয়ে আসাTELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"def get_gemini_response(user_text):    payload = {        "contents": [{            "parts": [{"text": user_text}]        }]    }    headers = {"Content-Type": "application/json"}    try:        response = requests.post(GEMINI_URL, json=payload, headers=headers)        res_json = response.json()        return res_json['candidates'][0]['content']['parts'][0]['text']    except Exception as e:        return "দুঃখিত, জেমিনি এপিআই রেসপন্স করতে পারছে না।"def send_telegram_message(chat_id, text):    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"    payload = {"chat_id": chat_id, "text": text}    requests.post(url, json=payload)
@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def webhook(path):
    if request.method == 'POST':
        update = request.get_json()
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"]
            
            # জেমিনি থেকে উত্তর আনা
            bot_response = get_gemini_response(user_tex
