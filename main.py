import json
import requests
from datetime import datetime, date

# 仅新增：18字截断，只给励志、健康用
def cut18(s):
    if not isinstance(s, str):
        s = str(s)
    if len(s) > 18:
        return s[:18] + "…"
    return s

with open("config.json","r",encoding="utf-8") as f:
    cfg = json.load(f)

APP_ID = cfg["app_id"]
APP_SECRET = cfg["app_secret"]
TEMPLATE_ID = cfg["template_id"]
USER_LIST = cfg["user"]
PROVINCE = cfg["province"]
CITY = cfg["city"]
LOVE_START = cfg["love_start"]
TIANXING_KEY = cfg.get("tianxing_key","")
QWEATHER_KEY = cfg.get("qweather_key","")
ASTRO = cfg["astro"]

SWITCH = {
    "caihongpi": cfg.get("Whether_caihongpi",False),
    "lizhi": cfg.get("Whether_lizhi",False),
    "en": cfg.get("Whether_en",False),
    "tip": cfg.get("Whether_tip",False),
    "health": cfg.get("Whether_health",False),
    "lucky": cfg.get("Whether_lucky",False),
    "star": cfg.get("Whether_star",False),
}
birth1 = cfg.get("birthday1","").strip()
birth2 = cfg.get("birthday2","").strip()

def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    res = requests.get(url,timeout=15).json()
    return res.get("access_token")

def calc_love_days():
    start = datetime.strptime(LOVE_START,"%Y-%m-%d").date()
    today = date.today()
    return f"我们在一起{(today - start).days}天"

def get_birthday_count(birth_str):
    if not birth_str:
        return ""
    bdt = datetime.strptime(birth_str,"%Y-%m-%d").date()
    today = date.today()
    next_b = date(today.year, bdt.month, bdt.day)
    if next_b < today:
        next_b = date(today.year+1, bdt.month, bdt.day)
    diff = (next_b - today).days
    return f"还有{diff}天"

def get_weather():
    if not QWEATHER_KEY:
        return "天气获取失败"
    try:
        loc_url = f"https://geoapi.qweather.com/v2/city/lookup?location={CITY}&key={QWEATHER_KEY}"
        loc_res = requests.get(loc_url,timeout=12).json()
        if loc_res.get("code") != "200":
            return "天气获取失败"
        loc_id = loc_res["location"][0]["id"]
        weather_url = f"https://devapi.qweather.com/v7/weather/now?location={loc_id}&key={QWEATHER_KEY}"
        w_res = requests.get(weather_url,timeout=12).json()
        if w_res.get("code") == "200":
            now = w_res["now"]
            return f"{now['text']}，{now['temp']}℃"
    except Exception:
        pass
    return "天气获取失败"

def get_caihongpi():
    if not SWITCH["caihongpi"] or not TIANXING_KEY:
        return "愿你天天开心"
    try:
        r = requests.get(f"https://api.tianapi.com/caihongpi/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return "愿你天天开心"

# 励志：拿到内容才截断，兜底文字不变
def get_lizhi():
    if not SWITCH["lizhi"] or not TIANXING_KEY:
        return "保持热爱奔赴山海"
    try:
        r = requests.get(f"https://api.tianapi.com/lzmy/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return cut18(r["newslist"][0]["content"])
    except Exception:
        pass
    return "保持热爱奔赴山海"

def get_en():
    if not SWITCH["en"] or not TIANXING_KEY:
        return "Have a nice day."
    try:
        r = requests.get(f"https://api.tianapi.com/english/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return f"{r['newslist'][0]['en']}."
    except Exception:
        pass
    return "Have a nice day."

def get_tip():
    if not SWITCH["tip"] or not TIANXING_KEY:
        return "好好休息，照顾好自己"
    try:
        r = requests.get(f"https://api.tianapi.com/tianqi/index?key={TIANXING_KEY}&city={CITY}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["tip"]
    except Exception:
        pass
    return "好好休息，照顾好自己"

# 健康小知识：拿到内容才截断，兜底文字不变
def get_health():
    if not SWITCH["health"] or not TIANXING_KEY:
        return "规律作息，身体健康最重要"
    try:
        r = requests.get(f"https://api.tianapi.com/healthtip/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return cut18(r["newslist"][0]["content"])
    except Exception:
        pass
    return "规律作息，身体健康最重要"

def get_lucky():
    return "今日好运在线"

def get_star():
    if not SWITCH["star"] or not TIANXING_KEY:
        return "运势平稳，万事顺心"
    try:
        r = requests.get(f"https://api.tianapi.com/star/index?key={TIANXING_KEY}&astro={ASTRO}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return "运势平稳，万事顺心"

def main():
    token = get_access_token()
    if not token:
        print("❌ 获取access_token失败")
        return
    today_str = date.today().strftime("%Y-%m-%d")
    love_days = calc_love_days()
    girl_birth = get_birthday_count(birth1)
    boy_birth = get_birthday_count(birth2)
    weather_txt = get_weather()
    caihong = get_caihongpi()
    lizhi = get_lizhi()
    en_txt = get_en()
    tip_txt = get_tip()
    health_txt = get_health()
    lucky_txt = get_lucky()
    star_txt = get_star()

    payload_data = {
        "date": {"value": today_str},
        "weather": {"value": weather_txt},
        "love": {"value": love_days},
        "girl_birth": {"value": girl_birth},
        "boy_birth": {"value": boy_birth},
        "caihong": {"value": caihong},
        "lizhi": {"value": lizhi},
        "en": {"value": en_txt},
        "tip": {"value": tip_txt},
        "health": {"value": health_txt},
        "lucky": {"value": lucky_txt},
        "star": {"value": star_txt}
    }
    for openid in USER_LIST:
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        send_body = {
            "touser": openid,
            "template_id": TEMPLATE_ID,
            "data": payload_data
        }
        res = requests.post(url,json=send_body,timeout=15)
        print(openid, res.json())

if __name__ == "__main__":
    main()
