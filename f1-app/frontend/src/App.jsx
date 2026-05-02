import { useState } from 'react';
import './App.css';
import RaceSelector from './components/RaceSelector';
import PredictionTable from './components/PredictionTable';
import ChampionshipDashboard from './components/ChampionshipDashboard';
import { predictRace, predictChampionship } from './api/api';

function App() {
  const [predictionData, setPredictionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [currentMode, setCurrentMode] = useState('race');

  const handlePredict = async (predictionConfig) => {
    const { mode, season, round } = predictionConfig;

    setIsLoading(true);
    setError(null);
    setPredictionData(null);
    setCurrentMode(mode);

    try {
      let data;

      if (mode === 'race') {
        data = await predictRace(season, round);
      } else {
        data = await predictChampionship(season);
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
          <h2>Select Prediction</h2>
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

              {currentMode === 'race' ? (
                <PredictionTable predictions={predictionData.predicted_order || predictionData.predictions} />
              ) : (
                <ChampionshipDashboard data={predictionData} />
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;