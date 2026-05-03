import React, { useState } from 'react';
import { Trophy, Medal, ChevronDown, ChevronUp } from 'lucide-react';
import { getDriverInfo } from '../utils/driverMap';

const PredictionTable = ({ predictions, summary }) => {
    const [expandedRow, setExpandedRow] = useState(null);

    if (!predictions || predictions.length === 0) return null;

    const sortedPredictions = [...predictions].sort((a, b) => a.position - b.position);

    const toggleRow = (id) => {
        setExpandedRow(expandedRow === id ? null : id);
    };

    return (
        <div className="table-wrapper">
            {summary && (
                <blockquote className="pull-quote">{summary}</blockquote>
            )}
            <table className="prediction-table">
                <thead>
                    <tr>
                        <th>Pos</th>
                        <th>Driver</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {sortedPredictions.map((pred) => {
                        const { name, team, color } = getDriverInfo(pred.driver_id);
                        const isExpanded = expandedRow === pred.driver_id;

                        return (
                            <React.Fragment key={pred.driver_id}>
                                <tr
                                    className="main-row"
                                    style={{ '--team-color': color }}
                                    onClick={() => toggleRow(pred.driver_id)}
                                >
                                    <td className="col-pos">
                                        {pred.position === 1 ? <Trophy size={20} color="#FFD700" /> :
                                            pred.position === 2 ? <Medal size={20} color="#C0C0C0" /> :
                                                pred.position === 3 ? <Medal size={20} color="#CD7F32" /> :
                                                    <span className="pos-badge">P{pred.position}</span>}
                                    </td>
                                    <td className="col-driver">
                                        <div className="driver-info">
                                            <span className="driver-name">{name}</span>
                                            <span className="team-name" style={{ color: color }}>{team}</span>
                                        </div>
                                    </td>
                                    <td>
                                        {isExpanded ? <ChevronUp size={18} color="var(--text-muted)" /> : <ChevronDown size={18} color="var(--text-muted)" />}
                                    </td>
                                </tr>
                                {isExpanded && (
                                    <tr className="reasoning-row" style={{ '--team-color': color }}>
                                        <td colSpan="3">
                                            <strong>AI Reasoning:</strong> {pred.reasoning}
                                        </td>
                                    </tr>
                                )}
                            </React.Fragment>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default PredictionTable;