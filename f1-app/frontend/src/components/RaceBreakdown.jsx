import { useState } from 'react';
import { getDriverInfo } from '../utils/driverMap';
import { ChevronDown, ChevronUp, Timer, Zap } from 'lucide-react';

const RaceBreakdown = ({ races }) => {
    const [expandedRound, setExpandedRound] = useState(null);

    if (!races || races.length === 0) return null;

    const toggle = (round) => setExpandedRound(expandedRound === round ? null : round);

    return (
        <div className="race-breakdown">
            <h2 className="breakdown-title">Race-by-Race Breakdown</h2>
            <div className="breakdown-list">
                {races.map((race) => {
                    const isOpen = expandedRound === race.round;
                    const winner = race.top_5?.[0];
                    const winnerInfo = winner ? getDriverInfo(winner) : null;

                    return (
                        <div
                            key={race.round}
                            className={`breakdown-row ${isOpen ? 'open' : ''}`}
                            style={{ '--winner-color': winnerInfo?.color || '#fff' }}
                        >
                            <button
                                className="breakdown-header"
                                onClick={() => toggle(race.round)}
                                type="button"
                            >
                                <div className="breakdown-round-badge">R{race.round}</div>
                                <div className="breakdown-race-name">{race.race_name}</div>
                                <div className="breakdown-winner-pill" style={{ color: winnerInfo?.color }}>
                                    🏆 {winnerInfo?.name || winner}
                                </div>
                                <div className="breakdown-chevron">
                                    {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                                </div>
                            </button>

                            {isOpen && (
                                <div className="breakdown-details">
                                    <div className="breakdown-top5">
                                        {(race.top_5 || []).map((driverId, idx) => {
                                            const info = getDriverInfo(driverId);
                                            return (
                                                <div key={driverId} className="breakdown-driver-row">
                                                    <span className="breakdown-position" style={{
                                                        color: idx === 0 ? '#FFD700' : idx === 1 ? '#C0C0C0' : idx === 2 ? '#CD7F32' : 'var(--text-muted)'
                                                    }}>
                                                        P{idx + 1}
                                                    </span>
                                                    <span className="breakdown-driver-bar" style={{ background: info.color }} />
                                                    <span className="breakdown-driver-name">{info.name}</span>
                                                    <span className="breakdown-driver-team" style={{ color: info.color }}>{info.team}</span>
                                                </div>
                                            );
                                        })}
                                    </div>

                                    <div className="breakdown-meta">
                                        {race.fastest_lap && (
                                            <div className="breakdown-meta-item">
                                                <Timer size={13} />
                                                <span>FL: {getDriverInfo(race.fastest_lap).name}</span>
                                            </div>
                                        )}
                                        {race.notable_dnfs && race.notable_dnfs.length > 0 && (
                                            <div className="breakdown-meta-item dnf">
                                                <Zap size={13} />
                                                <span>DNF: {race.notable_dnfs.map(id => getDriverInfo(id).name).join(', ')}</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default RaceBreakdown;
