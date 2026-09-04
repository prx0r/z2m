import { Hono } from 'hono';
import { serve } from '@hono/node-server';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { v4 as uuid } from 'uuid';
import fs from 'fs/promises';
import path from 'path';

const app = new Hono();
const PORT = 3000;

// Middleware
app.use('*', cors());
app.use('*', logger());

// In-memory store (replace with D1/KV later)
const store = {
  photos: new Map(),
  sessions: new Map(),
  products: new Map()
};

// Ensure upload directory
const UPLOAD_DIR = './uploads';
await fs.mkdir(UPLOAD_DIR, { recursive: true });

// ============================================
// ROUTES
// ============================================

// Health check
app.get('/', (c) => c.json({ 
  name: 'Star at Night API',
  version: '0.1.0',
  status: 'running',
  endpoints: {
    photos: 'POST /api/photos',
    sessions: 'POST /api/sessions',
    generate: 'POST /api/generate',
    products: 'GET /api/products/:id',
    mcp: 'POST /mcp'
  }
}));

// ============================================
// PHOTOS
// ============================================

// Upload photo
app.post('/api/photos', async (c) => {
  try {
    const body = await c.req.parseBody();
    const file = body['photo'];
    
    if (!file || !(file instanceof File)) {
      return c.json({ error: 'No photo provided' }, 400);
    }

    const id = uuid();
    const ext = path.extname(file.name) || '.jpg';
    const filename = `${id}${ext}`;
    const filepath = path.join(UPLOAD_DIR, filename);

    // Save file
    const buffer = Buffer.from(await file.arrayBuffer());
    await fs.writeFile(filepath, buffer);

    // Store metadata
    const photo = {
      id,
      filename,
      originalName: file.name,
      mimetype: file.type,
      size: file.size,
      path: filepath,
      createdAt: new Date().toISOString()
    };
    store.photos.set(id, photo);

    return c.json({ 
      success: true, 
      photo: {
        id: photo.id,
        name: photo.originalName,
        url: `/api/photos/${id}`
      }
    });
  } catch (error) {
    return c.json({ error: error.message }, 500);
  }
});

// Get photo
app.get('/api/photos/:id', async (c) => {
  const id = c.req.param('id');
  const photo = store.photos.get(id);
  
  if (!photo) {
    return c.json({ error: 'Photo not found' }, 404);
  }

  const buffer = await fs.readFile(photo.path);
  return new Response(buffer, {
    headers: {
      'Content-Type': photo.mimetype,
      'Cache-Control': 'public, max-age=31536000'
    }
  });
});

// ============================================
// SESSIONS
// ============================================

// Create session (recipient info)
app.post('/api/sessions', async (c) => {
  const body = await c.req.json();
  const { name, relationship, occasion, description, tone, photoIds } = body;

  const id = uuid();
  const session = {
    id,
    recipient: { name, relationship },
    occasion: occasion || '',
    description: description || '',
    tone: tone || [],
    photoIds: photoIds || [],
    status: 'created',
    createdAt: new Date().toISOString()
  };

  store.sessions.set(id, session);

  return c.json({ success: true, session });
});

// Get session
app.get('/api/sessions/:id', (c) => {
  const id = c.req.param('id');
  const session = store.sessions.get(id);
  
  if (!session) {
    return c.json({ error: 'Session not found' }, 404);
  }

  return c.json({ session });
});

// ============================================
// GENERATE PRODUCTS
// ============================================

app.post('/api/generate', async (c) => {
  const body = await c.req.json();
  const { sessionId } = body;

  const session = store.sessions.get(sessionId);
  if (!session) {
    return c.json({ error: 'Session not found' }, 404);
  }

  // Update status
  session.status = 'generating';
  store.sessions.set(sessionId, session);

  // Get photos for this session
  const photos = session.photoIds
    .map(id => store.photos.get(id))
    .filter(Boolean);

  // Generate products (mock AI pipeline)
  const products = generateProducts(session, photos);

  // Store products
  session.products = products.map(p => p.id);
  session.status = 'completed';
  store.sessions.set(sessionId, session);

  products.forEach(p => store.products.set(p.id, p));

  return c.json({ 
    success: true, 
    session,
    products 
  });
});

// ============================================
// PRODUCTS
// ============================================

app.get('/api/products/:id', (c) => {
  const id = c.req.param('id');
  const product = store.products.get(id);
  
  if (!product) {
    return c.json({ error: 'Product not found' }, 404);
  }

  return c.json({ product });
});

