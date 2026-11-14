import json
import os
import random
import requests

TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_CHANNEL_ID = os.environ["TG_CHANNEL_ID"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

COUNTRIES = [
    ("au", "Австралия", "🇦🇺"), ("at", "Австрия", "🇦🇹"), ("az", "Азербайджан", "🇦🇿"),
    ("dz", "Алжир", "🇩🇿"), ("ai", "Ангилья", "🇦🇮"), ("ao", "Ангола", "🇦🇴"),
    ("ag", "Антигуа и Барбуда", "🇦🇬"), ("ar", "Аргентина", "🇦🇷"), ("am", "Армения", "🇦🇲"),
    ("bs", "Багамы", "🇧🇸"), ("bb", "Барбадос", "🇧🇧"), ("bh", "Бахрейн", "🇧🇭"),
    ("by", "Беларусь", "🇧🇾"), ("bz", "Белиз", "🇧🇿"), ("be", "Бельгия", "🇧🇪"),
    ("bj", "Бенин", "🇧🇯"), ("bm", "Бермуды", "🇧🇲"), ("bg", "Болгария", "🇧🇬"),
    ("bo", "Боливия", "🇧🇴"), ("ba", "Босния и Герцеговина", "🇧🇦"), ("bw", "Ботсвана", "🇧🇼"),
    ("br", "Бразилия", "🇧🇷"), ("vg", "Британские Виргинские острова", "🇻🇬"), ("bn", "Бруней", "🇧🇳"),
    ("bf", "Буркина-Фасо", "🇧🇫"), ("bt", "Бутан", "🇧🇹"), ("vu", "Вануату", "🇻🇺"),
    ("gb", "Великобритания", "🇬🇧"), ("hu", "Венгрия", "🇭🇺"), ("ve", "Венесуэла", "🇻🇪"),
    ("vn", "Вьетнам", "🇻🇳"), ("ga", "Габон", "🇬🇦"), ("gy", "Гайана", "🇬🇾"),
    ("gm", "Гамбия", "🇬🇲"), ("gh", "Гана", "🇬🇭"), ("gt", "Гватемала", "🇬🇹"),
    ("gw", "Гвинея-Бисау", "🇬🇼"), ("de", "Германия", "🇩🇪"), ("hn", "Гондурас", "🇭🇳"),
    ("hk", "Гонконг", "🇭🇰"), ("gd", "Гренада", "🇬🇩"), ("gr", "Греция", "🇬🇷"),
    ("ge", "Грузия", "🇬🇪"), ("dk", "Дания", "🇩🇰"), ("dm", "Доминика", "🇩🇲"),
    ("do", "Доминиканская Республика", "🇩🇴"), ("eg", "Египет", "🇪🇬"), ("zm", "Замбия", "🇿🇲"),
    ("zw", "Зимбабве", "🇿🇼"), ("il", "Израиль", "🇮🇱"), ("in", "Индия", "🇮🇳"),
    ("id", "Индонезия", "🇮🇩"), ("jo", "Иордания", "🇯🇴"), ("iq", "Ирак", "🇮🇶"),
    ("ie", "Ирландия", "🇮🇪"), ("is", "Исландия", "🇮🇸"), ("es", "Испания", "🇪🇸"),
    ("it", "Италия", "🇮🇹"), ("ye", "Йемен", "🇾🇪"), ("cv", "Кабо-Верде", "🇨🇻"),
    ("kz", "Казахстан", "🇰🇿"), ("ky", "Каймановы острова", "🇰🇾"), ("kh", "Камбоджа", "🇰🇭"),
    ("cm", "Камерун", "🇨🇲"), ("ca", "Канада", "🇨🇦"), ("qa", "Катар", "🇶🇦"),
    ("ke", "Кения", "🇰🇪"), ("cy", "Кипр", "🇨🇾"), ("cn", "Китай", "🇨🇳"),
    ("co", "Колумбия", "🇨🇴"), ("cr", "Коста-Рика", "🇨🇷"), ("ci", "Кот-д’Ивуар", "🇨🇮"),
    ("kw", "Кувейт", "🇰🇼"), ("kg", "Кыргызстан", "🇰🇬"), ("la", "Лаос", "🇱🇦"),
    ("lv", "Латвия", "🇱🇻"), ("lb", "Ливан", "🇱🇧"), ("lr", "Либерия", "🇱🇷"),
    ("ly", "Ливия", "🇱🇾"), ("lt", "Литва", "🇱🇹"), ("lu", "Люксембург", "🇱🇺"),
    ("mu", "Маврикий", "🇲🇺"), ("mr", "Мавритания", "🇲🇷"), ("mg", "Мадагаскар", "🇲🇬"),
    ("mo", "Макао", "🇲🇴"), ("mw", "Малави", "🇲🇼"), ("my", "Малайзия", "🇲🇾"),
    ("ml", "Мали", "🇲🇱"), ("mv", "Мальдивы", "🇲🇻"), ("mt", "Мальта", "🇲🇹"),
    ("ma", "Марокко", "🇲🇦"), ("mx", "Мексика", "🇲🇽"), ("mz", "Мозамбик", "🇲🇿"),
    ("md", "Молдова", "🇲🇩"), ("mn", "Монголия", "🇲🇳"), ("ms", "Монтсеррат", "🇲🇸"),
    ("mm", "Мьянма", "🇲🇲"), ("na", "Намибия", "🇳🇦"), ("np", "Непал", "🇳🇵"),
    ("ne", "Нигер", "🇳🇪"), ("ng", "Нигерия", "🇳🇬"), ("nl", "Нидерланды", "🇳🇱"),
    ("ni", "Никарагуа", "🇳🇮"), ("nz", "Новая Зеландия", "🇳🇿"), ("no", "Норвегия", "🇳🇴"),
    ("ae", "ОАЭ", "🇦🇪"), ("om", "Оман", "🇴🇲"), ("pa", "Панама", "🇵🇦"),
    ("pg", "Папуа — Новая Гвинея", "🇵🇬"), ("py", "Парагвай", "🇵🇾"), ("pe", "Перу", "🇵🇪"),
    ("pl", "Польша", "🇵🇱"), ("pt", "Португалия", "🇵🇹"), ("cg", "Республика Конго", "🇨🇬"),
    ("rw", "Руанда", "🇷🇼"), ("ro", "Румыния", "🇷🇴"), ("sv", "Сальвадор", "🇸🇻"),
    ("sa", "Саудовская Аравия", "🇸🇦"), ("mk", "Северная Македония", "🇲🇰"), ("sc", "Сейшелы", "🇸🇨"),
    ("sn", "Сенегал", "🇸🇳"), ("vc", "Сент-Винсент и Гренадины", "🇻🇨"), ("kn", "Сент-Китс и Невис", "🇰🇳"),
    ("lc", "Сент-Люсия", "🇱🇨"), ("rs", "Сербия", "🇷🇸"), ("sg", "Сингапур", "🇸🇬"),
    ("sk", "Словакия", "🇸🇰"), ("si", "Словения", "🇸🇮"), ("sb", "Соломоновы Острова", "🇸🇧"),
    ("us", "США", "🇺🇸"), ("sl", "Сьерра-Леоне", "🇸🇱"), ("tj", "Таджикистан", "🇹🇯"),
    ("th", "Таиланд", "🇹🇭"), ("tw", "Тайвань", "🇹🇼"), ("tz", "Танзания", "🇹🇿"),
    ("tc", "Тёркс и Кайкос", "🇹🇨"), ("tt", "Тринидад и Тобаго", "🇹🇹"), ("tn", "Тунис", "🇹🇳"),
    ("tm", "Туркменистан", "🇹🇲"), ("tr", "Турция", "🇹🇷"), ("ug", "Уганда", "🇺🇬"),
    ("uz", "Узбекистан", "🇺🇿"), ("ua", "Украина", "🇺🇦"), ("uy", "Уругвай", "🇺🇾"),
    ("fj", "Фиджи", "🇫🇯"), ("ph", "Филиппины", "🇵🇭"), ("fi", "Финляндия", "🇫🇮"),
    ("fr", "Франция", "🇫🇷"), ("hr", "Хорватия", "🇭🇷"), ("td", "Чад", "🇹🇩"),
    ("me", "Черногория", "🇲🇪"), ("cz", "Чехия", "🇨🇿"), ("cl", "Чили", "🇨🇱"),
    ("ch", "Швейцария", "🇨🇭"), ("se", "Швеция", "🇸🇪"), ("lk", "Шри-Ланка", "🇱🇰"),
    ("ec", "Эквадор", "🇪🇨"), ("ee", "Эстония", "🇪🇪"), ("sz", "Эсватини", "🇸🇿"),
    ("za", "ЮАР", "🇿🇦"), ("kr", "Южная Корея", "🇰🇷"), ("jm", "Ямайка", "🇯🇲"),
    ("jp", "Япония", "🇯🇵")
]

HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def fetch_chart(country_code):
    parts = ["https://rss.marketingtools.apple.com", "api", "v2", country_code, "music", "most-played", "10", "songs.json"]
    url = "/".join(parts)
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    results = resp.json().get("feed", {}).get("results", [])
    if not results:
        return None
    tracks = [f"{i}. {x.get('artistName', 'Unknown')} — {x.get('name', 'Unknown')}" for i, x in enumerate(results[:10], 1)]
    return "\n".join(tracks)


def get_country_and_tracks():
    history = load_history()
    available = [c for c in COUNTRIES if c not in history]
    if not available:
        history = []
        available = COUNTRIES[:]
    random.shuffle(available)
    for code, name, flag in available:
        try:
            tracks = fetch_chart(code)
            if tracks:
                history.append(code)
                save_history(history)
                return {"code": code, "name": name, "flag": flag}, tracks
        except Exception as e:
            print(f"Пропуск {name} ({code}): {e}")
    raise RuntimeError("Не удалось получить чарт ни для одной страны")


def generate_post(country, tracks_text):
    prompt = f"""Ты — музыкальный редактор популярного Telegram-канала.
Оформи красивый, живой пост на русском языке с актуальным топ-10 треков страны: {country['flag']} {country['name']}.

Вот реальный список треков из чарта Apple Music прямо сейчас:
{tracks_text}

Требования к посту:
1. Начни с яркого заголовка с флагом страны (например: {country['flag']} <b>Топ-10 чарта: {country['name']}</b>).
2. Выведи пронумерованный список всех 10 треков. Названия треков и артистов оставь в оригинале.
3. После списка добавь короткий блок «🎧 Что происходит в чарте» (2–3 предложения с интересными наблюдениями или фактами о лидерах этого списка).
4. В конце добавь 3–4 подходящих хэштега на русском и английском.
5. Используй только базовые HTML-теги Telegram: <b> и <i>. Не используй Markdown (** или #) и не пиши никаких вступительных слов от себя."""

    models = [
        "openrouter/free",
        "google/gemma-3-27b-it:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-r1-0528:free"
    ]
    api_url = "/".join(["https://openrouter.ai", "api", "v1", "chat", "completions"])
    headers = {
        "Authorization": "Bearer " + OPENROUTER_API_KEY.strip(),
        "Content-Type": "application/json"
    }
    for model in models:
        try:
            resp = requests.post(
                api_url,
                headers=headers,
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=45
            )
            if resp.status_code == 200 and resp.text.strip():
                data = resp.json()
                content = data["choices"][0]["message"]["content"].strip()
                if content:
                    return content
            else:
                print(f"Model {model} status {resp.status_code}: {resp.text[:150]}")
        except Exception as e:
            print(f"Model {model} failed: {e}")
    raise RuntimeError("Все бесплатные модели OpenRouter временно недоступны")
def send_to_telegram(text):
    url = f"https://telegram.org{TG_BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": TG_CHANNEL_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=20)
    resp.raise_for_status()


if __name__ == "__main__":
    country, tracks = get_country_and_tracks()
    print(f"Выбрана страна: {country['name']}")
    post_text = generate_post(country, tracks)
    send_to_telegram(post_text)
    print("Пост успешно опубликован!")
