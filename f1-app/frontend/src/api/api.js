export const predictChampionship = async (season) => {
    const response = await fetch(`http://localhost:8000/api/championship/championship/${season}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail || "Failed to fetch championship prediction");
    }
    return data.data || data;
};

export const predictRace = async (season, round) => {
    const response = await fetch(`http://localhost:8000/api/predictions/pre-race/${season}/${round}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Failed to fetch prediction");
    }

    return data;
};
