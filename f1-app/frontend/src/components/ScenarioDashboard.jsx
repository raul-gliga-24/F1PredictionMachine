import { getDriverInfo } from '../utils/driverMap';
import { CheckCircle, XCircle, Target, Flag, Trophy, AlertTriangle } from 'lucide-react';

const ScenarioDashboard = ({ data }) => {
    if (!data) return null;

    const driverInfo = getDriverInfo(data.target_driver);

    if (!data.possible) {
        return (
            <div className="scenario-dashboard">
                <div className="scenario-impossible-banner">
                    <XCircle size={32} />
                    <div>
                        <h2>Championship Mathematically Impossible</h2>
                        <p>{data.summary}</p>
                        <div className="scenario-pts-row">
                            <span>Points deficit: <b>{data.points_deficit}</b></span>
                            <span>Max available: <b>{data.max_available}</b></span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="scenario-dashboard">
            {/* Possible Banner */}
            <div className="scenario-possible-banner" style={{ '--driver-color': driverInfo.color }}>
                <CheckCircle size={28} />
                <div>
                    <h2>
                        <span style={{ color: driverInfo.color }}>{driverInfo.name}</span> can still win the championship
                    </h2>
                    <p className="scenario-clinch-info">
                        Projected clinch: <b>Round {data.championship_clinched_round}</b> — <b>{data.final_projected_points} pts</b>
                    </p>
                </div>
            </div>

            {/* Summary */}
            {data.summary && (
                <blockquote className="pull-quote scenario-summary">
                    {data.summary}
                </blockquote>
            )}

            {/* Key Requirements */}
            {data.key_requirements && data.key_requirements.length > 0 && (
                <div className="scenario-requirements">
                    <h3 className="scenario-section-title">
                        <Target size={16} /> Key Requirements
                    </h3>
                    <ul className="scenario-req-list">
                        {data.key_requirements.map((req, i) => (
                            <li key={i} className="scenario-req-item">
                                <AlertTriangle size={13} className="req-icon" />
                                {req}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Race-by-race timeline */}
            {data.required_scenario && data.required_scenario.length > 0 && (
                <div className="scenario-timeline">
                    <h3 className="scenario-section-title">
                        <Flag size={16} /> Required Race Results
                    </h3>
                    <div className="timeline-list">
                        {data.required_scenario.map((race, idx) => {
                            const isClinch = race.round === data.championship_clinched_round;
                            return (
                                <div key={race.round} className={`timeline-item ${isClinch ? 'clinch-round' : ''}`}>
                                    <div className="timeline-connector">
                                        <div className="timeline-dot" style={{ background: isClinch ? '#FFD700' : driverInfo.color }} />
                                        {idx < data.required_scenario.length - 1 && <div className="timeline-line" />}
                                    </div>
                                    <div className="timeline-content">
                                        <div className="timeline-header">
                                            <span className="timeline-round">R{race.round}</span>
                                            <span className="timeline-race-name">{race.race_name}</span>
                                            {isClinch && <span className="clinch-badge"><Trophy size={11} /> Clinch</span>}
                                        </div>
                                        <div className="timeline-result">
                                            <span className="timeline-target-result" style={{ color: driverInfo.color }}>
                                                {driverInfo.name}: {race.target_result}
                                            </span>
                                            {race.critical_rival_results && Object.keys(race.critical_rival_results).length > 0 && (
                                                <div className="timeline-rivals">
                                                    {Object.entries(race.critical_rival_results).map(([dId, result]) => (
                                                        <span key={dId} className="timeline-rival-chip">
                                                            {getDriverInfo(dId).name}: {result}
                                                        </span>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                        {race.points_after_race !== undefined && (
                                            <span className="timeline-pts-after">{race.points_after_race} pts</span>
                                        )}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ScenarioDashboard;
