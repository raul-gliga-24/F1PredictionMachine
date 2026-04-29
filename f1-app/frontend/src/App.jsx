import { useState } from 'react';
import './App.css';
import RaceSelector from './components/RaceSelector';
import PredictionTable from './components/PredictionTable';

function App() {
  const [predictionData, setPredictionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (season, round) => {
    setIsLoading(true);
    setError(null);
    setPredictionData(null);

    try {
      const response = await fetch(`http://localhost:8000/api/predictions/pre-race/${season}/${round}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to fetch prediction");
      }

      setPredictionData(data);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>F1 Race Predictor</h1>
        <p>AI-Powered insights for the 2026 Season</p>
      </header>

      <main className="dashboard">
        <div className="card">
          <h2>Select Race</h2>
          <RaceSelector onPredict={handlePredict} />
        </div>

        <div className="card results-card">
          <h2>Prediction Results</h2>

          {isLoading && <div className='loading-state'>Generating AI Predictions...</div>}

          {error && <div className='error-state'>{error}</div>}

          {!isLoading && !error && !predictionData && (
            <p style={{ color: "var(--text-secondary)" }}>Run a prediction to see the results.</p>
          )}

          {!isLoading && !error && predictionData && (
            <div className='prediction-content'>
              {predictionData.summary && (
                <div className='prediction-summary'>
                  <p>{predictionData.summary}</p>
                </div>
              )}
              <PredictionTable predictions={predictionData.predicted_order} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
