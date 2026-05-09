import { useEffect, useState } from 'react';
import { fetchWeather } from './weather-api.js';
import { buildWeatherViewModel } from './weather-view.js';

const initialState = { status: 'loading', data: null, error: null };

export function App() {
  const [state, setState] = useState(initialState);

  useEffect(() => {
    const controller = new AbortController();

    async function loadWeather() {
      setState({ status: 'loading', data: null, error: null });

      try {
        const data = await fetchWeather(controller.signal);
        setState({ status: 'ready', data, error: null });
      } catch (error) {
        if (error.name === 'AbortError') {
          return;
        }

        setState({
          status: 'error',
          data: null,
          error: error instanceof Error ? error.message : 'Unable to load weather data.',
        });
      }
    }

    loadWeather();

    return () => controller.abort();
  }, []);

  const viewModel = buildWeatherViewModel(state.data);

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Firefly sample</p>
          <h1>Demo Weather</h1>
          <p className="lede">
            A compact React client for the demo weather contract.
          </p>
        </div>
        <button className="button" onClick={() => window.location.reload()} type="button">
          Refresh
        </button>
      </section>

      {state.status === 'loading' && <StatusPanel title="Loading weather data" />}

      {state.status === 'error' && (
        <StatusPanel
          title="Weather request failed"
          message={state.error}
          tone="error"
        />
      )}

      {viewModel.kind === 'empty' && state.status === 'ready' && (
        <StatusPanel title="No forecast available" message={viewModel.message} tone="empty" />
      )}

      {viewModel.kind === 'ready' && (
        <section className="panel">
          <div className="summary-grid">
            <Metric label="Location" value={viewModel.location} />
            <Metric label="Generated" value={viewModel.generatedAt} />
            <Metric label="Units" value={viewModel.units} />
          </div>

          <div className="forecast-list">
            {viewModel.forecast.map((forecast) => (
              <article className="forecast-card" key={forecast.date}>
                <p className="forecast-date">{forecast.date}</p>
                <h2>{forecast.summary}</h2>
                <p className="forecast-temp">{forecast.temperatureC} °C</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

function StatusPanel({ title, message, tone = 'default' }) {
  return (
    <section className={`panel panel-${tone}`}>
      <h2>{title}</h2>
      {message ? <p>{message}</p> : null}
    </section>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
