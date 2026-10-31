import json
import requests
from datetime import datetime, date
import os
os.environ["TZ"] = "Asia/Shanghai"

# 仅励志专用截断函数
def cut_lizhi(text, max_len=18):
    if not isinstance(text, str):
        text = str(text)
    if len(text) > max_len:
        return text[:max_len] + "…"
    return text

# 清洗生日：自动去掉开头的r
def clean_birth_str(raw: str):
    s = raw.strip()
    if s.startswith("r"):
        s = s[1:]
    return s

# 读取配置
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

APP_ID = cfg["app_id"]
APP_SECRET = cfg["app_secret"]
TEMPLATE_ID = cfg["template_id"]
USER_LIST = cfg["user"]
CITY = cfg["city"]
PROVINCE = cfg["province"]

# 兼容带r的生日
birth1_raw = cfg.get("birthday1", "")
birth2_raw = cfg.get("birthday2", "")
birth1 = clean_birth_str(birth1_raw)
birth2 = clean_birth_str(birth2_raw)

LOVE_START_RAW = cfg.get("love_start", "2021-12-12")
TIANXING_KEY = cfg.get("tianxing_key", "")
QWEATHER_KEY = cfg.get("qweather_key", "")
ASTRO = cfg.get("astro", "pisces")

SWITCH = {
    "caihongpi": cfg.get("Whether_caihongpi", True),
    "lizhi": cfg.get("Whether_lizhi", True),
    "en": cfg.get("Whether_en", True),
    "tip": cfg.get("Whether_tip", True),
    "health": cfg.get("Whether_health", True),
    "lucky": cfg.get("Whether_lucky", True),
    "star": cfg.get("Whether_star", True),
}

def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        resp = requests.get(url, timeout=15)
        res = resp.json()
        print("access_token返回：", res)
        return res.get("access_token")
    except Exception as e:
        print("获取token失败：", e)
        return None

# 恋爱天数，加兜底
def calc_love_days():
    try:
        start = datetime.strptime(LOVE_START_RAW, "%Y-%m-%d").date()
        today = date.today()
        return f"我们在一起{ (today - start).days }天"
    except Exception as e:
        print("恋爱天数计算异常：", e)
        return "恋爱天数计算异常"

# 生日倒计时，清洗+兜底
def get_birthday_count(birth_str):
    if not birth_str:
        return "生日信息未配置"
    try:
        bdt = datetime.strptime(birth_str, "%Y-%m-%d").date()
        today = date.today()
        next_birth = date(today.year, bdt.month, bdt.day)
        if next_birth < today:
            next_birth = date(today.year + 1, bdt.month, bdt.day)
        diff = (next_birth - today).days
        return f"还有{diff}天"
    except Exception as e:
        print("生日计算异常：", birth_str, e)
        return "生日计算异常"

# 天气
def get_weather():
    if not QWEATHER_KEY:
        return "暂未配置天气key"
    try:
        loc_url = f"https://geoapi.qweather.com/v2/city/lookup?location={CITY}&key={QWEATHER_KEY}"
        loc_res = requests.get(loc_url, timeout=12).json()
        if loc_res.get("code") != "200":
            return "天气获取失败"
        loc_id = loc_res["location"][0]["id"]
        weather_url = f"https://devapi.qweather.com/v7/weather/now?location={loc_id}&key={QWEATHER_KEY}"
        w_res = requests.get(weather_url, timeout=12).json()
        if w_res.get("code") == "200":
            now = w_res["now"]
            return f"{now['text']}，{now['temp']}℃"
    except Exception as e:
        print("天气接口异常：", e)
    return "天气获取失败"

# 彩虹屁【不截断】
def get_caihongpi():
    if not SWITCH["caihongpi"] or not TIANXING_KEY:
        return "愿你今日万事顺心"
    try:
        r = requests.get(f"https://api.tianapi.com/caihongpi/index?key={TIANXING_KEY}", timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception as e:
        print("彩虹屁接口异常：", e)
    return "愿你今日万事顺心"

# 励志【唯一截断点，18字】
def get_lizhi():
    if not SWITCH["lizhi"] or not TIANXING_KEY:
        return "保持热爱奔赴山海"
    try:
        r = requests.get(f"https://api.tianapi.com/lzjiyan/index?key={TIANXING_KEY}", timeout=12).json()
        if r["code"] == 200:
            return cut_lizhi(r["newslist"][0]["content"])
    except Exception as e:
        print("励志接口异常：", e)
    return "保持热爱奔赴山海"

# 英文句子【不截断】
def get_en():
    if not SWITCH["en"] or not TIANXING_KEY:
        return "Have a nice day."
    try:
        r = requests.get(f"https://api.tianapi.com/english/index?key={TIANXING_KEY}", timeout=12).json()
        if r["code"] == 200:
            return f"{r['newslist'][0]['en']}."
    except Exception as e:
        print("英文接口异常：", e)
    return "Have a nice day."

# 温馨提示【不截断】
def get_tip():
    if not SWITCH["tip"] or not TIANXING_KEY:
        return "好好休息，照顾好自己"
    try:
        r = requests.get(f"https://api.tianapi.com/tianqi/index?key={TIANXING_KEY}&city={CITY}", timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["tip"]
    except Exception as e:
        print("温馨提示接口异常：", e)
    return "好好休息，照顾好自己"

# 健康小知识【不截断】
def get_health():
    if not SWITCH["health"] or not TIANXING_KEY:
        return "规律作息，身体健康最重要"
    try:
        r = requests.get(f"https://api.tianapi.com/healthtip/index?key={TIANXING_KEY}", timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception as e:
        print("健康接口异常：", e)
    return "规律作息，身体健康最重要"

# 今日好运
def get_lucky():
    return "今日好运在线"

# 星座运势【不截断】
def get_star():
    if not SWITCH["star"] or not TIANXING_KEY:
        return "运势平稳，万事顺心"
    try:
        r = requests.get(f"https://api.tianapi.com/star/index?key={TIANXING_KEY}&astro={ASTRO}", timeout=12).json()
        if r["code"] == 200:
            return r["newslist"][0]["content"]
    except Exception as e:
        print("星座接口异常：", e)
    return "运势平稳，万事顺心"

def main():
    token = get_access_token()
    if not token:
        print("❌ 无法获取access_token，终止推送")
        return
    today_str = date.today().strftime("%Y-%m-%d")

    love_text = calc_love_days()
    girl_birth_text = get_birthday_count(birth1)
    boy_birth_text = get_birthday_count(birth2)
    weather_text = get_weather()
    caihong_text = get_caihongpi()
    lizhi_text = get_lizhi()
    en_text = get_en()
    tip_text = get_tip()
    health_text = get_health()
    lucky_text = get_lucky()
    star_text = get_star()

    payload_data = {
        "date": {"value": today_str},
        "weather": {"value": weather_text},
        "love": {"value": love_text},
        "girl_birth": {"value": girl_birth_text},
        "boy_birth": {"value": boy_birth_text},
        "caihong": {"value": caihong_text},
        "lizhi": {"value": lizhi_text},
        "en": {"value": en_text},
        "tip": {"value": tip_text},
        "health": {"value": health_text},
        "lucky": {"value": lucky_text},
        "star": {"value": star_text}
    }
    print("组装完成的推送数据：", payload_data)

    for openid in USER_LIST:
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        body = {
            "touser": openid,
            "template_id": TEMPLATE_ID,
            "data": payload_data
        }
        resp = requests.post(url, json=body, timeout=15)
        print(f"推送给{openid} 结果：", resp.json())

if __name__ == "__main__":
    main()
