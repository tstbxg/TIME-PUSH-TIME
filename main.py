import json
import requests
from datetime import datetime, date

# 仅增加这个工具函数，除此之外，前面全部是你的原版main(3).py
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
    return (today - start).days

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

# 和风天气
def get_weather():
    if not QWEATHER_KEY:
        return ""
    try:
        loc_url = f"https://geoapi.qweather.com/v2/city/lookup?location={CITY}&key={QWEATHER_KEY}"
        loc_res = requests.get(loc_url,timeout=12).json()
        if loc_res.get("code") != "200":
            return ""
        loc_id = loc_res["location"][0]["id"]
        weather_url = f"https://devapi.qweather.com/v7/weather/now?location={loc_id}&key={QWEATHER_KEY}"
        w_res = requests.get(weather_url,timeout=12).json()
        if w_res.get("code") == "200":
            now = w_res["now"]
            return f"{now['text']}，{now['temp']}℃"
    except Exception:
        pass
    return ""

# 彩虹屁
def get_caihongpi():
    if not SWITCH["caihongpi"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/caihongpi/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return ""

# 励志语录
def get_lizhi():
    if not SWITCH["lizhi"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/lzmy/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return ""

# 英文句子
def get_en():
    if not SWITCH["en"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/english/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return f"{r['newslist'][0]['en']}."
    except Exception:
        pass
    return ""

# 温馨提示
def get_tip():
    if not SWITCH["tip"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/tianqi/index?key={TIANXING_KEY}&city={CITY}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["tip"]
    except Exception:
        pass
    return ""

# 健康小知识
def get_health():
    if not SWITCH["health"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/healthtip/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return ""

# 今日好运
def get_lucky():
    if not SWITCH["lucky"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/lucky/index?key={TIANXING_KEY}",timeout=12).json()
        if r["code"] == 200:
            return "今日好运在线"
    except Exception:
        pass
    return ""

# 星座运势
def get_star():
    if not SWITCH["star"] or not TIANXING_KEY:
        return ""
    try:
        r = requests.get(f"https://api.tianapi.com/star/index?key={TIANXING_KEY}&astro={ASTRO}",timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return ""

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

    # =========唯一改动点：在这里对拿到的结果做截断，函数完全不动！=========
    if lizhi:
        lizhi = cut18(lizhi)
    if health_txt:
        health_txt = cut18(health_txt)
    # =================================================================

    payload_data = {
        "date": {"value": today_str},
        "weather": {"value": weather_txt},
        "love": {"value": f"我们在一起{love_days}天"},
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