// List products for session
app.get('/api/sessions/:id/products', (c) => {
  const id = c.req.param('id');
  const session = store.sessions.get(id);
  
  if (!session) {
    return c.json({ error: 'Session not found' }, 404);
  }

  const products = (session.products || [])
    .map(pid => store.products.get(pid))
    .filter(Boolean);

  return c.json({ products });
});

// ============================================
// PRODUCT GENERATION (Mock AI Pipeline)
// ============================================

function generateProducts(session, photos) {
  const name = session.recipient?.name || 'Someone';
  const relationship = session.recipient?.relationship || '';
  const occasion = session.occasion || 'special';
  const description = session.description || '';
  const tone = session.tone || ['beautiful'];
  
  const photoUrls = photos.map(p => `/api/photos/${p.id}`);
  const madeFrom = photos.map(p => p.originalName.split('.')[0]).join(' · ');

  return [
    {
      id: uuid(),
      type: 'newspaper',
      title: `The ${name} Times`,
      subtitle: `A very special edition about ${name}`,
      description: `A personalized newspaper celebrating ${name}, with headlines and stories drawn from your memories and photos.`,
      badge: 'NEWSPAPER',
      price: 29,
      currency: 'GBP',
      photoUrls,
      madeFrom,
      recipient: { name, relationship },
      occasion,
      tone: tone[0] || 'beautiful',
      createdAt: new Date().toISOString()
    },
    {
      id: uuid(),
      type: 'book',
      title: `${name}: The Biography`,
      subtitle: 'An unauthorized account of a life well-lived',
      description: `A beautifully designed biography capturing the essence of ${name}'s story, from your words and photos.`,
      badge: 'BOOK',
      price: 49,
      currency: 'GBP',
      photoUrls,
      madeFrom,
      recipient: { name, relationship },
      occasion,
      tone: tone[0] || 'beautiful',
      createdAt: new Date().toISOString()
    },
    {
      id: uuid(),
      type: 'ornament',
      title: `${name} Christmas Ornament`,
      subtitle: 'A keepsake for years to come',
      description: `A ceramic ornament featuring ${name}'s portrait, perfect for hanging on the tree year after year.`,
      badge: 'ORNAMENT',
      price: 18,
      currency: 'GBP',
      photoUrls,
      madeFrom,
      recipient: { name, relationship },
      occasion: 'christmas',
      tone: tone[0] || 'beautiful',
      createdAt: new Date().toISOString()
    },
    {
      id: uuid(),
      type: 'puzzle',
      title: `${name} Memory Puzzle`,
      subtitle: '500 pieces of memories',
      description: `A custom jigsaw puzzle featuring your favorite photos of ${name}, perfect for family game night.`,
      badge: 'PUZZLE',
      price: 35,
      currency: 'GBP',
      photoUrls,
      madeFrom,
      recipient: { name, relationship },
      occasion,
      tone: tone[0] || 'beautiful',
      createdAt: new Date().toISOString()
    },
    {
      id: uuid(),
      type: 'card',
      title: `${name} Greeting Card`,
      subtitle: 'With a little something inside',
      description: `A personalized greeting card with a custom illustration and message for ${name}.`,
      badge: 'CARD',
      price: 8,
      currency: 'GBP',
      photoUrls,
      madeFrom,
      recipient: { name, relationship },
      occasion,
      tone: tone[0] || 'beautiful',
      createdAt: new Date().toISOString()
    },
    {
      id: uuid(),
      type: 'print',
      title: `${name} Art Print`,
      subtitle: 'Framed and ready to hang',
      description: `A high-quality art print featuring ${name}'s portrait in a beautiful artistic style.`,
      badge: 'PRINT',
      price: 24,
      currency: 'GBP',
      photoUrls,
      madeFrom,
      recipient: { name, relationship },
      occasion,
      tone: tone[0] || 'beautiful',
      createdAt: new Date().toISOString()
    }
  ];
}

// ============================================
// MCP SERVER
// ============================================

