import requests
import json
import random
from datetime import datetime

# 星座英文映射
astro_map = {
    "aries": "aries",
    "taurus": "taurus",
    "gemini": "gemini",
    "cancer": "cancer",
    "leo": "leo",
    "virgo": "virgo",
    "libra": "libra",
    "scorpio": "scorpio",
    "sagittarius": "sagittarius",
    "capricorn": "capricorn",
    "aquarius": "aquarius",
    "pisces": "pisces"
}

# 365条寄言库
msg_list = [
"岁岁年年，万喜万般宜。",
"风遇山止，船到岸停，我遇你而心安。",
"朝朝暮暮，岁岁相依。",
"愿我们，细水长流，岁岁相伴。",
"世界一般，但你超值。",
"有你在，每一天都值得期待。",
"慢慢相处，好好相爱。",
"和你，今年，明年，年年。",
"爱意随风起，风止意难平，所幸是你。",
"平凡日子，因你闪闪发光。",
"不用奔赴大海，也能春暖花开。",
"日子平淡，好在我喜欢，好在是你。",
"遇见你之后，所有温柔都有了归宿。",
"晚风轻踩云朵，你在我的心上。",
"好好生活，慢慢爱你。",
"你是藏在烟火里的浪漫。",
"所求不多，平安，有你。",
"与你有关，皆是浪漫。",
"山野万里，你是我藏在微风里的欢喜。",
"有幸相遇，恰好合拍。",
"四季更迭，爱你不变。",
"一屋两人，三餐四季。",
"目光所及，皆是你。",
"满心欢喜，只因是你。",
"携一束月光，奔赴有你的远方。",
"你是黄昏的橘，是温柔的诗。",
"人海浮沉，还好遇见了你。",
"爱意不必喧哗，长久安稳就好。",
"愿所有美好，都与你环环相扣。",
"故事不长，四个字：有你真好。",
"日子温柔，你是首选。",
"看山是山，看海是海，看你满心欢喜。",
"朝暮与年岁并往，与你共至光年。",
"山河辽阔，人间烟火，无一是你，无一不是你。",
"不必刻意浪漫，你在就是浪漫。",
"岁岁常欢愉，年年皆胜意。",
"想和你，看遍人间烟火。",
"温柔和偏爱，全都留给你。",
"慢慢理解世界，慢慢更新自己，慢慢爱你。",
"你是明目张胆的偏爱。",
"晚风、落日、还有你。",
"有幸相逢，不负遇见。",
"心有所向，心有所属，是你。",
"平安喜乐，有你相伴。",
"把温柔和浪漫都给你。",
"人间值得，你更值得。",
"从此，粥可温，立黄昏。",
"与君同渡，岁岁无忧。",
"星河万顷，都不及你一眼。",
"时光缓缓，爱意满满。",
"你是惊喜，也是来日方长。",
"十里春风，不如你。",
"所有温柔，向你奔赴。",
"相守于烟火，相爱于朝夕。",
"愿我们，长久且坚定。",
"有幸成为彼此的依靠。",
"不慌不忙，慢慢走。",
"喜欢是乍见之欢，爱是久处不厌。",
"你是平淡生活里的光。",
"朝看日出，暮看晚霞，身边是你。",
"世间万般美好，都不及你。",
"爱意藏在日常，温柔落在朝夕。",
"愿我们平安顺遂，一直在一起。",
"不用轰轰烈烈，安稳就很好。",
"一想到你，心里就软软的。",
"时光慢慢，爱意不散。",
"你是首选，也是唯一。",
"人海茫茫，还好牵住你的手。",
"岁岁平安，年年有你。",
"浪漫不止今天，朝朝暮暮皆是。",
"和你在一起，就是最好的时光。",
"心之所向，素履以往，方向是你。",
"落日归于山海，我归于你。",
"打包所有温柔，全都送给你。",
"平凡的每一天，因为你特别。",
"愿风雨同舟，岁岁相守。",
"慢慢相爱，慢慢变老。",
"你本身就是温柔。",
"遇见你的意义，是互相照亮。",
"往后余生，冷暖有相知。",
"甜有很多种，你是第一种。",
"世界乱糟糟，我只偏爱你。",
"风很温柔，花很浪漫，你很特别。",
"好好相爱，不负时光。",
"何其有幸，岁岁相伴。",
"朝朝暮暮，平安相伴。",
"爱意无声，细水长流。",
"奔赴春夏秋冬，和你。",
"你是我的满心欢喜。",
"山河远阔，只想和你。",
"日子有光，身边有你。",
"所有期待，都关于你。",
"最长情的告白是陪伴。",
"温柔予你，偏爱予你。",
"与你共度，岁岁无忧。",
"遇见即是上上签。",
"慢慢靠近，深深相爱。",
"星河入梦，而你入我心。",
"烟火人间，喜乐有你。",
"愿日子清净，抬头皆是温柔，温柔是你。",
"爱意绵长，岁岁不忘。",
"不必万丈光芒，但始终温暖有光，我的宝贝。",
"朝暮相伴，情深意长。",
"有幸相逢，刚好是你。",
"心动于你，终老于你。",
"所有风景，都想和你一起看。",
"安稳相伴，岁岁年年。",
"你是心底藏起来的温柔。",
"晚风捎去我对你的想念。",
"爱，是细水长流的陪伴。",
"与你奔赴朝暮。",
"人间朝暮，叶落惊秋，我只想和你。",
"岁岁无忧，有爱相守。",
"喜欢年年岁岁，喜欢岁岁年年的你。",
"时光温柔，感恩有你。",
"你是我的来日方长。",
"寻常日常，皆是浪漫。",
"心有归处，归处是你。",
"愿我们相伴到老，永不走散。",
"爱意落在每一个朝夕。",
"春风十里，不如和你。",
"落日晚霞，不及你。",
"携手同行，岁岁欢喜。",
"好好相爱，慢慢相伴。",
"你是限定温柔，也是永久浪漫。",
"人海相遇，何其有幸。",
"温柔岁岁，爱意年年。",
"心动都归你。",
"烟火寻常，有你就甜。",
"星河璀璨，不如你一眼。",
"朝朝念你，暮暮想你。",
"相伴朝夕，不负相遇。",
"愿初心不变，爱意不减。",
"你是平淡日子里的糖。",
"万千人海，独钟于你。",
"岁岁欢喜，年年是你。",
"时光知味，岁月沉香，身旁是你。",
"爱意无言，岁岁相守。",
"晚风轻轻，思念长长。",
"有幸相伴，岁岁无忧。",
"和你，看日出日落。",
"心有所属，是你刚好。",
"浪漫藏在细碎日常。",
"长路有你，不惧风雨。",
"把所有的温柔，都留给最爱的你。",
"三餐四季，欢喜是你。",
"愿往后余生，温柔以待。",
"有你，便是人间好时节。",
"世间温柔，皆予吾爱。",
"与你相逢，万事可期。",
"爱意缓缓，岁岁安然。",
"愿我们，平安，相爱，长久。",
"岁岁朝朝，念你如初。",
"你是藏在时光里的温柔。",
"朝暮相思，岁岁相依。",
"漫漫人生路，有幸同路。",
"满心温柔，只为你。",
"相逢不易，相守珍惜。",
"愿晚风将我思念吹向你。",
"爱意藏于朝夕，久处不厌。",
"山河皆过客，你是归人。",
"岁岁平安，爱意长存。",
"和你，共度朝朝暮暮。",
"最好的时光，是和你。",
"你是我的人间理想。",
"岁岁年年，爱意不变。",
"承蒙相遇，何其有幸。",
"温柔不止一瞬，爱意岁岁年年。",
"目光长远，终点是你。",
"平凡日常，因你闪光。",
"愿岁岁无忧，相爱永久。",
"我攒了很久的温柔，给你。",
"朝暮相伴，喜乐无忧。",
"心之所向，皆是你。",
"爱不是一时兴起，是岁岁年年。",
"人海万千，唯你入心。",
"烟火温柔，有你很甜。",
"落日余晖，爱意相随。",
"愿我们，一直是我们。",
"慢慢相逢，深深相爱。",
"你是惊喜，也是归宿。",
"岁岁欢愉，爱你如一。",
"余生漫漫，请多指教。",
"思念无声，震耳欲聋。",
"爱意浅浅，岁岁长长。",
"与你，共赏人间朝暮。",
"有幸遇见你，余生都是你。",
"温柔落于眼底，爱意藏于心间。",
"岁岁常相见，年年常相伴。",
"风遇流云，我遇见你。",
"世间美好，与你环环相扣。",
"爱意不慌，慢慢生长。",
"朝看晨光，暮伴你旁。",
"你是我的偏爱和例外。",
"长路漫漫，有你作伴。",
"岁岁年年，温柔不变。",
"所有浪漫，只为你。",
"平安喜乐，岁岁有你。",
"相逢在人海，相守在朝夕。",
"爱意悠悠，岁岁长久。",
"愿日子缓缓，爱意满满。",
"一想到你，万物温柔。",
"山河辽阔，只想和你慢慢走。",
"你是岁月赠予我的礼物。",
"朝暮与共，岁岁情深。",
"欢喜是你，偏爱是你。",
"人海漂流，幸而有你。",
"爱意朴素，长久动人。",
"愿风雨来时，我们并肩。",
"岁岁无忧，与你相守。",
"晚风温柔，思念不休。",
"最好的缘分，是刚好是你。",
"温柔岁岁，欢喜年年。",
"和你，岁岁年年，永不分离。",
"心动不止一刻，爱不止今天。",
"人间烟火，最抚人心，有你足矣。",
"心有所栖，爱有所依。"
]

