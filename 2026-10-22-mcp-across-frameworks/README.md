# MCP across frameworks: LangChain 1.4 MCPAdapter

**Released** 3 September 2026 in LangChain 1.4.0 · [release](https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.4.0) · [migration guide](https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters)

MCP support now ships inside LangChain as `langchain.mcp`, built on FastMCP. One `MCPAdapter` replaces `MultiServerMCPClient` from the archived `langchain-mcp-adapters`. Give it a URL, a script `Path` or a config; it works out the transport. A bare string is always read as a URL, so a script never starts as a subprocess by accident.

```bash
ANTHROPIC_API_KEY=... uv run agent.py
```

`server.py` is a one-tool MCP server (currency conversion at fixed rates). `agent.py` loads its tools through `MCPAdapter` and hands them to a Claude agent.

**Our run, 2 October 2026:** the agent found the `convert` tool and answered "1,250 USD is ₹110,500.00 and ₱72,375.00".

Note: `langchain.mcp` is marked beta by LangChain, so its API may still change.

Needs: an Anthropic API key and [uv](https://docs.astral.sh/uv/).
