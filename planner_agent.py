import asyncio
import logging

from agents import Agent, Runner, ModelSettings
from openai.types import Reasoning
from pydantic import BaseModel, Field

from configuration.configuration import configure_all

logger = logging.getLogger(__name__)


class WebSearchItem(BaseModel):
    query: str = Field(description="The search term to use for the web search")
    reason: str = Field(description="Your reasoning for why this search is important to the query")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query")


async def plan(query: str) -> WebSearchPlan:
    agent = Agent(
        name="Planner agent",
        instructions="""
            You are a helpful research assistant. Your job is to help me find information about a topic.
            Output 2 terms to query for.
        """,
        model="gpt-5-mini",
        model_settings=ModelSettings(reasoning=Reasoning(effort="high")),
        output_type=WebSearchPlan
    )

    response = await Runner.run(agent, query)
    web_search_plan = response.final_output
    logger.info(web_search_plan.model_dump_json())
    return web_search_plan


if __name__ == '__main__':
    configure_all()
    asyncio.run(plan("Due to 2025 year, What is the best model for agentic AI frontier model?"))
