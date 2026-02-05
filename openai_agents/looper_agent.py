import asyncio
import logging
import textwrap

from agents import function_tool, Agent, Runner, trace, ModelSettings, OpenAIResponsesModel
from openai.types import Reasoning
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel, Field

from openai_agents import OPENAI_ASYNC_CLIENT

logger = logging.getLogger(__name__)


class TodoItem(BaseModel):
    description: str = Field(description="The text describing the task")
    completed: bool = Field(description="Whether the task is completed", default=False)


todos = []


def get_todo_report() -> str:
    result = ""
    for index, todo in enumerate(todos):
        status = "✓" if todo.completed else "✗"
        result += f"Todo #{index + 1}: [{status}] {todo.description}\n"
    return result


@function_tool
def create_todos(descriptions: list[str]) -> str:
    """Add new todos from a list of descriptions and return the full list"""
    for desc in descriptions:
        todos.append(TodoItem(description=desc))
    return get_todo_report()


@function_tool
def mark_complete(index: int) -> str:
    """Marks the todo item at the given index(starting from 1) as completed and return the full list"""
    if 1 <= index <= len(todos):
        todos[index - 1].completed = True
    else:
        return f"Todo #{index} does not exist."
    return get_todo_report()


agent = Agent(
    name="Looper agent",
    model=OpenAIResponsesModel(model="gpt-5.2", openai_client=OPENAI_ASYNC_CLIENT),
    model_settings=ModelSettings(reasoning=Reasoning(effort="none")),
    instructions=textwrap.dedent(
        """
        You are given a problem to solve, by using your todo tools to plan a list of steps, then carrying out each step in turn.
        Now use the todo list tools, create a plan, carry out the steps, and reply with the solution.
        """
    ),
    tools=[create_todos, mark_complete]
)


async def main():
    with trace("Looper Agent"):
        result = Runner.run_streamed(agent, "2025 년 기준으로, 어떤 frontier model 이 agentic AI 에 제일 적합할까?")
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_output_item":
                    logger.info(f"{event.item.output}")


if __name__ == '__main__':
    asyncio.run(main())
