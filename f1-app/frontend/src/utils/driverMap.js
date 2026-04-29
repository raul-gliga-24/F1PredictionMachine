const driverMap = {
  // McLaren
  "norris": { name: "Lando Norris", team: "McLaren", color: "#FF8000" },
  "piastri": { name: "Oscar Piastri", team: "McLaren", color: "#FF8000" },

  // Ferrari
  "leclerc": { name: "Charles Leclerc", team: "Ferrari", color: "#E8002D" },
  "hamilton": { name: "Lewis Hamilton", team: "Ferrari", color: "#E8002D" },

  // Red Bull Racing
  "verstappen": { name: "Max Verstappen", team: "Red Bull", color: "#3671C6" },
  "hadjar": { name: "Isack Hadjar", team: "Red Bull", color: "#3671C6" },

  // Mercedes
  "russell": { name: "George Russell", team: "Mercedes", color: "#27F4D2" },
  "antonelli": { name: "Kimi Antonelli", team: "Mercedes", color: "#27F4D2" },

  // Aston Martin
  "alonso": { name: "Fernando Alonso", team: "Aston Martin", color: "#229971" },
  "stroll": { name: "Lance Stroll", team: "Aston Martin", color: "#229971" },

  // Alpine
  "gasly": { name: "Pierre Gasly", team: "Alpine", color: "#FF87BC" },
  "colapinto": { name: "Franco Colapinto", team: "Alpine", color: "#FF87BC" },

  // Haas
  "ocon": { name: "Esteban Ocon", team: "Haas", color: "#B6BABD" },
  "bearman": { name: "Oliver Bearman", team: "Haas", color: "#B6BABD" },

  // Racing Bulls (RB)
  "lawson": { name: "Liam Lawson", team: "Racing Bulls", color: "#6692FF" },
  "lindblad": { name: "Arvid Lindblad", team: "Racing Bulls", color: "#6692FF" },

  // Williams
  "albon": { name: "Alex Albon", team: "Williams", color: "#00A1FE" },
  "sainz": { name: "Carlos Sainz", team: "Williams", color: "#00A1FE" },

  // Audi
  "hulkenberg": { name: "Nico Hülkenberg", team: "Audi", color: "#F50537" },
  "bortoleto": { name: "Gabriel Bortoleto", team: "Audi", color: "#F50537" },

  // Cadillac
  "perez": { name: "Sergio Pérez", team: "Cadillac", color: "#D4AF37" }, // Gold/Premium accent
  "bottas": { name: "Valtteri Bottas", team: "Cadillac", color: "#D4AF37" }
};

export const getDriverInfo = (driver_id) => {
  if (!driverMap[driver_id]) {
    const formattedName = driver_id.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    return { name: formattedName, team: "Unknown Team", color: "#FFFFFF" };
  }
  return driverMap[driver_id];
};
