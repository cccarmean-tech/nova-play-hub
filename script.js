const categories = ['All', 'Adventure', 'Action', 'Strategy', 'Puzzle', 'Simulation', 'Sports', 'Racing', 'Sandbox', 'Horror', 'Fantasy', 'Sci-Fi', 'Social'];

const titleAdjectives = [
  'Aether', 'Atlas', 'Aurora', 'Cinder', 'Cobalt', 'Cosmos', 'Dusk', 'Echo', 'Ember', 'Eon',
  'Fable', 'Frost', 'Glint', 'Halo', 'Haven', 'Horizon', 'Hyper', 'Kestrel', 'Lumen', 'Lynx',
  'Mirage', 'Nebula', 'Nova', 'Orbit', 'Pioneer', 'Quantum', 'Rift', 'Rogue', 'Solar', 'Summit',
  'Vanta', 'Velora', 'Vortex', 'Warden', 'Zephyr'
];

const titleNouns = [
  'Harbor', 'Ridge', 'Vault', 'Circuit', 'Arcade', 'Echoes', 'Signal', 'Summit', 'Shore', 'Gate',
  'Mosaic', 'Tide', 'Hollow', 'Lattice', 'Nexus', 'Drift', 'Frontier', 'Orbit', 'Beacon', 'Ritual',
  'Crest', 'Arena', 'Wilds', 'Field', 'Plex', 'Ascent', 'Convergence', 'Paradox', 'Waves', 'City'
];

const titleSuffixes = ['Online', 'Pro', 'Prime', 'Zero', 'X', 'Live', 'Rush', 'Arena', 'Eclipse', 'Beta'];

const descriptors = [
  'A refined multiplayer experience built around momentum and style.',
  'A high-contrast adventure with cinematic pacing and satisfying progression.',
  'A vivid sandbox designed for creativity, social play, and quick drops.',
  'A competitive challenge that balances fast reflexes with tactical depth.',
  'A polished escape room with layered puzzles and elegant feedback.',
  'A calming world that rewards curiosity, crafting, and experimentation.',
  'A story-rich quest filled with beautiful environments and smart encounters.',
  'A fresh social hub made for casual play, parties, and shared goals.'
];

const gameLibrary = Array.from({ length: 300 }, (_, index) => {
  const category = categories[(index % (categories.length - 1)) + 1];
  const title = `${titleAdjectives[index % titleAdjectives.length]} ${titleNouns[(index * 3 + 1) % titleNouns.length]} ${titleSuffixes[index % titleSuffixes.length]}`;
  const description = descriptors[index % descriptors.length];
  const rating = (4.5 + (index % 5) * 0.1).toFixed(1);
  const players = 1200 + ((index * 53) % 18000);

  return {
    id: index + 1,
    title,
    category,
    description,
    rating,
    players,
    tag: `${category} • ${index % 2 === 0 ? 'Co-op' : 'Solo'}`
  };
});

const state = {
  activeCategory: 'All',
  search: ''
};

const gamesEl = document.getElementById('games');
const searchInput = document.getElementById('searchInput');
const chipRow = document.getElementById('chipRow');
const featuredTitleEl = document.getElementById('featuredTitle');
const featuredDescriptionEl = document.getElementById('featuredDescription');
const featuredTagsEl = document.getElementById('featuredTags');
const gameModal = document.getElementById('gameModal');
const modalTitle = document.getElementById('modalTitle');
const modalDescription = document.getElementById('modalDescription');
const modalBadges = document.getElementById('modalBadges');
const modalPlayers = document.getElementById('modalPlayers');
const closeModal = document.getElementById('closeModal');
const launchButton = document.getElementById('launchButton');

function renderChips() {
  chipRow.innerHTML = '';
  categories.forEach((category) => {
    const button = document.createElement('button');
    button.className = `chip ${state.activeCategory === category ? 'active' : ''}`;
    button.textContent = category;
    button.addEventListener('click', () => {
      state.activeCategory = category;
      renderChips();
      renderGames();
    });
    chipRow.appendChild(button);
  });
}

function getFilteredGames() {
  const query = state.search.trim().toLowerCase();
  return gameLibrary.filter((game) => {
    const matchesCategory = state.activeCategory === 'All' || game.category === state.activeCategory;
    const matchesSearch = !query || `${game.title} ${game.description} ${game.category}`.toLowerCase().includes(query);
    return matchesCategory && matchesSearch;
  });
}

function renderGames() {
  const filteredGames = getFilteredGames();
  gamesEl.innerHTML = '';

  if (!filteredGames.length) {
    gamesEl.innerHTML = '<div class="card"><h4>No worlds matched</h4><p>Try another keyword or switch category.</p></div>';
    return;
  }

  filteredGames.forEach((game) => {
    const card = document.createElement('article');
    card.className = 'card';
    card.innerHTML = `
      <p class="eyebrow">${game.category}</p>
      <h4>${game.title}</h4>
      <p>${game.description}</p>
      <div class="card-footer">
        <span>${game.tag}</span>
        <span>★ ${game.rating}</span>
      </div>
    `;
    card.addEventListener('click', () => openModal(game));
    gamesEl.appendChild(card);
  });
}

function openModal(game) {
  modalTitle.textContent = game.title;
  modalDescription.textContent = game.description;
  modalPlayers.textContent = `${game.players.toLocaleString()}+`;
  modalBadges.innerHTML = `
    <span class="badge">${game.category}</span>
    <span class="badge">★ ${game.rating}</span>
    <span class="badge">${game.tag}</span>
  `;
  launchButton.onclick = () => {
    modalTitle.textContent = `${game.title} • Launching`;
    launchButton.textContent = 'Ready to play';
  };

  gameModal.classList.add('open');
  gameModal.setAttribute('aria-hidden', 'false');
}

function closeCurrentModal() {
  gameModal.classList.remove('open');
  gameModal.setAttribute('aria-hidden', 'true');
  launchButton.textContent = 'Launch experience';
}

function setFeaturedGame() {
  const featured = gameLibrary[17];
  featuredTitleEl.textContent = featured.title;
  featuredDescriptionEl.textContent = featured.description;
  featuredTagsEl.innerHTML = `
    <span>${featured.category}</span>
    <span>★ ${featured.rating}</span>
    <span>${featured.tag}</span>
  `;
}

searchInput.addEventListener('input', (event) => {
  state.search = event.target.value;
  renderGames();
});

closeModal.addEventListener('click', closeCurrentModal);
gameModal.addEventListener('click', (event) => {
  if (event.target === gameModal) {
    closeCurrentModal();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeCurrentModal();
  }
});

renderChips();
setFeaturedGame();
renderGames();
