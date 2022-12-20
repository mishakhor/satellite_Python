import integrator
import numpy as np
import threading
from dataclasses import dataclass
import time
import socket
import json


@dataclass
class Params:
    mass: float = 100
    mu: float = 398600.4415e9
    R: float = 6371e3
    e0: float = 4.2666e-6


params = Params()

initial_q = np.array([2.66306016e+07, 9.70516730e+06, 0.00000000e+00, -2.34551642e+03, 1.33025620e+03, 0.00000000e+00])
current_q = initial_q
current_t = 0
h = 1

def calc_current_position():
    global current_t
    while True:
        global current_q
        current_t += h
        current_q = integrator.make_iter_runge_kutta(current_t, current_q, params, h)
        time.sleep(0.0001)


    # Формируем и отправляем JSON-данные
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))


def send_current_position():
    global current_q
    while(True):

        msg = {'sat': current_q[0:3].tolist()}
        client_socket.sendall(json.dumps(msg).encode())
        # Закрываем сокет
        print("sent")
        time.sleep(1)


thread1 = threading.Thread(target=calc_current_position)
thread1.start()

thread2 = threading.Thread(target=send_current_position)
thread2.start()