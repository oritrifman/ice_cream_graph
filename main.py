from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFileDialog,
                               QVBoxLayout, QHBoxLayout)
# matplotlib parts that let a graph live inside a PySide6 window
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
# TODO (your code): import numpy as np
from About import About


class IceCreamWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = About()   # created once, but not visible until about_clicked calls show()

        # TODO (your code): define the two lists of the window here (temperatures and revenues)

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

        self.draw_graph()                           # shows the temporary graph at start

    def draw_graph(self):
        # temporary graph - TODO (your code): replace it with the real graph
        self.ax.clear()                             # remove the previous graph before drawing a new one
        self.ax.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
        self.ax.set_title("Temporary graph")
        self.canvas.draw()                          # without this line the window is not refreshed

        # TODO (your code), inside this method:
        # - scatter with point size 1: temperature on the X axis, revenue on the Y axis
        # - remove the top and right lines of the frame
        # - a correct title and axis titles
        # - the trend line (np.polyfit) with its equation written on the graph

    def load_clicked(self):
        # the dialog returns the chosen path (and the filter, which we don't need)
        file_name, _ = QFileDialog.getOpenFileName(self, "Select ice cream file", "", "CSV Files (*.csv)")
        if file_name == '':                         # the user closed the dialog without choosing
            return

        # TODO (your code):
        # 1. open the file for reading, skip the header line
        # 2. for every line: append the temperature and the revenue to the two lists you defined in __init__
        #    (tip: temperatures have decimals - use float, not int)
        # 3. call self.draw_graph()

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
