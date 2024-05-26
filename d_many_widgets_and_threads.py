"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""


import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,\
    QSlider, QHBoxLayout, QWidget
from PySide6.QtCore import Slot, Qt
from a_threads import SystemInfo, WeatherHandler  # Предполагается, что эти классы доступны


class SystemInfoWidget(QWidget):
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


class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.lat_input = QLineEdit(self)
        self.lon_input = QLineEdit(self)
        self.lat_input.setPlaceholderText("Введите широту")
        self.lon_input.setPlaceholderText("Введите долготу")
        layout.addWidget(self.lat_input)
        layout.addWidget(self.lon_input)

        self.delay_slider = QSlider(Qt.Horizontal, self)
        self.delay_slider.setMinimum(1)
        self.delay_slider.setMaximum(60)
        self.delay_slider.setValue(10)
        layout.addWidget(self.delay_slider)

        self.start_stop_button = QPushButton('Start', self)
        self.start_stop_button.clicked.connect(self.toggle_thread)
        layout.addWidget(self.start_stop_button)

        self.setLayout(layout)
        self.setWindowTitle('Weather App')

    @Slot()
    def toggle_thread(self):
        lat = float(self.lat_input.text())
        lon = float(self.lon_input.text())
        delay = self.delay_slider.value()
        print(delay)

        if hasattr(self, 'weather_handler') and self.weather_handler.isRunning():
            self.enable_fields(True)
            return

        self.weather_handler = WeatherHandler(lat, lon)
        self.weather_handler.weather_data_signal.connect(self.print_weather_data)
        self.weather_handler.start()
        self.enable_fields(False)

    def print_weather_data(self, data):
        print(data)  # Выводим данные о погоде в stdout

    def enable_fields(self, enabled):
        self.lat_input.setEnabled(enabled)
        self.lon_input.setEnabled(enabled)
        self.delay_slider.setEnabled(enabled)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sysinfo and Weather')
        self.setGeometry(100, 100, 200, 200)

        tab_widget = QTabWidget()
        self.system_info_tab = SystemInfoWidget()
        self.weather_tab = WeatherWidget()

        tab_widget.addTab(self.system_info_tab, "System Info")
        tab_widget.addTab(self.weather_tab, "Weather")

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(tab_widget)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
