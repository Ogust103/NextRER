import { getTimeRemaining, formatLocalHour, getWeatherIcon, getWeatherImage } from "./utils.js";

// Fonction pour mettre à jour l'heure actuelle
export function updateCurrentTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('current-time').textContent = `${hours}:${minutes}:${seconds}`;
            
    const date = now.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
    document.getElementById('current-date').textContent = date.charAt(0).toUpperCase() + date.slice(1); // Met la première lettre en majuscule
}

// Fonction pour mettre à jour l'affichage du temps restant
export function updateTimeRemaining(nextRersData, columnId) {
    const now = new Date();
    const list = document.getElementById(columnId);

    list.innerHTML = nextRersData.map((rer) => {

        const arrival = new Date(rer.expectedArrivalTime || rer.aimedArrivalTime);

        const expectedDeparture = new Date(rer.expectedDepartureTime || 0);
        const aimedDeparture = new Date(rer.aimedDepartureTime || 0);

        let departure = expectedDeparture > arrival ? expectedDeparture : aimedDeparture;

        const isArriving = now < arrival;
        const isAtPlatform = now >= arrival && now < departure;
        const isFuture = departure > now;

        if (!isFuture) return "";

        const minutesSeconds = getTimeRemaining(arrival.toISOString());
        const minutes3lettres = minutesSeconds.minutes.length > 2;

        return `
            <div class="cell">
                <div class="cell-left">
                    <div class="name-rectangle">
                        <span>${rer.vehicleJourneyName}</span>
                    </div>
                    <span class="direction-name">${rer.destinationName}</span>
                </div>

                <div class="cell-right">
                    <div class="time-container">

                        <div class="${isAtPlatform ? 'on-platform' : 'minutes'}"
                             ${minutes3lettres ? 'style="font-size: 52px;"' : ''}>
                             
                            <span>${isAtPlatform ? 'à quai' : minutesSeconds.minutes}</span>
                        </div>

                        ${isArriving ? `<span class="seconds"> : ${minutesSeconds.seconds}</span>` : ''}

                    </div>

                    <div class="platform-rectangle">
                        <span class="text">quai</span>
                        <span class="number">${rer.platform !== "unknown" ? rer.platform : "-"}</span>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

export function updateWeatherDisplay(weatherData) {
    const actualTime = new Date();
    const weatherScreen = document.getElementById('weather-screen');
    const currentWeather = document.getElementById('current-weather');
    const hourlyWeather = document.getElementById('hourly-scrollbar');

    // Affichage de la météo actuelle
    if (weatherData.current) {
        weatherScreen.style.backgroundImage = `url('static/weather_images/${getWeatherImage(weatherData.current.weather_code, weatherData.current.is_day)}')`;
        document.getElementById('current-temp').textContent = `${weatherData.current.temperature}°C`;
    }

    const dailyWeather = weatherData.daily ? weatherData.daily[formatLocalHour(actualTime).split('T')[0]] : null;
    if (dailyWeather) {
        document.getElementById('temperature-min').textContent = `${dailyWeather.temperature_min}°`;
        document.getElementById('temperature-max').textContent = `${dailyWeather.temperature_max}°`;
        document.getElementById('sunrise-time').textContent = dailyWeather.sunrise.split('T')[1].slice(0, 5);
        document.getElementById('sunset-time').textContent = dailyWeather.sunset.split('T')[1].slice(0, 5);
    }

    // Affichage des prévisions horaires
    if (weatherData.hourly) {
        const today = actualTime.toISOString().split('T')[0];
        const daysOfWeek = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
        let html ="";
        for (const [time, data] of Object.entries(weatherData.hourly)) {
            const [date, hour] = time.split('T');
            const isToday = date === today;
            let dateLabel = '';
            if (!isToday) {
                const forecastDate = new Date(date);
                const dayName = daysOfWeek[forecastDate.getDay()];
                dateLabel = `${dayName} `;
            }
            
            html += `
                <div class="hourly-card" id="hourly-${time}">
                    <span>${dateLabel}${hour}</span>
                    <img src="static/weather_icons/${getWeatherIcon(data.weather_code, data.is_day)}" alt="Weather Icon" class="weather-icon" width="35">
                    <span>${data.temperature}°C</span>
                </div>
            `;
        }
        hourlyWeather.innerHTML = html;
        const card = document.getElementById(`hourly-${formatLocalHour(actualTime)}`);
        if (card) {
            hourlyWeather.scrollTo({
                left: card.offsetLeft - hourlyWeather.offsetLeft,
                behavior: 'smooth'
            });
        }
    }
}

export function resetScroll() {
    const hourlyWeather = document.getElementById('hourly-scrollbar');
    const card = document.getElementById(`hourly-${formatLocalHour(new Date())}`);
    if (hourlyWeather && card) {
        hourlyWeather.scrollTo({
            left: card.offsetLeft - hourlyWeather.offsetLeft,
            behavior: 'smooth'
        });
    }

    const mainRerList = document.getElementById('main-rer-list');
    if (mainRerList) {
        console.log("Resetting main RER list scroll");
        mainRerList.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    const secondaryRerList = document.getElementById('secondary-rer-list');
    if (secondaryRerList) {
        secondaryRerList.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}