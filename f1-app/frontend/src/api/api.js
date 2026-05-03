export const predictChampionship = async (season, detailed = false) => {
    const response = await fetch(`http://localhost:8000/api/championship/championship/${season}?detailed=${detailed}`, {
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

export const predictScenario = async (season, driverId) => {
    const response = await fetch(`http://localhost:8000/api/championship/scenario/${season}/${driverId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail || "Failed to fetch scenario prediction");
    }
    return data.data || data;
};
