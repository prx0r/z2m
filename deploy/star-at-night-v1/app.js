// Star at Night — App with Real API
import { StarAtNightAPI } from './api.js';

const state = {
  photos: [],
  sessionId: null,
  products: []
};

const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const photoGrid = document.getElementById('photoGrid');
const generateBtn = document.getElementById('generateBtn');
const loading = document.getElementById('loading');
const loadingText = document.getElementById('loadingText');
const results = document.getElementById('results');
const resultsTitle = document.getElementById('resultsTitle');
const resultsGrid = document.getElementById('resultsGrid');

// Drag & drop
uploadZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
  uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', async (e) => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  await handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', async (e) => {
  await handleFiles(e.target.files);
});

async function handleFiles(files) {
  for (const file of files) {
    if (!file.type.startsWith('image/')) continue;

    // Upload to API
    const result = await StarAtNightAPI.uploadPhoto(file);
    
    if (result.success) {
      state.photos.push(result.photo);

      const reader = new FileReader();
      reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'photo';
        img.alt = file.name;
        photoGrid.appendChild(img);
      };
      reader.readAsDataURL(file);

      if (state.photos.length > 0) {
        generateBtn.classList.add('visible');
      }
    }
  }
}

// Generate products
generateBtn.addEventListener('click', generateProducts);

async function generateProducts() {
  generateBtn.disabled = true;
  loading.classList.add('active');

  const texts = [
    'Looking at your photos...',
    'Finding the perfect details...',
    'Creating something special...',
    'Almost ready...'
  ];

  let i = 0;
  const interval = setInterval(() => {
    loadingText.textContent = texts[Math.min(i, texts.length - 1)];
    i++;
  }, 1200);

  // Create session with default values
  const sessionResult = await StarAtNightAPI.createSession({
    name: 'Your loved one',
    relationship: '',
    occasion: '',
    description: 'Created from uploaded photos',
    tone: ['beautiful'],
    photoIds: state.photos.map(p => p.id)
  });

  state.sessionId = sessionResult.session?.id;

  // Generate products
  const genResult = await StarAtNightAPI.generateProducts(state.sessionId);
  
  clearInterval(interval);

  if (genResult.success) {
    state.products = genResult.products;
    loading.classList.remove('active');
    showResults(genResult.products);
  }
}

function showResults(products) {
  resultsTitle.textContent = `We made ${products.length} things from your photos.`;
  resultsGrid.innerHTML = '';

  products.forEach((product, i) => {
    const photo = state.photos[0];
    const card = document.createElement('article');
    card.className = 'product-card';
    card.innerHTML = `
      <div class="product-card__image">
        <span class="product-card__badge">${product.badge}</span>
        ${photo ? `<img src="${API_BASE}/api/photos/${photo.id}" alt="${product.title}">` : ''}
      </div>
      <div class="product-card__body">
        <h3 class="product-card__title">${product.title}</h3>
        <p class="product-card__desc">${product.subtitle}</p>
        <p class="product-card__made">Made from ${product.madeFrom}</p>
        <p class="product-card__price">£${product.price}</p>
      </div>
    `;

    resultsGrid.appendChild(card);

    // Staggered reveal
    setTimeout(() => {
      card.classList.add('visible');
    }, i * 100);
  });

  results.classList.add('active');
  results.scrollIntoView({ behavior: 'smooth' });
}

// Scroll header
window.addEventListener('scroll', () => {
  document.querySelector('.header').classList.toggle('scrolled', window.scrollY > 50);
});
