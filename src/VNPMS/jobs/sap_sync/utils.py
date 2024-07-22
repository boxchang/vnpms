import datetime
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_date_str():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d")


def get_batch_no():
    now = datetime.datetime.now()
    batch_no = now.strftime("%y%m%d%H%M%S")
    return batch_no
