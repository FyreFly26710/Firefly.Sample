export async function fetchWeather(signal) {
  const response = await fetch('/weather', {
    headers: { Accept: 'application/json' },
    signal,
  });

  if (!response.ok) {
    throw new Error(`Weather request failed with status ${response.status}`);
  }

  return response.json();
}
