# W4SD - Local Coop Game Hub 🎮

A modern web application showcasing a curated collection of multiplayer and competitive games perfect for fun with friends and family.

## About the Project

W4SD is a local cooperative game hub that brings together diverse gaming experiences. Whether you're into action, strategy, sports, or party games, W4SD helps you discover your next favorite multiplayer game. This project features a beautiful gallery of games with detailed information, screenshots, and links to shop pages.

## Features

✨ **Game Gallery** - Browse through a diverse collection of multiplayer games  
🎯 **Detailed Game Info** - View comprehensive details including:
- Game title and developer
- Number of players supported
- Multiplayer type (versus, cooperative, etc.)
- Genre classification
- Release date
- Game summary
- Screenshots

🔍 **Easy Navigation** - Clean and intuitive interface with quick access to game details  
📱 **Responsive Design** - Optimized for different screen sizes  
🎨 **Modern UI** - Smooth scrolling with custom scrollbars

## Project Structure

```
coop-game/
├── index.html              # Main page
├── script.js               # Main JavaScript logic
├── pages/
│   ├── about.html         # About page
│   ├── game-details.html  # Game details page
│   └── templates/
│       └── footer.html    # Reusable footer
├── src/
│   ├── css/               # Stylesheets
│   │   ├── styles.css     # Main styles
│   │   ├── gallery.css    # Gallery styles
│   │   ├── game-details.css
│   │   └── table.css
│   ├── js/                # JavaScript modules
│   │   ├── loadGames.js   # Load games from JSON
│   │   ├── loadGameDetails.js
│   │   └── gallery.js
│   └── img/               # Images (100+ game screenshots)
└── data/
    └── games.json         # Game database
```

## Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- No server installation required for local viewing

### Installation

1. Clone the repository:
```bash
git clone https://github.com/metanef/coop-game.git
cd coop-game
```

2. Open the project:
```bash
# Option 1: Open directly in your browser
open index.html

# Option 2: Use a local server (recommended for development)
# With Python 3:
python -m http.server 8000

# With Node.js (http-server):
npx http-server
```

3. Navigate to `http://localhost:8000` (or your server's port)

## Usage

- **Home Page**: Browse all available games in a grid layout
- **Game Details**: Click on any game to view full details and screenshots
- **Navigation**: Use the navigation menu to explore different sections
- **About**: Learn more about the W4SD project

## Game Database

Games are stored in `data/games.json` with the following structure:

```json
{
  "id": 1,
  "title": "Game Title",
  "players": 4,
  "multiplayerType": "versus",
  "genre": "shooter",
  "releaseDate": "2011-05-18",
  "developer": "Developer Name",
  "summary": "Game description...",
  "screenshots": ["path/to/img1.png", "path/to/img2.png"],
  "shopLink": "https://example.com"
}
```

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Styling and animations
- **JavaScript (ES6+)** - Dynamic content loading and interactions
- **JSON** - Data storage for games
- **OverlayScrollbars** - Custom scrollbar styling

## Development

### Current Features
- ✅ Game gallery with filtering
- ✅ Detailed game information pages
- ✅ Responsive design
- ✅ Footer template system

### TODO
- ⏳ Add all game pictures
- ⏳ Navigation arrows for next/previous game on details page
- ⏳ Optimize image storage solution

## File Description

| File | Purpose |
|------|---------|
| `index.html` | Landing page with game gallery |
| `script.js` | Main app initialization and module imports |
| `src/js/loadGames.js` | Fetch and display games from JSON |
| `src/js/gallery.js` | Gallery interaction and filtering |
| `src/js/loadGameDetails.js` | Load individual game details |
| `src/css/styles.css` | Global styles |
| `data/games.json` | Game database |

## Contributing

Contributions are welcome! Feel free to:
- Add new games to the database
- Improve the UI/UX
- Fix bugs
- Optimize performance

## License

This project is open source and available for personal and educational use.

## Contact & Links

- 🎮 Discover games on [itch.io](https://itch.io)
- 📧 Questions? Feel free to open an issue

---

**W4SD** - Where Gamers Find Their Next Adventure! 🚀
