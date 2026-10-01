# /// script
# requires-python = ">=3.10"
# dependencies = ["langchain[mcp]>=1.4", "langchain-anthropic"]
# ///
"""langchain-mcp-adapters is archived. Here is the one-class replacement.

LangChain 1.4 ships MCP support in the langchain.mcp namespace. MCPAdapter
takes a URL, a script or a config and works out the transport; its tools go
straight into an agent.

Run:  ANTHROPIC_API_KEY=... uv run agent.py
"""
import asyncio
from pathlib import Path
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter


async def main():
    adapter = MCPAdapter(Path("server.py"))
    tools = await adapter.list_tools()
    print("tools from the MCP server:", [t.name for t in tools])
    agent = create_agent("anthropic:claude-opus-5-5", tools=tools)
    result = await agent.ainvoke({"messages": [("user", "An invoice is 1,250 USD. What is that in INR and in PHP?")]})
    print(result["messages"][-1].text)


asyncio.run(main())
