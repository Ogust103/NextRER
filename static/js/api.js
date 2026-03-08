// Fonction pour récupérer les données de l'API
export async function fetchNextRers(directions) {
    console.log("Fetching next RERs...");

    const response = await fetch("/api/next_rers");

    if (!response.ok) {
        throw new Error(`Erreur API: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
        console.error("Invalid data format received", data);
        throw new Error("Received data is not an array");
    }

    console.log("RATP data received:", data);

    const main = data.filter(rer =>
        rer &&
        (
            (rer.quayRef && directions.main.quayRef.includes(rer.quayRef)) ||
            (rer.destinationCode && directions.main.directionCodes.includes(rer.destinationCode))
        )
    );

    const secondary = data.filter(rer =>
        rer &&
        (
            (rer.quayRef && directions.secondary.quayRef.includes(rer.quayRef)) ||
            (rer.destinationCode && directions.secondary.directionCodes.includes(rer.destinationCode))
        )
    );

    return { main, secondary };
}


export async function fetchWeather() {
    console.log("Fetching weather...");

    const response = await fetch("/api/weather");

    if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    if (!data || typeof data !== "object") {
        console.error("Invalid weather data format", data);
        throw new Error("Invalid weather data format");
    }

    console.log("Weather data received:", data);

    return data;
}