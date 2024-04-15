#! /usr/bin/env python3
#! encoding=utf-8

import sys
import requests
import json
from datetime import datetime, timezone

address = "0x"
url_info = "https://app.ether.fi/api/portfolio/v3/{address}"
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
    print("===============\nether.fi checkin start at {}\n- account: {}\n".format(datetime.today(), address))

def print_end():
    print("ether.fi checkin end at {}".format(datetime.today()))

def print_points(lp=0,ep=0):
    print("points: \n- ether.fi: {}\n- eigen layer: {}\n".format(lp ,ep))

def get_badge_points(badge={}) -> float:
    return float(badge.get("points"))

def get_total_points(data={}) -> (float, float):
    total_lp = 0
    total_ep = 0
    for (k, v) in data.items():
        if k == "badges":
            for (season, badges) in v.items():
                tp = iter_season_badges(badges)
                total_lp = total_lp + tp

        else:
            try:
                lp = v.get("loyaltyPoints")
                ep = v.get("eigenlayerPoints")
                total_lp = total_lp + lp
                total_ep = total_ep + ep
            except:
                pass

    return  total_lp, total_ep

def iter_season_badges(badges=[]) -> float:
    tp = 0
    for badge in badges:
        points = get_badge_points(badge)
        tp = tp + points
        wait_to_streak(badge)

    return tp

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
    lp, ep = get_total_points(data)
    print_points(lp,ep)
    print_end()

