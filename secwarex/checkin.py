#! /usr/bin/env python3
#! encoding=utf-8

import requests
import time
import sys
import json
from datetime import datetime

url_scan = "https://api.secwarex.io/api/v1/secwarex/riskDetection/scanAddress"
address = "0x"

def print_start():
    print("===============.\nsecwarex checkin start at {}\n- account: {}\n".format(datetime.today(), address))

def print_end():
    print("secwarex checkin end at {}".format(datetime.today()))

def scan(token="",timestamp=0):
    data = {
        "X-Address": address,
        "X-Project": "secwarex",
        "language":"cn",
        "manageId":"100004",
        "timestamp":timestamp
    }

    resp = requests.post(url=url_scan, data = json.dumps(data),headers={
        "X-Project": "secwarex",
        "Token": token
    })

    return resp.json()

if __name__ == "__main__":
    address = sys.argv[1]
    token = sys.argv[2]
    now = int(time.time_ns()/1e6)
    print_start()
    data = scan(token, now)
    print(data)
    print_end()
