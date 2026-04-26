// src/js/loadGameDetails.js

import { setupGallery } from './gallery.js';

export async function loadGameDetails(gameId) {
    try {
        const response = await fetch('../data/games.json');
        if (!response.ok) {
            throw new Error('Error loading games: ' + response.statusText);
        }

        const games = await response.json();
        const game = games.find(g => g.id === gameId);

        if (game) {
            updateGameDetails(game);
            setupGallery(game.screenshots);
        } else {
            console.warn('Game not found for ID:', gameId);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateGameDetails(game) {
    document.title = game.title;
    document.getElementById('game-title').innerText = game.title;
    document.getElementById('game-players').innerText = game.players.toString();
    document.getElementById('game-genre').innerText = game.genre;
    document.getElementById('multiplayer-type').innerText = game.multiplayerType;
    document.getElementById('game-summary').innerText = game.summary;
    document.getElementById('game-release-date').innerText = game.releaseDate;
    document.getElementById('game-developer').innerText = game.developer;

    const screenshotsContainer = document.getElementById('game-screenshots');
    screenshotsContainer.innerHTML = ''; // Clear previous content
    game.screenshots.forEach(screenshot => {
        const img = document.createElement('img');
        img.src = screenshot;
        img.alt = `${game.title} Screenshot`;
        screenshotsContainer.appendChild(img);
    });

    document.getElementById('shop-link').setAttribute('href', game.shopLink);
}

function getGameIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return parseInt(urlParams.get('id') || '0', 10);
}

async function setBackground() {
    try {
        // const response = await fetch('https://api.unsplash.com/photos/random?client_id=BukV4kcX2Jz8v60-oTtVSVAbLu2BRA4SRRnWmQaYL4I');
        if (!response.ok) {
            throw new Error('Failed to fetch image');
        }
        const data = await response.json();
        const mainElement = document.querySelector('main');
        mainElement.style.backgroundImage = `url(${data.urls.regular})`;
        mainElement.style.backgroundSize = 'cover';
        mainElement.style.backgroundPosition = 'center';
    } catch (error) {
        console.warn('Error setting background:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const gameId = getGameIdFromUrl();
    if (gameId) {
        loadGameDetails(gameId);
    } else {
        console.info('No game ID provided in the URL.');
    }

    setBackground();
});