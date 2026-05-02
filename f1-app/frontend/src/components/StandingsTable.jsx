import React from "react";
import { Trophy, Medal } from "lucide-react";
import { getDriverInfo } from "../utils/driverMap"
import { getTeamInfo } from "../utils/teamMap";

const StandingsTable = ({ title, type, standings }) => {
  if (!standings || standings.length === 0) return null;

  const sortedStanding = [...standings].sort((a, b) => a.position - b.position);


  return (
    <div className="standings-section">
      <h3 className="standings-title">{title}</h3>
      <div className="table-wrapper">
        <table className="prediction-table">
          <thead>
            <tr>
              <th>Pos</th>
              <th>{type === 'driver' ? 'Driver' : 'Team'}</th>
              <th>Points</th>
              <th>Reasoning</th>
            </tr>
          </thead>
          <tbody>
            {sortedStanding.map((row) => {
              let name, subText, color

              if (type === 'driver') {
                const info = getDriverInfo(row.driver_id);
                name = info.name
                subText = info.team;
                color = info.color;
              }
              else {
                const info = getTeamInfo(row.team_id);
                name = info.name
                subText = info.team;
                color = info.color;
              }

              return (
                <tr key={type === 'driver' ? row.driver_id : row.team_id} style={{ '--team-color': color }}>
                  <td className="col-pos">
                    {row.position === 1 ? <Trophy size={20} color="#FFD700" /> :
                      row.position === 2 ? <Medal size={20} color="#C0C0C0" /> :
                        row.position === 3 ? <Medal size={20} color="#CD7F32" /> :
                          <span className="pos-text">P{row.position}</span>}
                  </td>
                  <td className="col-driver">
                    <div className="driver-info">
                      <span className="driver-name">{name}</span>
                      <span className="team-name" style={{ color: color }}>{subText}</span>
                    </div>
                  </td>
                  <td className="col-pts">{row.points}</td>
                  <td className="col-reasoning">{row.reasoning}</td>
                </tr>
              );

            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default StandingsTable;