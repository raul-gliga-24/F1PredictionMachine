import React from "react";
import StandingsTable from "./StandingsTable";

const ChampionshipDashboard = ({ data }) => {
    if (!data) return null;

    return (
        <div className="results-card championship-dashboard">
            {data.summary && (
                <div className="championship-summary">
                    <h2>Season Overview</h2>
                    <p className="summary-text">{data.summary}</p>
                </div>
            )}
            <div className="standings-grid">
                <StandingsTable
                    title="Driver's Championship"
                    type="driver"
                    standings={data.driver_standings}
                />

                <StandingsTable
                    title="Constructor's Championship"
                    type="constructor"
                    standings={data.constructor_standings}
                />
            </div>
        </div>
    );
};
export default ChampionshipDashboard;