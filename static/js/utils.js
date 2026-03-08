// Fonction pour retourner le temps restant en minutes et secondes
export function getTimeRemaining(departureTime) {
    const now = new Date();
    const departure = new Date(departureTime);
    const diffMs = Math.max(0, departure - now);
    const diffMinutes = Math.floor(diffMs / 60000);
    const diffSeconds = Math.floor((diffMs % 60000) / 1000);
    return { minutes: String(diffMinutes), seconds: String(diffSeconds).padStart(2, '0') };
}

export function formatLocalHour(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    const h = String(date.getHours()).padStart(2, '0');

    return `${y}-${m}-${d}T${h}:00`;
}

export function getWeatherIcon(weatherCode, is_day) {
    const isDay = is_day === 1

    switch (weatherCode) {

        // ☀️ Clair à nuageux
        case 0:
        return isDay ? "day_1.png" : "night_1.png"
        case 1:
        return isDay ? "day_2.png" : "night_2.png"
        case 2:
        return isDay ? "day_3.png" : "night_3.png"
        case 3:
        return "cloudy.png"

        // 🌫️ Brouillard
        case 45:
        return "fog.png"
        case 48:
        return "fog.png"

        // 🌧️ Bruine
        case 51:
        return "rain_1.png"
        case 53:
        return "rain_2.png"
        case 55:
        return "rain_3.png"

        // 🧊 Grêle / grésil
        case 56:
        return "sleet_hail.png"
        case 57:
        return "sleet_hail.png"

        // 🌧️ Pluie
        case 61:
        return "rain_1.png"
        case 63:
        return "rain_2.png"
        case 65:
        return "rain_3.png"

        // 🧊 Pluie verglaçante / grésil
        case 66:
        return "sleet_hail.png"
        case 67:
        return "sleet_hail.png"

        // ❄️ Neige
        case 71:
        return "snow_1.png"
        case 73:
        return "snow_2.png"
        case 75:
        return "snow_3.png"
        case 77:
        return "snow_2.png"

        // 🌧️ Averses de pluie
        case 80:
        return isDay ? "day_rain.png" : "night_rain.png"
        case 81:
        return isDay ? "day_rain.png" : "night_rain.png"
        case 82:
        return "rain_3.png"

        // 🌨️ Averses de neige
        case 85:
        return "snow_1.png"
        case 86:
        return "snow_3.png"

        // ⛈️ Orages
        case 95:
        return isDay ? "day_storm.png" : "night_storm.png"
        case 96:
        return "storm.png"
        case 99:
        return "storm.png"

        // 🔁 Fallback
        default:
        return isDay ? "day_1.png" : "night_1.png"
    }
}

export function getWeatherImage(weatherCode, is_day) {
    const isDay = is_day === 1

    switch (weatherCode) {

        // ☀️ Clair à nuageux
        case 0:
        return isDay ? "day_1.jpg" : "night_1.jpg"
        case 1:
        return isDay ? "day_1.jpg" : "night_1.jpg"
        case 2:
        return isDay ? "day_3.jpg" : "night_3.jpg"
        case 3:
        return isDay ? "day_3.jpg" : "night_3.jpg"

        // 🌫️ Brouillard
        case 45:
        return "fog.jpg"
        case 48:
        return "fog.jpg"

        // 🌧️ Bruine
        case 51:
        return "rain_2.jpg"
        case 53:
        return "rain_2.jpg"
        case 55:
        return "rain_2.jpg"

        // 🧊 Grêle / grésil
        case 56:
        return "sleet_hail.jpg"
        case 57:
        return "sleet_hail.jpg"

        // 🌧️ Pluie
        case 61:
        return "rain_2.jpg"
        case 63:
        return "rain_2.jpg"
        case 65:
        return "rain_2.jpg"

        // 🧊 Pluie verglaçante / grésil
        case 66:
        return "sleet_hail.jpg"
        case 67:
        return "sleet_hail.jpg"

        // ❄️ Neige
        case 71:
        return "snow.jpg"
        case 73:
        return "snow.jpg"
        case 75:
        return "snow.jpg"
        case 77:
        return "snow.jpg"

        // 🌧️ Averses de pluie
        case 80:
        return "rain_2.jpg"
        case 81:
        return "rain_2.jpg"
        case 82:
        return "rain_2.jpg"

        // 🌨️ Averses de neige
        case 85:
        return "snow.jpg"
        case 86:
        return "snow.jpg"

        // ⛈️ Orages
        case 95:
        return "storm.jpg"
        case 96:
        return "storm.jpg"
        case 99:
        return "storm.jpg"

        // 🔁 Fallback
        default:
        return isDay ? "day_1.jpg" : "night_1.jpg"
    }
}