import sys

sys.path.append('..')
import pytest
from base.do_log import DoLog
from utils.timer import Timer
from functools import reduce
import time
import json

variables = {
    "timestamp": Timer.get_timestamp(),
    "ago_timestamp": Timer.get_ago_timestamp(5),
    "date": time.strftime("%Y-%m-%d", time.localtime()),
    "date_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    "tokens": {
        "robot": "robot_token"
    },
    "user_id": 293733,
    "flight_order": "Flight-{}".format(str(int(time.time()) * 1000)),
    "hotel_order": "Hotel-{}".format(str(int(time.time()) * 1000)),
    "taxi_order": "Taxi-{}".format(str(int(time.time()) * 1000)),
    "train_order": "Train-{}".format(str(int(time.time()) * 1000)),
    "meal_order": "Meal-{}".format(str(int(time.time()) * 1000)),
    "errors": []
}


@pytest.fixture(scope='session', name='log')
def get_log():
    log = DoLog.do_log()
    return log


@pytest.fixture(scope='session', name='result', autouse=True)
def reset_result_file():
    with open('result.json', 'w') as f:
        f.write('[]')

    yield

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(variables['errors'], f, ensure_ascii=False)
