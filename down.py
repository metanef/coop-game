import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- CONFIGURATION ---
BASE_FOLDER = "Game_Screenshots"
MIN_SIZE_KB = 144  # Taille minimale en Ko
TARGET_COUNT = 4   # Nombre d'images par jeu

# Votre liste de jeux (extraits)
games_list = [
    {
    "id": 101,
    "title": "Indigo viper (itch.io)",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "shooter",
    "releaseDate": "2019",
    "developer": "Max Pohlenz",
    "summary": "Indigo Viper is a fast-paced local multiplayer jump and shoot arena game that focuses on one-shot kills and speedy combat. Players battle in various arenas using different weapons and a mix of game modes, all with a nostalgic feel of late 90s console games. It supports up to four players locally and features plug-and-play controls.",
    "screenshots": [],
    "shopLink": "https://bambivalent.itch.io/indigoviper"
  },
  {
    "id": 102,
    "title": "Insanity's Blade",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "action rpg",
    "releaseDate": "2014",
    "developer": "Causal Bit Games Inc.",
    "summary": "Insanity's Blade is an action platformer where players control Thurstan, a father journeying through hell to rescue the souls of his wife and child. It combines classic arcade action, RPG elements, and a gripping story with cutscenes and side quests. The game features both single-player and local co-op gameplay.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/334190/Insanitys_Blade/"
  },
  {
    "id": 103,
    "title": "Invisigun heroes",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "stealth",
    "releaseDate": "2017",
    "developer": "Sombr Studio",
    "summary": "A multiplayer stealth arena game where all players are invisible. Use environmental cues, footprints, and sound to locate enemies while avoiding detection. The game features grid-based movement, diverse maps, characters, and abilities for highly strategic gameplay.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/375750/Invisigun_Reloaded/"
  },
  {
    "id": 104,
    "title": "Jamestown",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "shoot emp up",
    "releaseDate": "2011",
    "developer": "Final Form Games",
    "summary": "Set in an alternate 17th-century British colonial Mars, Jamestown+ is a cooperative shoot-em-up that blends rich pixel art with an orchestral soundtrack. It is accessible for newcomers while challenging for die-hard genre fans, supporting up to four players.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/377950/Jamestown/"
  },
  {
    "id": 105,
    "title": "Jawbreaker (itch.io)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "beat em up",
    "releaseDate": "2018",
    "developer": "jackbreen",
    "summary": "Jawbreaker is a 2D arcade style beat em up. The rules are simple: get as high up the elevator as you can before meeting your fate at the hands of the enemies. Fight for the highest score! Jawbreaker can also be played with a buddy! Grab a friend and hit the elevator together as a team. Or, if you've got a score to settle, face off in Versus Mode!",
    "screenshots": [],
    "shopLink": "https://jackbreen-hg.itch.io/jawbreaker"
  },
  {
    "id": 106,
    "title": "Jazz jackrabbit 2",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "platformer",
    "releaseDate": "1998",
    "developer": "Epic MegaGames",
    "summary": "A fast-paced platformer with a humorous tone, featuring Jazz and Spaz as playable characters. Known for its vibrant levels, unique gameplay mechanics, and multiplayer options, including co-op and competitive modes like capture the flag.",
    "screenshots": [],
    "shopLink": "https://www.gog.com/fr/game/jazz_jackrabbit_2_collection"
  },
  {
    "id": 107,
    "title": "Justice league task force 2 (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2020",
    "developer": "Zvitor",
    "summary": "A fan-made fighting game featuring Justice League characters in an engaging MUGEN-based platform. It offers a nostalgic experience with updated graphics and movesets for DC Comics fans.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/justiceleagueTF2/467929"
  },
  {
    "id": 108,
    "title": "Kamen rider super climax mugen (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "",
    "developer": "Community-based MUGEN project",
    "summary": "Kamen Rider Super Climax Heroes is a fan-made fighting game created with the MUGEN engine, featuring characters and transformations from the Kamen Rider franchise, including various Riders from different series with customizable moves and battles.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/NOJOKETH/286242"
  },
  {
    "id": 109,
    "title": "Kingdom two crowns",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "simulation",
    "releaseDate": "2018",
    "developer": "Fury Studios, Stumpy Squid, and Coatsink",
    "summary": "A side-scrolling micro-strategy game that focuses on exploration, building, and resource management. Players act as monarchs, working to grow their kingdoms, recruit loyal subjects, and protect their lands from the mysterious Greed.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/701160/Kingdom_Two_Crowns"
  },
  {
    "id": 110,
    "title": "Kirby the dream battle (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2013",
    "developer": "Fou the Mage of the Sun and brazilmugenteam",
    "summary": "A 2D fighting game featuring numerous Kirby characters, each with unique attacks and 'Hyper' ultimate moves. The gameplay is inspired by Kirby Super Star Ultra, offering pixel art visuals and retro vibes​",
    "screenshots": [],
    "shopLink": "https://brazilmugenteam.itch.io/kirby-the-dream-battle"
  },
  {
    "id": 111,
    "title": "Knights & Dragons: The Endless Quest (openbor)",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2013",
    "developer": "Pier Wolf",
    "summary": "A fan-made beat-em-up game inspired by classic arcade titles, set in a fantasy world reminiscent of Dungeons & Dragons, offering cooperative gameplay and exciting action sequences.",
    "screenshots": [],
    "shopLink": "https://openborgames.com/knights-dragons-the-endless-quest-v-3-3-OpenBOR"
  },
  {
    "id": 112,
    "title": "Kryp (itch.io)",
    "players": 8,
    "multiplayerType": "versus",
    "genre": "shooter",
    "releaseDate": "2017",
    "developer": "Therese, Kim, Ivan & Erik",
    "summary": "A relaxing game about digging in the soil and picking apples to alter your environment. This game offers an engaging experience that grows on you.",
    "screenshots": [],
    "shopLink": "https://nahkala.itch.io/kryp"
  },
  {
    "id": 113,
    "title": "Lance a lot",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "party brawler",
    "releaseDate": "2016",
    "developer": "Brimstone",
    "summary": "RUIN FRIENDSHIPS. ON ROCKETS. Challenge your friends to a GLORIOUS tournament of rocket jousting! Up to 4 players can fight each other locally – but only one will be left standing when the dust settles.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/495900/Lance_A_Lot_Classic_Edition"
  },
  {
    "id": 114,
    "title": "Last one standing (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "casual",
    "releaseDate": "2016",
    "developer": "DmGregory",
    "summary": "Chase your opponents and knock down their dominoes - be the Last One Standing!",
    "screenshots": [],
    "shopLink": "https://dmgregory.itch.io/last-one-standing"
  },
  {
    "id": 115,
    "title": "Legend of dungeon",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "action rpg",
    "releaseDate": "2013",
    "developer": "Robot Loves Kitty",
    "summary": "A visually striking roguelike with randomized dungeons and dynamic music. Players explore 26 unique floors full of traps, monsters, and treasures in solo or up to 4-player co-op. Features permadeath, unlockable classes, tameable pets, and VR mode for immersive gameplay.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/238280/Legend_of_Dungeon/"
  },
  {
    "id": 116,
    "title": "Lego (TT games)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "racing,strategy,action, etc",
    "releaseDate": "Varies (first LEGO game by TT Games was released in 2005, with many subsequent releases including 'LEGO Star Wars: The Skywalker Saga' in 2022).",
    "developer": "TT Games",
    "summary": "TT Games has developed numerous LEGO-themed video games based on popular franchises such as Star Wars, Harry Potter, Jurassic Park, and Marvel. These games combine puzzle-solving, combat, and exploration, with humor and co-op gameplay that appeals to players of all ages.",
    "screenshots": [],
    "shopLink": "https://www.ttgames.com/games/"
  },
  {
    "id": 117,
    "title": "Light bound",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "top down shooter",
    "releaseDate": "2015",
    "developer": "Garden Knight Games",
    "summary": "Get thrown into randomly generated arenas that can only be seen by the light of the players and their weapons. Explore, collect weapons and upgrades, and do battle against your friends or the computer. Customize each game using a variety of configurable options.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/335560/Light_Bound/"
  },
  {
    "id": 118,
    "title": "Little fighter 2",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "beat em up",
    "releaseDate": "2002",
    "developer": "Marti Wong and Starsky Wong",
    "summary": "A freeware side-scrolling fighting game supporting up to 8 players in local or online multiplayer. Players control unique characters with special attacks, engaging in single or co-op modes like survival or campaign battles against hordes of enemies.",
    "screenshots": [],
    "shopLink": "https://www.lf2.net/index_en.html"
  },
  {
    "id": 119,
    "title": "Lovers in dangerous spacetime",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "space shooter/management",
    "releaseDate": "2015",
    "developer": "Asteroid Base",
    "summary": "This colorful 2D arcade game blends action and platforming. Players control operators aboard a mobile space station, defending it against waves of enemies. Cooperation between players is key, as they manage turrets, shields, and other systems to navigate through the galaxy and restore peace.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/252110/Lovers_in_a_Dangerous_Spacetime/"
  },
  {
    "id": 120,
    "title": "Mad snowboarding",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "sport",
    "releaseDate": "2015",
    "developer": "Denis Lapiner",
    "summary": "Mad Snowboarding is an open-world snowboarding game where players race down mountains, perform tricks, and create custom levels to share with the community. The game supports split-screen multiplayer for up to four players and features worldwide high score challenges",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/399900/Mad_Snowboarding/"
  },
  {
    "id": 121,
    "title": "Marvel infinity war (openbor)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2017",
    "developer": "Zvitor",
    "summary": "Marvel Infinity War is a fan-made beat 'em up using the OpenBOR engine. It features 85 playable Marvel characters across various teams like the Avengers and X-Men, with unique moves and assist characters. Players battle through stages filled with bosses from the Marvel universe.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/marvel-infinity-war/201435"
  },
  {
    "id": 122,
    "title": "Mayan death robots",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "srtategy",
    "releaseDate": "2015",
    "developer": "Sileni Studios",
    "summary": "Mayan Death Robots is an artillery strategy game set in the Mayan civilization, where players control alien robots battling to destroy each other's power cores. The game combines the strategic depth of titles like Worms with unique mechanics, including landscape-altering blocks. It features both single-player and local multiplayer modes.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/347470/Mayan_Death_Robots/"
  },
  {
    "id": 123,
    "title": "Megabyte punch",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "beat em up",
    "releaseDate": "2013",
    "developer": "Team Reptile",
    "summary": "Megabyte Punch is a fighting game where you can customize your own fighter. As you progress through different levels, you fight other creatures to collect body parts that grant new abilities and powers, creating a unique combat experience.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/248550/Megabyte_Punch/"
  },
  {
    "id": 124,
    "title": "Megaman Powered Up REMIX 2 (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2013",
    "developer": "Douglas Baldan",
    "summary": "This game is based, somehow, on Megaman Powered Up game.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/megaman-powered-up-remix/19509"
  },
  {
    "id": 125,
    "title": "Megaman robot master mayhem (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2019",
    "developer": "Douglas Baldan",
    "summary": "This is a fighting game in versus style, highly influenced by games like Marvel vs. Capcom.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/robotmastermayhem/405160"
  },
  {
    "id": 126,
    "title": "Metal slug 3",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "run n gun",
    "releaseDate": "2014",
    "developer": "SNK",
    "summary": "A classic arcade run-and-gun shooter with detailed pixel art, diverse levels, and intense boss battles.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/250180/METAL_SLUG_3/"
  },
  {
    "id": 127,
    "title": "Metal slug x",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "run n gun",
    "releaseDate": "2014",
    "developer": "SNK",
    "summary": "A fast-paced arcade shooter in the Metal Slug series known for refined gameplay and enhanced graphics.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/312610/METAL_SLUG_X/"
  },
  {
    "id": 128,
    "title": "Mighty final fight rebirth",
    "players": 3,
    "multiplayerType": "versus/coop",
    "genre": "beat em up",
    "releaseDate": "2024",
    "developer": "ReinLv",
    "summary": "Mayor Mike Haggar takes on the notorious Mad Gear Gang, who have kidnapped his daughter Jessica to force him under their control. Joined by allies including Jessica’s boyfriend Cody, Haggar fights through the dangerous streets of Metro City—collecting food and weapons along the way—to rescue her and reclaim the city from crime.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/mffr/515218"
  },
  {
    "id": 129,
    "title": "Mortal kombat Defenders of the Earth (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2015",
    "developer": "Daniloabella",
    "summary": "MK Defenders of the Earth is a non-profit fan-game based on the classic games of the MK saga. Powered on Mugen, this game uses Borg117's Season 2 FINAL (PATCH 4) as the base and material of the MKP 4.1 by MKP Team.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/MKDE/84520"
  },
  {
    "id": 130,
    "title": "Mortal kombat legacy 2.5 (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2017",
    "developer": "Kyra",
    "summary": "none",
    "screenshots": [],
    "shopLink": "https://www.youtube.com/watch?v=WZ2DJVLHh8k"
  },
  {
    "id": 131,
    "title": "Motorball derby (itch.io)",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "sport",
    "releaseDate": "2017",
    "developer": "NaBUru38",
    "summary": "Motorball Derby is a clash between motor sports and ball sports. You must bump the ball with a vehicle into the rival team's goal. No fouls, no kick button, no rockets. You can crash into you rivals and block them – be sure they will.",
    "screenshots": [],
    "shopLink": "https://naburu38.itch.io/motorball-derby"
  },
  {
    "id": 132,
    "title": "Move or die",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "platformer",
    "releaseDate": "2016",
    "developer": "Xelu, Those Awesome Guys",
    "summary": "A fast-paced multiplayer party game where constant movement is key to survival, featuring dynamic and chaotic gameplay.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/323850/Move_or_Die/"
  },
  {
    "id": 133,
    "title": "N++",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "platformer",
    "releaseDate": "2016",
    "developer": "Metanet Software",
    "summary": "A minimalist, challenging platformer with precise controls and procedurally generated levels, supporting local multiplayer.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/230270/N_NPLUSPLUS/"
  },
  {
    "id": 134,
    "title": "Neon genesis evangelion MUGEN (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2018",
    "developer": "TonyADV",
    "summary": "Neon Genesis Evangelion is a two-dimensional fight game where players control all the Evas of the mythical animated series Evangelion to combat their enemies, the fearsome Angels.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/NGEMUGEN/641107"
  },
  {
    "id": 135,
    "title": "Neonplat",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "platformer",
    "releaseDate": "2015",
    "developer": "Jayenkai",
    "summary": "In true arcade classic fashion, NeonPlat starts on the left, and makes his way to the right. There are evil bad things along the way, and also a number of objects he can collect, pickup and occasionally throw.",
    "screenshots": [],
    "shopLink": "https://neonplat.en.softonic.com/"
  },
  {
    "id": 136,
    "title": "Neverendia (gamejolt)",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "card",
    "releaseDate": "2019",
    "developer": "Very soft owl",
    "summary": "Play alone or in a party with up to 4 friends on one device! Collaborate to beat the game together or see who will be the last one to survive!",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/neverendia/426445"
  },
  {
    "id": 137,
    "title": "Nidhogg",
    "players": 8,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2014",
    "developer": "Messhof",
    "summary": "A fast-paced, minimalist fencing duel game where players race through side-scrolling arenas to outmaneuver and defeat their opponents.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/94400/Nidhogg"
  },
  {
    "id": 138,
    "title": "Normal human face simulation",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2017",
    "developer": "Lingdong Huang",
    "summary": "Challenge your friend to this local 2-player face-biting simulation! Chew their face off while they yours! No bath salt needed.",
    "screenshots": [],
    "shopLink": "https://lingdonh.itch.io/normal-human-face-simulator"
  },
  {
    "id": 139,
    "title": "Nuclear reaction (itch.io)",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "casual",
    "releaseDate": "2016",
    "developer": "Sven Ahlgrimm",
    "summary": "Nuclear Reaction is a one-button local-multiplayer game for two to four players. The goal for each player is to survive a world-war, while everyone else gets destroyed.",
    "screenshots": [],
    "shopLink": "https://svenahlgrimm.itch.io/nuclear-reaction"
  },
  {
    "id": 140,
    "title": "Obscure 1,2",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "horror",
    "releaseDate": "2004-2007",
    "developer": "Hydravision Entertainment",
    "summary": "A survival horror game where a group of high school students uncovers a sinister secret within their school, leading to a nightmarish battle for survival. The sequel continues the story of the survivors as they face new horrors in college, with cooperative gameplay and multiple playable characters.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/254460/Obscure/"
  },
  {
    "id": 141,
    "title": "OpenLieroX",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "shooter",
    "releaseDate": "2007",
    "developer": "OpenLierox team",
    "summary": "An open-source, real-time worm shooter game inspired by the classic Liero, featuring customizable weapons, levels, and online multiplayer.",
    "screenshots": [],
    "shopLink": "https://www.openlierox.net/"
  },
  {
    "id": 142,
    "title": "Overcooked",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "party",
    "releaseDate": "2016",
    "developer": "Ghost town game",
    "summary": "A chaotic couch co-op cooking game where players must prepare and serve a variety of dishes under time constraints in increasingly challenging kitchens.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/448510/Overcooked/"
  },
  {
    "id": 143,
    "title": "Pac-man 256",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "arcade",
    "releaseDate": "2015",
    "developer": "Hipster Whale, 3 Sprockets",
    "summary": "An endless maze runner where Pac-Man must outmaneuver ghosts and a glitched screen, collecting power-ups and achieving high scores.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/455400/PACMAN_256/"
  },
  {
    "id": 144,
    "title": "Pacapong (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "casual",
    "releaseDate": "none",
    "developer": "King Penguin",
    "summary": "A mashup of classic arcade games combining elements of Pac-Man, Pong, and Space Invaders into a single competitive experience.",
    "screenshots": [],
    "shopLink": "https://kingpenguin.itch.io/pacapong"
  },
  {
    "id": 145,
    "title": "Pax Britannica (itch.io)",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "real time strategy",
    "releaseDate": "2010",
    "developer": "No fun games",
    "summary": "A one-button real-time strategy game where players control factories that produce units to battle for supremacy in the depths of the ocean.",
    "screenshots": [],
    "shopLink": "https://gangles.itch.io/pax-britannica"
  },
  {
    "id": 146,
    "title": "Penarium",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "platformer",
    "releaseDate": "2015",
    "developer": "Self Made Miracle",
    "summary": "A frantic 2D arena arcade game where a contestant must survive deadly traps in a sinister circus show.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/307590/Penarium/"
  },
  {
    "id": 147,
    "title": "Pestering party plebs for pizza",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "arcade",
    "releaseDate": "2013",
    "developer": "Nik",
    "summary": "A rival club has opened downtown that is putting the Party King out of business. He hires you and your friends to infiltrate the club and get the clubbers to fight each other!",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/pestering-party-plebs-for-pizza/18983"
  },
  {
    "id": 148,
    "title": "Pitfall planet",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "puzzle adventure",
    "releaseDate": "2016",
    "developer": "Bonfire Games",
    "summary": "A cooperative puzzle-adventure game where two robots explore a mysterious planet, solving puzzles and collecting treasures.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/464900/Pitfall_Planet/"
  },
  {
    "id": 149,
    "title": "Pixeljunk monster ultimate HD",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "tower defense",
    "releaseDate": "2013",
    "developer": "Double Eleven, Q-Games Ltd.",
    "summary": "A tower defense game where players control Tikiman, defending his offspring from hordes of monsters by strategically building weapon towers.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/243780/PixelJunk_Monsters_Ultimate/"
  },
  {
    "id": 150,
    "title": "Planet Squares Incorporated (itch.io)",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "casual",
    "releaseDate": "2015",
    "developer": "Miguel Murça",
    "summary": "A multiplayer game where 2 to 6 players test various mechanics in a corporate-themed environment, supporting keyboard and Xbox controller inputs.",
    "screenshots": [],
    "shopLink": "https://miguelmurca.itch.io/psi"
  },
  {
    "id": 151,
    "title": "Pocket world DC edition (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2022",
    "developer": "ScruffyDragon Productions",
    "summary": "A 2D fighting game using the MUGEN engine, featuring super-deformed versions of DC Universe characters battling across iconic locations.",
    "screenshots": [],
    "shopLink": "https://pocket-world-dc-edition.en.uptodown.com/windows"
  },
  {
    "id": 152,
    "title": "Powball deluxe (itch.io)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "casual",
    "releaseDate": "1996, 2006",
    "developer": "POW Games",
    "summary": "Brick breaking retro action Arkanoid fans will love. Breakout with a few added twists. Farm Alchemite by destroying each level with your balls and weapons. Mysterious power-ups. Navigate through sub-games. Buy extra ammo, balls and lives to help you progress through increasingly difficult levels. Fun played solo or up to 3 players local multiplayer.",
    "screenshots": [],
    "shopLink": "https://powgames.itch.io/powball-deluxe"
  },
  {
    "id": 153,
    "title": "Power bomberman",
    "players": 8,
    "multiplayerType": "versus/coop",
    "genre": "action puzzle",
    "releaseDate": "2013, 2025",
    "developer": "Jei, Bomberman community",
    "summary": "A feature-rich Bomberman fangame. It is still in development, but a playable build is out. More infos here : https://www.bombermanboard.com/viewtopic.php?t=1925",
    "screenshots": [],
    "shopLink": "https://power-bomberman.fr.uptodown.com/windows"
  },
  {
    "id": 154,
    "title": "Power rangers: Beats of Power special edition (openbor)",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2017",
    "developer": "MersoX",
    "summary": "Power Rangers: Beats of Power is a FREE fan-made beat-em-up videogame for PC and Mac. It combines aspects of classic Power Rangers video games for the Super Nintendo and Sega Genesis, as well as adding original elements.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/power-rangers-beats-of-power/30577"
  },
  {
    "id": 155,
    "title": "Super super super super",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "platformer",
    "releaseDate": "2015",
    "developer": "Daniel Linssen",
    "summary": "Four players each take control of a superhero and work together to escape the laboratory!",
    "screenshots": [],
    "shopLink": "https://managore.itch.io/supersupersupersuper"
  },
  {
    "id": 156,
    "title": "Push push penguin",
    "players": 8,
    "multiplayerType": "coop",
    "genre": "puzzle",
    "releaseDate": "2004",
    "developer": "Pengo, Fan made",
    "summary": "Push-Push Penguin est un remake du jeu d'arcade original de Sega de 1982, Pengo. Guidez Pen-Pen ou sa chérie Deda-Deda dans les labyrinthes et essayez d'écraser tous les monstres à l'écran à l'aide des blocs de glace disséminés.",
    "screenshots": [],
    "shopLink": "https://pushpush-penguin.en.uptodown.com/windows"
  },
  {
    "id": 157,
    "title": "Rainforest (itch.io)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "casual",
    "releaseDate": "2018",
    "developer": "SimoGecko, p1nkmaria",
    "summary": "Help Joe push a trolley through a delivery warehouse on your first day at a job at rainforest, Inc. Pick up boxes of the right size and carry them to the appropriate shelf. Watch out for space on your trolley and avoid boxes from falling out of the conveyor belt, or else you will get fired!",
    "screenshots": [],
    "shopLink": "https://simogecko.itch.io/rainforest"
  },
  {
    "id": 158,
    "title": "Rayman origins",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "platformer",
    "releaseDate": "2012",
    "developer": "Ubisoft Montpellier",
    "summary": "A 2D platformer featuring Rayman and friends as they battle the Darktoons to save the Glade of Dreams, offering both single-player and co-op modes.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/207490/Rayman_Origins/"
  },
  {
    "id": 159,
    "title": "Red Earth-Warzard Mugenation Edition 2021",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2021",
    "developer": "MugenNationGameplay",
    "summary": "none",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/redearth/573644"
  },
  {
    "id": 160,
    "title": "Regular human basketball",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "sport",
    "releaseDate": "2018",
    "developer": "Powerhoof",
    "summary": "A multiplayer party game where players control giant mechanical robots to play basketball, coordinating with teammates to operate thrusters, magnet arms, and wheels in chaotic matches.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/661940/Regular_Human_Basketball/"
  },
  {
    "id": 161,
    "title": "Resident evil MUGEN (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2019",
    "developer": "Mugen community",
    "summary": "A fan-made fighting game using the MUGEN engine, featuring characters from the Resident Evil series in 2D combat scenarios.",
    "screenshots": [],
    "shopLink": "https://mugenguild.com/forum/topics/resident-evil-mugen-1-1-full-game-186128.0.html"
  },
  {
    "id": 162,
    "title": "Sagittarius (itch.io)",
    "players": 5,
    "multiplayerType": "versus",
    "genre": "turn based strategy",
    "releaseDate": "",
    "developer": "George Prosser",
    "summary": "Shoot your friends in this turn-based archery game where the main mechanic is gravity! Aim carefully and move strategically to be the last player standing in a cosmic deathmatch.",
    "screenshots": [],
    "shopLink": "https://gprosser.itch.io/sagittarius"
  },
  {
    "id": 163,
    "title": "Saint seiya Ultimate Cosmo 2.2 (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2011",
    "developer": "Fan community project",
    "summary": "A fan-developed 2D fighting game using the MUGEN engine, featuring characters from the Saint Seiya series with various stages and special moves.",
    "screenshots": [],
    "shopLink": "https://mail.jeuxmangas.com/jeux-mugen/10146-saint-seiya-ultimate-cosmo-2-2-2018"
  },
  {
    "id": 164,
    "title": "Samurai gunn",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2013",
    "developer": "Beau Blyth, Doseone",
    "summary": "A fast-paced local multiplayer game where players engage in one-hit-kill duels using swords and guns, set in a stylized feudal Japan.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/239090/Samurai_GUNN/"
  },
  {
    "id": 165,
    "title": "Sengoku basara samurai heroes (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2019",
    "developer": "Mugen community",
    "summary": "A fan-made 2D fighting game using the MUGEN engine, featuring characters from the Sengoku Basara series in combat scenarios.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/sengokumugen/420065"
  },
  {
    "id": 166,
    "title": "Serious Sam the first encounter, the second encounter",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "first person shooter",
    "releaseDate": "2009",
    "developer": "Croteam",
    "summary": "A first-person shooter where players take on the role of Sam Serious Stone, battling hordes of enemies in various environments to save humanity. The sequel to The First Encounter, continuing Sam's battle against alien forces with new weapons, enemies, and expansive levels.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/41000/Serious_Sam_HD_The_First_Encounter/"
  },
  {
    "id": 167,
    "title": "Shock troopers",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "run n gun",
    "releaseDate": "1997",
    "developer": "Saurus",
    "summary": "A run-and-gun arcade game where players choose from multiple characters to rescue a scientist's granddaughter from a terrorist organization.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/366270/SHOCK_TROOPERS/"
  },
  {
    "id": 168,
    "title": "Shoot first (download.cnet.com)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "roguelike",
    "releaseDate": "2011",
    "developer": "Teknopants",
    "summary": "A roguelike shooter combining elements of classic dungeon crawling and fast-paced gunplay, featuring procedurally generated levels.",
    "screenshots": [],
    "shopLink": "https://download.cnet.com/shoot-first/3000-2099_4-75446711.html"
  },
  {
    "id": 169,
    "title": "Shopping spree (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "racing",
    "releaseDate": "2023",
    "developer": "JustOneDev",
    "summary": "Shopping Spree is a simple endless game where you play as a shopping cart and carry items from boxes into their respective shelves. ",
    "screenshots": [],
    "shopLink": "https://justonedev.itch.io/shopping-spree"
  },
  {
    "id": 170,
    "title": "Shutshimi",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "shoot em up",
    "releaseDate": "2015",
    "developer": "Neon Deity Games",
    "summary": "A randomized shoot 'em up about a muscle-bound fish with memory problems defending the seven seas.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/332530/Shutshimi/"
  },
  {
    "id": 171,
    "title": "Sim war V",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "shooter",
    "releaseDate": "2007",
    "developer": "Beau Blyth",
    "summary": "An intense 8-bit game between 2 teams, with many available weapons and cards for battle.",
    "screenshots": [],
    "shopLink": "https://www.jetelecharge.com/Jeux/4685.php"
  },
  {
    "id": 172,
    "title": "Silver Knights’s crusaders",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "action platformer",
    "releaseDate": "2023",
    "developer": "True role dreams",
    "summary": "Fangame inspired by the Castlevania saga, in which you can choose between three completely original characters. The story and the development of the game, moreover, are adapted so that you can play both solo and in coop mode, with a friend playing on the same computer.",
    "screenshots": [],
    "shopLink": "https://silver-nights-crusaders.en.uptodown.com/windows"
  },
  {
    "id": 173,
    "title": "Skadonk showdown (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "racing",
    "releaseDate": "2017",
    "developer": "Duncanbellsa",
    "summary": "Shadonk Showdown is a physics charged, multiplayer vehicle game wrapped in a South African theme. Fast reflexes, itchy trigger fingers and luck are needed to come out on top. The game concept, was sparked by the rich concentration of different individuals and cultures within South Africa – most importantly the Taxi culture.",
    "screenshots": [],
    "shopLink": "https://duncanbellsa.itch.io/skadonk-showdown"
  },
  {
    "id": 174,
    "title": "Skulls of the shogun",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "turn based strategy",
    "releaseDate": "2013",
    "developer": "17-BIT",
    "summary": "A turn-based strategy game where players control undead samurai in a quest for revenge in the afterlife.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/228960/Skulls_of_the_Shogun/"
  },
  {
    "id": 175,
    "title": "Sleight (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "stealth",
    "releaseDate": "2018",
    "developer": "Demerara Games",
    "summary": "The great art exposition at Manor LeBleu unites some of the most valuable art pieces in one single place this night. You were hired to follow the trail of the most deceitful and sly spy known: your friend!",
    "screenshots": [],
    "shopLink": "https://demeraragames.itch.io/sleight"
  },
  {
    "id": 176,
    "title": "Snake snafu (itch.io)",
    "players": 3,
    "multiplayerType": "versus",
    "genre": "casual",
    "releaseDate": "2016",
    "developer": "orange08, yellowafterlife",
    "summary": "Snake Snafu is a 2 player game which can be played locally(hotseat) or online. A maximum of 3 players can play simultaneously. Snake Snafu has been designed and created primarily for a 2 Player experience. Single player mode may feel somewhat empty.",
    "screenshots": [],
    "shopLink": "https://orange08.itch.io/snake-snafu"
  },
  {
    "id": 177,
    "title": "Snowman Arena",
    "players": 3,
    "multiplayerType": "versus/coop",
    "genre": "arena shooter",
    "releaseDate": "2021",
    "developer": "Nukeborn",
    "summary": "Top-down local multiplayer arena shooter where players can gather advantage via varied projectiles and power-ups. Snowman Arena connects everyone together in a fun way, no matter the age or level of the player.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/1768980/Snowman_Arena/"
  },
  {
    "id": 178,
    "title": "Sonic robo blast 2 kart",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "racing",
    "releaseDate": "",
    "developer": "NeoRetroGames",
    "summary": "SRB2Kart is a classic styled kart racer, complete with beautiful courses, and wacky items. Of course, because it’s SRB2Kart, it has a Sonic twist that really shows the classic charm that a lot of us know and love from the good old days™",
    "screenshots": [],
    "shopLink": "https://miimoka.itch.io/sonic-robo-blast-2-kart-fp"
  },
  {
    "id": 179,
    "title": "Soulstice (itch.io)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "puzzle",
    "releaseDate": "2022",
    "developer": "Reply Game Studios",
    "summary": "An action-adventure game where players control two sisters in a dark fantasy world, combining their abilities to combat enemies and uncover secrets.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/1602080/Soulstice/"
  },
  {
    "id": 180,
    "title": "spaceship hunters",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "shooter",
    "releaseDate": "2022",
    "developer": "Pierre Nury",
    "summary": "Spaceship Hunters is a chaotic couch co-op shoot-em-up for 4 players. Working as a crew, fight your way through the worst criminals the universe has to offer.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/1819290/Spaceship_Hunters/"
  },
  {
    "id": 181,
    "title": "Speedrunners",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "racing",
    "releaseDate": "2016",
    "developer": "Double dutch games",
    "summary": "Cut-throat multiplayer running game that pits 4 players against each other, locally and/or online. Run, jump, swing around, and use devious weapons and pick-ups to knock opponents off-screen! One of the most competitive games you'll ever play.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/207140/SpeedRunners/"
  },
  {
    "id": 182,
    "title": "Spelunky",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "action roguelike",
    "releaseDate": "2013",
    "developer": "Mossmouth",
    "summary": "A unique platformer with randomized levels, challenging players to explore underground caves filled with monsters, traps, and treasure.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/239350/Spelunky/"
  },
  {
    "id": 183,
    "title": "Star wars ultimate battle (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2013",
    "developer": "Cenobite 53",
    "summary": "A fan-made fighting game using the MUGEN engine, featuring characters from the Star Wars universe.",
    "screenshots": [],
    "shopLink": "https://star-wars-the-ultimate-battle.en.uptodown.com/windows"
  },
  {
    "id": 184,
    "title": "Steel warriors (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2013",
    "developer": "MabsKMK",
    "summary": "Steel Warriors is a Metal Slug fan game created by MabsKMK for the M.U.G.E.N fighting game engine. You can choose over a variety of vehicles from the series, and fight the others in 1-on-1 battle. The game is still on development, currently on beta version 241213.",
    "screenshots": [],
    "shopLink": "https://mugen.fandom.com/wiki/Steel_Warriors"
  },
  {
    "id": 185,
    "title": "Street fighter SNK edition (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2020",
    "developer": "Mugen community",
    "summary": "A MUGEN-based game combining characters from the Street Fighter and SNK universes.",
    "screenshots": [],
    "shopLink": "https://mugenplayer.blogspot.com/2020/05/street-fighter-snk-edition.html"
  },
  {
    "id": 186,
    "title": "Street fighters II deluxe 2 (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2017",
    "developer": "Elecbyte",
    "summary": "An enhanced MUGEN version of Street Fighter II with additional features and characters.",
    "screenshots": [],
    "shopLink": "https://steemit.com/gaming/@madviking/street-fighter-2-deluxe-2-m-u-g-e-n-a-lot-of-playability-modes-characters-and-challenges-for-free"
  },
  {
    "id": 187,
    "title": "Street fighters one remake (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "",
    "developer": "Valkyrie Project",
    "summary": "An enhanced MUGEN version of Street Fighter II with additional features and characters.",
    "screenshots": [],
    "shopLink": "https://gamebanana.com/mods/382658"
  },
  {
    "id": 188,
    "title": "street of rage remake",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "beat em up",
    "releaseDate": "2011",
    "developer": "BomberGames",
    "summary": "A fan-made remake of the classic beat 'em up series, combining elements from all three original games with new content.",
    "screenshots": [],
    "shopLink": "https://street-rage-remake.fr.uptodown.com/windows"
  },
  {
    "id": 189,
    "title": "Super Final Fight Gold Plus",
    "players": 3,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2022",
    "developer": "EverlastingGaming",
    "summary": "A fan-made beat 'em up game inspired by the Final Fight series, featuring enhanced graphics and gameplay.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/SFFGPBootleg/698995"
  },
  {
    "id": 190,
    "title": "Super head ball (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "sport",
    "releaseDate": "2019",
    "developer": "SethSafety",
    "summary": "A local multiplayer game for 2-4 players where participants compete to throw a decapitated head into a blazing pyre while avoiding friendly fire.",
    "screenshots": [],
    "shopLink": "https://sethsafety.itch.io/super-head-ball"
  },
  {
    "id": 191,
    "title": "Super Mario brawl (openbor)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2011",
    "developer": "SEEP",
    "summary": "A fan-made beat 'em up game using the OpenBOR engine, allowing players to control Mario or Luigi in various modes to save the Mushroom Kingdom from Bowser.",
    "screenshots": [],
    "shopLink": "https://www.gamebrew.org/wiki/Super_Mario_Brawl_PSP"
  },
  {
    "id": 192,
    "title": "Super punchball (itch.io)",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "sport",
    "releaseDate": "2013",
    "developer": "Neverpants",
    "summary": "Super Punchball is a 4-player sports game where players can engage in local multiplayer games of boxing or soccer using various controllers, including Xbox 360 controllers and keyboard controls.",
    "screenshots": [],
    "shopLink": "https://neverpants.itch.io/super-punchball"
  },
  {
    "id": 193,
    "title": "Super street fighter 2 Turbo Snes plus (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "",
    "developer": "Mugen community",
    "summary": "A MUGEN-based fan game that enhances the classic Super Street Fighter 2 Turbo with additional features and characters.",
    "screenshots": [],
    "shopLink": "https://mugenplayer.blogspot.com/2020/07/super-street-fighter-2-turbo-plus-snes.html"
  },
  {
    "id": 194,
    "title": "Super street fighter II nes/ mighty street fighter (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2019",
    "developer": "Cobra Caddie",
    "summary": "A MUGEN adaptation that brings the Street Fighter experience to an NES-style platform with unique gameplay elements.",
    "screenshots": [],
    "shopLink": "https://mugenguild.com/forum/PHPSESSID.ncg5lf95a92i2gtri47adf9btn/topics/mighty-street-fighter-formerly-sf2nes-185528.0.html"
  },
  {
    "id": 195,
    "title": "superfighters",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "arena shooter",
    "releaseDate": "2011",
    "developer": "MythoLogic Interactive",
    "summary": "An action-packed 2D platformer where players engage in chaotic battles using a variety of weapons and tactics.",
    "screenshots": [],
    "shopLink": "https://mythologicinteractive.com/Superfighters"
  },
  {
    "id": 196,
    "title": "superfighters deluxe",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "arena shooter",
    "releaseDate": "2018",
    "developer": "MythoLogic Interactive",
    "summary": "Superfighters Deluxe is a unique action game that combines brawling, shooting and platforming in dynamic sandboxy 2D levels. Lots of weapons and fun gameplay systems interlock to create absurd action-movie chaos.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/855860/Superfighters_Deluxe/"
  },
  {
    "id": 197,
    "title": "Surf shogun (itch.io)",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "action",
    "releaseDate": "",
    "developer": "farmergnome",
    "summary": "The time is the distant future. the place is neo kalifornyO, a peaceful city ruled by the law of zen until gangs of surf samurai arrived, bringing their ancient feudal conflicts to the beachfront. now the city is desperate for a hero…",
    "screenshots": [],
    "shopLink": "https://farmergnome.itch.io/surf-shogun"
  },
  {
    "id": 198,
    "title": "Swarm Alien : reactive drop",
    "players": 8,
    "multiplayerType": "versus",
    "genre": "top-down shooter",
    "releaseDate": "2017",
    "developer": "Reactive Drop Team",
    "summary": "Co-operative top-down shooter game available for free. An epic bug hunt featuring a unique blend of co-op play and squad-level tactics.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/563560/Alien_Swarm_Reactive_Drop/"
  },
  {
    "id": 199,
    "title": "Swing on me (itch.io)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "climbing",
    "releaseDate": "2016",
    "developer": "UnknownLogicStudios",
    "summary": "A co-op endless runner style game where both players are attached by a rope and can use this rope to swing off of each other. Just make sure one of you holds on.",
    "screenshots": [],
    "shopLink": "https://unknownlogicstudios.itch.io/swing-on-me"
  },
  {
    "id": 200,
    "title": "Tasty blue",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "arcade",
    "releaseDate": "2015",
    "developer": "Dingo games",
    "summary": "An underwater side-scrolling game where you start as a small goldfish with an insatiable appetite, escaping into the ocean and eating everything you encounter to grow larger.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/345200/Tasty_Blue/"
  },
  {
    "id": 201,
    "title": "Teenage mutant ninja turtles vs justice league (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "",
    "developer": "Kamekaze",
    "summary": "A fan-made fighting game using the MUGEN engine, featuring characters from both the Teenage Mutant Ninja Turtles and the Justice League universes. https://mugenguild.com/forum/topics/teenage-mutant-ninja-turtles-x-justice-league-updated41720-189648.0.html",
    "screenshots": [],
    "shopLink": "https://kamekaze.world/xjlt/"
  },
  {
    "id": 202,
    "title": "Teenage Mutant Ninja Turtles: Rescue-Palooza! (openbor)",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2019",
    "developer": "MersoX",
    "summary": "A fan-made beat 'em up game developed using the OpenBOR engine, featuring numerous playable characters from the TMNT universe.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/TMNT-Rescue-Palooza/39658"
  },
  {
    "id": 203,
    "title": "Telepath tatics",
    "players": 6,
    "multiplayerType": "versus",
    "genre": "turn based strategy",
    "releaseDate": "2015",
    "developer": "Sinister Design",
    "summary": "A turn-based strategy RPG set in a steampunk universe, featuring destructible battlefields and environmental hazards.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/357940/Telepath_Tactics/"
  },
  {
    "id": 204,
    "title": "Tempo quest (itch.io)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "rhythm rpg",
    "releaseDate": "",
    "developer": "pixel-boy",
    "summary": "The game is a Roguelike mixed with Dance dance revolution mechanic, 1 - 4 players local coop, with gamepad support, French and English languages.",
    "screenshots": [],
    "shopLink": "https://pixel-boy.itch.io/tempo-quest"
  },
  {
    "id": 205,
    "title": "Tennis elbow 2013",
    "players": 3,
    "multiplayerType": "versus/coop",
    "genre": "sport",
    "releaseDate": "2013",
    "developer": "Mana Games",
    "summary": "A tennis simulation game praised for its realistic gameplay and physics, offering both single-player and multiplayer modes.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/346470/Tennis_Elbow_2013/"
  },
  {
    "id": 206,
    "title": "Terrordrome (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "",
    "developer": "Hur4c4n",
    "summary": "A fan-made fighting game using the MUGEN engine, featuring horror movie characters as fighters.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/1291170/Terrordrome__Reign_of_the_Legends/"
  },
  {
    "id": 207,
    "title": "The Expendabros",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "gun n run",
    "releaseDate": "2014",
    "developer": "Free Lives",
    "summary": "A crossover game combining the action of Broforce with characters from The Expendables film series, offering explosive side-scrolling gameplay.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/312990/The_Expendabros/"
  },
  {
    "id": 208,
    "title": "TMNT 8-Bit Recolored & Extended (openbor)",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "beat em up",
    "releaseDate": "2024",
    "developer": "Gabotico",
    "summary": "A fan-made beat 'em up game using the OpenBOR engine, featuring enhanced graphics and extended content from the original 8-bit TMNT games.",
    "screenshots": [],
    "shopLink": "https://gamejolt.com/games/TMNTRE/911813"
  },
  {
    "id": 209,
    "title": "TMNT tournament fighters NES (mugen)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "",
    "developer": "Zelgadis",
    "summary": "A MUGEN adaptation of the classic TMNT Tournament Fighters game from the NES era, featuring enhanced gameplay and character roster.",
    "screenshots": [],
    "shopLink": "https://gamebanana.com/mods/379064"
  },
  {
    "id": 210,
    "title": "Toadal war (itch.io)",
    "players": 6,
    "multiplayerType": "versus",
    "genre": "rhythm",
    "releaseDate": "2016",
    "developer": "Sofa Squadron",
    "summary": "A multiplayer rhythm game in which each player is a musical toad. Press a button to sing when the wave hits you. If you miss, you're eliminated!",
    "screenshots": [],
    "shopLink": "https://sofasquadron.itch.io/toadalwar"
  },
  {
    "id": 211,
    "title": "Totemori",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "action puzzle",
    "releaseDate": "2017",
    "developer": "Schrolab",
    "summary": "Totemori is a free-to-play local-multiplayer brawler where you build towers while trying to topple everyone else’s!",
    "screenshots": [],
    "shopLink": "https://schrolab.itch.io/totemori"
  },
  {
    "id": 212,
    "title": "Tough guy: fighting titans (mugen)",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2019",
    "developer": "Super Fight Team",
    "summary": "A life investment in intense training has transformed one man into a chiseled form of near perfection. The level of vitality flowing through his body is astounding. This man, Cula, is restless for lack of a suitable adversary.",
    "screenshots": [],
    "shopLink": "https://www.superfighter.com/tough/index.html"
  },
  {
    "id": 213,
    "title": "Towerclimb",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "platformer",
    "releaseDate": "2015",
    "developer": "Davioware",
    "summary": "TowerClimb is a difficult and rewarding procedurally generated platformer with roguelike elements. Enormous and mysterious towers of ancient unknown origin stand above humanity, extending to the heavens. Struggle forward as a weak human, driven by an iron will to reach the top.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/396640/TowerClimb/"
  },
  {
    "id": 214,
    "title": "Towerfall- Ascension",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "party brawler",
    "releaseDate": "2014",
    "developer": "Maddy Makes Games Inc.",
    "summary": "TowerFall Ascension is the definitive version of the hit archery combat game. Inspired by classics from the golden age of couch multiplayer, it's a 4-player local party game centering around hilarious, intense versus matches. The core mechanics are simple and accessible, but hard to master and combat is fierce.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/251470/TowerFall_Ascension"
  },
  {
    "id": 215,
    "title": "Trench run",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "run n gun",
    "releaseDate": "2015",
    "developer": "Transhuman Design",
    "summary": "Trench Run is a mayhem-filled, laugh a minute casual 4-player action game brought to you by the makers of King Arthur’s Gold and Soldat.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/262100/Trench_Run"
  },
  {
    "id": 216,
    "title": "Turbo taucher",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "arcade",
    "releaseDate": "",
    "developer": "Yobllud",
    "summary": "Turbo Taucher is a action-oriented multiplayer diving game! You and up to 3 Opponents search for hidden Treasure in the deep sea. An epic fight will take place over whom will dominate the other players. Dodge their TURBO-Attacks to be safe or try for yourself to forcefully get ahold of their earnings.",
    "screenshots": [],
    "shopLink": "https://yobllud.itch.io/turbo-taucher"
  },
  {
    "id": 217,
    "title": "unrailed!",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "survival",
    "releaseDate": "2020",
    "developer": "Indoor Astronaut",
    "summary": "Unrailed! is a co-op multiplayer game where you have to work together with your friends to build a train track across endless procedurally generated worlds. Master random encounters with its inhabitants, upgrade your train and keep it from derailing!",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/1016920/Unrailed/"
  },
  {
    "id": 218,
    "title": "Unsung warriors",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "platformer",
    "releaseDate": "Coming soon",
    "developer": "Osarion",
    "summary": "The prologue is available but the complete game is coming soon. Unsung Warriors is a 2D action-adventure game. The game can be played solo or in couch co-op mode. Enjoy beautiful handcrafted levels. Fight against ferocious enemies and discover the many secrets of this ancient world.",
    "screenshots": [],
    "shopLink": "https://unsungwarriors.itch.io/unsung-warriors-prologue"
  },
  {
    "id": 219,
    "title": "V-texer (itch.io)",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "racing",
    "releaseDate": "2015",
    "developer": "Outlier Interactive",
    "summary": "V-TEXER is a high speed racing game, inspired by futuristic racing games like F-Zero and Wipeout. Players race each other on twisting roller coaster-like race tracks at over 1000 km/h!",
    "screenshots": [],
    "shopLink": "https://outlier.itch.io/vtexer"
  },
  {
    "id": 220,
    "title": "Vagante",
    "players": 4,
    "multiplayerType": "coop",
    "genre": "action rpg",
    "releaseDate": "2018",
    "developer": "Nuke Nine",
    "summary": "Vagante is an action-packed platformer that features permanent death and procedurally generated levels. Play cooperatively with friends both locally and online, or adventure solo in this challenging roguelike-inspired game.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/323220/Vagante/"
  },
  {
    "id": 221,
    "title": "Van tourisimo (itch.io)",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "racing",
    "releaseDate": "2018",
    "developer": "Stevie G",
    "summary": "A de-make of the old arcade favourite Super-Sprint for 1 or 2 players. ",
    "screenshots": [],
    "shopLink": "https://stevieg.itch.io/van-tourisimo"
  },
  {
    "id": 222,
    "title": "Viper League (itch.io)",
    "players": 4,
    "multiplayerType": "versus",
    "genre": "arcade",
    "releaseDate": "2017",
    "developer": "Viperleague",
    "summary": "Viper League is a local multiplayer snake arena combat game for 2-8 players.",
    "screenshots": [],
    "shopLink": "https://viperleague.itch.io/play"
  },
  {
    "id": 223,
    "title": "Wanba warriors",
    "players": 2,
    "multiplayerType": "versus",
    "genre": "fighting",
    "releaseDate": "2020",
    "developer": "Wanba studio",
    "summary": "Have you got what it takes to be a Wanba Warrior? Step into the absurd world of calligraphy combat and prepare to lay the smackdown upon all who dare to oppose you, dishing out damage with your chosen ink brush of brutality! highly recommend playing with controllers.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/1021770/_Wanba_Warriors/"
  },
  {
    "id": 224,
    "title": "Wave for me (itch.io)",
    "players": 9,
    "multiplayerType": "coop",
    "genre": "casual",
    "releaseDate": "2018",
    "developer": "Zuggamasta",
    "summary": "This game is based on fantasy Famicon cartridges. It is designed around one of those Cartridges with the title Wave For Me",
    "screenshots": [],
    "shopLink": "https://zuggamasta.itch.io/wave-for-me"
  },
  {
    "id": 225,
    "title": "worms armageddon",
    "players": 8,
    "multiplayerType": "versus/coop",
    "genre": "turn based strategy",
    "releaseDate": "1999",
    "developer": "Team 17 Digital Ltd",
    "summary": "Those intrepid invertebrates return with a vengeance in the much-loved Worms™ Armageddon. It’s a whole new can of worms! It’s hilarious fun that you can enjoy on your own or with all your friends.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/217200/worms_armageddon/"
  },
  {
    "id": 226,
    "title": "worms reloaded",
    "players": 4,
    "multiplayerType": "versus/coop",
    "genre": "turn based strategy",
    "releaseDate": "2010",
    "developer": "Team 17 Digital Ltd",
    "summary": "Ten years on from Worms™ Armageddon and the turn-based comic mayhem continues in Worms™ Reloaded, an all-new edition available for PC through Steam.",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/22600/Worms_Reloaded/"
  },
  {
    "id": 227,
    "title": "worms world party",
    "players": 6,
    "multiplayerType": "versus/coop",
    "genre": "turn based strategy",
    "releaseDate": "2015",
    "developer": "Team 17 Digital Ltd",
    "summary": "Imagine taking the perfect online gaming experience and one of the most popular Worms games ever made, adding a touch of Steam achievements, leaderboards, cloud saves, full controller support; a little sprinkle of 1080 / 60FPS, and you have Worms World Party Remastered!",
    "screenshots": [],
    "shopLink": "https://store.steampowered.com/app/270910/Worms_World_Party_Remastered/"
  },
  {
    "id": 228,
    "title": "WWE raw 2007",
    "players": 2,
    "multiplayerType": "versus/coop",
    "genre": "fighting",
    "releaseDate": "2006",
    "developer": "Yuke’s",
    "summary": "WWE SmackDown vs. Raw 2007 is a professional wrestling video game developed by Yuke’s and published by THQ. It is based on the professional wrestling promotion World Wrestling Entertainment (WWE)",
    "screenshots": [],
    "shopLink": "https://oldgamesdownload.com/wwe-smackdown-vs-raw-2007-u34/"
  },
  {
    "id": 229,
    "title": "X-Men legends 2: rise of apocalypse",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "action rpg",
    "releaseDate": "2005",
    "developer": "Raven Software Corporation, SuperVillain Studios, Inc., Vicarious Visions, Inc.",
    "summary": "X-Men Legends II: Rise of Apocalypse is an action role-playing game developed primarily by Raven Software and published by Activision.",
    "screenshots": [],
    "shopLink": "https://oldgamesdownload.com/x-men-legends-ii-rise-of-apocalypse/"
  },
  {
    "id": 230,
    "title": "XO-plantets (itch.io)",
    "players": 2,
    "multiplayerType": "coop",
    "genre": "action rpg",
    "releaseDate": "2015",
    "developer": "Bohfam",
    "summary": "Frantic rogue-lite, action platformer, and tower defense, with a little rpg elements.",
    "screenshots": [],
    "shopLink": "https://bohfam.itch.io/xo-planets"
  }
]

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_images_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = []
        for img in soup.find_all(['img', 'source']):
            src = img.get('src') or img.get('data-src') or img.get('srcset')
            if src:
                # Nettoyage sommaire pour srcset
                src = src.split(' ')[0]
                full_url = urljoin(url, src)
                if any(ext in full_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    if "icon" not in full_url.lower() and "logo" not in full_url.lower():
                        images.append(full_url)
        return list(dict.fromkeys(images))
    except Exception:
        return []

def download_and_organize(data):
    if not os.path.exists(BASE_FOLDER):
        os.makedirs(BASE_FOLDER)

    for game in data:
        title = clean_filename(game['title'])
        link = game['shopLink']
        game_path = os.path.join(BASE_FOLDER, title)
        
        # Vérification si le dossier est déjà complet
        if os.path.exists(game_path):
            existing_files = [f for f in os.listdir(game_path) if os.path.isfile(os.path.join(game_path, f))]
            if len(existing_files) >= TARGET_COUNT:
                print(f"[-] {title} possède déjà {TARGET_COUNT} images. Skip.")
                continue

        print(f"[+] Analyse de : {title}...")
        if not os.path.exists(game_path):
            os.makedirs(game_path)

        image_urls = get_images_from_url(link)
        downloaded_count = 0
        
        for img_url in image_urls:
            if downloaded_count >= TARGET_COUNT:
                break
            
            try:
                # On récupère l'image
                img_res = requests.get(img_url, timeout=5, stream=True)
                if img_res.status_code == 200:
                    # Vérification de la taille via Content-Length ou mesure du contenu
                    content = img_res.content
                    size_kb = len(content) / 1024
                    
                    if size_kb < MIN_SIZE_KB:
                        # Image trop légère, on passe à la suivante
                        continue

                    # Détermination de l'extension
                    ext = ".jpg"
                    if ".png" in img_url.lower(): ext = ".png"
                    elif ".webp" in img_url.lower(): ext = ".webp"
                    
                    file_full_path = os.path.join(game_path, f"screenshot_{downloaded_count + 1}{ext}")
                    
                    # On n'écrase pas si déjà là (cas d'une reprise de script)
                    if not os.path.exists(file_full_path):
                        with open(file_full_path, 'wb') as f:
                            f.write(content)
                        downloaded_count += 1
                        print(f"    Image {downloaded_count} sauvegardée ({int(size_kb)}ko)")
                        time.sleep(0.5)
            except Exception:
                continue

        if downloaded_count < TARGET_COUNT:
            print(f"    [!] Attention : seulement {downloaded_count} images trouvées > {MIN_SIZE_KB}ko.")

if __name__ == "__main__":
    download_and_organize(games_list)