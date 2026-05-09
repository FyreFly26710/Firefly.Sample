# Server

This folder contains a dependency-free demo weather API.

## Run

```bash
python3 src/server/weather_api.py
```

The API listens on `http://127.0.0.1:8000/weather` and returns stable sample weather data.

## Validate

```bash
python3 -m unittest discover -s src/server -p 'test_*.py'
```
