import { useState } from 'react';
import { Trophy, Flag } from 'lucide-react';

function RaceSelector({ onPredict }) {

    const [mode, setMode] = useState('race');

    const [season, setSeason] = useState('2026');
    const [round, setRound] = useState('4');


    const handlePredict = () => {

        if (mode === 'race') {
            onPredict({ mode: 'race', season, round })
        } else {
            onPredict({ mode: 'championship', season })
        }
    };


    return (
        <div className='race-selectoor'>
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
                <label>Seasonn</label>
                <select value={season} onChange={(e) => setSeason(e.target.value)}>
                    <option value="2026">2026</option>
                    <option value="2025">2025</option>
                </select>
            </div>

            {mode === 'race' && (
                <div className='form-group slide-in'>
                    <label>Round</label>
                    <select value={round} onChange={(e) => setRound(e.target.value)}>
                        <option value="1">Round 1 (Australia)</option>
                        <option value="2">Round 2 (China)</option>
                        <option value="3">Round 3 (Japan)</option>
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