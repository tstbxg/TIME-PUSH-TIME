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
LOVE_START = cfg["love_start"]
BIRTHDAY1 = cfg["birthday1"]
BIRTHDAY2 = cfg["birthday2"]
BIRTHDAY3 = cfg.get("birthday3", "")
ASTRO = cfg.get("astro", "aries")

# 功能开关
SWITCH_CAIHONGPI = cfg.get("Whether_caihongpi", True)
SWITCH_LIZHI = cfg.get("Whether_lizhi", True)
SWITCH_EN = cfg.get("Whether_en", True)
SWITCH_TIP = cfg.get("Whether_tip", True)
SWITCH_HEALTH = cfg.get("Whether_health", True)
SWITCH_LUCKY = cfg.get("Whether_lucky", True)
SWITCH_STAR = cfg.get("Whether_star", True)


def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    res = requests.get(url, timeout=10)
    return res.json().get("access_token")


# WMO天气编码 + 配套提示
weather_rule = {
    0: {"name": "晴天", "tip": "阳光很好，记得防晒"},
    1: {"name": "晴", "tip": "阳光很好，记得防晒"},
    2: {"name": "少云", "tip": "天气舒服，适合出门"},
    3: {"name": "阴天", "tip": "阴天，出门建议随身带伞"},
    45: {"name": "雾", "tip": "有雾，能见度低，路上慢行"},
    48: {"name": "雾凇", "tip": "路面易滑，出行注意安全"},
    51: {"name": "毛毛雨", "tip": "有小雨，记得带伞"},
    53: {"name": "毛毛雨", "tip": "有小雨，记得带伞"},
    55: {"name": "毛毛雨", "tip": "有小雨，记得带伞"},
    61: {"name": "小雨", "tip": "下雨啦，带伞，小心路滑"},
    63: {"name": "中雨", "tip": "中雨，出门务必带伞，注意防滑"},
    65: {"name": "大雨", "tip": "大雨，尽量减少外出，注意安全"},
    80: {"name": "阵雨", "tip": "阵雨不定时，随身带伞备用"},
    81: {"name": "阵雨", "tip": "阵雨不定时，随身带伞备用"},
    82: {"name": "强阵雨", "tip": "强阵雨，出门带伞，注意避雨"},
    95: {"name": "雷暴", "tip": "打雷下雨，尽量不要在户外久待"},
    96: {"name": "雷暴伴冰雹", "tip": "强对流天气，尽量待在室内"},
    99: {"name": "强雷暴", "tip": "强雷暴，注意安全，减少外出"},
}

# Open-Meteo 广州 23.13,113.27 实时天气+温度+提示
def get_weather():
    params = {
        "latitude": 23.13,
        "longitude": 113.27,
        "current_weather": "true",
        "timezone": "Asia/Shanghai"
    }
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        cw = data["current_weather"]
        code = cw["weathercode"]
        temp = round(cw["temperature"])
        info = weather_rule.get(code, {"name": "多云", "tip": "今日平安顺遂"})
        return f"{info['name']}，{temp}℃｜{info['tip']}"
    except Exception as e:
        print("天气接口异常", e)
        return "天气暂时获取失败，记得照顾好自己"


# 彩虹屁，限制最多30个字
def get_caihongpi():
    try:
        res = requests.get("https://api.shadiao.pro/chp", timeout=10)
        js = res.json()
        text = js["data"]["text"]
        if len(text) > 30:
            text = text[:30]
        return text
    except Exception:
        return "今日也要开开心心"


# 励志语录，限制最多30个字
def get_lizhi():
    try:
        res = requests.get("https://api.xygeng.cn/one", timeout=10)
        js = res.json()
        text = js["data"]["content"]
        if len(text) > 30:
            text = text[:30]
        return text
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


# 星座运势
def get_star(astro_name):
    try:
        res = requests.get(f"https://api.qqsuu.cn/api/dm-star?astro={astro_name}", timeout=10)
        js = res.json()
        return js["data"]["content"]
    except Exception:
        return "运势平稳，万事顺心"


# 生日倒计时
def calc_birthday(birth_str):
    if not birth_str:
        return ""
    b = datetime.strptime(birth_str, "%Y-%m-%d")
    today = date.today()
    next_birth = date(today.year, b.month, b.day)
    if next_birth < today:
        next_birth = date(today.year + 1, b.month, b.day)
    diff = (next_birth - today).days
    if diff == 0:
        return "🎂今天生日！生日快乐！"
    else:
        return f"还有{diff}天"


# 恋爱天数
def calc_love_day(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    today = date.today()
    return (today - start).days


if __name__ == "__main__":
    token = get_access_token()
    if not token:
        print("access_token 获取失败")
        exit()

    today_str = datetime.now().strftime("%Y-%m-%d")
    love_days = calc_love_day(LOVE_START)
    b1_text = calc_birthday(BIRTHDAY1)
    b2_text = calc_birthday(BIRTHDAY2)
    b3_text = calc_birthday(BIRTHDAY3)

    weather_text = get_weather()
    chp_text = get_caihongpi() if SWITCH_CAIHONGPI else ""
    lizhi_text = get_lizhi() if SWITCH_LIZHI else ""
    en_text = get_en_sentence() if SWITCH_EN else ""
    tip_text = get_tip() if SWITCH_TIP else ""
    health_text = get_health() if SWITCH_HEALTH else ""
    lucky_text = get_lucky() if SWITCH_LUCKY else ""
    star_text = get_star(ASTRO) if SWITCH_STAR else ""

    data = {
        "date": {"value": today_str},
        "love_days": {"value": f"我们在一起{love_days}天"},
        "birthday1": {"value": b1_text},
        "birthday2": {"value": b2_text},
        "weather": {"value": weather_text},
        "caihongpi": {"value": chp_text},
        "lizhi": {"value": lizhi_text},
        "en": {"value": en_text},
        "tip": {"value": tip_text},
        "health": {"value": health_text},
        "lucky": {"value": lucky_text},
        "star": {"value": star_text}
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
