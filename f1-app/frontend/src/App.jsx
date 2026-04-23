import './App.css';
import RaceSelector from './components/RaceSelector';

function App() {
  const handlePredict = (season, round) => {
    console.log(`Predicting for Season: ${season}, Round: ${round}`);
    // We will add the fetch() call to the backend here later
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
        
        <div className="card">
          <h2>Prediction Results</h2>
          <p style={{color: "var(--text-secondary)"}}>Run a prediction to see the results.</p>
        </div>
      </main>
    </div>
  );
}

export default App;
