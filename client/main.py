import socket
import json
import time
import threading
from matplotlib.animation import FuncAnimation
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Адрес и порт сервера
        self.SERVER_ADDRESS = ('localhost', 8000)

        # Создаем сокет
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Подключаемся к серверу
        self.client_sock.connect(self.SERVER_ADDRESS)

        self.res = []
        self.current_coords = [0, 0, 0]


        # Создаем фигуру и оси
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-40e6, 40e6)
        self.ax.set_ylim(-40e6, 40e6)
        self.ax.set_zlim(-40e6, 40e6)
        # создаем экземпляр FigureCanvas
        self.canvas = FigureCanvas(self.fig)

        # добавляем холст в окно
        self.setCentralWidget(self.canvas)

        # Создаем анимацию
        self.ani = FuncAnimation(self.fig, self.update_data, interval=2000)

        # обновляем холст
        self.canvas.draw()

        rx, ry, rz = 6400000, 6400000, 6400000
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = rx * np.outer(np.cos(u), np.sin(v))
        y = ry * np.outer(np.sin(u), np.sin(v))
        z = rz * np.outer(np.ones_like(u), np.cos(v))

        self.ax.plot_wireframe(x, y, z, alpha=0.1)
        # max_radius = max(rx, ry, rz)
        # for axis in 'xyz':
        #     getattr(self.ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

        self.thread1 = threading.Thread(target=self.Listen)
        self.thread1.start()

    def Send_reqv(self):
        msg = {'usr': 1}
        self.client_sock.send(json.dumps(msg).encode())

    def Listen(self):
        while True:
            data = self.client_sock.recv(1024).decode()
            data = json.loads(data)
            self.current_coords = list(data.values())[0]
            time.sleep(0.1)

    # Обновляем данные для анимации
    def update_data(self, num):
        self.Send_reqv()
        self.res.append(self.current_coords)
        # print(current_coords)
        plot = np.array(self.res)
        self.ax.scatter(plot[:, 0], plot[:, 1], plot[:, 2])


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.setApplicationName('Satellite viewer v1.1')
    app.setWindowIcon(QIcon('icons/window_icon.png'))
    window.show()
    app.exec_()