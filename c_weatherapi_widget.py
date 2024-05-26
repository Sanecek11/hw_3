"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""


from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QSlider, QHBoxLayout
from PySide6.QtCore import Slot, Qt
from a_threads import WeatherHandler
import sys


class MainWindow(QWidget):
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
        self.enable_fields(True)

    def print_weather_data(self, data):
        print(data)  # Выводим данные о погоде в stdout

    def enable_fields(self, enabled):
        self.lat_input.setEnabled(enabled)
        self.lon_input.setEnabled(enabled)
        self.delay_slider.setEnabled(enabled)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
