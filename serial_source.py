import numpy as np
import serial
import sys
from data_source import DataSource

class SerialDataSource(DataSource):
    def __init__(self, port: str, baudrate: int):
        self.ser = serial.Serial(port, baudrate)

    def read(self):
        rows = []
        while len(rows) < 2000:
            line = self.ser.readline()
            try:
                line = line.decode("utf-8").strip().split(",")
                line = [float(v) for v in line]
                if len(line) == 3:
                    rows.append(line)
                    print(line)
            except ValueError:
                print("Parse error:", line)
        return np.array(rows, dtype=float)
