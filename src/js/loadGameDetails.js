// src/js/loadGameDetails.js

import { setupGallery } from './gallery.js';

let gamesData = []; // Store games data globally for navigation

export async function loadGameDetails(gameId) {
    try {
        const response = await fetch('../data/games.json');
        if (!response.ok) {
            throw new Error('Error loading games: ' + response.statusText);
        }

        gamesData = await response.json();
        const game = gamesData.find(g => g.id === gameId);

        if (game) {
            updateGameDetails(game);
            setupGallery(game.screenshots);
            setupNavigation(gameId);
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

function setupNavigation(currentGameId) {
    const prevButton = document.getElementById('prev-game');
    const nextButton = document.getElementById('next-game');

    if (!prevButton || !nextButton) return;

    const currentIndex = gamesData.findIndex(g => g.id === currentGameId);
    const totalGames = gamesData.length;

    // Enable/disable buttons based on position
    prevButton.disabled = currentIndex <= 0;
    nextButton.disabled = currentIndex >= totalGames - 1;

    // Add click handlers
    prevButton.onclick = () => {
        if (currentIndex > 0) {
            const prevGameId = gamesData[currentIndex - 1].id;
            navigateToGame(prevGameId);
        }
    };

    nextButton.onclick = () => {
        if (currentIndex < totalGames - 1) {
            const nextGameId = gamesData[currentIndex + 1].id;
            navigateToGame(nextGameId);
        }
    };

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft' && !prevButton.disabled) {
            prevButton.click();
        } else if (e.key === 'ArrowRight' && !nextButton.disabled) {
            nextButton.click();
        }
    });
}

function navigateToGame(gameId) {
    // Update URL without page reload
    const newUrl = `${window.location.pathname}?id=${gameId}`;
    window.history.pushState({ gameId }, '', newUrl);

    // Load new game details
    loadGameDetails(gameId);
}

function getGameIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return parseInt(urlParams.get('id') || '0', 10);
}

document.addEventListener('DOMContentLoaded', () => {
    const gameId = getGameIdFromUrl();
    if (gameId) {
        loadGameDetails(gameId);
    } else {
        console.info('No game ID provided in the URL.');
    }
});