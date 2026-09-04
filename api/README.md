# Star at Night API

## Quick Start

```bash
cd /root/z2m/api
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/photos` | Upload photo |
| GET | `/api/photos/:id` | Get photo |
| POST | `/api/sessions` | Create session |
| GET | `/api/sessions/:id` | Get session |
| POST | `/api/generate` | Generate products |
| GET | `/api/products/:id` | Get product |

## MCP Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mcp` | MCP server (JSON-RPC 2.0) |

### MCP Tools

| Tool | Description |
|------|-------------|
| `upload_photo` | Upload a photo for gift creation |
| `create_session` | Create a gift session with recipient info |
| `generate_products` | Generate personalized gift products |
| `get_products` | Get generated products for a session |

## Example Usage

### Create Session

```bash
curl -X POST http://localhost:3000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Luna",
    "relationship": "dog",
    "occasion": "christmas",
    "description": "A golden retriever who loves walks",
    "tone": ["funny", "beautiful"]
  }'
```

### Generate Products

```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "YOUR_SESSION_ID"}'
```

### MCP Call

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "create_session",
      "arguments": {
        "name": "Sophie",
        "relationship": "sister",
        "occasion": "birthday"
      }
    }
  }'
```

## Architecture

```
Client → API Server → In-Memory Store
  ↓
MCP Protocol → Tools → Business Logic
  ↓
Photos → Upload → Storage
  ↓
Sessions → Recipient Info → Products
  ↓
Generate → AI Pipeline → Products
```

## Next Steps

1. Connect to D1/KV for persistence
2. Add real AI generation (Replicate/OpenAI)
3. Add Prodigi integration
4. Deploy to Cloudflare Workers
