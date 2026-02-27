# IMU Calibration

## File input format

The program reads a `.txt` file and calibrates the gyroscope and accelerometer.
There must not be a header.
The columns from left to right should be: gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z.
The units for gyroscope are in radians/sec and the units for accelerometer should be in g.
An example of the file format is located in the `examples` folder.

## Running the program

1. Create the virtual environment

```sh
python3 -m venv venv/
```

2. Activate the virtual environment

```sh
source venv/bin/activate
```

3. Install dependencies

```sh
pip install -r requirements.txt
```

4. Run the program

```sh
python3 main.py
```
