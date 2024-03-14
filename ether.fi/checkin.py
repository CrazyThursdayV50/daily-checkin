#! /usr/bin/env python3
#! encoding=utf-8

import sys
import requests
import json
from datetime import datetime, timezone

address = "0x"
url_info = "https://app.ether.fi/api/portfolio/v2/{address}"
url_streak = "https://app.ether.fi/api/dailyStreak/updateStreak"

def get_info():
    url = url_info.replace("{address}",address)
    resp = requests.get(url=url)
    return resp.json()

def streak():
    data = {"account": address}
    resp = requests.post(url=url_streak, data = json.dumps(data))
    return resp.json()

def print_start():
    print("===============.\nether.fi checkin start at {}\n- account: {}\n".format(datetime.today(), address))

def print_end():
    print("ether.fi checkin end at {}".format(datetime.today()))

def print_points(data={}):
    print("points: \n- ether.fi: {}\n- eigen layer: {}\n".format(data.get("loyaltyPoints"), data.get("eigenlayerPoints")))

def get_badge_points(badge={}):
    return float(badge.get("points"))

def iter_badges(data={}):
    for badge in data.get("badges"):
        points = get_badge_points(badge)
        total_points = data.get("loyaltyPoints")
        data.update(loyaltyPoints = total_points+points)
        wait_to_streak(badge)

def wait_to_streak(badge={}):
    if badge.get("id") == "15":
        cooldown_time = datetime.fromisoformat(badge.get("cooldownTime")).replace(tzinfo=timezone.utc).astimezone(tz=None)
        now = datetime.today().astimezone(tz=None)
        if cooldown_time > now:
            print("cooldown time: {}, check streak next time\n".format(cooldown_time))
            return

        data = streak()
        print("streak message: {}\n".format(data.get("message")))

if __name__ == "__main__":
    address = sys.argv[1]
    print_start()
    data = get_info()
    iter_badges(data)
    print_points(data)
    print_end()

