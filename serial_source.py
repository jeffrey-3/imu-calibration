import serial
import sys
from data_source import DataSource

class SerialDataSource(DataSource):
    def __init__(self, port: str, baudrate: int):
        self.ser = serial.Serial(port, baudrate)

    def read(self):
        try:
            while True:
                b = self.ser.read(1)
                if b:
                    sys.stdout.write(b.decode(errors='replace'))
                    sys.stdout.flush()
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.ser.close()
