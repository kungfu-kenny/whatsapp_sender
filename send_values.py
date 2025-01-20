import os
import json
import logging
import traceback

import requests
from twilio.rest import Client

from datetime import datetime


CONFIG = os.path.join(
    os.getcwd(),
    'config.json'
)
FOLDER_OUTPUT = os.path.join(
    os.getcwd(),
    'logs',
)
FOLDER_OUTPUT_DAY = os.path.join(
    FOLDER_OUTPUT,
    datetime.now().strftime("%Y-%m-%d"),
)
FILE_LOG = os.path.join(
    FOLDER_OUTPUT_DAY,
    f"{datetime.now().strftime('%H-%M')}.log"
)

def produce_basic():
    for i in [
        FOLDER_OUTPUT,
        FOLDER_OUTPUT_DAY,
    ]:
        os.path.exists(i) or os.mkdir(i)

def send_request(ip: str) -> dict:
    dict_used = {"ip": ip,}
    try:
        dict_used.update(
            requests.get(f"http://{ip}/api/battery").json()
        )
        # dict_used.update(
        #     {
        #         "voltage": '14.00',
        #         "capacity": '41.67',
        #         "pin_voltage": '2.51',
        #         "pin_coefficient": '5.58',
        #     }
        # )
    except Exception:
        print(f'Error of requests: {traceback.format_exc()}')
        print()
        print()
    finally:
        return dict_used

def produce_log(list_log: list[dict[str]], list_send: list[dict[str]]) -> None:
    try:
        date_write = datetime.now().strftime('%d.%m.%Y %H:%M')
        for dict_log in list_log:
            dict_log = {
                key: i if (i := dict_log.get(key)) and i.strip() else "Not Specified"
                for key in [
                    "ip",
                    "voltage",
                    "capacity",
                    "pin_voltage",
                    "pin_coefficient",
                ]
            }
            message_whatsapp = \
                f"Datetime: {date_write}\n"\
                f"Voltage: {dict_log['voltage']}\n"\
                f"Capacity: {dict_log['capacity']}\n"\
                f"Pin Voltage: {dict_log['pin_voltage']}\n"\
                f"Pin coeficient: {dict_log['pin_coefficient']}\n"\
                f"Website: {dict_log['ip']}"
            message_log =  \
                f"{date_write} | "\
                f"Voltage: {dict_log['voltage']} | "\
                f"Capacity: {dict_log['capacity']} | "\
                f"Pin Voltage: {dict_log['pin_voltage']} | "\
                f"Pin coeficient: {dict_log['pin_coefficient']} | "\
                f"Website: {dict_log['ip']}\n"
            with open(FILE_LOG, 'a') as file_log:
                file_log.write(
                    message_log
                )    

            for phone in list_send:
                client = Client(phone["account_sid"], phone["auth_token"])
                client.messages.create(
                    body=message_whatsapp,
                    from_ = phone["from"],
                    to = phone["to"],
                )
    except Exception:
        print(f'Error of log sending: {traceback.format_exc()}')
        print()
        print()


if __name__ == "__main__":
    produce_basic()
    if not os.path.exists(CONFIG):
        print('You need to create config.json')
    else:
        dict_used = {}
        with open(CONFIG, 'r') as json_file:
            dict_used = json.load(json_file)
        list_res = []
        for ip in dict_used.get('IP', []):
            print(ip)
            print('===============================')
            list_res.append(send_request(ip))
        produce_log(list_res, dict_used["PHONE"])