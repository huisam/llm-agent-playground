import asyncio
import os

from agents import Agent, trace, Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from dotenv import load_dotenv

from log.logger import get_logger

logger = get_logger()
load_dotenv(override=True)

async def serf(query: str) -> str:
    params = MCPServerStdioParams(command="uvx", args=["serper-mcp-server"], env={"SERPER_API_KEY": os.getenv("SERPER_API_KEY")})
    with trace("Search"):
        async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
            agent = Agent(
                name="Search agent",
                instructions="""You are a internet searcher. Please search about the query string and explain the search result""",
                model="gpt-4o-mini",
                mcp_servers=[server]
            )
            result = await Runner.run(agent, query)
            logger.info(result.final_output)
            return result.final_output

if __name__ == '__main__':
    asyncio.run(serf("What is the tomorrow weather in seoul?"))