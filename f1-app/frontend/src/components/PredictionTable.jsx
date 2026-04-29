import React from 'react';
import { Trophy, Medal } from 'lucide-react';
import { getDriverInfo } from '../utils/driverMap';

const PredictionTable = ({ predictions }) => {
    if (!predictions || predictions.length === 0) {
        return null;
    }

    const sortedPredictions = [...predictions].sort((a, b) => a.position - b.position);

    return (
        <div className='table-wrapper'>
            <table className='prediction-table'>
                <thead>
                    <tr>
                        <th>Pos</th>
                        <th>Driver</th>
                        <th>Reasoning</th>

                    </tr>
                </thead>
                <tbody>
                    {sortedPredictions.map((pred) => {
                        const { name, team, color } = getDriverInfo(pred.driver_id);

                        return (

                            <tr key={pred.driver_id} style={{ '--team-color': color }}>
                                <td className='col-pos'>
                                    {
                                        pred.position === 1 ? <Trophy size={20} color='#FFD700' /> :
                                            pred.position === 2 ? <Trophy size={20} color='#C0C0C0' /> :
                                                pred.position === 3 ? <Trophy size={20} color='#CD7F32' /> :
                                                    <span className='pos-text'>{pred.position}</span>
                                    }
                                </td>

                                <td className='col-driver'>
                                    <div className='driver-info'>
                                        <span className='driver-name'>{name}</span>
                                        <span className='team-name' style={{ color: color }}>{team}</span>

                                    </div>
                                </td>

                                <td className='col-reasoning'>{pred.reasoning}</td>

                            </tr>



                        );
                    })}
                </tbody>

            </table>
        </div>

    );
};

export default PredictionTable;