import asyncio
import logging

from agents import Agent, Runner, ModelSettings, OpenAIResponsesModel
from openai.types import Reasoning
from pydantic import BaseModel, Field

from openai_agents import OPENAI_ASYNC_CLIENT

logger = logging.getLogger(__name__)


class WebSearchItem(BaseModel):
    query: str = Field(description="The search term to use for the web search")
    reason: str = Field(description="Your reasoning for why this search is important to the query")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query")


def create_planner_agent() -> Agent:
    return Agent(
        name="Planner agent",
        instructions="""
            You are a helpful research assistant. Your job is to help me find information about a topic.
            Output 1 terms to query for.
        """,
        model=OpenAIResponsesModel(model="gpt-5-mini", openai_client=OPENAI_ASYNC_CLIENT),
        model_settings=ModelSettings(reasoning=Reasoning(effort="high")),
        output_type=WebSearchPlan
    )


async def plan(query: str) -> WebSearchPlan:
    agent = create_planner_agent()
    response = await Runner.run(agent, query)
    web_search_plan = response.final_output
    logger.info(web_search_plan.model_dump_json())
    return web_search_plan


if __name__ == '__main__':
    asyncio.run(plan("Due to 2025 year, What is the best model for agentic AI frontier model?"))
