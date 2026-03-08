import { fetchNextRers, fetchWeather } from "./api.js";
import { updateCurrentTime, updateTimeRemaining, updateWeatherDisplay, resetScroll } from "./ui.js";

const directions = JSON.parse(
    document.getElementById("directions-data").textContent
);

let nextMainRersData = []; // Variable globale pour stocker les rer allant vers Paris
let nextSecondaryRersData = []; // Variable globale pour stocker les rer allant vers Saint-Germain-en-Laye
let weatherData = {}; // Variable globale pour stocker les données météo

const rerRequestInterval = 10000; // Intervalle de 10 secondes pour les données RER
const weatherRequestInterval = 180000; // Intervalle de 3 minutes pour les données météo

// Fonction pour récupérer et mettre à jour les données des RER
async function updateRers() {
    try {
        const result = await fetchNextRers(directions);

        nextMainRersData = result.main;
        nextSecondaryRersData = result.secondary;

        updateTimeRemaining(nextMainRersData, "main-rer-list");
        updateTimeRemaining(nextSecondaryRersData, "secondary-rer-list");

    } catch (error) {
        console.error(error);
    }
}

// Fonction pour récupérer et mettre à jour les données météo
async function updateWeather() {
    try {
        weatherData = await fetchWeather();
        updateWeatherDisplay(weatherData);
    } catch (error) {
        console.error(error);
    }
}

// Met à jour l'heure actuelle toutes les secondes
setInterval(updateCurrentTime, 1000);

// Met à jour le temps restant toutes les secondes
setInterval(() => updateTimeRemaining(nextMainRersData, 'main-rer-list'), 1000);
setInterval(() => updateTimeRemaining(nextSecondaryRersData, 'secondary-rer-list'), 1000);
        
// Rafraîchit les données de l'API toutes les 10 secondes        
setInterval(updateRers, rerRequestInterval);

// Rafraîchit les données météo toutes les 3 minutes
setInterval(updateWeather, weatherRequestInterval); 

// Charge les données au démarrage
window.onload = () => {
    updateCurrentTime();
    updateRers();
    updateWeather();

    // Affiche les noms des directions dans les en-têtes
    document.getElementById("mainDirection").textContent = directions.main.directionNames.join(" • ");
    document.getElementById("secondaryDirection").textContent = directions.secondary.directionNames.join(" • ");

    // Ajouter un gestionnaire de clic sur l'heure pour réinitialiser les scrolls
    document.getElementById("current-time").addEventListener("click", resetScroll);
};