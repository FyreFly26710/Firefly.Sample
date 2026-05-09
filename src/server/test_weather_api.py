import json
import threading
import unittest
from http import HTTPStatus
from urllib.request import urlopen

from weather_api import build_weather_response, create_server, route_request


class WeatherApiTests(unittest.TestCase):
    def test_weather_response_has_stable_demo_contract(self):
        payload = build_weather_response()

        self.assertEqual(payload["location"], "Demo City")
        self.assertEqual(payload["generatedAt"], "2026-05-09T00:00:00Z")
        self.assertEqual(payload["units"], "metric")
        self.assertEqual(
            payload["forecast"],
            [
                {"date": "2026-05-09", "summary": "Sunny", "temperatureC": 22},
                {"date": "2026-05-10", "summary": "Partly cloudy", "temperatureC": 19},
                {"date": "2026-05-11", "summary": "Light rain", "temperatureC": 16},
            ],
        )

    def test_route_request_serves_weather_endpoint(self):
        status, payload = route_request("/weather")

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(payload["forecast"][0]["summary"], "Sunny")

    def test_route_request_returns_json_404_for_unknown_paths(self):
        status, payload = route_request("/missing")

        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual(payload["error"], "not_found")
        self.assertEqual(payload["message"], "No route matches /missing")

    def test_server_returns_weather_json(self):
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            host, port = server.server_address
            with urlopen(f"http://{host}:{port}/weather", timeout=2) as response:
                payload = json.loads(response.read().decode("utf-8"))

            self.assertEqual(response.status, HTTPStatus.OK)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(payload["location"], "Demo City")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
