import { useState, useEffect } from 'react';
import { Trophy, Flag, Crosshair } from 'lucide-react';

// Driver list for Scenario mode — hardcoded for zero API overhead
const SCENARIO_DRIVERS = [
    { id: 'norris', name: 'Lando Norris' },
    { id: 'piastri', name: 'Oscar Piastri' },
    { id: 'leclerc', name: 'Charles Leclerc' },
    { id: 'hamilton', name: 'Lewis Hamilton' },
    { id: 'verstappen', name: 'Max Verstappen' },
    { id: 'hadjar', name: 'Isack Hadjar' },
    { id: 'russell', name: 'George Russell' },
    { id: 'antonelli', name: 'Kimi Antonelli' },
    { id: 'alonso', name: 'Fernando Alonso' },
    { id: 'stroll', name: 'Lance Stroll' },
    { id: 'gasly', name: 'Pierre Gasly' },
    { id: 'colapinto', name: 'Franco Colapinto' },
    { id: 'ocon', name: 'Esteban Ocon' },
    { id: 'bearman', name: 'Oliver Bearman' },
    { id: 'lawson', name: 'Liam Lawson' },
    { id: 'lindblad', name: 'Arvid Lindblad' },
    { id: 'albon', name: 'Alex Albon' },
    { id: 'sainz', name: 'Carlos Sainz' },
    { id: 'hulkenberg', name: 'Nico Hülkenberg' },
    { id: 'bortoleto', name: 'Gabriel Bortoleto' },
];

function RaceSelector({ onPredict, isLoading }) {
    const [mode, setMode] = useState('race');
    const [detailMode, setDetailMode] = useState('simple'); // 'simple' | 'detailed'
    const [season, setSeason] = useState('2026');
    const [round, setRound] = useState('4');
    const [schedule, setSchedule] = useState([]);
    const [scheduleLoading, setScheduleLoading] = useState(false);
    const [scenarioDriver, setScenarioDriver] = useState('verstappen');

    const availableSeasons = [2027, 2026, 2025, 2024];

    useEffect(() => {
        const fetchSchedule = async () => {
            setScheduleLoading(true);
            try {
                const response = await fetch(`http://localhost:8000/api/races/schedule/${season}`);
                if (response.ok) {
                    const data = await response.json();
                    setSchedule(data.schedule || []);
                    if (data.schedule && data.schedule.length > 0) {
                        setRound(data.schedule[0].round.toString());
                    }
                }
            } catch (error) {
                console.error("Failed to fetch schedule", error);
            } finally {
                setScheduleLoading(false);
            }
        };
        fetchSchedule();
    }, [season]);

    const handlePredict = () => {
        if (mode === 'race') {
            onPredict({ mode: 'race', season, round });
        } else if (mode === 'championship') {
            onPredict({ mode: 'championship', season, detailed: detailMode === 'detailed' });
        } else {
            onPredict({ mode: 'scenario', season, driverId: scenarioDriver });
        }
    };

    const modeButtons = [
        { id: 'race', label: 'Single Race', icon: <Flag size={15} /> },
        { id: 'championship', label: 'Season', icon: <Trophy size={15} /> },
        { id: 'scenario', label: 'Simulate to Win', icon: <Crosshair size={15} /> },
    ];

    return (
        <div className='race-selector'>
            {/* Mode Toggle */}
            <div className='mode-toggle'>
                {modeButtons.map(btn => (
                    <button
                        key={btn.id}
                        type='button'
                        className={`toggle-btn ${mode === btn.id ? 'active' : ''}`}
                        onClick={() => setMode(btn.id)}
                    >
                        {btn.icon} {btn.label}
                    </button>
                ))}
            </div>

            {/* Season */}
            <div className='form-group'>
                <label>Season</label>
                <select value={season} onChange={(e) => setSeason(e.target.value)}>
                    {availableSeasons.map(s => (
                        <option key={s} value={s}>{s}</option>
                    ))}
                </select>
            </div>

            {/* Race round (Single Race mode) */}
            {mode === 'race' && (
                <div className='form-group slide-in'>
                    <label>Round</label>
                    <select value={round} onChange={(e) => setRound(e.target.value)} disabled={scheduleLoading}>
                        {scheduleLoading ? (
                            <option>Loading schedule...</option>
                        ) : (
                            schedule.map(r => (
                                <option key={r.round} value={r.round}>Round {r.round} - {r.raceName}</option>
                            ))
                        )}
                    </select>
                </div>
            )}

            {/* Detail mode (Season mode) */}
            {mode === 'championship' && (
                <div className='form-group slide-in'>
                    <label>Detail Level</label>
                    <div className='detail-toggle'>
                        <button
                            type='button'
                            className={`toggle-btn ${detailMode === 'simple' ? 'active' : ''}`}
                            onClick={() => setDetailMode('simple')}
                        >
                            Simple
                        </button>
                        <button
                            type='button'
                            className={`toggle-btn ${detailMode === 'detailed' ? 'active' : ''}`}
                            onClick={() => setDetailMode('detailed')}
                        >
                            Detailed
                        </button>
                    </div>
                </div>
            )}

            {/* Driver selector (Scenario mode) */}
            {mode === 'scenario' && (
                <div className='form-group slide-in'>
                    <label>Simulate until wins</label>
                    <select value={scenarioDriver} onChange={(e) => setScenarioDriver(e.target.value)}>
                        {SCENARIO_DRIVERS.map(d => (
                            <option key={d.id} value={d.id}>{d.name}</option>
                        ))}
                    </select>
                </div>
            )}

            <button className='predict-btn' onClick={handlePredict} disabled={isLoading}>
                {isLoading ? 'Running...' : `Predict ${mode === 'race' ? 'Race' : mode === 'championship' ? 'Season' : 'Scenario'}`}
            </button>
        </div>
    );
}

export default RaceSelector;