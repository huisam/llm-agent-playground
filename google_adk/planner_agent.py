import asyncio
import logging

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from opik.integrations.adk import OpikTracer, track_adk_agent_recursive
from pydantic import BaseModel, Field

from configuration import configure_all
from google_adk.runner import run_agent

logger = logging.getLogger(__name__)


class WebSearchItem(BaseModel):
    query: str = Field(description="The search term to use for the web search")
    reason: str = Field(description="Your reasoning for why this search is important to the query")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query")


def create_planner_agent() -> LlmAgent:
    return LlmAgent(
        name="planner_agent",
        instruction="""
            You are a helpful research assistant. Your job is to help me find information about a topic.
            Output 1 terms to query for.
        """,
        model=Gemini(model="gemini-2.5-flash"),
        output_schema=WebSearchPlan,
        output_key="web_search_plan",
    )


async def plan(query: str) -> WebSearchPlan:
    agent = create_planner_agent()
    multi_agent_tracer = OpikTracer(
        name="planner-agent",
        project_name="adk-multi-agent-demo"
    )
    track_adk_agent_recursive(agent, multi_agent_tracer)

    final_answer = None
    async for event in run_agent(app_name="planner", user_id="test_user", session_id="test_session", agent=agent,
                                 query=query):
        final_answer = event
        logger.info(final_answer)
    return WebSearchPlan.model_validate_json(final_answer)


if __name__ == '__main__':
    configure_all()
    asyncio.run(plan("Due to 2025 year, What is the best model for agentic AI frontier model?"))
