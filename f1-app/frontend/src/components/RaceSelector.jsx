import { useState, useEffect } from 'react';
import { Trophy, Flag } from 'lucide-react';

function RaceSelector({ onPredict }) {

    const [mode, setMode] = useState('race');

    const [season, setSeason] = useState('2026');
    const [round, setRound] = useState('4');

    const [schedule, setSchedule] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const availableSeasons = [2027, 2026, 2025, 2024];

    useEffect(() => {
        const fetchSchedule = async () => {
            setIsLoading(true);
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
                setIsLoading(false);
            }
        };

        fetchSchedule();
    }, [season]);

    const handlePredict = () => {

        if (mode === 'race') {
            onPredict({ mode: 'race', season, round })
        } else {
            onPredict({ mode: 'championship', season })
        }
    };


    return (
        <div className='race-selector'>
            <div className='mode-toggle-container'>
                <div className='mode-toggle'>
                    <button
                        type='button'
                        className={`toggle-btn ${mode === 'race' ? 'active' : ''}`}
                        onClick={() => setMode('race')}
                    >
                        <Flag size={16} /> Single Race
                    </button>
                    <button
                        type='button'
                        className={`toggle-btn ${mode === 'championship' ? 'active' : ''}`}
                        onClick={() => setMode('championship')}
                    >
                        <Trophy size={16} />Championship
                    </button>
                </div>
            </div>
            <div className='form-group'>
                <label>Season</label>
                <select value={season} onChange={(e) => setSeason(e.target.value)}>
                    {availableSeasons.map(s => (
                        <option key={s} value={s}>{s}</option>
                    ))}
                </select>
            </div>

            {mode === 'race' && (
                <div className='form-group slide-in'>
                    <label>Round</label>
                    <select value={round} onChange={(e) => setRound(e.target.value)} disabled={isLoading}>
                        {isLoading ? (
                            <option>Loading schedule...</option>
                        ) : (
                            schedule.map(r => (
                                <option key={r.round} value={r.round}>Round {r.round} - {r.raceName}</option>
                            ))
                        )}
                    </select>
                </div>
            )}
            <button className='predict-btn' onClick={handlePredict}>
                Predict {mode === 'race' ? 'Race' : 'Season'}
            </button>
        </div>
    )
}
export default RaceSelector;