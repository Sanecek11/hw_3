"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""


import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Slot
from a_threads import SystemInfo


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('System Info Widget')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Поле для ввода времени задержки
        self.delayInput = QLineEdit("1")
        self.delayInput.textChanged.connect(self.onDelayTextChanged)
        layout.addWidget(QLabel("Задержка (сек):"))
        layout.addWidget(self.delayInput)

        # Текстовое поле для вывода информации о загрузке CPU
        self.cpuLoadLabel = QLabel("Загрузка CPU: 0%")
        layout.addWidget(self.cpuLoadLabel)

        # Текстовое поле для вывода информации о загрузке RAM
        self.ramLoadLabel = QLabel("Загрузка RAM: 0%")
        layout.addWidget(self.ramLoadLabel)

        self.setLayout(layout)

        # Инициализация потока без задержки
        self.thread = SystemInfo()
        self.thread.systemInfoReceived.connect(self.updateLabels)
        self.thread.start()

    @Slot(str)
    def onDelayTextChanged(self, text):
        """Обновляет задержку в потоке при изменении текста в QLineEdit."""
        try:
            new_delay = int(text)
            self.thread.setDelay(new_delay)
        except ValueError:
            pass

    def updateLabels(self, values):
        """Обновляет метки с информацией о загрузке."""
        self.cpuLoadLabel.setText(f"Загрузка CPU: {values[0]}%")
        self.ramLoadLabel.setText(f"Загрузка RAM: {values[1]}%")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
