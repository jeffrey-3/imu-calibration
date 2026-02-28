import numpy as np
import time
import serial
import sys
from data_source import DataSource

class SerialDataSource(DataSource):
    def __init__(self, port: str, baudrate: int):
        self.ser = serial.Serial(port, baudrate)

    def read(self):
        start_time = time.time()
        duration_per_position = 5
        time_elapsed = 0
        rows = []
        positions = [
            "Upright",
            "Inverted",
            "Nose Down",
            "Nose Up",
            "Roll Left",
            "Roll Right"
        ]
        while time_elapsed < duration_per_position * len(positions):
            time_elapsed = time.time() - start_time
            position = min(int(time_elapsed // duration_per_position),
                len(positions) - 1)
            print(positions[position])
            print(round(time_elapsed - position * duration_per_position), "/",
                duration_per_position)
            print(position + 1, "/", len(positions))

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
