import serial
from data_source import DataSource

class SerialDataSource(DataSource):
    def __init__(self, port: str, baudrate: int):
        self.ser = serial.Serial(port, baudrate)

    def read(self) -> list:
        return self.ser.read()
