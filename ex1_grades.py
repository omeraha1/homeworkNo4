import os
import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QFileDialog, QMessageBox, QHeaderView
)
from PySide6.QtGui import QIntValidator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grades')
        self.resize(600, 550)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel('Grades Editor')
        self.title.setObjectName('title')
        layout.addWidget(self.title)

        top_row = QHBoxLayout()

        self.load_button = QPushButton('Open File')
        self.load_button.clicked.connect(self.load_file)
        top_row.addWidget(self.load_button)

        self.bonus_label = QLabel('Bonus:')
        top_row.addWidget(self.bonus_label)

        self.bonus_input = QLineEdit()
        self.bonus_input.setPlaceholderText('Enter number')
        self.bonus_input.setValidator(QIntValidator(-100, 100))
        self.bonus_input.returnPressed.connect(self.add_bonus)
        top_row.addWidget(self.bonus_input)

        layout.addLayout(top_row)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(['ID', 'Original Grades', 'Corrected Grades'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        bottom_row = QHBoxLayout()

        self.update_button = QPushButton('Update File')
        self.update_button.clicked.connect(self.update_file)
        bottom_row.addWidget(self.update_button)

        bottom_row.addStretch()

        self.about_button = QPushButton('About')
        self.about_button.setObjectName('aboutBtn')
        self.about_button.clicked.connect(self.show_about)
        bottom_row.addWidget(self.about_button)

        layout.addLayout(bottom_row)
        self.setLayout(layout)

    def update_table(self):
        self.table.setRowCount(len(self.student_ids))
        for row in range(len(self.student_ids)):
            self.table.setItem(row, 0, QTableWidgetItem(str(self.student_ids[row])))
            self.table.setItem(row, 1, QTableWidgetItem(str(self.original_grades[row])))
            self.table.setItem(row, 2, QTableWidgetItem(str(self.corrected_grades[row])))

    def open_file(self, path):
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', path])
        else:
            subprocess.run(['xdg-open', path])

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

        self.selected_file = file_name
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, 'r') as f:
            next(f)
            for line in f:
                s_id, grade = line.strip().split(',')
                grade = int(grade)
                self.student_ids.append(s_id)
                self.original_grades.append(grade)
                self.corrected_grades.append(grade)

        self.update_table()

    def add_bonus(self):
        text = self.bonus_input.text().strip()
        if text == '' or text == '-':
            return

        bonus = int(text)
        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if self.selected_file == '':
            return

        with open(self.selected_file, 'w') as f:
            f.write('ID,Grade\n')
            for i in range(len(self.student_ids)):
                f.write(f'{self.student_ids[i]},{self.corrected_grades[i]}\n')

        self.open_file(self.selected_file)


if __name__ == '__main__':
    app = QApplication()
    with open('style.qss', 'r') as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    app.exec()