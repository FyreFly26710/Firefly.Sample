export function buildWeatherViewModel(payload) {
  if (!payload || !Array.isArray(payload.forecast)) {
    return { kind: 'empty', message: 'No forecast data is available.' };
  }

  if (payload.forecast.length === 0) {
    return { kind: 'empty', message: 'No forecast data is available.' };
  }

  return {
    kind: 'ready',
    location: payload.location,
    generatedAt: payload.generatedAt,
    units: payload.units,
    forecast: payload.forecast,
  };
}
