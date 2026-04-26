// src/js/loadGames.js

export async function loadGames() {
    try {
        const response = await fetch('data/games.json');
        
        if (!response.ok) {
            throw new Error('Error loading games: ' + response.statusText);
        }

        const games = await response.json();
        displayGames(games);

        // Add event listeners for sorting
        addSortEventListeners(games);
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayGames(games) {
    const gamesList = document.getElementById('games-list');
    const table = document.createElement('table');
    table.setAttribute('id', "games-table");

    // Create the header row
    const headerRow = document.createElement('tr');
    headerRow.setAttribute('id', "table-header");
    headerRow.innerHTML = `
        <th>N° <span class="sort-icon" data-sort="id">⇅</span></th>
        <th>Title <span class="sort-icon" data-sort="title">⇅</span></th>
        <th>Genre <span class="sort-icon" data-sort="genre">⇅</span></th>
        <th>Max Players <span class="sort-icon" data-sort="players">⇅</span></th>
        <th>Multiplayer <span class="sort-icon" data-sort="multiplayerType">⇅</span></th>
    `;
    table.appendChild(headerRow);

    // Create rows for each game
    games.forEach(game => {
        const row = createGameRow(game);
        table.appendChild(row);
    });

    gamesList.innerHTML = ''; // Clear previous content
    gamesList.appendChild(table); // Append the table to the container
}

function createGameRow(game) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${game.id}</td>
        <td><a href="pages/game-details.html?id=${game.id}">${game.title}</a></td>
        <td>${game.genre}</td>
        <td>${game.players}</td>
        <td>${game.multiplayerType}</td>
    `;
    return row;
}

function sortGames(games, criterion) {
    return games.sort((a, b) => {
        if (typeof a[criterion] === 'number' && typeof b[criterion] === 'number') {
            return a[criterion] - b[criterion];
        }
        if (a[criterion] < b[criterion]) return -1;
        if (a[criterion] > b[criterion]) return 1;
        return 0;
    });
}

function displaySortedGames(games) {
    displayGames(games);

    // Re-add event listeners for sorting after updating the table
    addSortEventListeners(games);
}

function addSortEventListeners(games) {
    const sortIcons = document.querySelectorAll('.sort-icon');
    sortIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const criterion = icon.getAttribute('data-sort');
            const sortedGames = sortGames(games, criterion);
            displaySortedGames(sortedGames);
        });
    });
}