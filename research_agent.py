import asyncio
import os

from agents import Agent, trace, Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from log.logger import get_logger

logger = get_logger()
load_dotenv(override=True)


class ResearchReport(BaseModel):
    short_summary: str = Field(description="A short 2~3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")


async def research(query: str) -> str:
    params = MCPServerStdioParams(command="uvx", args=["serper-mcp-server"],
                                  env={"SERPER_API_KEY": os.getenv("SERPER_API_KEY")})
    with trace("Research agent"):
        async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
            agent = Agent(
                name="Research agent",
                instructions="""
                You are a senior researcher tasked with writing a cohesive report for a research query.
                You will be provided original query, ann return the following data output.
                """,
                model="gpt-4o-mini",
                mcp_servers=[server],
                output_type=ResearchReport
            )
            result = await Runner.run(agent, query)
            logger.info(result.final_output)
            return result.final_output


if __name__ == '__main__':
    asyncio.run(research("What is the tomorrow weather in seoul?"))
