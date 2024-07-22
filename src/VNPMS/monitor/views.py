import json
from ast import literal_eval

from django.shortcuts import render
import socket
from monitor.models import Config


def index(request):
    configs = Config.objects.all()
    for config in configs:
        try:
            HOST = config.ip_addr
            PORT = int(config.port)
            server_addr = (HOST, PORT)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(config.command.encode(), server_addr)
            info, addr = s.recvfrom(1024)
            print('recvfrom ' + str(addr) + ': ' + info.decode())
            info = literal_eval(info.decode())
            config.disk = info["DISK"]
            for disk in config.disk:
                if disk["usage_percent"] >=70 and disk["usage_percent"] < 90:
                    disk["background"] = "bg-warning"
                elif disk["usage_percent"] > 90:
                    disk["background"] = "bg-danger"
                else:
                    disk["background"] = "bg-success"
            print(config.disk)
            config.cpu = max(info["CPU"]["cpu_percent"])
            print(config.cpu)
            config.memory = info["MEMORY"]
            print(config.memory)
        except Exception as ex:
            msg = "主機{HOST} {PORT}無法連上{ERROR}".format(HOST=HOST, PORT=PORT, ERROR=ex)
            print(msg)
    return render(request, 'monitor/index.html', locals())