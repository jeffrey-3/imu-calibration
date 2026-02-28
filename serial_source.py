import numpy as np
import time
import serial
import sys
from data_source import DataSource

class SerialDataSource(DataSource):
    def __init__(self, port: str, baudrate: int):
        self.ser = serial.Serial(port, baudrate)

    def read(self):
        duration_per_position = 3
        rows = []
        positions = [
            "Upright",
            "Inverted",
            "Nose Down",
            "Nose Up",
            "Roll Left",
            "Roll Right"
        ]

        for i in range(len(positions)):
            print(positions[i])
            input("Press enter to start")
            self.ser.reset_input_buffer()
            start_time = time.time()
            time_elapsed = 0
            print_msg = ""
            while time_elapsed < duration_per_position:
                time_elapsed = time.time() - start_time
                new_print_msg = str(round(time_elapsed)) + '/' + \
                    str(duration_per_position)
                if not print_msg == new_print_msg:
                    print(new_print_msg)
                    print_msg = new_print_msg

                line = self.ser.readline()
                try:
                    line = line.decode("utf-8").strip().split(",")
                    line = [float(v) for v in line]
                    if len(line) == 3 and max(line, key=abs) < 1.5:
                        rows.append(line)
                except ValueError:
                    print("Parse error:", line)
        return np.array(rows, dtype=float)
