import json
import requests
from datetime import datetime, date
import os
os.environ["TZ"] = "Asia/Shanghai"

# 通用安全截断：防止微信因为内容过长直接把整个字段置空（关键！）
def safe_clip(text, max_len=42):
    if not isinstance(text, str):
        text = str(text)
    if len(text) > max_len:
        return text[:max_len] + "…"
    return text

# 励志专用更短截断，解决励志单行省略
def clip_lizhi(text, max_len=18):
    return safe_clip(text, max_len)

def clean_birth_str(raw: str):
    if not raw:
        return ""
    s = raw.strip()
    if s.startswith("r"):
        s = s[1:]
    return s

# 读取配置
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

APP_ID = cfg.get("app_id", "")
APP_SECRET = cfg.get("app_secret", "")
TEMPLATE_ID = cfg.get("template_id", "")
USER_LIST = cfg.get("user", [])
CITY = cfg.get("city", "广州")

birth1_raw = cfg.get("birthday1", "")
birth2_raw = cfg.get("birthday2", "")
birth1 = clean_birth_str(birth1_raw)
birth2 = clean_birth_str(birth2_raw)

LOVE_START_RAW = cfg.get("love_start")
if not LOVE_START_RAW or LOVE_START_RAW is None:
    LOVE_START_RAW = "2021-12-12"

TIANXING_KEY = cfg.get("tianxing_key", "")
QWEATHER_KEY = cfg.get("qweather_key", "")
ASTRO = cfg.get("astro", "pisces")

SWITCH = {
    "caihongpi": bool(cfg.get("Whether_caihongpi", True)),
    "lizhi": bool(cfg.get("Whether_lizhi", True)),
    "en": bool(cfg.get("Whether_en", True)),
    "tip": bool(cfg.get("Whether_tip", True)),
    "health": bool(cfg.get("Whether_health", True)),
    "lucky": bool(cfg.get("Whether_lucky", True)),
    "star": bool(cfg.get("Whether_star", True)),
}


def get_access_token():
    try:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
        resp = requests.get(url, timeout=15)
        res = resp.json()
        return res.get("access_token")
    except Exception:
        return None


def calc_love_days() -> str:
    try:
        start = datetime.strptime(LOVE_START_RAW, "%Y-%m-%d").date()
        today = date.today()
        return f"我们在一起{ (today - start).days }天"
    except Exception:
        return "恋爱天数计算失败"


def get_birthday_count(birth_str) -> str:
    if not birth_str:
        return "生日未配置"
    try:
        bdt = datetime.strptime(birth_str, "%Y-%m-%d").date()
        today = date.today()
        next_birth = date(today.year, bdt.month, bdt.day)
        if next_birth < today:
            next_birth = date(today.year + 1, bdt.month, bdt.day)
        diff = (next_birth - today).days
        return f"还有{diff}天"
    except Exception:
        return "生日计算失败"


def get_weather() -> str:
    if not QWEATHER_KEY:
        return "未配置天气密钥"
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
    except Exception:
        pass
    return "天气获取失败"


def get_caihongpi() -> str:
    if not SWITCH["caihongpi"] or not TIANXING_KEY:
        return "愿你日日开心"
    try:
        r = requests.get(f"https://api.tianapi.com/caihongpi/index?key={TIANXING_KEY}", timeout=12).json()
        if r.get("code") == 200 and r.get("newslist"):
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return "愿你日日开心"


def get_lizhi() -> str:
    if not SWITCH["lizhi"] or not TIANXING_KEY:
        return "保持热爱奔赴山海"
    try:
        r = requests.get(f"https://api.tianapi.com/lzjiyan/index?key={TIANXING_KEY}", timeout=12).json()
        if r.get("code") == 200 and r.get("newslist"):
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return "保持热爱奔赴山海"


def get_en() -> str:
    if not SWITCH["en"] or not TIANXING_KEY:
        return "Have a nice day."
    try:
        r = requests.get(f"https://api.tianapi.com/english/index?key={TIANXING_KEY}", timeout=12).json()
        if r.get("code") == 200 and r.get("newslist"):
            return f"{r['newslist'][0]['en']}."
    except Exception:
        pass
    return "Have a nice day."


def get_tip() -> str:
    if not SWITCH["tip"] or not TIANXING_KEY:
        return "好好休息，照顾好自己"
    try:
        r = requests.get(f"https://api.tianapi.com/tianqi/index?key={TIANXING_KEY}&city={CITY}", timeout=12).json()
        if r.get("code") == 200 and r.get("newslist"):
            return r["newslist"][0]["tip"]
    except Exception:
        pass
    return "好好休息，照顾好自己"


def get_health() -> str:
    if not SWITCH["health"] or not TIANXING_KEY:
        return "规律作息，身体健康最重要"
    try:
        r = requests.get(f"https://api.tianapi.com/healthtip/index?key={TIANXING_KEY}", timeout=12).json()
        if r.get("code") == 200 and r.get("newslist"):
            return r["newslist"][0]["content"]
    except Exception:
        pass
    return "规律作息，身体健康最重要"


def get_lucky() -> str:
    return "今日好运在线"


def get_star() -> str:
    if not SWITCH["star"] or not TIANXING_KEY:
        return "运势平稳，万事顺心"
    try:
        r = requests.get(f"https://api.tianapi.com/star/index?key={TIANXING_KEY}&astro={ASTRO}", timeout=12).json()
        if r.get("code") == 200 and r.get("newslist"):
            item = r["newslist"][0]
            if "content" in item:
                return item["content"]
            elif "percent" in item:
                return f"{item['percent']}%"
    except Exception:
        pass
    return "运势平稳，万事顺心"


def main():
    token = get_access_token()
    if not token:
        print("❌ 获取access_token失败")
        return

    # 原始内容（API返回原汁原味，不在这里截断）
    raw_date = date.today().strftime("%Y-%m-%d")
    raw_weather = get_weather()
    raw_love = calc_love_days()
    raw_girl = get_birthday_count(birth1)
    raw_boy = get_birthday_count(birth2)
    raw_caihong = get_caihongpi()
    raw_lizhi = get_lizhi()
    raw_en = get_en()
    raw_tip = get_tip()
    raw_health = get_health()
    raw_lucky = get_lucky()
    raw_star = get_star()

    # ✅【只在发给微信这一步做截断！！】
    payload_data = {
        "date": {"value": safe_clip(raw_date)},
        "weather": {"value": safe_clip(raw_weather)},
        "love": {"value": safe_clip(raw_love)},
        "girl_birth": {"value": safe_clip(raw_girl)},
        "boy_birth": {"value": safe_clip(raw_boy)},
        "caihong": {"value": safe_clip(raw_caihong)},
        "lizhi": {"value": clip_lizhi(raw_lizhi)},
        "en": {"value": safe_clip(raw_en)},
        "tip": {"value": safe_clip(raw_tip)},
        "health": {"value": safe_clip(raw_health)},
        "lucky": {"value": safe_clip(raw_lucky)},
        "star": {"value": safe_clip(raw_star)},
    }
    print("原始数据打印",{
        "raw_caihong":raw_caihong,
        "raw_lizhi":raw_lizhi,
        "raw_health":raw_health,
        "raw_star":raw_star
    })
    print("发给微信的payload", payload_data)

    for openid in USER_LIST:
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        body = {
            "touser": openid,
            "template_id": TEMPLATE_ID,
            "data": payload_data
        }
        resp = requests.post(url, json=body, timeout=15)
        print("推送结果：", resp.json())


if __name__ == "__main__":
    main()
