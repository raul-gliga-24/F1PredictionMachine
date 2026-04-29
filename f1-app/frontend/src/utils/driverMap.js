const driverMap = {
  // McLaren
  "lando_norris": { name: "Lando Norris", team: "McLaren", color: "#FF8000" },
  "oscar_piastri": { name: "Oscar Piastri", team: "McLaren", color: "#FF8000" },

  // Ferrari
  "charles_leclerc": { name: "Charles Leclerc", team: "Ferrari", color: "#E8002D" },
  "lewis_hamilton": { name: "Lewis Hamilton", team: "Ferrari", color: "#E8002D" },

  // Red Bull Racing
  "max_verstappen": { name: "Max Verstappen", team: "Red Bull", color: "#3671C6" },
  "isack_hadjar": { name: "Isack Hadjar", team: "Red Bull", color: "#3671C6" },

  // Mercedes
  "george_russell": { name: "George Russell", team: "Mercedes", color: "#27F4D2" },
  "kimi_antonelli": { name: "Kimi Antonelli", team: "Mercedes", color: "#27F4D2" },

  // Aston Martin
  "fernando_alonso": { name: "Fernando Alonso", team: "Aston Martin", color: "#229971" },
  "lance_stroll": { name: "Lance Stroll", team: "Aston Martin", color: "#229971" },

  // Alpine
  "pierre_gasly": { name: "Pierre Gasly", team: "Alpine", color: "#FF87BC" },
  "franco_colapinto": { name: "Franco Colapinto", team: "Alpine", color: "#FF87BC" },

  // Haas
  "esteban_ocon": { name: "Esteban Ocon", team: "Haas", color: "#B6BABD" },
  "oliver_bearman": { name: "Oliver Bearman", team: "Haas", color: "#B6BABD" },

  // Racing Bulls (RB)
  "liam_lawson": { name: "Liam Lawson", team: "Racing Bulls", color: "#6692FF" },
  "arvid_lindblad": { name: "Arvid Lindblad", team: "Racing Bulls", color: "#6692FF" },

  // Williams
  "alex_albon": { name: "Alex Albon", team: "Williams", color: "#00A1FE" },
  "carlos_sainz": { name: "Carlos Sainz", team: "Williams", color: "#00A1FE" },

  // Audi
  "nico_hulkenberg": { name: "Nico Hülkenberg", team: "Audi", color: "#F50537" },
  "gabriel_bortoleto": { name: "Gabriel Bortoleto", team: "Audi", color: "#F50537" },

  // Cadillac
  "sergio_perez": { name: "Sergio Pérez", team: "Cadillac", color: "#D4AF37" }, // Gold/Premium accent
  "valtteri_bottas": { name: "Valtteri Bottas", team: "Cadillac", color: "#D4AF37" }
};

export const getDriverInfo = (driver_id) => {
  if (!driverMap[driver_id]) {
    const formattedName = driver_id.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    return { name: formattedName, team: "Unknown Team", color: "#FFFFFF" };
  }
  return driverMap[driver_id];
};