# 兜底文案
rainbow_backup = [
    "你是落在我世界里的一束光",
    "怎么会有人这么好看，说的就是你",
    "我的所有温柔，都想给你",
    "你真的超棒，是我最爱的宝贝",
    "一想到你，心情就变好了"
]
lizhi_backup = [
    "万事顺意，平安喜乐",
    "好好生活，慢慢相遇",
    "保持热爱，奔赴山海",
    "前路浩浩荡荡，万事尽可期待",
    "愿你今天，轻松自在"
]
en_backup = [
    "May all your wishes come true.",
    "You are my favorite surprise.",
    "Stay happy, stay bright.",
    "Love you, today and always.",
    "The best is yet to come."
]
tip_backup = "记得好好照顾自己哦"
health_backup = "多喝温水，早睡早起"
luck_backup = "今日好运满满✨"


def get_birthday_left(birth_date_str):
    """计算距离下一个生日还有多少天"""
    if not birth_date_str:
        return ""
    birth = datetime.strptime(birth_date_str, "%Y-%m-%d")
    today = datetime.now()
    next_birth = datetime(year=today.year, month=birth.month, day=birth.day)
    if next_birth < today:
        next_birth = datetime(year=today.year+1, month=birth.month, day=birth.day)
    days = (next_birth - today).days
    if days == 0:
        return "🎂今天生日！生日快乐！"
    return f"距离生日还有{days}天"


