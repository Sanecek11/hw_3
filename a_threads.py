"""
Модуль в котором содержаться потоки Qt
"""

import time
import requests
import psutil
from PySide6 import QtCore
from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import Slot


class SystemInfo(QtCore.QThread):
    systemInfoReceived = Signal(list)

    def __init__(self, delay=None, parent=None):
        super().__init__(parent)
        self.delay = delay if delay is not None else 1

    def run(self) -> None:
        while True:
            cpu_value = psutil.cpu_percent()
            ram_value = psutil.virtual_memory().percent
            self.systemInfoReceived.emit([cpu_value, ram_value])
            time.sleep(self.delay)

    @Slot(int)
    def setDelay(self, new_delay):
        self.delay = new_delay


class WeatherHandler(QtCore.QThread):
    weather_data_signal = Signal(dict)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = True

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay

    def run(self) -> None:
        while self.__status:
            try:
                response = requests.get(self.__api_url)
                if response.status_code == 200:
                    data = response.json()
                    self.weather_data_signal.emit(data)
                else:
                    print("Не удалось получить данные о погоде.")
            except Exception as e:
                print(f"ошибка: {e}")
            time.sleep(self.__delay)
