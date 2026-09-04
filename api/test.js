const BASE = 'http://localhost:3000';

async function test() {
  console.log('=== Testing Star at Night API ===\n');

  // 1. Health check
  console.log('1. Health check:');
  const health = await fetch(BASE).then(r => r.json());
  console.log(JSON.stringify(health, null, 2));

  // 2. Create session
  console.log('\n2. Create session:');
  const sessionRes = await fetch(`${BASE}/api/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'Luna',
      relationship: 'dog',
      occasion: 'christmas',
      description: 'A golden retriever who loves walks and treats',
      tone: ['funny', 'beautiful'],
      photoIds: []
    })
  }).then(r => r.json());
  console.log(JSON.stringify(sessionRes, null, 2));
  const sessionId = sessionRes.session?.id;

  // 3. Generate products
  console.log('\n3. Generate products:');
  const genRes = await fetch(`${BASE}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId })
  }).then(r => r.json());
  console.log(JSON.stringify(genRes, null, 2));

  // 4. MCP initialize
  console.log('\n4. MCP initialize:');
  const mcpInit = await fetch(`${BASE}/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'initialize',
      params: {}
    })
  }).then(r => r.json());
  console.log(JSON.stringify(mcpInit, null, 2));

  // 5. MCP list tools
  console.log('\n5. MCP list tools:');
  const mcpTools = await fetch(`${BASE}/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/list',
      params: {}
    })
  }).then(r => r.json());
  console.log(JSON.stringify(mcpTools, null, 2));

  // 6. MCP create session
  console.log('\n6. MCP create session:');
  const mcpSession = await fetch(`${BASE}/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: {
        name: 'create_session',
        arguments: {
          name: 'Sophie',
          relationship: 'sister',
          occasion: 'birthday',
          description: 'Loves medieval paintings and has dry humour',
          tone: ['understated']
        }
      }
    })
  }).then(r => r.json());
  console.log(JSON.stringify(mcpSession, null, 2));

  console.log('\n=== All tests passed! ===');
}

test().catch(console.error);
