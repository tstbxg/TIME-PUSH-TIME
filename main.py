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
# 这里换成和风天气key，config里新增 qweather_key
QWEATHER_KEY = cfg.get("qweather_key", "")


def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    res = requests.get(url, timeout=10)
    return res.json().get("access_token")


# 和风天气
def get_weather(qkey, city_name):
    if not qkey:
        return "暂时无法获取天气，记得好好照顾自己"
    try:
        # 先拿城市id
        loc_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={qkey}"
        r1 = requests.get(loc_url, timeout=10)
        j1 = r1.json()
        if j1.get("code") != "200":
            return "暂时无法获取天气，记得好好照顾自己"
        loc_id = j1["location"][0]["id"]
        # 获取实况天气
        weather_url = f"https://devapi.qweather.com/v7/weather/now?location={loc_id}&key={qkey}"
        r2 = requests.get(weather_url, timeout=10)
        j2 = r2.json()
        if j2.get("code") == "200":
            now = j2["now"]
            return f"{now['text']}，气温{now['temp']}℃，体感{now['feelsLike']}℃"
        else:
            return "暂时无法获取天气，记得好好照顾自己"
    except Exception:
        return "暂时无法获取天气，记得好好照顾自己"


# 彩虹屁 免费接口
def get_caihongpi():
    try:
        res = requests.get("https://api.shadiao.pro/chp", timeout=10)
        js = res.json()
        return js["data"]["text"]
    except Exception:
        return "今日也要开开心心"


# 励志语录
def get_lizhi():
    try:
        res = requests.get("https://api.xygeng.cn/one", timeout=10)
        js = res.json()
        return js["data"]["content"]
    except Exception:
        return "保持热爱，奔赴美好"


# 英文句子
def get_en_sentence():
    try:
        res = requests.get("https://api.vvhan.com/api/en", timeout=10)
        js = res.json()
        return js["data"]["content"]
    except Exception:
        return "Hope everything goes well."


# 温馨提示
def get_tip():
    try:
        res = requests.get("https://api.qqsuu.cn/api/dm-tips", timeout=10)
        js = res.json()
        return js["data"]["content"]
    except Exception:
        return "好好休息，照顾好自己"


# 健康小知识
def get_health():
    try:
        res = requests.get("https://api.qqsuu.cn/api/dm-health", timeout=10)
        js = res.json()
        return js["data"]["content"]
    except Exception:
        return "规律作息，身体健康最重要"


# 今日好运
def get_lucky():
    try:
        res = requests.get("https://api.qqsuu.cn/api/dm-lucky", timeout=10)
        js = res.json()
        return js["data"]["content"]
    except Exception:
        return "今日好运在线"


# 星座运势（白羊座aries，你可以自己改）
def get_star():
    try:
        res = requests.get("https://api.qqsuu.cn/api/dm-star?astro=aries", timeout=10)
        js = res.json()
        return js["data"]["content"]
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
    weather = get_weather(QWEATHER_KEY, CITY)
    caihongpi = get_caihongpi()
    lizhi = get_lizhi()
    en = get_en_sentence()
    tip = get_tip()
    health = get_health()
    lucky = get_lucky()
    star = get_star()

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

    for openid in USER_LIST:
        post_data = {
            "touser": openid,
            "template_id": TEMPLATE_ID,
            "data": data,
            "topcolor": "#FF6666"
        }
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        resp = requests.post(url, json=post_data, timeout=15)
        print(openid, resp.json())
