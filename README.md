# IMU Calibration

## UART input format

```
0.12302,0.12394,0.234324\r\n
```

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

## Testing

You can test the program using fake generated data:

```sh
python3 main.py --fake
```
