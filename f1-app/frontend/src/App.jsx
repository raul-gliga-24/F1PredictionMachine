import { useState, useEffect } from 'react';
import './App.css';
import RaceSelector from './components/RaceSelector';
import PredictionTable from './components/PredictionTable';
import ChampionshipDashboard from './components/ChampionshipDashboard';
import ScenarioDashboard from './components/ScenarioDashboard';
import { predictRace, predictChampionship, predictScenario } from './api/api';
import { Gauge } from 'lucide-react';

function App() {
  const [predictionData, setPredictionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentMode, setCurrentMode] = useState('race');

  const handlePredict = async (predictionConfig) => {
    const { mode, season, round, detailed, driverId } = predictionConfig;

    setIsLoading(true);
    setError(null);
    setPredictionData(null);
    setCurrentMode(mode);

    try {
      let data;
      if (mode === 'race') {
        data = await predictRace(season, round);
      } else if (mode === 'championship') {
        data = await predictChampionship(season, detailed);
      } else {
        data = await predictScenario(season, driverId);
      }
      setPredictionData(data);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const hasResults = isLoading || error || predictionData;

  useEffect(() => {
    if (hasResults) {
      document.body.classList.add('has-results');
    } else {
      document.body.classList.remove('has-results');
    }
  }, [hasResults]);

  const renderResults = () => {
    if (currentMode === 'race') {
      return <PredictionTable predictions={predictionData.predicted_order || predictionData.predictions} summary={predictionData.summary} />;
    } else if (currentMode === 'championship') {
      return <ChampionshipDashboard data={predictionData} />;
    } else {
      return <ScenarioDashboard data={predictionData} />;
    }
  };

  return (
    <>
      <div className="speed-lines">
        <div className="speed-line line-1"></div>
        <div className="speed-line line-2"></div>
        <div className="speed-line line-3"></div>
        <div className="speed-line line-4"></div>
      </div>
      <div className={`app-container ${hasResults ? 'has-results' : ''}`}>
        <header className="app-header">
          <div className="brand-logo">
            <Gauge size={24} className="brand-icon" />
            <span className="brand-text">F1<b>Predict</b></span>
          </div>
          <h1>Season Predictor <span className="beta-chip">BETA</span></h1>
        </header>

        <main className="dashboard">
          <div className="card">
            <RaceSelector onPredict={handlePredict} isLoading={isLoading} />
          </div>
          {hasResults && (
            <div className="results-area">
              {isLoading && <div className='loading-state'>Generating AI Predictions...</div>}
              {error && <div className='error-state'>{error}</div>}
              {!isLoading && !error && predictionData && (
                <div className='prediction-content'>
                  {renderResults()}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </>
  );
}

export default App;