def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        res = requests.get(url, timeout=15)
        data = res.json()
        if "access_token" in data:
            return data["access_token"]
        print("【token获取失败】", data)
        return None
    except Exception as e:
        print("【token请求异常】", e)
        return None


def get_weather(api_key, province, city):
    if not api_key:
        return "未配置天行key"
    try:
        url = f"https://api.tianapi.com/tianqi/index?key={api_key}&province={province}&city={city}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            info = js["newslist"][0]
            return f"{info['weather']}，气温{info['low']}~{info['high']}，{info['tips']}"
        return "天气获取失败"
    except Exception as e:
        print("【天气接口异常】", e)
        return "天气获取失败"


def get_star(api_key, astro):
    if not api_key:
        return "未配置天行key"
    try:
        url = f"https://api.tianapi.com/star/index?key={api_key}&astro={astro}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        return "星座运势获取失败"
    except Exception as e:
        print("【星座接口异常】", e)
        return "星座运势获取失败"


def get_caihongpi(api_key):
    if not api_key:
        return random.choice(rainbow_backup)
    try:
        url = f"https://api.tianapi.com/caihongpi/index?key={api_key}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        return random.choice(rainbow_backup)
    except Exception:
        return random.choice(rainbow_backup)


def get_lizhi(api_key):
    if not api_key:
        return random.choice(lizhi_backup)
    try:
        url = f"https://api.tianapi.com/lzmy/index?key={api_key}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        return random.choice(lizhi_backup)
    except Exception:
        return random.choice(lizhi_backup)


