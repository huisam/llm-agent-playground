import asyncio
import logging
from contextlib import AsyncExitStack

from agents import Agent, trace, Runner, ModelSettings
from openai.types import Reasoning

from agent import create_research_mcp_server, create_summarize_mcp_server, create_planner_agent, create_research_agent, \
    create_summarize_agent
from configuration import configure_all

logger = logging.getLogger(__name__)

async def orchestration(topic: str):
    async with AsyncExitStack() as stack:
        research_mcp_server = await stack.enter_async_context(create_research_mcp_server())
        summarize_mcp_server = await stack.enter_async_context(create_summarize_mcp_server())

        planner_agent = create_planner_agent()
        research_agent = create_research_agent(research_mcp_server)
        summarize_agent = create_summarize_agent(summarize_mcp_server)

        agent = Agent(
            name="orchestrator agent",
            instructions="""
                You are a orchestrator agent. You are responsible for orchestrating the research process.
                
                Follow the given work flow
                1. plan
                2. research
                3. summarize
                """,
            tools=[
                planner_agent.as_tool(
                    tool_name="plan",
                    tool_description="Plan a research plan for the given research topic."
                ),
                research_agent.as_tool(
                    tool_name="research",
                    tool_description="Research on the given topic"
                ),
                summarize_agent.as_tool(
                    tool_name="summarize",
                    tool_description="Summarize the research result to markdown file"
                )
            ],
            model="gpt-5-mini",
            model_settings=ModelSettings(reasoning=Reasoning(effort="low"))
        )

        with trace("Research workflow"):
            result = await Runner.run(agent, topic)
            logger.info(result.final_output)

if __name__ == '__main__':
    configure_all()
    asyncio.run(orchestration("Due to 2025.10, What is the best model for agentic AI frontier model?"))