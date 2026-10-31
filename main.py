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
CITY = cfg["city"]
LOVE_START = cfg["love_start"]
BIRTHDAY1 = cfg["birthday1"]
BIRTHDAY2 = cfg["birthday2"]
BIRTHDAY3 = cfg.get("birthday3", "")
QWEATHER_KEY = cfg.get("qweather_key", "")
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


# 和风天气 - 直接使用广州固定ID：101280101，跳过城市搜索接口
def get_weather(qkey, city_name):
    if not qkey:
        return "暂时无法获取天气，记得好好照顾自己"
    try:
        loc_id = "101280101"
        weather_url = f"https://devapi.qweather.com/v7/weather/now?location={loc_id}&key={qkey}"
        r2 = requests.get(weather_url, timeout=10)
        j2 = r2.json()
        if j2.get("code") == "200":
            now = j2["now"]
            return f"{now['text']}，气温{now['temp']}℃，体感{now['feelsLike']}℃"
        else:
            print("和风返回code:", j2.get("code"), j2.get("message"))
            return "暂时无法获取天气，记得好好照顾自己"
    except Exception as e:
        print("天气接口异常：", str(e))
        return "暂时无法获取天气，记得好好照顾自己"


# 彩虹屁
def get_caihongpi():
    try:
        res = requests.get("https://api.shadiao.pro/chp", timeout=10)
        js = res.json()
        return js["data"]["text"]
    except Exception:
        return "今日也要开开心心"


# 励志
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

    weather_text = get_weather(QWEATHER_KEY, CITY)
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