def get_en(api_key):
    if not api_key:
        return random.choice(en_backup)
    try:
        url = f"https://api.tianapi.com/everyday/index?key={api_key}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["en"]
        return random.choice(en_backup)
    except Exception:
        return random.choice(en_backup)


def get_tip(api_key):
    if not api_key:
        return tip_backup
    try:
        url = f"https://api.tianapi.com/healthtip/index?key={api_key}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        return tip_backup
    except Exception:
        return tip_backup


def get_health(api_key):
    if not api_key:
        return health_backup
    try:
        url = f"https://api.tianapi.com/health/index?key={api_key}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        return health_backup
    except Exception:
        return health_backup


def get_lucky(api_key):
    if not api_key:
        return luck_backup
    try:
        url = f"https://api.tianapi.com/zhoyun/index?key={api_key}"
        res = requests.get(url, timeout=15)
        js = res.json()
        if js.get("code") == 200:
            return js["newslist"][0]["content"]
        return luck_backup
    except Exception:
        return luck_backup


def calc_love_days(start):
    s = datetime.strptime(start, "%Y-%m-%d")
    now = datetime.now()
    return f"{(now - s).days}天"


def main():
    cfg = load_config()
    # ========== 填充所有字段 ==========
    today = datetime.now().strftime("%Y-%m-%d")
    love_day = calc_love_days(cfg["love_start"])
    msg = random.choice(msg_list)
    weather = get_weather(cfg["tianxing_key"], cfg["province"], cfg["city"])
    star = get_star(cfg["tianxing_key"], cfg["astro"])

    birthday1_text = get_birthday_left(cfg["birthday1"])
    birthday2_text = get_birthday_left(cfg["birthday2"])

    caihongpi = get_caihongpi(cfg["tianxing_key"]) if cfg["Whether_caihongpi"] else ""
    lizhi = get_lizhi(cfg["tianxing_key"]) if cfg["Whether_lizhi"] else ""
    en = get_en(cfg["tianxing_key"]) if cfg["Whether_en"] else ""
    tip = get_tip(cfg["tianxing_key"]) if cfg["Whether_tip"] else ""
    health = get_health(cfg["tianxing_key"]) if cfg["Whether_health"] else ""
    lucky = get_lucky(cfg["tianxing_key"]) if cfg["Whether_lucky"] else ""

    # =====================【自测打印！重点！】=====================
    print("===== 本地自测结果 =====")
    print(f"日期：{today}")
    print(f"恋爱天数：{love_day}")
    print(f"寄言：{msg}")
    print(f"生日1倒计时：{birthday1_text}")
    print(f"生日2倒计时：{birthday2_text}")
    print(f"天气：{weather}")
    print(f"彩虹屁：{caihongpi}")
    print(f"励志语录：{lizhi}")
    print(f"英文句子：{en}")
    print(f"温馨提示：{tip}")
    print(f"健康小知识：{health}")
    print(f"今日好运：{lucky}")
    print(f"星座运势：{star}")
    # ==========================================================

    # 组装微信模板消息
    data = {
        "template_id": cfg["template_id"],
        "data": {
            "date": {"value": today},
            "love_days": {"value": love_day},
            "say": {"value": msg},
            "birthday1": {"value": birthday1_text},
            "birthday2": {"value": birthday2_text},
            "weather": {"value": weather},
            "caihongpi": {"value": caihongpi},
            "lizhi": {"value": lizhi},
            "en": {"value": en},
            "tip": {"value": tip},
            "health": {"value": health},
            "lucky": {"value": lucky},
            "star": {"value": star}
        }
    }
    access_token = get_access_token(cfg["app_id"], cfg["app_secret"])
    if not access_token:
        print("access_token 获取失败，停止推送")
        return
    for openid in cfg["user"]:
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
        data["touser"] = openid
        resp = requests.post(url, json=data)
        print(f"发给 {openid} 结果：{resp.json()}")


if __name__ == "__main__":
    main()

