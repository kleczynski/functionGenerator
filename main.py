import sys
import os
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import write
from PyQt5.QtWidgets import *
from pyqtgraph import PlotWidget
from PyQt5 import uic
import pyqtgraph as pg
import pandas as pd


def exit_program():
    os._exit(0)


class App(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("layout.ui", self)
        self.title = "Generator Funkcji"
        self.setWindowTitle(self.title)

        save = QAction("Save", self)
        save.triggered.connect(self.save)

        exit_program_button = QAction("Exit", self)
        exit_program_button.triggered.connect(exit_program)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(save)
        fileMenu.addAction(exit_program_button)

        # wartości do wykresu
        self.dsb_1 = self.doubleSpinBox
        self.dsb_1.setMaximum(100000.0)
        self.dsb_2 = self.doubleSpinBox_2
        self.dsb_2.setMaximum(100000.0)
        self.dsb_3 = self.doubleSpinBox_3
        self.dsb_3.setMaximum(100000.0)
        self.dsb_4 = self.doubleSpinBox_4
        self.dsb_4.setMaximum(100000.0)

        # wykres sinus
        self.sinus = self.findChild(QCheckBox, "checkBox")
        self.sinus.stateChanged.connect(lambda: self.sine())
        # wykres triangle
        self.triangle = self.findChild(QCheckBox, "checkBox_2")
        self.triangle.stateChanged.connect(lambda: self.triangle_sin())
        # wykres sawtooth
        self.sawtooth = self.findChild(QCheckBox, "checkBox_3")
        self.sawtooth.stateChanged.connect(lambda: self.sawtooth_sin())
        # wykres rectangle
        self.rectangle = self.findChild(QCheckBox, "checkBox_4")
        self.rectangle.stateChanged.connect(lambda: self.rectangle_sin())
        # wykres white noise
        self.white_noise = self.findChild(QCheckBox, "checkBox_5")
        self.white_noise.stateChanged.connect(lambda: self.white_noise_graph())

        # resetowanie wykresów
        self.btn_reset = self.findChild(QPushButton, "pushButton")
        self.btn_reset.clicked.connect(self.reset)


        self.show()

    def save(self):
        print('Zapisuje wynik działania do pliku')
        file_filter = '*.csv'
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   options=options, filter=file_filter)
        file = open(file_name, 'w')
        text = ""
        file.write(text)
        file.close()

    def sine(self):
        graph = self.graphicsView
        graph.setTitle('<font size=12>Sinus</font>')
        x = np.linspace(0, int(self.dsb_3.value()), int(self.dsb_3.value()) * int(self.dsb_4.value()))
        y = self.dsb_2.value() * np.sin(2 * np.pi * self.dsb_1.value() * x)
        table = self.findChild(pg.TableWidget, "tableWidget")
        table.setData((x, y))
        fourier_graph = self.findChild(PlotWidget, "graphicsView_2")
        fourier_graph.setTitle('<font size=12>Fourier Transform</font>')
        N = len(x)
        dt = x[1] - x[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        fourier_graph.plot().setData(y=yf, x=xf)
        graph.plot().setData(y=y, x=x)

    def triangle_sin(self):
        graph = self.graphicsView
        graph.setTitle('<font size=12>Triangle</font>')
        x = np.linspace(0, int(self.dsb_3.value()), int(self.dsb_3.value()) * int(self.dsb_4.value()))
        y = 2 * self.dsb_2.value() / np.pi * np.arcsin(np.sin(2 * np.pi * x * self.dsb_1.value()))
        table = self.findChild(pg.TableWidget, "tableWidget")
        table.setData((x, y))
        fourier_graph = self.findChild(PlotWidget, "graphicsView_2")
        fourier_graph.setTitle('<font size=12>Fourier Transform</font>')
        N = len(x)
        dt = x[1] - x[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        fourier_graph.plot().setData(y=yf, x=xf)
        graph.plot().setData(y=y, x=x)

    def sawtooth_sin(self):
        graph = self.graphicsView
        graph.setTitle('<font size=12>Sawtooth</font>')
        x = np.linspace(0, int(self.dsb_3.value()), int(self.dsb_3.value()) * int(self.dsb_4.value()))
        y = 2 * self.dsb_2.value() / np.pi * np.arctan(np.tan(2 * np.pi * self.dsb_1.value() * x))
        table = self.findChild(pg.TableWidget, "tableWidget")
        table.setData((x, y))
        fourier_graph = self.findChild(PlotWidget, "graphicsView_2")
        fourier_graph.setTitle('<font size=12>Fourier Transform</font>')
        N = len(x)
        dt = x[1] - x[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        fourier_graph.plot().setData(y=yf, x=xf)
        graph.plot().setData(y=y, x=x)

    def rectangle_sin(self):
        graph = self.graphicsView
        graph.setTitle('<font size=12>Rectangle</font>')
        x = np.linspace(0, int(self.dsb_3.value()), int(self.dsb_3.value()) * int(self.dsb_4.value()))
        y = np.sign(self.dsb_2.value() * np.sin(2 * np.pi * self.dsb_1.value() * x))
        table = self.findChild(pg.TableWidget, "tableWidget")
        table.setData((x, y))
        fourier_graph = self.findChild(PlotWidget, "graphicsView_2")
        fourier_graph.setTitle('<font size=12>Fourier Transform</font>')
        N = len(x)
        dt = x[1] - x[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        fourier_graph.plot().setData(y=yf, x=xf)
        graph.plot().setData(y=y, x=x)

    def white_noise_graph(self):
        graph = self.graphicsView
        graph.setTitle('<font size=12>White Noise</font>')
        x = np.linspace(0, int(self.dsb_3.value()), int(self.dsb_3.value()) * int(self.dsb_4.value()))
        y = self.dsb_2.value() * (2 * np.random.random(len(x)) - 1)
        table = self.findChild(pg.TableWidget, "tableWidget")
        table.setData((x, y))
        fourier_graph = self.findChild(PlotWidget, "graphicsView_2")
        fourier_graph.setTitle('<font size=12>Fourier Transform</font>')
        N = len(x)
        dt = x[1] - x[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        fourier_graph.plot().setData(y=yf, x=xf)
        graph.plot().setData(y=y, x=x)

    def reset(self):
        plot_widget = self.graphicsView
        fourier_graph = self.findChild(PlotWidget, "graphicsView_2")
        fourier_graph.setTitle('')
        plot_widget.setTitle('')
        plot_widget.clear()
        fourier_graph.clear()


app = QApplication(sys.argv)
ex = App()
app.exec_()
