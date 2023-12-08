from PyQt5 import uic  # Импортируем uic
import webcolors

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget, QColorDialog, QFileDialog
import sys

import sqlite3


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.main_layout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.figure.set_tight_layout("top = 0.973, bottom = 0.069, left = 0.053, right = 0.984, hspace = 0.2, wspace = 0.2")

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

        self.save_grapf.clicked.connect(self.save_graph)
        self.import_graph.clicked.connect(self.import_file_graph)

        self.save_kit_graph.clicked.connect(self.save_file_kit_graph)
        self.import_kit_graph.clicked.connect(self.import_file_kit_graph)

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
                    val_y.append(eval(dg['function'].replace('x', f'({i})')))
                except Exception as ex:
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
            if dg['on']:
                self.plot_widget.update(dg['val_x'], dg['val_y'], dg['color'], f'№{i + 1} f(x)=' + dg['function'],
                                        dg['o2'], dg['o3'])

    def update_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color.setStyleSheet(f'background: rgb({color.getRgb()[0]},{color.getRgb()[1]},{color.getRgb()[2]});')
            data[self.num.value() - 1]['color'] = webcolors.rgb_to_hex((color.getRgb()[0], color.getRgb()[1], color.getRgb()[2]))
            self.update_graphs()

    def save_graph(self):
        fname = QFileDialog.getSaveFileName(self, 'Сохранить график', '', 'График (*.graph)')[0]
        with open(fname, 'w') as f:
            dg = data[self.num.value() - 1]
            keys_str = '::::'.join(list(dg.keys()))
            print(keys_str)
            values = list(dg.values())
            values_str = '\n'.join([values[0], str(values[1]), str(values[2]), str(values[3]),
                                    '1' if values[4] else '0',
                                    '1' if values[5] else '0',
                                    '1' if values[6] else '0',
                                    '1' if values[7] else '0',
                                    ':'.join([str(i) for i in values[8]]),
                                    ':'.join([str(i) for i in values[9]]),
                                    values[10]])
            print(values_str)
            f.write(keys_str + '::_::\n::_::' + values_str)

    def import_file_graph(self):
        fname = QFileDialog.getOpenFileName(self, 'Открыть график', '', 'График (*.graph)')[0]
        with open(fname, 'r') as f:
            keys_str, values_str = f.read().split('::_::\n::_::')
            keys = keys_str.split('::::')
            values = values_str.split('\n')
            values[1] = int(values[1])
            values[2] = int(values[2])
            values[3] = int(values[3])
            values[4] = True if values[4] == '1' else False
            values[5] = True if values[5] == '1' else False
            values[6] = True if values[6] == '1' else False
            values[7] = True if values[7] == '1' else False
            values[8] = [float(i) for i in values[8].split(':')]
            values[9] = [float(i) for i in values[9].split(':')]
            d = dict()
            for i, k in enumerate(keys):
                d[f'{k}'] = values[i]
            data[self.num.value() - 1] = d
        self.update_num()
        self.update_graphs()

    def save_file_kit_graph(self):
        fname = QFileDialog.getSaveFileName(self, 'Сохранить набор графиков', '', 'Набор графиков (*.gsdb)')[0]
        open(fname, 'w')
        conn = sqlite3.connect(fname)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE graphs (function TEXT, min_x INTEGER, max_x INTEGER, accuracy INTEGER, 
        o1 INTEGER, o2 INTEGER, o3 INTEGER, is_on INTEGER, val_x TEXT, val_y TEXT, color TEXT)''')
        for d in data:
            cursor.execute(f'''INSERT INTO graphs (function, min_x, max_x, accuracy, o1, o2, o3, is_on, val_x, val_y, 
color) VALUES ({'"'}{d['function']}{'"'}, {d['min_x']}, {d['max_x']}, {d['accuracy']},
{1 if d['o1'] else 0}, {1 if d['o2'] else 0}, {1 if d['o3'] else 0}, {1 if d['on'] else 0}, 
{'"'}{':'.join([str(i) for i in d['val_x']])}{'"'}, {'"'}{':'.join([str(i) for i in d['val_y']])}{'"'}, 
{'"'}{d['color']}{'"'})''')
        conn.commit()
        conn.close()

    def import_file_kit_graph(self):
        global data
        fname = QFileDialog.getOpenFileName(self, 'Открыть набор графиков', '', 'Набор графиков (*.gsdb)')[0]
        conn = sqlite3.connect(fname)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM graphs')
        res = cursor.fetchall()
        print(res)
        new_data = []
        for i in range(10):
            d = dict()
            d['function'] = str(res[i][0])
            d['min_x'] = int(res[i][1])
            d['max_x'] = int(res[i][2])
            d['accuracy'] = int(res[i][3])
            d['o1'] = True if int(res[i][4]) == 1 else False
            d['o2'] = True if int(res[i][5]) == 1 else False
            d['o3'] = True if int(res[i][6]) == 1 else False
            d['on'] = True if int(res[i][7]) == 1 else False
            d['val_x'] = [float(j) if j != '' else '' for j in res[i][8].split(':')]
            d['val_y'] = [float(j) if j != '' else '' for j in res[i][9].split(':')]
            d['color'] = str(res[i][10])

            new_data.append(d)
        data = new_data
        self.update_num()
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