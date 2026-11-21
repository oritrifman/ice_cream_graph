from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFileDialog,
                               QVBoxLayout, QHBoxLayout)
# matplotlib parts that let a graph live inside a PySide6 window
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np
from About import About

class IceCreamWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = About()   # created once, but not visible until about_clicked calls show()
        self.temperatures = []
        self.revenues = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ice Cream Revenue")
        self.setGeometry(100, 100, 760, 640)

        # step 1 of layouts: widgets without parent and without setGeometry
        self.title = QLabel("Ice Cream Revenue")
        self.title.setObjectName("title")           # lets style.qss style only this label (QLabel#title)

        # each button is connected to a method: the method runs when the button is clicked
        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_clicked)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.about_clicked)

        # the graph: a figure with one axes (self.ax - draw on it like in the lessons),
        # shown inside the window by a canvas
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasQTAgg(self.fig)

        # toolbar with zoom, pan and a Save button for the graph, connected to the canvas
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # step 2: layouts
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.about_button)
        buttons_layout.addStretch()                 # pushes the buttons to the left

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        # step 3: give the main layout to the window
        self.setLayout(main_layout)

    def draw_graph(self):
        self.ax.clear()                             # remove the previous graph before drawing a new one
        self.ax.scatter(self.temperatures, self.revenues, s=1)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_title("Ice Cream Revenue vs. Temperature")
        self.ax.set_ylabel('Revenue ($)')
        self.ax.set_xlabel('Temperature (°C)')
        slope, intercept = np.polyfit(self.temperatures, self.revenues, 1)

        x_line = [min(self.temperatures), max(self.temperatures)]
        y_line = [slope * x_line[0] + intercept, slope * x_line[1] + intercept]
        self.ax.plot(x_line, y_line, color='red')
        self.ax.text(0.05, 0.9, f'y = {slope:.2f}x {intercept:+.2f}', transform=self.ax.transAxes)  
        self.canvas.draw()                          # without this line the window is not refreshed

    def load_clicked(self):
        # the dialog returns the chosen path (and the filter, which we don't need)
        file_name, _ = QFileDialog.getOpenFileName(self, "Select ice cream file", "", "CSV Files (*.csv)")
        if file_name == '':                         # the user closed the dialog without choosing
            return
        self.temperatures = []
        self.revenues = []
        with open(file_name, 'r') as f:
            next(f)
            for line in f:
                temp, revenue = line.strip().split(',')
                self.temperatures.append(float(temp))
                self.revenues.append(float(revenue))
        self.draw_graph()

    def about_clicked(self):
        self.about_window.show()

    def closeEvent(self, event):
        # PySide6 calls this when the window closes. closes About too, so the program really ends
        self.about_window.close()


if __name__ == "__main__":
    app = QApplication()

    # load the design file once, before app.exec(). run the program from the folder that has style.qss
    with open("style.qss") as f:
        app.setStyleSheet(f.read())

    window = IceCreamWindow()
    window.show()
    app.exec()
