import requests
import json
from datetime import datetime, date

# 读取配置
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

APP_ID = cfg["app_id"]
APP_SECRET = cfg["app_secret"]
TEMPLATE_ID = cfg["template_id"]
USER_LIST = cfg["user"]
PROVINCE = cfg["province"]
CITY = cfg["city"]
BIRTHDAY1 = cfg["birthday1"]
BIRTHDAY2 = cfg["birthday2"]
TIANXING_KEY = cfg.get("tianxing_key", "")


def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    res = requests.get(url, timeout=10)
    return res.json().get("access_token")


def get_weather(api_key, city):
    if not api_key:
        return "暂时无法获取天气，记得好好照顾自己"
    try:
        url = f"https://api.tianapi.com/tianqi/index?key={api_key}&city={city}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            info = js["newslist"][0]
            return f"{info['weather']}，气温{info['low']}~{info['high']}，{info['tips']}"
        else:
            return "暂时无法获取天气，记得好好照顾自己"
    except Exception:
        return "暂时无法获取天气，记得好好照顾自己"


def get_caihongpi(api_key):
    if not api_key:
        return "今日也要开开心心"
    try:
        url = f"https://api.tianapi.com/caihongpi/index?key={api_key}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "今日也要开开心心"
    except Exception:
        return "今日也要开开心心"


def get_lizhi(api_key):
    if not api_key:
        return "保持热爱，奔赴美好"
    try:
        url = f"https://api.tianapi.com/lizhi/index?key={api_key}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "保持热爱，奔赴美好"
    except Exception:
        return "保持热爱，奔赴美好"


def get_en_sentence(api_key):
    if not api_key:
        return "Hope everything goes well."
    try:
        url = f"https://api.tianapi.com/en/index?key={api_key}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "Hope everything goes well."
    except Exception:
        return "Hope everything goes well."


def get_tip(api_key):
    if not api_key:
        return "好好休息，照顾好自己"
    try:
        url = f"https://api.tianapi.com/tip/index?key={api_key}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "好好休息，照顾好自己"
    except Exception:
        return "好好休息，照顾好自己"


def get_health(api_key):
    if not api_key:
        return "规律作息，身体健康最重要"
    try:
        url = f"https://api.tianapi.com/healthtip/index?key={api_key}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "规律作息，身体健康最重要"
    except Exception:
        return "规律作息，身体健康最重要"


def get_lucky(api_key):
    if not api_key:
        return "今日好运在线"
    try:
        url = f"https://api.tianapi.com/lucky/index?key={api_key}"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "今日好运在线"
    except Exception:
        return "今日好运在线"


def get_star(api_key):
    if not api_key:
        return "运势平稳，万事顺心"
    try:
        url = f"https://api.tianapi.com/star/index?key={api_key}&astro=aries"
        res = requests.get(url, timeout=10)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        else:
            return "运势平稳，万事顺心"
    except Exception:
        return "运势平稳，万事顺心"


def calc_birthday(birth_str):
    s = birth_str.replace("r", "")
    b = datetime.strptime(s, "%Y-%m-%d")
    today = date.today()
    next_birth = date(today.year, b.month, b.day)
    if next_birth < today:
        next_birth = date(today.year + 1, b.month, b.day)
    diff = (next_birth - today).days
    if diff == 0:
        return "🎂今天生日！生日快乐！"
    else:
        return f"还有{diff}天"


def calc_love_day():
    start = date(2021, 12, 12)
    today = date.today()
    return (today - start).days


if __name__ == "__main__":
    token = get_access_token()
    if not token:
        print("获取access_token失败")
        exit()

    today_str = datetime.now().strftime("%Y-%m-%d")
    love_days = calc_love_day()
    b1 = calc_birthday(BIRTHDAY1)
    b2 = calc_birthday(BIRTHDAY2)
    weather = get_weather(TIANXING_KEY, CITY)
    caihongpi = get_caihongpi(TIANXING_KEY)
    lizhi = get_lizhi(TIANXING_KEY)
    en = get_en_sentence(TIANXING_KEY)
    tip = get_tip(TIANXING_KEY)
    health = get_health(TIANXING_KEY)
    lucky = get_lucky(TIANXING_KEY)
    star = get_star(TIANXING_KEY)

    data = {
        "date": {"value": today_str},
        "love_days": {"value": f"我们在一起{love_days}天"},
        "birthday1": {"value": b1},
        "birthday2": {"value": b2},
        "weather": {"value": weather},
        "caihongpi": {"value": caihongpi},
        "lizhi": {"value": lizhi},
        "en": {"value": en},
        "tip": {"value": tip},
        "health": {"value": health},
        "lucky": {"value": lucky},
        "star": {"value": star}
    }

    # 标题在这里！就是小冯电视台开场白
    for openid in USER_LIST:
        post_data = {
            "touser": openid,
            "template_id": TEMPLATE_ID,
            "data": data,
            "topcolor": "#FF6666",
            "title": "Good Morning,这里是小冯电视台，现在为你播报"
        }
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        resp = requests.post(url, json=post_data, timeout=15)
        print(openid, resp.json())
