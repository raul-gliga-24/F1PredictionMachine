import { useState } from 'react';

function RaceSelector({ onPredict }) {
    const [season, setSeason] = useState('2026');
    const [round, setRound] = useState('4');


    const handlePredict = () => {
        onPredict(season, round);
    };


    return (
        <div className="race-selector">
            <div className="form-group">
                <label>Season</label>
                <select value={season}
                    onChange={(e) => setSeason(e.target.value)}>
                    <option
                        value="2026">2026</option>
                    <option value="2025">2025</option>
                </select>
            </div>

            <div className="form-group">
                <label>Round</label>
                <select value={round}
                    onChange={(e) => setRound(e.target.value)}>
                    <option value="1">Round 1(Australia)</option>
                    <option value="2">Round 2(China)</option>
                    <option value="3">Round 3(Japan)</option>
                    <option value="4">Round 4(Miami)</option>

                </select>
            </div>

            <button className="predict-btn" onClick={handlePredict}>
                Predict Race
            </button>



        </div>







    );

}
export default RaceSelector;