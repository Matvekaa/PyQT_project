from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.animation as animation

from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget
import sys


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.main_layout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.nacToolbar = NavigationToolbar2QT(self.canvas, self)
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.grid()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        self.main_layout.addWidget(self.canvas)
        self.main_layout.addWidget(self.nacToolbar)

    # def update(self, time, bar, nap):
    #     # if time[-1] < 5:
    #     #     self.ax.set_xlim(0, 5)
    #     self.ax.plot(time, bar, color='red')
    #     self.ax.plot(time, nap, color='green')
    #     self.canvas.draw()

    def clear(self):
        # self.ax.clear()
        # self.ax = self.figure.add_subplot(1, 1, 1)
        # self.ax.set_facecolor('#DCDCDC')
        # self.ax.grid()
        # # self.ax.set_xlim(0, 5)
        # self.ax.set_ylim(0, 1030)
        pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружаем дизайн
        self.plot_widget = PlotWidget()
        self.layout_plot.addWidget(self.plot_widget)

        self.num.valueChanged.connect(self.update_num)
        self.function.textChanged.connect(self.update_f_text)
        self.radio_on.toggled.connect(self.update_on)
        self.radio_off.toggled.connect(self.update_on)
        self.min_x.valueChanged.connect(self.update_min_x)
        self.max_x.valueChanged.connect(self.update_max_x)
        self.accuracy.valueChanged.connect(self.update_accuracy)
        self.update_f.clicked.connect(self.build)

    def update_num(self):
        self.function.setText(data[self.num.value() - 1]['function'])
        if data[self.num.value() - 1]['on']:
            self.radio_on.setChecked(True)
        else:
            self.radio_off.setChecked(True)
        self.min_x.setValue(data[self.num.value() - 1]['min_x'])
        self.max_x.setValue(data[self.num.value() - 1]['max_x'])
        self.accuracy.setValue(data[self.num.value() - 1]['accuracy'])
        self.o1.setChecked(data[self.num.value() - 1]['o1'])
        self.o2.setChecked(data[self.num.value() - 1]['o2'])
        self.o3.setChecked(data[self.num.value() - 1]['o3'])

    def update_f_text(self):
        data[self.num.value() - 1]['function'] = self.function.text()

    def update_on(self):
        data[self.num.value() - 1]['on'] = self.radio_on.isChecked()

    def update_min_x(self):
        data[self.num.value() - 1]['min_x'] = self.min_x.value()

    def update_max_x(self):
        data[self.num.value() - 1]['max_x'] = self.max_x.value()

    def update_accuracy(self):
        data[self.num.value() - 1]['accuracy'] = self.accuracy.value()

    def build(self):
        dg = data[self.num.value() - 1]
        val_x = []
        if dg['on']:
            if dg['min_x'] < 0:
                min_x_for_range = dg['min_x'] + 1
            else:
                min_x_for_range = dg['min_x']

            for i in range(min_x_for_range, dg['max_x']):
                if dg['accuracy'] >= 1:
                    for j in range(0, 10):
                        if dg['accuracy'] >= 2:
                            for k in range(0, 10):
                                if dg['accuracy'] >= 3:
                                    for a in range(0, 10):
                                        val_x.append(float(f'{i}.{j}{k}{a}'))
                                else:
                                    val_x.append(float(f'{i}.{j}{k}'))
                        else:
                            val_x.append(float(f'{i}.{j}'))
                else:
                    val_x.append(float(f'{i}'))
            val_x.append(float(dg['max_x']))
        val_x.sort()
        print(val_x)

if __name__ == '__main__':
    d = {'function': '', 'min_x': -10, 'max_x': 10, 'accuracy': 1, 'o1': False, 'o2': False, 'o3': False, 'on': False}
    data = [d.copy() for i in range(10)]
    graph = [[] for i in range(10)]
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())