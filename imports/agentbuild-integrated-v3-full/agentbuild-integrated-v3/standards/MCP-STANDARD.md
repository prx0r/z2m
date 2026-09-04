# MCP Standard

- tools are narrow capabilities, not giant prompts
- descriptions state exactly what is authoritative vs inferred
- schemas are strict and outputs bounded
- tool errors are structured, not hallucinated fallbacks
- costly calls disclose/meter cost where relevant
- avoid exposing hundreds of unrelated tools in one context; use family servers or dynamic discovery
- deterministic operations should not spend LLM tokens unnecessarily
- tool implementation and MCP transport remain separable
