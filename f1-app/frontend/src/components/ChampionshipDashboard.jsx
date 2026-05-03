import React from 'react';
import StandingsTable from './StandingsTable';
import RaceBreakdown from './RaceBreakdown';

const ChampionshipDashboard = ({ data }) => {
    if (!data) return null;

    return (
        <div className="championship-dashboard">
            {data.summary && (
                <blockquote className="pull-quote">
                    {data.summary}
                </blockquote>
            )}

            {data.race_results && data.race_results.length > 0 && (
                <RaceBreakdown races={data.race_results} />
            )}

            <div className="standings-grid">
                <StandingsTable
                    title="Driver Standings"
                    type="driver"
                    standings={data.driver_standings}
                />

                <StandingsTable
                    title="Constructor Standings"
                    type="constructor"
                    standings={data.constructor_standings}
                />
            </div>
        </div>
    );
};

export default ChampionshipDashboard;