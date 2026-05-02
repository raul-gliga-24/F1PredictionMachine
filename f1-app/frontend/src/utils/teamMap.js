const teamMap = {
  "mclaren": { name: "McLaren", principal: "Andrea Stella", color: "#FF8000" },
  "ferrari": { name: "Ferrari", principal: "Frédéric Vasseur", color: "#E8002D" },
  "red_bull": { name: "Red Bull", principal: "Christian Horner", color: "#3671C6" },
  "mercedes": { name: "Mercedes", principal: "Toto Wolff", color: "#27F4D2" },
  "aston_martin": { name: "Aston Martin", principal: "Mike Krack", color: "#229971" },
  "alpine": { name: "Alpine", principal: "Oliver Oakes", color: "#FF87BC" },
  "haas": { name: "Haas", principal: "Ayao Komatsu", color: "#B6BABD" },
  "rb": { name: "Racing Bulls", principal: "Laurent Mekies", color: "#6692FF" },
  "williams": { name: "Williams", principal: "James Vowles", color: "#00A1FE" },
  "audi": { name: "Audi", principal: "Mattia Binotto", color: "#F50537" },
  "cadillac": { name: "Cadillac", principal: "Michael Andretti", color: "#D4AF37" }
};

export const getTeamInfo = (team_id) => {
  if (!teamMap[team_id]) {
    const formattedName = team_id.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    return { name: formattedName, principal: "Unknown", color: "#FFFFFF" };
  }
  return teamMap[team_id];
};
