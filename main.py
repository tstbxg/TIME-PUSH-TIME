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


# Open-Meteo 广州实时天气（海外服务器，Action稳定访问，准确实时）
def get_weather():
    # 广州坐标 23.13,113.27
