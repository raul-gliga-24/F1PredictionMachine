import React from 'react';
import { getDriverInfo } from '../utils/driverMap';
import { getTeamInfo } from '../utils/teamMap';

const StandingsTable = ({ title, type, standings }) => {
  if (!standings || standings.length === 0) return null;

  const sortedStandings = [...standings].sort((a, b) => a.position - b.position);

  return (
    <div className="standings-section">
      <h2 style={{ marginBottom: '1rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: '1rem', letterSpacing: '1px' }}>
        {title}
      </h2>
      <div className="standings-list">
        {sortedStandings.map((row) => {
          let name, subText, color;

          if (type === 'driver') {
            const info = getDriverInfo(row.driver_id);
            name = info.name;
            subText = info.team;
            color = info.color;
          } else {
            const info = getTeamInfo(row.team_id);
            name = info.name;
            subText = info.principal;
            color = info.color;
          }

          const isTop3 = row.position <= 3;
          let glowColor = 'transparent';
          if (row.position === 1) glowColor = 'rgba(255, 215, 0, 0.2)'; // Gold
          if (row.position === 2) glowColor = 'rgba(192, 192, 192, 0.2)'; // Silver
          if (row.position === 3) glowColor = 'rgba(205, 127, 50, 0.2)'; // Bronze

          return (
            <div
              key={type === 'driver' ? row.driver_id : row.team_id}
              className={`standings-item ${isTop3 ? 'top-3' : ''}`}
              style={{
                '--team-color': color,
                boxShadow: isTop3 ? `-4px 0 15px ${glowColor}` : 'none'
              }}
            >
              <div className="standings-pos">{row.position}</div>
              <div className="standings-info">
                <span className="driver-name">{name}</span>
                <span className="team-name" style={{ color: color }}>{subText}</span>
              </div>
              <div className="standings-pts">{row.points} PTS</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StandingsTable;