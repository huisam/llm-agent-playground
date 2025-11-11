import asyncio

from agents import Agent, input_guardrail, RunContextWrapper, TResponseInputItem, \
    GuardrailFunctionOutput, Runner, trace
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class ResearchWorkOutput(BaseModel):
    is_research_work: bool = Field(description="Whether or not the query requires research work")


def create_guardrail_agent() -> Agent:
    return Agent(
        name="Guardrail agent",
        instructions="""Check if the user is asking you to research something""",
        model="gpt-4o-mini",
        output_type=ResearchWorkOutput
    )


@input_guardrail
async def research_guardrail(
        ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(create_guardrail_agent(), input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_research_work,
    )


async def main():
    with trace("test guardrail"):
        planner_agent = Agent(
            name="Planner agent",
            instructions="""
                    You are a helpful research assistant. Your job is to help me find information about a topic.
                    Output 1 terms to query for.
                """,
            model="gpt-4o-mini",
            input_guardrails=[research_guardrail]
        )
        await Runner.run(planner_agent, "What is my name?")


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
