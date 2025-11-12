from google.adk import Runner
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.genai import types

session_service = InMemorySessionService()


async def run_agent(app_name: str, user_id: str, session_id: str, query: str, agent: LlmAgent):
    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)

    runner = Runner(agent=agent, app_name=app_name, session_service=session_service)

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=types.UserContent(query)):
        if event.is_final_response() and event.content:
            yield event.content.parts[0].text
