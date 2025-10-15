import asyncio
import logging
import os

from agents import Agent, Runner, ModelSettings
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from openai.types import Reasoning
from pydantic import BaseModel, Field

from configuration.configuration import configure_all

logger = logging.getLogger(__name__)


class ResearchReport(BaseModel):
    short_summary: str = Field(description="A short 2~3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")


def create_research_mcp_server() -> MCPServerStdio:
    params = MCPServerStdioParams(command="uvx", args=["serper-mcp-server"],
                                  env={"SERPER_API_KEY": os.getenv("SERPER_API_KEY")})
    return MCPServerStdio(params=params, client_session_timeout_seconds=30)


def create_research_agent(server: MCPServerStdio) -> Agent:
    return Agent(
        name="Research agent",
        instructions="""
                You are a senior researcher tasked with writing a cohesive report for a research query.
                You will be provided original query, ann return the following data output.
                """,
        model="gpt-5-nano",
        model_settings=ModelSettings(reasoning=Reasoning(effort="low")),
        mcp_servers=[server],
        output_type=ResearchReport,
    )


async def research(query: str, feedback: str | None = None) -> ResearchReport:
    async with create_research_mcp_server() as server:
        agent = await create_research_agent(server)
        result = await Runner.run(agent, f"query: {query}\n feedback: {feedback}", max_turns=3)
        logger.info(result.final_output.model_dump_json())
        return result.final_output


if __name__ == '__main__':
    configure_all()
    asyncio.run(research("Due to 2025 year, What is the best model for agentic AI frontier model?"))
