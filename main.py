import matplotlib.colors
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import webcolors

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.animation as animation

from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget, QColorDialog
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
        # self.ax.set_xlim(-10, 10)
        # self.ax.set_ylim(-10, 10)

        self.main_layout.addWidget(self.canvas)
        self.main_layout.addWidget(self.nacToolbar)

    def update(self, x, y, color, legend, o2, o3):
        if o3:
            line = '--'
        else:
            line = '-'
        if o2:
            linewidth = 5
        else:
            linewidth = 2

        self.ax.plot(x, y, line, color=color, label=legend, linewidth=linewidth)
        self.ax.legend()
        self.canvas.draw()

    def clear(self):
        self.ax.clear()
        self.ax.grid()
        self.canvas.draw()


class MyWidget(QMainWindow):
    def __init__(self):

        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружаем дизайн
        self.plot_widget = PlotWidget()
        self.layout_plot.addWidget(self.plot_widget)

        self.num.valueChanged.connect(self.update_num)
        self.radio_on.toggled.connect(self.update_on)
        self.min_x.valueChanged.connect(self.update_min_x)
        self.max_x.valueChanged.connect(self.update_max_x)
        self.accuracy.valueChanged.connect(self.update_accuracy)
        self.update_f.clicked.connect(self.update_f_text)
        self.color.clicked.connect(self.update_color)

        self.o1.stateChanged.connect(self.update_o1)
        self.o2.stateChanged.connect(self.update_o2)
        self.o3.stateChanged.connect(self.update_o3)

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
        c_rgb = webcolors.hex_to_rgb(data[self.num.value() - 1]["color"])
        self.color.setStyleSheet(f'background: rgb({c_rgb.red},{c_rgb.green},{c_rgb.blue})')

    def update_f_text(self):
        data[self.num.value() - 1]['function'] = self.function.text()
        if data[self.num.value() - 1]['on']:
            self.build()

    def update_on(self):
        data[self.num.value() - 1]['on'] = self.radio_on.isChecked()
        if data[self.num.value() - 1]['on']:
            self.build()
        else:
            data[self.num.value() - 1]['val_x'] = []
            data[self.num.value() - 1]['val_y'] = []
            self.update_graphs()

    def update_min_x(self):
        data[self.num.value() - 1]['min_x'] = self.min_x.value()
        self.build()

    def update_max_x(self):
        data[self.num.value() - 1]['max_x'] = self.max_x.value()
        self.build()

    def update_accuracy(self):
        data[self.num.value() - 1]['accuracy'] = self.accuracy.value()
        self.build()

    def update_o1(self):
        data[self.num.value() - 1]['o1'] = self.o1.isChecked()
        self.build()

    def update_o2(self):
        data[self.num.value() - 1]['o2'] = self.o2.isChecked()
        self.build()

    def update_o3(self):
        data[self.num.value() - 1]['o3'] = self.o3.isChecked()
        self.build()

    def build(self):
        dg = data[self.num.value() - 1]
        if dg['function'] != '':
            val_x, val_y = [], []
            for i in range(dg['min_x'] * int(f'1{"0" * dg["accuracy"]}'),
                           (dg['max_x']) * int(f'1{"0" * dg["accuracy"]}')):
                val_x.append(i / int(f'1{"0" * dg["accuracy"]}'))
            val_x.append(dg['max_x'])
            if dg['o1'] and 0 in val_x:
                val_x.remove(0)
            flag_zero = False
            for i in val_x:
                try:
                    print(dg['function'].replace('x', f'({i})'))
                    val_y.append(eval(dg['function'].replace('x', f'({i})')))
                except Exception as ex:
                    print(ex, 'ERROR')
                    print(len(val_x), len(val_y), i)
                    flag_zero = True
            if flag_zero:
                val_x.remove(0)
                dg['o1'] = True
                self.o1.setChecked(True)

            data[self.num.value() - 1]['val_x'], data[self.num.value() - 1]['val_y'] = val_x, val_y
            self.update_graphs()

    def update_graphs(self):
        self.plot_widget.clear()
        print('clear')
        for i, dg in enumerate(data):
            print(dg)
            if dg['on']:
                self.plot_widget.update(dg['val_x'], dg['val_y'], dg['color'], f'№{i + 1} f(x)=' + dg['function'],
                                        dg['o2'], dg['o3'])

    def update_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color.setStyleSheet(f'background: rgb({color.getRgb()[0]},{color.getRgb()[1]},{color.getRgb()[2]});')
            data[self.num.value() - 1]['color'] = webcolors.rgb_to_hex((color.getRgb()[0], color.getRgb()[1], color.getRgb()[2]))
            self.update_graphs()


if __name__ == '__main__':
    d = {'function': '', 'min_x': -10, 'max_x': 10, 'accuracy': 1, 'o1': False, 'o2': False, 'o3': False, 'on': False,
         'val_x': [], 'val_y': []}
    data = [d.copy() for i in range(10)]
    color_list = ['#47db2a', '#2a38db', '#db1818', '#e8ce27', '#27e8bb', '#8011a8', '#e04e1d', '#e01d8f', '#020205',
                  '#aa0000']
    for i in range(10):
        data[i]['color'] = color_list[i]
    graph = [[] for i in range(10)]
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())