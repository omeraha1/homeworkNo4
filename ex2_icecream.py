from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Cream Sales')
        self.resize(700, 550)

        self.temps = []
        self.profits = []

        self.build_ui()
        self.draw_graph()

    def build_ui(self):
        layout = QVBoxLayout()

        top = QHBoxLayout()
        self.btn_open = QPushButton('Open File')
        self.btn_open.clicked.connect(self.load_file)
        top.addWidget(self.btn_open)

        top.addStretch()

        self.btn_about = QPushButton('About')
        self.btn_about.setObjectName('aboutBtn')
        self.btn_about.clicked.connect(self.show_about)
        top.addWidget(self.btn_about)

        layout.addLayout(top)

        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def show_about(self):
        QMessageBox.about(
            self,
            'About',
            'Omer Aharon\n'
            'aharonomer3@gmail.com\n\n'
            'GitHub: https://github.com/omeraha1/homeworkNo4'
        )

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Select File', '', 'CSV Files (*.csv);;All Files (*)'
        )
        if not file_name:
            return

        self.temps = []
        self.profits = []

        with open(file_name, 'r') as f:
            next(f)
            for line in f:
                t, p = line.strip().split(',')
                self.temps.append(float(t))
                self.profits.append(float(p))

        self.draw_graph()

    def draw_graph(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        ax.scatter(self.temps, self.profits, s=1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.set_title('Ice Cream Revenue vs. Temperature')
        ax.set_xlabel('Temperature (°C)')
        ax.set_ylabel('Revenue ($)')

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication()
    with open('style.qss', 'r') as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    app.exec()