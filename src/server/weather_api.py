"""Small demo weather API using only the Python standard library."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
SAMPLE_START_DATE = date(2026, 5, 9)


@dataclass(frozen=True)
class WeatherForecast:
    date: str
    summary: str
    temperatureC: int


def build_weather_response() -> dict[str, Any]:
    """Return stable sample weather data for demos and client testing."""

    summaries = ("Sunny", "Partly cloudy", "Light rain")
    temperatures = (22, 19, 16)

    forecasts = [
        WeatherForecast(
            date=(SAMPLE_START_DATE + timedelta(days=index)).isoformat(),
            summary=summary,
            temperatureC=temperatures[index],
        )
        for index, summary in enumerate(summaries)
    ]

    return {
        "location": "Demo City",
        "generatedAt": "2026-05-09T00:00:00Z",
        "units": "metric",
        "forecast": [asdict(forecast) for forecast in forecasts],
    }


def route_request(path: str) -> tuple[HTTPStatus, dict[str, Any]]:
    parsed_path = urlparse(path).path

    if parsed_path == "/weather":
        return HTTPStatus.OK, build_weather_response()

    return (
        HTTPStatus.NOT_FOUND,
        {
            "error": "not_found",
            "message": f"No route matches {parsed_path}",
        },
    )


class WeatherApiHandler(BaseHTTPRequestHandler):
    server_version = "FireflySampleWeatherApi/1.0"

    def do_GET(self) -> None:
        status, payload = route_request(self.path)
        self._send_json(status, payload)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), WeatherApiHandler)


def main() -> None:
    server = create_server()
    print(f"Weather API listening on http://{DEFAULT_HOST}:{DEFAULT_PORT}/weather")
    server.serve_forever()


if __name__ == "__main__":
    main()
