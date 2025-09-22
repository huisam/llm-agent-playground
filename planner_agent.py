import asyncio

from agents import Agent, Runner, trace
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from log.logger import get_logger

load_dotenv(override=True)
logger = get_logger()


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query")
    query: str = Field(description="The search term to use for the web search")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query")


async def plan(query: str) -> str:
    agent = Agent(
        name="Planner agent",
        instructions="""
            You are a helpful research assistant. Your job is to help me find information about a topic.
            Output 3 terms to query for.
        """,
        model="gpt-4.1",
        output_type=WebSearchPlan
    )

    with trace("Planner agent"):
        response = await Runner.run(agent, query)
        logger.info(response.final_output)
        return response.final_output


if __name__ == '__main__':
    asyncio.run(plan("Due to 2025 year, What is the best model for agentic AI frontier model?"))