app.post('/mcp', async (c) => {
  const body = await c.req.json();
  const { method, params, id } = body;

  // JSON-RPC 2.0 response
  const response = { jsonrpc: '2.0', id };

  try {
    switch (method) {
      case 'initialize':
        response.result = {
          protocolVersion: '2024-11-05',
          capabilities: {
            tools: {},
            resources: {}
          },
          serverInfo: {
            name: 'star-at-night',
            version: '0.1.0'
          }
        };
        break;

      case 'tools/list':
        response.result = {
          tools: [
            {
              name: 'upload_photo',
              description: 'Upload a photo for gift creation',
              inputSchema: {
                type: 'object',
                properties: {
                  photo_url: { type: 'string', description: 'URL or base64 of the photo' },
                  filename: { type: 'string', description: 'Original filename' }
                },
                required: ['photo_url']
              }
            },
            {
              name: 'create_session',
              description: 'Create a gift session with recipient info',
              inputSchema: {
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Recipient name' },
                  relationship: { type: 'string', description: 'Relationship to recipient' },
                  occasion: { type: 'string', description: 'Occasion (birthday, christmas, etc)' },
                  description: { type: 'string', description: 'Description of the recipient' },
                  tone: { type: 'array', items: { type: 'string' }, description: 'Tone preferences' },
                  photo_ids: { type: 'array', items: { type: 'string' }, description: 'Uploaded photo IDs' }
                },
                required: ['name']
              }
            },
            {
              name: 'generate_products',
              description: 'Generate personalized gift products',
              inputSchema: {
                type: 'object',
                properties: {
                  session_id: { type: 'string', description: 'Session ID' }
                },
                required: ['session_id']
              }
            },
            {
              name: 'get_products',
              description: 'Get generated products for a session',
              inputSchema: {
                type: 'object',
                properties: {
                  session_id: { type: 'string', description: 'Session ID' }
                },
                required: ['session_id']
              }
            }
          ]
        };
        break;

      case 'tools/call':
        const { name: toolName, arguments: args } = params;
        
        switch (toolName) {
          case 'upload_photo': {
            // Store the photo reference
            const photoId = uuid();
            store.photos.set(photoId, {
              id: photoId,
              filename: args.filename || 'photo.jpg',
              originalName: args.filename || 'photo.jpg',
              mimetype: 'image/jpeg',
              url: args.photo_url,
              createdAt: new Date().toISOString()
            });
            
            response.result = {
              content: [{
                type: 'text',
                text: JSON.stringify({ 
                  success: true, 
                  photo_id: photoId,
                  message: `Photo uploaded successfully. ID: ${photoId}`
                })
              }]
            };
            break;
          }

          case 'create_session': {
            const sessionId = uuid();
            const session = {
              id: sessionId,
              recipient: { name: args.name, relationship: args.relationship || '' },
              occasion: args.occasion || '',
              description: args.description || '',
              tone: args.tone || [],
              photoIds: args.photo_ids || [],
              status: 'created',
              createdAt: new Date().toISOString()
            };
            store.sessions.set(sessionId, session);
            
            response.result = {
              content: [{
                type: 'text',
                text: JSON.stringify({ 
                  success: true, 
                  session_id: sessionId,
                  session 
                })
              }]
            };
            break;
          }

          case 'generate_products': {
            const session = store.sessions.get(args.session_id);
            if (!session) {
              response.error = { code: -32000, message: 'Session not found' };
              break;
            }

            const photos = session.photoIds
              .map(id => store.photos.get(id))
              .filter(Boolean);

            const products = generateProducts(session, photos);
            
            session.products = products.map(p => p.id);
            session.status = 'completed';
            store.sessions.set(args.session_id, session);
            products.forEach(p => store.products.set(p.id, p));

            response.result = {
              content: [{
                type: 'text',
                text: JSON.stringify({ 
                  success: true, 
                  products_count: products.length,
                  products: products.map(p => ({
                    id: p.id,
                    type: p.type,
                    title: p.title,
                    price: p.price
                  }))
                })
              }]
            };
            break;
          }

          case 'get_products': {
            const sess = store.sessions.get(args.session_id);
            if (!sess) {
              response.error = { code: -32000, message: 'Session not found' };
              break;
            }

            const products = (sess.products || [])
              .map(pid => store.products.get(pid))
              .filter(Boolean);

            response.result = {
              content: [{
                type: 'text',
                text: JSON.stringify({ 
                  success: true, 
                  products 
                })
              }]
            };
            break;
          }

          default:
            response.error = { code: -32601, message: `Unknown tool: ${toolName}` };
        }
        break;

      case 'ping':
        response.result = {};
        break;

      default:
        response.error = { code: -32601, message: `Unknown method: ${method}` };
    }
  } catch (error) {
    response.error = { code: -32000, message: error.message };
  }

  return c.json(response);
});

// ============================================
// START SERVER
// ============================================

console.log(`✦ Star at Night API running on http://localhost:${PORT}`);
console.log(`  MCP endpoint: http://localhost:${PORT}/mcp`);

serve({
  fetch: app.fetch,
  port: PORT
});
