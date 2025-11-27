import asyncio
import logging
import os

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters
from opik.integrations.adk import OpikTracer, track_adk_agent_recursive
from pydantic import BaseModel, Field

from configuration import configure_all
from google_adk.runner import run_agent

logger = logging.getLogger(__name__)


class ResearchReport(BaseModel):
    short_summary: str = Field(description="A short 2~3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")


research_mcp_server_tool = McpToolset(
    tool_name_prefix="serper",
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=["serper-mcp-server"],
            env={"SERPER_API_KEY": os.getenv("SERPER_API_KEY")}
        ),
        timeout=30
    ),
)


def create_research_agent() -> LlmAgent:
    return LlmAgent(
        name="research_agent",
        instruction="""
                You are a senior researcher tasked with writing a cohesive report for a research query.
                You will be provided original query, and return the following data output.
                """,
        model=Gemini(model="gemini-2.5-flash"),
        tools=[research_mcp_server_tool],
        output_schema=ResearchReport,
        output_key="research_report"
    )


async def research(query: str, feedback: str | None = None) -> ResearchReport:
    agent = create_research_agent()
    opik_tracer = OpikTracer(
        name="research-agent",
        project_name="adk-multi-agent-demo"
    )
    track_adk_agent_recursive(agent, opik_tracer)

    final_answer = None
    async for event in run_agent(app_name="research", user_id="test_user", session_id="test_session", agent=agent,
                                 query=query):
        final_answer = event
        logger.info(final_answer)
    await research_mcp_server_tool.close()
    return ResearchReport.model_validate_json(final_answer)


if __name__ == '__main__':
    configure_all()
    asyncio.run(research("Due to 2025 year, What is the best model for agentic AI frontier model?"))
