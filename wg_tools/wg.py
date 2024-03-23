import os
import subprocess
from datetime import datetime

import pytz

from model.peer import Wg_peer


def convert_byte_to_gib(byte):
    gb = byte / 1024 / 1024 / 1024
    gb = format(gb, '.2f')
    return float(gb)


def convert_time_to_tehran_time(time):
    tehran_timezone = pytz.timezone('Asia/Tehran')

    timestamp = int(time)
    dt = datetime.fromtimestamp(timestamp)
    tehran_dt = dt.astimezone(tehran_timezone)

    formatted_datetime = tehran_dt.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime


def dump_peer(public_key):
    sys_name = os.getenv("SYSTEM_NAME")

    try:
        wg = subprocess.check_output(f"wg show {sys_name} dump | grep {public_key}", shell=True).decode("utf-8")
    except subprocess.CalledProcessError:
        return []
    wg = wg.split("\t")
    return wg


def calculate_transfer(upload, download):
    transfer = convert_byte_to_gib(float(upload) + float(download))
    return transfer


def get_peer(public_key):
    data = dump_peer(public_key)
    if len(data) == 0:
        return None

    peer = Wg_peer(
        public_key=data[0],
        endpoint=data[2],
        latest_handshake=convert_time_to_tehran_time(data[4]),
        transfer=calculate_transfer(data[5], data[6]),
    )

    return peer


def pause_peer(public_key, allowed_ips):
    sys_name = os.getenv("SYSTEM_NAME")

    try:
        subprocess.run(['bash', '-c', f"wg set {sys_name} peer {public_key} remove"])
        subprocess.run(['bash', '-c', f"ip -4 route delete {allowed_ips} dev {sys_name}"])

    except subprocess.CalledProcessError:
        print("Error in pausing peer")


def resume_peer(public_key, allowed_ips, pre_shared_key):
    sys_name = os.getenv("SYSTEM_NAME")

    try:
        command1 = f"wg set {sys_name} peer \"{public_key}\" allowed-ips {allowed_ips} " \
                   f"preshared-key <(echo \"{pre_shared_key}\")"

        command2 = f"ip -4 route add {allowed_ips} dev {sys_name}"

        subprocess.run(['bash', '-c', command1], check=True)
        subprocess.run(['bash', '-c', command2], check=True)

    except subprocess.CalledProcessError:
        print("Error in resuming peer")