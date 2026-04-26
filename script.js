// script.js

import { loadGames } from './src/js/loadGames.js';
import { loadGameDetails } from './src/js/loadGameDetails.js';

// Check if we are on the home page
if (document.getElementById('games-list')) {
    loadGames(); // Load the game list on the home page
}

// Check if we are on the game details page
const urlParams = new URLSearchParams(window.location.search);
const gameId = parseInt(urlParams.get('id') || '0', 10);
if (gameId) {
    loadGameDetails(gameId); // Load game details if an ID is present
} else {
    console.info('No game ID provided in the URL.');
}