# /// script
# requires-python = ">=3.10"
# dependencies = ["fastmcp"]
# ///
"""A tiny MCP server with one tool: the exchange rates a team uses for invoices."""
from fastmcp import FastMCP

mcp = FastMCP("rates")
RATES = {"USD": 1.0, "INR": 88.4, "AED": 3.67, "PHP": 57.9, "LKR": 301.2}


@mcp.tool
def convert(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert an amount between USD, INR, AED, PHP and LKR at this week's fixed rates."""
    return round(amount / RATES[from_currency] * RATES[to_currency], 2)


if __name__ == "__main__":
    mcp.run(show_banner=False, log_level="WARNING")
