import test from 'node:test';
import assert from 'node:assert/strict';
import { buildWeatherViewModel } from './weather-view.js';

test('buildWeatherViewModel returns empty when forecast is missing', () => {
  const viewModel = buildWeatherViewModel(null);

  assert.equal(viewModel.kind, 'empty');
});

test('buildWeatherViewModel keeps stable weather fields for populated data', () => {
  const viewModel = buildWeatherViewModel({
    location: 'Demo City',
    generatedAt: '2026-05-09T00:00:00Z',
    units: 'metric',
    forecast: [{ date: '2026-05-09', summary: 'Sunny', temperatureC: 22 }],
  });

  assert.equal(viewModel.kind, 'ready');
  assert.equal(viewModel.location, 'Demo City');
  assert.equal(viewModel.forecast[0].summary, 'Sunny');
});
