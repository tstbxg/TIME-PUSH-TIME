import json
import requests
from datetime import datetime

# 读取配置文件
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

APP_ID = cfg["app_id"]
APP_SECRET = cfg["app_secret"]
TEMPLATE_ID = cfg["template_id"]
USER_LIST = cfg["user"]
CITY = cfg["city"]
LOVE_DATE = cfg["love_date"]
TIANXING_KEY = cfg["tianxing_API"]
ASTRO = cfg["astro"]

Whether_Eng = cfg["Whether_Eng"]
Whether_caihongpi = cfg["Whether_caihongpi"]
Whether_lizhi = cfg["Whether_lizhi"]
Whether_tip = cfg["Whether_tip"]
Whether_health = cfg["Whether_health"]
Whether_lucky = cfg["Whether_lucky"]


def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    res = requests.get(url, timeout=10).json()
    return res.get("access_token")


# 恋爱天数
def get_love_days():
    start = datetime.strptime(LOVE_DATE, "%Y-%m-%d")
    return (datetime.now() - start).days


# 天行接口通用请求
def tianxing_req(api_path):
    try:
        url = f"https://api.tianapi.com/{api_path}?key={TIANXING_KEY}"
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("code") == 200 and data.get("newslist"):
            return data["newslist"][0]
        else:
            return None
    except Exception:
        return None


# 获取天气（下雨概率pop、天气、高低温、tips）
def get_weather():
    try:
        url = f"https://api.tianapi.com/tianqi/index?key={TIANXING_KEY}&city={CITY}"
        r = requests.get(url, timeout=10).json()
        if r["code"] == 200:
            w = r["newslist"][0]
            return {
                "weather": w["weather"],
                "min_t": w["lowest"],
                "max_t": w["highest"],
                "pop": w.get("pop", "无"),
                "tips": w["tips"]
            }
    except Exception:
        pass
    return {"weather": "获取失败", "min_t": "获取失败", "max_t": "获取失败", "pop": "获取失败", "tips": "获取失败"}


def main():
    token = get_access_token()
    if not token:
        print("access_token 获取失败！检查appid/appsecret")
        return

    today_str = datetime.now().strftime("%Y-%m-%d %A")
    love_day = get_love_days()
    weather_info = get_weather()

    note_en = ""
    note_ch = ""
    if Whether_Eng:
        eng_data = tianxing_req("enwords/index")
        if eng_data:
            note_en = eng_data["english"]
            note_ch = eng_data["chinese"]
        else:
            note_en = "获取失败"
            note_ch = "获取失败"

    pipi = "获取失败"
    if Whether_caihongpi:
        pi_data = tianxing_req("caihongpi/index")
        if pi_data:
            pipi = pi_data["content"]

    lizhi = "获取失败"
    if Whether_lizhi:
        lz_data = tianxing_req("lzju/index")
        if lz_data:
            lizhi = lz_data["content"]

    tips = weather_info["tips"] if Whether_tip else "已关闭"
    pop = weather_info["pop"]

    health = "获取失败"
    if Whether_health:
        h_data = tianxing_req("healthtip/index")
        if h_data:
            health = h_data["content"]

    lucky = "获取失败"
    if Whether_lucky:
        lu_data = tianxing_req(f"star/index?astro={ASTRO}")
        if lu_data:
            love = lu_data["love"]
            work = lu_data["work"]
            summary = lu_data["summary"]
            lucky = f"爱情指数：{love}  工作指数：{work}\n今日概述：{summary}"

    # 随机寄言文案
    msg_list = [
        "新的一天，也要好好热爱生活，我一直都在❤️",
        "早安，愿你今天所有的温柔和期待，都有回应",
        "日子慢慢，爱意满满，今天也要开开心心",
        "风很温柔，花很浪漫，你很特别，早安",
        "愿平安喜乐，万事顺意，今天也要加油",
        "岁岁年年，朝朝暮暮，我喜欢你这件事不变"
    ]
    import random
    msg = random.choice(msg_list)

    # 和微信模板变量一一对应
    send_data = {
        "date": {"value": today_str},
        "city": {"value": CITY},
        "weather": {"value": weather_info["weather"]},
        "min_temperature": {"value": weather_info["min_t"]},
        "max_temperature": {"value": weather_info["max_t"]},
        "love_day": {"value": love_day},
        "note_en": {"value": note_en},
        "note_ch": {"value": note_ch},
        "pipi": {"value": pipi},
        "lizhi": {"value": lizhi},
        "pop": {"value": pop},
        "tips": {"value": tips},
        "health": {"value": health},
        "lucky": {"value": lucky},
        "msg": {"value": msg}
    }

    for openid in USER_LIST:
        push_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        post_body = {
            "touser": openid,
            "template_id": TEMPLATE_ID,
            "data": send_data
        }
        resp = requests.post(push_url, json=post_body, timeout=10)
# 新增下面这两行
wx_result = resp.json()
print("【微信返回完整结果】", wx_result)

if __name__ == "__main__":
    main()
