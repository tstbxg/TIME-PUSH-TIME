import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
import sys
import os
import http.client, urllib
import json
from zhdate import ZhDate


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url, timeout=10).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    return access_token


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    try:
        response_json = eval(response_data)
    except Exception as e:
        print("天气接口解析异常", e)
        sys.exit(1)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn


#词霸每日一句
def get_ciba():
    if Whether_Eng:
        try:
            url = "http://open.iciba.com/dsapi/"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
            r = get(url, headers=headers, timeout=10)
            note_en = r.json()["content"]
            note_ch = r.json()["note"]
            return (note_en, note_ch)
        except Exception as e:
            print("词霸API异常：", e)
            return ("词霸API调取错误", "词霸API调取错误")
    else:
        return ("", "")


#彩虹屁
def caihongpi():
    if Whether_caihongpi:
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')
            params = urllib.parse.urlencode({'key':tianxing_API})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/caihongpi/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            data = data["newslist"][0]["content"]
            if("XXX" in data):
                data = data.replace("XXX","蒋蒋")
            return data
        except Exception as e:
            print("彩虹屁API异常：", e)
            return ("彩虹屁API调取错误，请检查API是否正确申请或是否填写正确")
    else:
        return ""


#健康小提示API
def health():
    if Whether_health:
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')
            params = urllib.parse.urlencode({'key':tianxing_API})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/healthtip/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            data = data["newslist"][0]["content"]
            return data
        except Exception as e:
            print("健康小提示API异常：", e)
            return ("健康小提示API调取错误，请检查API是否正确申请或是否填写正确")
    else:
        return ""


#星座运势
def lucky():
    if Whether_lucky:
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')
            params = urllib.parse.urlencode({'key':tianxing_API,'astro':astro})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/star/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            data = "爱情指数："+str(data["newslist"][1]["content"])+"   工作指数："+str(data["newslist"][2]["content"])+"\n今日概述："+str(data["newslist"][8]["content"])
            return data
        except Exception as e:
            print("星座运势API异常：", e)
            return ("星座运势API调取错误，请检查API是否正确申请或是否填写正确")
    else:
        return ""


#励志名言
def lizhi():
    if Whether_lizhi:
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')
            params = urllib.parse.urlencode({'key':tianxing_API})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/lzmy/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            return data["newslist"][0]["saying"]
        except Exception as e:
            print("励志古言API异常：", e)
            return ("励志古言API调取错误，请检查API是否正确申请或是否填写正确")
    else:
        return ""


#下雨概率和建议
def tip():
    if Whether_tip:
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')
            params = urllib.parse.urlencode({'key':tianxing_API,'city':city})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/tianqi/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            pop = data["newslist"][0]["pop"]
            tips = data["newslist"][0]["tips"]
            return pop, tips
        except Exception as e:
            print("下雨提示API异常：", e)
            return "获取失败", "获取失败"
    else:
        return "", ""


#推送信息
def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, pipi, lizhi, pop, tips, note_en, note_ch, health_tip, lucky_):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature,
                "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            },
            "pipi": {
                "value": pipi,
                "color": get_color()
            },
            "lucky": {
                "value": lucky_,
                "color": get_color()
            },
            "lizhi": {
                "value": lizhi,
                "color": get_color()
            },
            "pop": {
                "value": pop,
                "color": get_color()
            },
            "health": {
                "value": health_tip,
                "color": get_color()
            },
            "tips": {
                "value": tips,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        birth_day = get_birthday(value, year, today)
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data, timeout=10).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("./config.json", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("推送消息失败，请检查config.json文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except json.JSONDecodeError:
        print("推送消息失败，请检查config.json格式是否正确")
        os.system("pause")
        sys.exit(1)

    accessToken = get_access_token()
    users = config["user"]
    province, city = config["province"], config["city"]
    weather, max_temperature, min_temperature = get_weather(province, city)
    tianxing_API=config["tianxing_API"]
    Whether_tip=config["Whether_tip"]
    Whether_Eng=config["Whether_Eng"]
    Whether_lucky=config["Whether_lucky"]
    Whether_lizhi=config["Whether_lizhi"]
    Whether_caihongpi=config["Whether_caihongpi"]
    Whether_health=config["Whether_health"]
    astro = config["astro"]

    note_ch, note_en = get_ciba()
    pipi = caihongpi()
    health_tip = health()
    pop,tips = tip()
    lizhi = lizhi()
    lucky_ = lucky()

    for user in users:
        send_message(user, accessToken, city, weather, max_temperature, min_temperature, pipi, lizhi,pop,tips, note_en, note_ch, health_tip, lucky_)

    import time
    time_duration = 3.5
    time.sleep(time_duration)
